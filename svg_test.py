"""
printbed 5x5 inches


bed_range_y = 5 #inches
bed_range_x = 5 #inches
drawing_scale = 100 #incriments per inch
point_range_y = bed_range_y*drawing_scale
point_range_x = bed_range_x*drawing_scale
"""


def initialize_drawing(filename,bed_size,drawing_scale):
    """
    filename:
        a string representing the name of the file to write to
    bed_size:
        a list of 2 integers with the drawable bed size in x and y coordinates
        in inches
    drawing_scale:
        an integer representing the resolution of the images in points per inch
    """

    bed_range_y = bed_size[1] #inches
    bed_range_x = bed_size[0] #inches
    point_range_y = bed_range_y*drawing_scale
    point_range_x = bed_range_x*drawing_scale

    with open(filename,"w") as f:
        
        #open svg and set viewbox
        f.write(f"<svg viewBox=\"0 0 {point_range_x} {point_range_y}\">\n")
def finish_drawing(filename):
    "add the final line to an svg"
    with open(filename,"a") as f: f.write("</svg>")

def polyline_svg(filename,pointlist):
    """
    filename:
        a string representing the name of the file to write to
    pointlist:
        a list of lists containing two integers, containing an x and a y 
        coordinates in points
    """
    with open(filename,"a") as f:
        
        #open svg and set viewbox
        f.write("<polyline points=\"")
        for coords in pointlist:
            f.write(f"{pointlist[0]},{pointlist[1]} ")
        f.write("\"\n")
        f.write("style=\"fill:none;stroke:black;stroke-width:3\" />\n")