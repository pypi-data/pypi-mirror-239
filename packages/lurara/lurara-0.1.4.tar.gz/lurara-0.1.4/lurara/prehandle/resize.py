import cv2
import numpy as np
from copy import deepcopy

def fillresize(x:np.ndarray, new_size:tuple, fill:float) -> np.ndarray:
    # Compute the ratio of the new size and the original size
    ratio = min(new_size[0] / x.shape[0], new_size[1] / x.shape[1])

    # Compute the size of the resized image
    resize_size = (round(x.shape[1] * ratio), round(x.shape[0] * ratio))

    # Resize the image
    x_resized = cv2.resize(x, resize_size, interpolation = cv2.INTER_AREA)

    # Create a new array filled with the fill value
    new_x = np.full((*new_size, x.shape[2]), fill, dtype=x.dtype)

    # Compute the starting indices for x_resized
    start_y = (new_size[0] - x_resized.shape[0]) // 2
    start_x = (new_size[1] - x_resized.shape[1]) // 2

    # Copy x_resized into the center of new_x
    new_x[start_y:start_y+x_resized.shape[0], start_x:start_x+x_resized.shape[1]] = x_resized

    return new_x

def bboxresize(y: list, old_size: tuple, new_size: tuple) -> list:
    """
    Resize bounding boxes according to the ratio of the new size and the original size
    :param y: list of [cx, cy, w, h, cls], and cx cy w h is float 0 - 1
    :param old_size:
    :param new_size:
    :return:
    """
    y = deepcopy(y)
    # Compute the ratio of the new size and the original size
    _y, _x = new_size[0] / old_size[0], new_size[1] / old_size[1]
    if _y == _x:
        return y

    if 1 < _y < _x:
        _ratio = [_y / _x, 1]
    elif _y < _x < 1:
        _ratio = [1, _y / _x]

    if 1 < _x < _y:
        _ratio = [1, _x / _y]
    elif _x < _y < 1:
        _ratio = [_x / _y, 1]

    for bbox in y:
        if _ratio[1] != 1:
            bbox[0] = (bbox[0] - 0.5) * _ratio[1] + .5
        if _ratio[0] != 1:
            bbox[1] = (bbox[1] - 0.5) * _ratio[0] + 0.5
        bbox[2] *= _ratio[1]
        bbox[3] *= _ratio[0]

    return y
