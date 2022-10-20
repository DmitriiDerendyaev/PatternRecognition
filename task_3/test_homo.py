import cv2
import numpy as np


def mouse_handler(event, x, y, flags, data):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(data['im'], (x, y), 25, (0, 0, 255), -1)
        cv2.imshow("Image", data['im'])
        if len(data['points']) == 4:
            data['points'].append([x, y])


def get_four_points(im):
    data = {}
    data['im'] = im.copy()
    data['points'] = []

    cv2.imshow("Image", im)
    cv2.setMouseCallback("Image", mouse_handler, data)
    cv2.waitKey(0)

    points = np.float32(data['points'])
    return points


if __name__ == '__main__':
    # Read in the image.
    im_src = cv2.imread('book1.jpg')

    # Show image and wait for 4 clicks.
    pts_src = get_four_points(im_src)

    # Book size
    size = (1500, 2000)

    # Destination coordinates located in the center of the image
    pts_dst = np.float32(
        [
            [im_src.shape[1] / 2 - size[0] / 2, im_src.shape[0] / 2 - size[1] / 2],
            [im_src.shape[1] / 2 + size[0] / 2, im_src.shape[0] / 2 - size[1] / 2],
            [im_src.shape[1] / 2 + size[0] / 2, im_src.shape[0] / 2 + size[1] / 2],
            [im_src.shape[1] / 2 - size[0] / 2, im_src.shape[0] / 2 + size[1] / 2]
        ]
    )

    # Calculate the homography
    M = cv2.getPerspectiveTransform(pts_src, pts_dst)

    # Warp source image to destination
    im_out = cv2.warpPerspective(im_src, M, (im_src.shape[1], im_src.shape[0]))

    # Show output
    cv2.imshow("Warped Source Image", im_out)
    cv2.imwrite("book_bird_eye_view.jpg", im_out)

    cv2.waitKey(0)