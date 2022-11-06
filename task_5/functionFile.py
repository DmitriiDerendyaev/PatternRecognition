import cv2
import numpy as np


def show_image(image, graph):
    if image.shape[1] > 450:
        scale = 450 / image.shape[1]
        dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
        image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
        img_bytes = cv2.imencode('.png', image)[1].tobytes()
        graph.erase()
        a_id = graph.draw_image(data=img_bytes, location=(0, int((450-image.shape[0])/2)))
        graph.send_figure_to_back(a_id)

    if image.shape[0] > 450:
        scale = 450 / image.shape[0]
        dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
        image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
        img_bytes = cv2.imencode('.png', image)[1].tobytes()
        graph.erase()
        a_id = graph.draw_image(data=img_bytes, location=(int((450-image.shape[1])/2), 0))
        graph.send_figure_to_back(a_id)

    if image.shape[0] < 450 and image.shape[1] < 450:
        if image.shape[0] > image.shape[1]:
            scale = 450 / image.shape[0]
            dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
            image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
            img_bytes = cv2.imencode('.png', image)[1].tobytes()
            graph.erase()
            a_id = graph.draw_image(data=img_bytes, location=(int((450 - image.shape[1]) / 2), 0))
            graph.send_figure_to_back(a_id)
        else:
            scale = 450 / image.shape[1]
            dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
            image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
            img_bytes = cv2.imencode('.png', image)[1].tobytes()
            graph.erase()
            a_id = graph.draw_image(data=img_bytes, location=(0, int((450 - image.shape[0]) / 2)))
            graph.send_figure_to_back(a_id)

def copyRect(src, dst, srcRect, dstRect,
    interpolation = cv2.INTER_LINEAR):
    x0, y0, w0, h0 = srcRect
    x1, y1, w1, h1 = dstRect
    # Resize the contents of the source sub-rectangle.
    # Put the result in the destination sub-rectangle.
    dst[y1:y1 + h1, x1:x1 + w1] = \
        cv2.resize(src[y0:y0 + h0, x0:x0 + w0], (w1, h1),
                   interpolation=interpolation)
