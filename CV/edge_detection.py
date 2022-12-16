import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numpy import asarray as ar, exp
import cv2 as cv
import numpy as np
import sys

def read_image(file_path, display=False):
    """reads an image file from a file path

    Args:
        file_path (_type_): _description_
        display (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """    
    img = cv.imread(file_path)
    if display:
        cv.imshow("img",img)
        if cv.waitKey(0):
            cv.destroyAllWindows();

    return img
    
def save_image(img,target_path):
    cv.imwrite(target_path,img)

def take_image():
    cap = cv.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv.imshow("live view", frame)
        k = cv.waitKey(1)
        if k%256  == 32:
            cv.imwrite('pic.png', frame)
            cv.destroyAllWindows()
            break;
    cap.release()

def increase_brightness(img, value=30):
    """increases the brightness in an given BGR image

    @param:
        value: By what amount to increase the brightness, should range from 0 to 255.

    Returns:
        _type_: _description_
    """    
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv.merge((h, s, v))
    img = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)
    return img

def image_process(img, brightness_value=0,kernel_size=(5,5)):
    """preprocess image for edge detection if Canny does not work well.

    internal images:
        bright: brightness increased image
        gray: converts to gray image for future processings
        kernel: the kernel for dilation
        dilated: dilated image, makes edges more detectable
        diff1: how different is dilated from the original gray part -- we leave the emphasized part which are the edges
        median: blur the image so that the background can be smoother and not detected.
        diff2: how different is the original from the smoothed image

        normed images: normalize the 2 diff images
        thresh: binary image from the process -- our edges!
    """    
    bright = increase_brightness(img,brightness_value)
    gray = cv.cvtColor(bright, cv.COLOR_BGR2GRAY)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,kernel_size)
    dilated = cv.morphologyEx(gray, cv.MORPH_DILATE, kernel)
    diff1 = 255-cv.subtract(dilated, gray)

    median = cv.medianBlur(dilated, 15)
    diff2 = 255 - cv.subtract(median, gray)

    normed1 = cv.normalize(diff1, None, 0, 255, cv.NORM_MINMAX)
    normed2 = cv.normalize(diff2, None, 0, 255, cv.NORM_MINMAX)
    thresh = cv.threshold(normed1, 150, 255, cv.THRESH_BINARY_INV)[1]

    return thresh
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        inFile = sys.argv[1] # type the file path right after edge_detection.py
    else:
        take_image()
        inFile = "pic.png"
    filepath = inFile
    savepath = '.'.join([''.join([filepath.split(".")[0],"_edge"]), filepath.split(".")[1]])
    print(savepath)
    image = read_image(filepath,display=False)
    edge = image_process(image)
    save_image(edge, savepath)