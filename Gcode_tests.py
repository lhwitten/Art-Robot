"""
This file contains code for writing Gcode files
"""
#import numpy as np
#test_file = "straight_line_text.gcode"


def initialize_drawing(filename):
    """
    Write the first three lines of a Gcode file (unused)

    Args:
    filename: 
        a string representing a file to write to
    """
    with open(filename,"a") as f:

        f.write("G21\n") # set units to millimeters
        f.write("G90\n") # use absolute positioning
        f.write("G92 X0 Y0 Z0\n") #sets current coordinates, to 000, we're assuming we're starting the thing at 0 bc i don't know how homing works


def straight_line(filename,point1,point2,draw_height,linked=False):
    """
    Writes the directions to draw a straight line between two points to a file,
    also initiates picking and lowering the pen

    filename:
        a string representing a file to write to 
    point1: 
        a list with 2 integers or floats, xy coordinates in steps
    point2:
        a list with 2 integers or floats, xy coordinates in steps
    draw_height:
        the height at which to draw the image (unused)
    linked:
        a boolean representing if the current line follows directly from the last one
    """
    with open(filename,"a") as f:
        
        #round to two decimals
        xstart = round(point1[0], 2)
        ystart = round(point1[1], 2)
        xend = round(point2[0], 2)
        yend = round(point2[1], 2)

        if not linked:
            retraction_move(f,draw_height,[xstart,ystart])
        
        line = f"G1 X{xend} Y{yend};\n"
        f.write(line)

def retract(appendable,draw_height):
    """
    Writes to a file to retract the pen

    Args:
    appendable:
        an open file you can write to 
    draw_height:
        the height at which to draw the image (unused)
    
    """
    line = f"G1 Z{1};\n"
    appendable.write(line)

def unretract(appendable,draw_height):
    """
    Writes to a file to unretract the pen

    Args:
    appendable:
        an open file you can write to 
    draw_height:
        the height at which to draw the image (unused)
    
    """
    line = f"G1 Z{0};\n"
    appendable.write(line)

def arbitrary_curve(filename,xpoints,ypoints,draw_height,init_linked=False):
    """
    Writes the Gcode commands for any arbitary parametric curve to a file when
    provided a list of points

    Args:
    filename:
        a string representing a file to write to 
    xpoints: 
        a list containing floats of the x positions of all of the points
    ypoints:
        a list containing floats of the y positions of all of the points,
        equal in length to xpoints
    draw_height:
        the height at which to draw the image (unused)
    linked:
        a boolean representing if the current line follows directly from the last one
    """
    

    #move to first point 
    straight_line(filename,[xpoints[0],ypoints[0]],[xpoints[1],ypoints[1]],draw_height,init_linked)

    #other points can be done automatically
    for index in range(len(xpoints) -2 ):
        
        first_point = [xpoints[index+1],ypoints[index+1]]
        next_point = [xpoints[index+2],ypoints[index+2]]
        straight_line(filename,first_point,next_point,draw_height,True)

def retraction_move(f,draw_height,destination):
    """
    Writes to a file to retract the pen, move to a location, and then unretract

    Args:
    f:
        an open file you can write to 
    draw_height:
        the height at which to draw the image (unused)
    destination:
        a list containing an x and a y coordinate as a float to move to
    """
    x = destination[0]
    y = destination[1]
    retract(f,draw_height)
    mov_ln = f"G0 X{x} Y{y};\n"
    f.write(mov_ln)
    unretract(f,draw_height)
