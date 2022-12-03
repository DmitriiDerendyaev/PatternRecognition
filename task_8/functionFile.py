import cv2


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