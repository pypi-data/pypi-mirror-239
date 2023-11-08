import cv2
import numpy as np


def mosaic_augmentation(xs, ys, img_size=640, **k):
    """
    Perform mosaic data augmentation on a dataset.
    :param xs: list of images
    :param ys: list of bounding boxes [cx, cy, w, h, cls] or list of classes
    :param img_size: size of the output image
    :return: list of augmented images and list of new bounding boxes or classes
    """
    # List to store new images and bounding boxes or classes
    new_xs = []
    new_ys = []

    for i in range(0, len(xs), 4):
        # Create an empty image of the specified size
        output_image = np.zeros((img_size, img_size, 3))

        for j in range(4):
            # Choose an image
            index = i + j if i + j < len(xs) else i + j - len(xs)
            img = xs[index]
            target = ys[index]

            # Resize the image to the desired size
            h, w, _ = img.shape
            if w > h:
                img = cv2.resize(img, (img_size, int(img_size * h / w)))
            else:
                img = cv2.resize(img, (int(img_size * w / h), img_size))

            # Determine where to place the image based on its quadrant
            if j == 0:  # top-left
                output_image[:img.shape[0], :img.shape[1]] = img
                if isinstance(target[0], list):  # ys is a list of bounding boxes
                    new_ys.append([target[0] * img.shape[1], target[1] * img.shape[0], target[2] * img.shape[1],
                                   target[3] * img.shape[0], target[4]])
                else:  # ys is a list of classes
                    new_ys.append(target)
            elif j == 1:  # top-right
                output_image[:img.shape[0], -img.shape[1]:] = img
                if isinstance(target[0], list):  # ys is a list of bounding boxes
                    new_ys.append(
                        [img_size - target[0] * img.shape[1], target[1] * img.shape[0], target[2] * img.shape[1],
                         target[3] * img.shape[0], target[4]])
                else:  # ys is a list of classes
                    new_ys.append(target)
            elif j == 2:  # bottom-left
                output_image[-img.shape[0]:, :img.shape[1]] = img
                if isinstance(target[0], list):  # ys is a list of bounding boxes
                    new_ys.append(
                        [target[0] * img.shape[1], img_size - target[1] * img.shape[0], target[2] * img.shape[1],
                         target[3] * img.shape[0], target[4]])
                else:  # ys is a list of classes
                    new_ys.append(target)
            elif j == 3:  # bottom-right
                output_image[-img.shape[0]:, -img.shape[1]:] = img
                if isinstance(target[0], list):  # ys is a list of bounding boxes
                    new_ys.append([img_size - target[0] * img.shape[1], img_size - target[1] * img.shape[0],
                                   target[2] * img.shape[1], target[3] * img.shape[0], target[4]])
                else:  # ys is a list of classes
                    new_ys.append(target)

        new_xs.append(output_image)

    return new_xs, new_ys


def random_affine(xs, ys, degrees=10, translate=0.1, scale=0.1, shear=0.1, **k):
    new_xs = []
    new_ys = []

    for x, y in zip(xs, ys):
        # 获取图像的宽度和高度
        h, w = x.shape[:2]
        # 创建仿射变换矩阵
        angle = np.random.uniform(-degrees, degrees)
        tx = np.random.uniform(-translate, translate) * w
        ty = np.random.uniform(-translate, translate) * h
        s = np.random.uniform(1 - scale, 1 + scale)
        shear = np.random.uniform(-shear, shear)
        M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, s)
        M[0, 2] += tx
        M[1, 2] += ty
        M[1, 0] += shear
        # 对图像进行仿射变换
        new_x = cv2.warpAffine(x, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        new_xs.append(new_x)

        if isinstance(y, (list, np.ndarray)):
            new_y = []
            for bbox in y:
                cx, cy, w, h, cls = bbox
                cx *= x.shape[1]
                cy *= x.shape[0]
                w *= x.shape[1]
                h *= x.shape[0]

                # 将bbox的中心点坐标和宽高转换为左上角和右下角的坐标
                x1, y1, x2, y2 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
                # 创建表示bbox的3x3的坐标矩阵
                coords = np.array([[x1, y1, 1], [x2, y1, 1], [x2, y2, 1], [x1, y2, 1]])
                # 对坐标矩阵进行仿射变换
                new_coords = np.dot(coords, M.T)
                # 计算新的bbox的中心点坐标和宽高
                new_x1, new_y1 = new_coords.min(axis=0)
                new_x2, new_y2 = new_coords.max(axis=0)
                new_cx, new_cy = (new_x1 + new_x2) / 2, (new_y1 + new_y2) / 2
                new_w, new_h = new_x2 - new_x1, new_y2 - new_y1
                # 添加新的bbox到列表中
                new_y.append(
                    [new_cx / new_x.shape[1], new_cy / new_x.shape[0], new_w / new_x.shape[1], new_h / new_x.shape[0], cls])
            new_ys.append(new_y)
        else:
            new_ys = ys

    return new_xs, new_ys


def augment_hsv(xs, ys, hgain=0.1, sgain=0.1, vgain=0.1, **k):
    """
    Perform HSV data augmentation on a dataset.
    :param xs: list of images
    :param ys: list of bounding boxes [cx, cy, w, h, cls] or list of classes
    :param hgain: hue gain
    :param sgain: saturation gain
    :param vgain: value gain
    :return: list of augmented images and list of new bounding boxes or classes
    """
    # List to store new images and bounding boxes or classes
    new_xs = []
    new_ys = []

    for img, target in zip(xs, ys):
        # Convert image to HSV color space
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Apply transformations
        hue = np.random.uniform(1 - hgain, 1 + hgain)
        sat = np.random.uniform(1 - sgain, 1 + sgain)
        val = np.random.uniform(1 - vgain, 1 + vgain)
        img_hsv = (img_hsv * np.array([hue, sat, val])).clip(min=0, max=255).astype(np.uint8)

        # Convert image back to BGR color space
        img = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

        new_xs.append(img)
        new_ys.append(target)

    return new_xs, new_ys


def horizontal_flip(xs, ys, **k):
    """
    Perform Horizontal Flip data augmentation on a dataset.
    :param xs: list of images
    :param ys: list of bounding boxes [cx, cy, w, h, cls] or list of classes
    :return: list of augmented images and list of new bounding boxes or classes
    """
    # List to store new images and bounding boxes or classes
    new_xs = []
    new_ys = []

    for img, target in zip(xs, ys):
        # Apply horizontal flip
        img = cv2.flip(img, 1)

        if isinstance(target[0], list):  # ys is a list of bounding boxes
            # Flip bounding boxes
            target = [[1 - box[0], box[1], box[2], box[3], box[4]] for box in target]

        new_xs.append(img)
        new_ys.append(target)

    return new_xs, new_ys


def voc2clsfy(xs, ys, **kwargs):
    new_xs = []
    new_ys = []

    for x, y in zip(xs, ys):
        # 获取图像的宽度和高度
        h, w = x.shape[:2]

        for bbox in y:
            cx, cy, bw, bh, cls = bbox
            # 计算bbox的左上角和右下角的坐标
            x1 = int((cx - bw/2) * w)
            y1 = int((cy - bh/2) * h)
            x2 = int((cx + bw/2) * w)
            y2 = int((cy + bh/2) * h)
            # 创建一个新的随机子图
            new_x = np.random.randint(0, 255, (h, w, 3), dtype=np.uint8)
            # 将原图中对应区域的图片拷贝到新子图中
            new_x[y1:y2, x1:x2] = x[y1:y2, x1:x2]
            # 添加新的子图和类别到列表中
            new_xs.append(new_x)
            new_ys.append(cls)

    return new_xs, new_ys

