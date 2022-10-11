import cv2
from PIL import Image
import io
import numpy as np

import taichi as ti

ti.init(arch=ti.cpu)


def cv2ToGUI(currenFrame):
    scale = 300 / currenFrame.shape[1]
    dim = (round(currenFrame.shape[1] * scale), round(currenFrame.shape[0] * scale))

    correctFrame = cv2.resize(currenFrame, dim)

    img = Image.fromarray(correctFrame)
    bio = io.BytesIO()
    img.save(bio, format='PNG')
    imgbytes = bio.getvalue()

    return imgbytes