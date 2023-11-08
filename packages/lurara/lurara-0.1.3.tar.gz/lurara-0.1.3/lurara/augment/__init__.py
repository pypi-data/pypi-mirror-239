import concurrent.futures
import random

from lurara.augment.img_augment import *


class AugmentPipe:
    """
    用户将需要使用的数据增强的函数依次加入pipe, 这些函数必须以xs, ys作为通用的形参, 并且使用通用的kwargs
    """

    def __init__(self, use_multithreading: bool = False, num_threads: int = 4):
        self.augmentations = []
        self.use_multithreading = use_multithreading
        self.num_threads = num_threads
        if use_multithreading:
            assert num_threads > 1, f"num_threads must be greater than 1, but got {num_threads}"

    def add(self, func, prob=1.0):
        self.augmentations.append((func, prob))

    def remove(self, func):
        self.augmentations = [(f, p) for f, p in self.augmentations if f != func]

    def __call__(self, xs, ys, **kwargs):
        if self.use_multithreading:
            assert len(xs) == len(
                ys), f"len(xs) must be equal to len(ys), but got len_xs:{len(xs)} and len_xs:{len(ys)}"
            assert len(
                xs) >= self.num_threads, f"len(xs) must be greater than num_threads, but got len_xs:{len(xs)} and num_threads:{self.num_threads}"
            # Calculate the size of each chunk
            chunk_size = len(xs) // self.num_threads

            # Create a ThreadPoolExecutor
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_threads - 1) as executor:
                # Create futures for each thread
                futures = [executor.submit(self._process, xs[i * chunk_size:(i + 1) * chunk_size],
                                           ys[i * chunk_size:(i + 1) * chunk_size],
                                           i * chunk_size, (i + 1) * chunk_size, **kwargs) for i in
                           range(self.num_threads - 1)]
                # Process one part of the data in the main thread
                _start = chunk_size * (self.num_threads - 1)
                self._process(xs[_start:], ys[_start:], 0, -1, chunk_size, **kwargs)
                # Wait for all futures to complete
                concurrent.futures.wait(futures)
                # Get the results
                results = [f.result() for f in futures]
                new_xs = [img for sublist in results for img, _ in sublist]
                new_ys = [target for sublist in results for _, target in sublist]
        else:
            new_xs, new_ys = self._process(xs, ys, 0, -1, **kwargs)
        return new_xs, new_ys

    def _process(self, xs, ys, start, end, **kwargs):
        new_xs = xs.copy()
        new_ys = ys.copy()
        for func, prob in self.augmentations:
            if random.random() < prob:
                try:
                    new_xs, new_ys = func(new_xs, new_ys, **kwargs)
                except Exception as e:
                    raise Exception(f"Error occurred in function {func.__name__} for indexes[{start}, {end}): {str(e)}")
        return new_xs, new_ys


if __name__ == "__main__":
    from lurara.prefab.yolo import *

    _save_dir = r"C:\Users\22290\Desktop\yolovoc"
    _voc_path = r"D:\desktop20231030\yolov8\VOC_UG"
    _cls_txt_name = "predefined_classes.txt"
    img_paths, bboxes = load_pascal_voc_dataset(os.path.join(_voc_path, "JPEGImages"),
                                                os.path.join(_voc_path, "Annotations"),
                                                os.path.join(_voc_path, _cls_txt_name))
    imgs = [cv2.imread(img_path) for img_path in img_paths]

    # degrees=10, translate=.1, scale=.1, shear=10
    config = {
        'degrees': 10,
        'translate': 0.1,
        'scale': 0.1,
    }

    ap = AugmentPipe()

    ap.add(random_affine, prob=1)
    ap.add(augment_hsv, prob=1)
    ap.add(horizontal_flip, prob=0.5)

    new_imgs, new_bboxes = ap(imgs, bboxes, **config)
    # new_imgs, new_bboxes = imgs, bboxes
    # draw rect on img:
    for i, (img, bboxes) in enumerate(zip(new_imgs, new_bboxes)):
        h, w = img.shape[:2]
        for bbox in bboxes:
        #     # bbox is cx, cy, w, h
        #     # trans float to int by shape
            cx, cy, bw, bh = [int(bbox[0] * w), int(bbox[1] * h), int(bbox[2] * w), int(bbox[3] * h)]
            cv2.rectangle(img, (cx - bw // 2, cy - bh // 2), (cx + bw // 2, cy + bh // 2), (0, 0, 255), 2)
        cv2.imwrite(os.path.join(_save_dir, f"augmented_{i}.jpg"), img)