import cv2
import numpy as np


# def show_image(image, graph):
#     if image.shape[1] > 450:
#         scale = 450 / image.shape[1]
#         dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
#         image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
#         img_bytes = cv2.imencode('.png', image)[1].tobytes()
#         graph.erase()
#         a_id = graph.draw_image(data=img_bytes, location=(0, int((450 - image.shape[0]) / 2)))
#         graph.send_figure_to_back(a_id)
#
#     if image.shape[0] > 450:
#         scale = 450 / image.shape[0]
#         dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
#         image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
#         img_bytes = cv2.imencode('.png', image)[1].tobytes()
#         graph.erase()
#         a_id = graph.draw_image(data=img_bytes, location=(int((450 - image.shape[1]) / 2), 0))
#         graph.send_figure_to_back(a_id)
#
#     if image.shape[0] < 450 and image.shape[1] < 450:
#         if image.shape[0] > image.shape[1]:
#             scale = 450 / image.shape[0]
#             dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
#             image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
#             img_bytes = cv2.imencode('.png', image)[1].tobytes()
#             graph.erase()
#             a_id = graph.draw_image(data=img_bytes, location=(int((450 - image.shape[1]) / 2), 0))
#             graph.send_figure_to_back(a_id)
#         else:
#             scale = 450 / image.shape[1]
#             dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
#             image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
#             img_bytes = cv2.imencode('.png', image)[1].tobytes()
#             graph.erase()
#             a_id = graph.draw_image(data=img_bytes, location=(0, int((450 - image.shape[0]) / 2)))
#             graph.send_figure_to_back(a_id)

def show_image(image, window_graph):
    if image.shape[0] < image.shape[1]:
        scale = 450 / image.shape[1]

    else:
        scale = 450 / image.shape[0]

    dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
    image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
    img_bytes = cv2.imencode('.png', image)[1].tobytes()

    window_graph.erase()
    if image.shape[0] < image.shape[1]:
        a = 0
        b = int((450-image.shape[0])/2)
    else:
        a = int((450 - image.shape[1]) / 2)
        b = 0
    a_id = window_graph.draw_image(data=img_bytes, location=(a, b))
    window_graph.send_figure_to_back(a_id)

def copyRect(src, dst, srcRect, dstRect,
             interpolation=cv2.INTER_LINEAR):
    x0, y0, w0, h0 = srcRect
    x1, y1, w1, h1 = dstRect
    dst[y1:y1 + h1, x1:x1 + w1] = \
        cv2.resize(src[y0:y0 + h0, x0:x0 + w0], (w1, h1),
                   interpolation=interpolation)


def find_size(image):
    if image.shape[1] > 450:
        scale = 450 / image.shape[1]
        dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
        image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)

    if image.shape[0] > 450:
        scale = 450 / image.shape[0]
        dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
        image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)

    if image.shape[0] < 450 and image.shape[1] < 450:
        if image.shape[0] > image.shape[1]:
            scale = 450 / image.shape[0]
            dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
            image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)

        else:
            scale = 450 / image.shape[1]
            dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
            image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
    return image


def draw_found_faces(detected, image, color: tuple):
    for (x, y, width, height) in detected:
        cv2.rectangle(
            image,
            (x, y),
            (x + width, y + height),
            color,
            thickness=2
        )

def reSizeMask(image, sizeMask):
    if image.shape[1] > sizeMask:
        scale = sizeMask / image.shape[1]
        dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
        image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)

    if image.shape[0] > sizeMask:
        scale = sizeMask / image.shape[0]
        dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
        image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)

    if image.shape[0] < sizeMask and image.shape[1] < sizeMask:
        if image.shape[0] > image.shape[1]:
            scale = sizeMask / image.shape[0]
            dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
            image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)

        else:
            scale = sizeMask / image.shape[1]
            dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
            image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
    return image

def draw_mask_faces(detected, image, mask):
    for (x, y, width, height) in detected:
        newMask = reSizeMask(mask, width)
        heightMask, widthMask= newMask.shape[:2]
        image[y:y+heightMask, x:x+widthMask] = newMask