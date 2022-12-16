import cv2 as cv
from scipy.optimize import curve_fit
from numpy import asarray as ar, exp
import sys
import numpy as np

def read_binary(file_path):
    """takes in a binary image

    Args:
        file_path (string): file path to the binary image

    Returns:
        binary_img: the binary image
        coordinates ([x_list, y_list]): the pixel coordinates where x and y on the binary image in a detected edge
    """    
    binary_img = cv.imread(file_path,cv.IMREAD_GRAYSCALE)
    coordinates = np.where(binary_img != 0)

    return binary_img, coordinates



def group_coord(coordinates, threshold=10):
    """find all the pixels where there is an edge from the binary image, and group them into lines.

    Args:
        coordinates ([x_list, y_list]): the pixel coordinates where x and y on the binary image in a detected edge
        threshold (int, optional): the max distance for 2 pixels to be considered in the same group. Defaults to 10.

    Returns:
        new_groups: A nested list. Each line would be a list.
    """ 
    prev = [coordinates[0][0], coordinates[1][0]]
    groups = [[prev]]
    for i in range(1,len(coordinates[0])):
        x = coordinates[0][i]
        y = coordinates[1][i]
        if abs(x-prev[0]) > 10 or abs(y-prev[1]) > 10:
            groups.append([])
        groups[-1].append([x,y])
        prev = [x,y]
    new_groups = []
    for g in groups:
        x_list = [x for x,_ in g]
        y_list = [y for _,y in g]
        new_groups.append([x_list, y_list])

    return new_groups

def find_scale(x,y,bed_x=800, bed_y=400):
    """scales pixel value to bed size

    Args:
        x (list of int): all x coordinates in image
        y (list of int): all y coordinates in image
        bed_x (int, optional): size of bed in x axis. Defaults to 800.
        bed_y (int, optional): size of bed in y axis. Defaults to 400.
    Returns:
        scale_size (float): return the scale ratio to fully strech/shrink the image on canvas
    """    
    
    x_scale = (max(x) - min(x))/bed_x
    y_scale = (max(y) - min(y))/bed_y
    if x_scale < 1 and y_scale < 1:
        # if image is larger, we need to make smaller
        scale_size = max(x_scale,y_scale)
    elif x_scale > 1 and y_scale > 1:
        # image is too small, we need to make it larger
        scale_size = max(x_scale, y_scale)
    elif x_scale < 1:
        # y is too large, we need to scale down by y
        scale_size = y_scale
    else:
        # x is too large, scale down by x
        scale_size = x_scale
    return scale_size

def scale_image(x,y,scale):
    """scales all pixels in the binary image

    Args:
        x (list of int): all x coordinates in image
        y (list of int): all y coordinates in image
        scale (float): scale ratio

    Returns:
        the scaled image
    """        
    return [x/scale for x in x_lst], [y/scale for y in y_lst]


def generate_gcode(x,y):
    """Generate the command list to generate G-code

    Args:
        x (list of int): all x coordinates in one line
        y (list of int): all y coordinates in one line

    Returns:
        command_list: the command for this line
    """    
    command_list = ["G1 Z1;"]
    for i in range(len(x)):
        command_list += ["G1 X"+str(x[i]) + " Y"+str(y[i]) +";"]
    command_list.append("G1 Z0;")
    return command_list


def write_file(filepath, info):
    f = open(filepath,"w")
    f.write(info)
    f.close()

# find the a & b points
def get_bezier_coef(points):
    """finds matrix of control points for bezier curves

    Args:
        points: coordinates

    Returns:
        A,B: 2 control points for bezier curve
    """    

    n = len(points) - 1

    # build coefficents matrix
    C = 4 * np.identity(n)
    np.fill_diagonal(C[1:], 1)
    np.fill_diagonal(C[:, 1:], 1)
    C[0, 0] = 2
    C[n - 1, n - 1] = 7
    C[n - 1, n - 2] = 2

    # build points vector
    P = [2 * (2 * points[i] + points[i + 1]) for i in range(n)]
    P[0] = points[0] + 2 * points[1]
    P[n - 1] = 8 * points[n - 1] + points[n]

    # solve system, find a & b
    A = np.linalg.solve(C, P)
    B = [0] * n
    for i in range(n - 1):
        B[i] = 2 * points[i + 1] - A[i + 1]
    B[n - 1] = (A[n - 1] + points[n]) / 2

    return A, B

def get_cubic(a, b, c, d):
    """finds the general Bezier cubic formula given 4 control points
    """    
    return lambda t: np.power(1 - t, 3) * a + 3 * np.power(1 - t, 2) * t * b + 3 * (1 - t) * np.power(t, 2) * c + np.power(t, 3) * d


def get_bezier_cubic(points):
    """return one cubic curve for each consecutive points
    """    
    A, B = get_bezier_coef(points)
    return [
        get_cubic(points[i], A[i], B[i], points[i + 1])
        for i in range(len(points) - 1)
    ]

def get_control_points(points):
    """ find control points
    """    
    lst = []
    A, B = get_bezier_coef(points)
    for i in range(0,len(points)-1,5):
        lst.append([points[i],A[i],B[i],points[i+1]])
    return lst

def evaluate_bezier(points, n):
    """evalute each cubic curve on the range [0, 1] sliced in n points
    """    
    curves = get_bezier_cubic(points)
    return np.array([fun(t) for fun in curves for t in np.linspace(0, 1, n)])



if __name__ == "__main__":
    inFile = sys.argv[1] # type the file path right after generate_command.py
    img, points = read_binary(inFile)
    scale = find_scale(points[0],points[1])
    commands = []
    for line in points:
        if len(line) < 4:
            continue
        line = np.asarray(line)
        curve = get_control_points(line)
            
        starting_point = [["M"] + ["{:.2f}".format(l) for l in line[0]]]
        curve_command = []
        for c in curve:
            curve_command.append(["C"]+["{:.2f}".format(elem) for p in c[1:] for elem in p])
        commands += (starting_point + curve_command)
    
    savepath = '.'.join([''.join([inFile.split(".")[0],"_edge"]), inFile.split(".")[1]])
    write_file(savepath, commands)
