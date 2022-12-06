"""
Testing how to write Gcode files

we're working in mm


187 mm per 1000 steps
"""
#import numpy as np
test_file = "straight_line_text.gcode"


def initialize_drawing(filename):

    with open(filename,"a") as f:

        f.write("G21\n") # set units to millimeters
        f.write("G90\n") # use absolute positioning
        f.write("G92 X0 Y0 Z0\n") #sets current coordinates, to 000, we're assuming we're starting the thing at 0 bc i don't know how homing works


def straight_line(filename,point1,point2,draw_height,linked=False):
    """
    filename = string that is the filename of 
    point1 = a list with 2 integers, xy coordinates mm
    point2 = a list with 2 integers, xy coordinates mm

    """
    with open(filename,"a") as f:
        #blahblahblah

        xstart = point1[0]
        ystart = point1[1]
        xend = point2[0]
        yend = point2[1]

        if not linked:
            retraction_move(f,draw_height,[xstart,ystart])
        
        line = f"G1 X{xend} Y{yend}\n"
        f.write(line)

def retract(appendable,draw_height):
    line = f"G1 Z{draw_height+1}\n"
    appendable.write(line)

def unretract(appendable,draw_height):

    line = f"G1 Z{draw_height}\n"
    appendable.write(line)

def arbitrary_curve(filename,xpoints,ypoints,draw_height,init_linked=False):
    """
    init_linked:
        is this curve initially linked to another curve

    xpoints is a list of floats of equal length to ypoitns
    """
    

    #move to first point 
    straight_line(filename,[xpoints[0],ypoints[0]],[xpoints[1],ypoints[1]],draw_height,init_linked)

    #other points can be done automatically
    for index in range(len(xpoints) -2 ):
        
        first_point = [xpoints[index+1],ypoints[index+1]]
        next_point = [xpoints[index+2],ypoints[index+2]]
        straight_line(filename,first_point,next_point,draw_height,True)

def retraction_move(f,draw_height,destination):

    x = destination[0]
    y = destination[1]
    retract(f,draw_height)
    mov_ln = f"G0 X{x} Y{y}\n"
    f.write(mov_ln)
    unretract(f,draw_height)
