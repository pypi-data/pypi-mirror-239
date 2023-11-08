import os
import glob
import cv2
import numpy as np
import xml.etree.ElementTree as ET
from keras import Input
from keras.layers import Conv2D, Dense, Concatenate, Flatten
from Lutils.main import LModel
from Lutils.act import Softmax, SILU
from Lutils.ops.conv import Conv2DBS
from Lutils.ops.pooling import SPPF2D
from Lutils.ops.sample import UCC2D, DCCC2D


def draw_label(img, bboxes):
    """
    绘制检测框
    :param img: 输入图像
    :param bboxes: list of [cx, cy, w, h, cls]，其中cx, cy, w, h均为float,取值0-1
    :return: img
    """
    img_h, img_w = img.shape[:2]

    for bbox in bboxes:
        cx, cy, w, h, cls = bbox
        x_min = int((cx - w / 2) * img_w)
        y_min = int((cy - h / 2) * img_h)
        x_max = int((cx + w / 2) * img_w)
        y_max = int((cy + h / 2) * img_h)

        # 生成随机颜色
        color = np.random.randint(0, 255, 3)
        color_index = np.random.choice(3)
        color[color_index] //= 2
        color[color_index] += 127
        for i in range(3):
            if i == color_index:
                continue
            color[i] /= 2
        color_txt = color.copy()
        color_txt[color_index] *= 0.75
        for i in range(3):
            if i == color_index:
                continue
            color_txt[i] *= 1.25

        # 生成文本颜色
        color_txt = color_txt.astype(int)

        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), tuple(color.tolist()), 2)
        cv2.putText(img, str(cls), (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, tuple(color_txt.tolist()), 2)

    return img


def load_pascal_voc_dataset(jpeg_path, anno_path, cls_txt_path):
    # 获取所有JPEG图像的路径
    img_paths = glob.glob(os.path.join(jpeg_path, '*.jpg'))

    # 读取类别文件
    with open(cls_txt_path, 'r', encoding='utf-8') as f:
        classes = f.read().splitlines()

    bboxes = []
    for img_path in img_paths:
        # 获取对应的注释文件路径
        base_name = os.path.basename(img_path).replace('.jpg', '.xml')
        anno_file = os.path.join(anno_path, base_name)

        # 判断文件是否存在
        if not os.path.exists(anno_file):
            print("[Warning]: Can not find jpeg's annotation file: {}".format(anno_file))
            bboxes.append([])
            continue


        # 解析XML文件
        tree = ET.parse(anno_file)
        root = tree.getroot()

        # 获取图像的宽度和高度
        size = root.find('size')
        img_width = float(size.find('width').text)
        img_height = float(size.find('height').text)

        img_bboxes = []
        for obj in root.findall('object'):
            cls = classes.index(obj.find('name').text)

            bbox = obj.find('bndbox')
            xmin = float(bbox.find('xmin').text) / img_width
            ymin = float(bbox.find('ymin').text) / img_height
            xmax = float(bbox.find('xmax').text) / img_width
            ymax = float(bbox.find('ymax').text) / img_height

            # 计算中心点坐标和宽度、高度
            cx = (xmin + xmax) / 2
            cy = (ymin + ymax) / 2
            w = xmax - xmin
            h = ymax - ymin

            img_bboxes.append([cx, cy, w, h, cls])

        bboxes.append(np.array(img_bboxes))

    return img_paths, bboxes, classes


def build_yolov8(inputs_shape: tuple, classes: list, model_size: str = 'n', reg_max=4, debug=False) -> dict:
    """
    Create YoloV8 Net
    *return a dict with keys: body neck head
    :param inputs_shape:
    :param classes: list of str
    :param model_size: str, n s m l x
    :return: dict with keys: body neck head
    """
    d, w, r = -1, -1, -1  # deepen_factor, widden_factor, ratio
    model_size = model_size.lower()
    if model_size == 'n':
        d, w, r = 0.67, 0.25, 2.0
    elif model_size == 's':
        d, w, r = 0.67, 0.50, 2.0
    elif model_size == 'm':
        d, w, r = 1.0, 0.75, 1.5
    elif model_size == 'l':
        d, w, r = 1.34, 1.00, 1.0
    elif model_size == 'x':
        d, w, r = 1.34, 1.25, 1.0
    else:
        raise ValueError('Unknown model size: {}'.format(model_size))

    # build_body:
    body_inputs = Input(inputs_shape)  # 参考shape: 640 640 3
    x = Conv2DBS.TakeFeatures(body_inputs, filters=int(64 * w + .5))  # -> n 320 320 64*w
    # Stage1
    x1 = Conv2DBS.CCUnit(x, filters=int(128 * w + .5), splits=3 * d)  # x1 -> n 160 160 128*w
    # Stage2
    x2 = Conv2DBS.CCUnit(x1, filters=int(256 * w + .5), splits=3 * d)  # x2 -> n 80 80 256*w
    # Stage3
    x3 = Conv2DBS.CCUnit(x2, filters=int(512 * w + .5), splits=3 * d)  # x3 -> n 40 40 512*w
    # Stage4
    x = Conv2DBS.CCUnit(x3, filters=int(512 * w * r + .5), splits=3 * d)  # x4 -> n 20 20 512*w*r
    x4 = SPPF2D(x, int(512 * w * r + .5))

    net_body = LModel(input=body_inputs, output=[x2, x3, x4], name='YOLOv8_CSPDarknet')
    if debug: print("Create Body Finish!")
    # ------------------------------------

    cls_inputs = Input(inputs_shape)
    xs = [Flatten()(xsi) for xsi in net_body(cls_inputs)]
    x = Concatenate()(xs)
    x = Dense(len(classes))(x)
    x = Softmax()(x)
    net_body_cls = LModel(input=cls_inputs, output=x, name='YOLOv8_Pretrain_Classifier')
    if debug: print("Create Body Classifier Finish!")
    # ------------------------------------

    u1 = UCC2D(x3, x4)  # u1 -> x3 -> n 40 40 512*w
    u2 = UCC2D(x2, u1)  # u2 -> x2 -> n 80 80 256*w

    d1 = DCCC2D(u2, u1)  # d1 -> u1 -> n 40 40 512*w
    d2 = DCCC2D(d1, x4)  # d2 -> x4 -> n 20 20 512*w*r

    net_neck = LModel(input=body_inputs, output=[u2, d1, d2],  name='YOLOv8_CSPDarknet_PAFPN')
    cls_inputs = Input(inputs_shape)
    xs = net_neck(cls_inputs)
    xs = [Flatten()(xs_i) for xs_i in xs]
    x = Concatenate()(xs)
    x = Dense(len(classes))(x)
    x = Softmax()(x)
    net_neck_cls = LModel(cls_inputs, x,  name='YOLOv8_Neck_Pretrain_Classifier')
    if debug: print("Create Neck Finish!")
    # ------------------------------------

    h1_box = Conv2DBS(u2, 3, 1, 1)
    h1_box = Conv2D(4 * reg_max, 1, 1, 'valid')(h1_box)
    h1_cls = Conv2DBS(u2, 3, 1, 1)
    h1_cls = Conv2D(len(classes), 1, 1, 'valid')(h1_cls)

    h2_box = Conv2DBS(d1, 3, 1, 1)
    h2_box = Conv2D(4 * reg_max, 1, 1, 'valid')(h2_box)
    h2_cls = Conv2DBS(d1, 3, 1, 1)
    h2_cls = Conv2D(len(classes), 1, 1, 'valid')(h2_cls)

    h3_box = Conv2DBS(d2, 3, 1, 1)
    h3_box = Conv2D(4 * reg_max, 1, 1, 'valid')(h3_box)
    h3_cls = Conv2DBS(d2, 3, 1, 1)
    h3_cls = Conv2D(len(classes), 1, 1, 'valid')(h3_cls)

    net_head = LModel(input=body_inputs, output=[h1_box, h1_cls, h2_box, h2_cls, h3_box, h3_cls], name='YOLOv8')
    if debug: print("Create Head Finish!")
    # ------------------------------------

    return {
        "body": net_body,
        "neck": net_neck,
        "head": net_head,
        "yolo": net_head,
        "body_cls": net_body_cls,
        "neck_cls": net_neck_cls
    }


if __name__ == "__main__":
    _ = load_pascal_voc_dataset(r'D:\desktop20231030\yolov8\VOC_UG\JPEGImages', r'D:\desktop20231030\yolov8\VOC_UG\Anotations', r'D:\desktop20231030\yolov8\VOC_UG\predefined_classes.txt')
    print(*_, sep='\n')
