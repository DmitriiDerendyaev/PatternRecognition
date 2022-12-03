import cv2
import numpy as np


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

# function to read the images by taking there path
def read_image(path1, path2):
    read_img1 = cv2.imread(path1)
    read_img2 = cv2.imread(path2)
    return (read_img1, read_img2)


# function to convert images from RGB to gray scale
def convert_to_grayscale(pic1, pic2):
    gray_img1 = cv2.cvtColor(pic1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(pic2, cv2.COLOR_BGR2GRAY)
    return (gray_img1, gray_img2)


# function to detect the features by finding key points
# and descriptors from the image
def detector(image1, image2):
    # creating ORB detector
    detect = cv2.ORB_create()

    # finding key points and descriptors of both images using
    # detectAndCompute() function
    key_point1, descrip1 = detect.detectAndCompute(image1, None)
    key_point2, descrip2 = detect.detectAndCompute(image2, None)
    return (key_point1, descrip1, key_point2, descrip2)


# function to find best detected features using brute force
# matcher and match them according to there humming distance
def BF_FeatureMatcher(des1, des2):
    brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    no_of_matches = brute_force.match(des1, des2)

    # finding the humming distance of the matches and sorting them
    no_of_matches = sorted(no_of_matches, key=lambda x: x.distance)
    return no_of_matches


# function displaying the output image with the feature matching
def display_output(pic1, kpt1, pic2, kpt2, best_match):
    # drawing the feature matches using drawMatches() function
    output_image = cv2.drawMatches(pic1, kpt1, pic2, kpt2, best_match, None, flags=2)
    return output_image
