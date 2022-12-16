"""
Code for turning bezier curves into a list of points and then writing those points
to Gcode. Also includes code for scaling images
"""
import numpy as np
import Gcode_tests
def svg_commands_to_gcode(filename,start_point,path_commands,scalers,draw_height=0):
    """
    This function takes a list of svg commands with different key letters and
    converts those equations into points which it writes to Gcode.

    filename:
        a string representing the name of the file to write to
    start_point: 
        list of two floats representing the x and y coordinates of the next command will start at
    path_commands:
        list of strings containing the key letter and command arguments
    scalers: 
        list of 2 ints representing how much to scale an image (unused)
    draw_height:
        an integer representing the height at which to draw the image
    """
    points = []

    #need to have a curve start point for the Z,z commands
    curve_start = [0,0]
    for path_command in path_commands:
            
        command = path_command[0]

        if command.upper() == "M":
            
            #make sure everything is absolute
            destination = [float(path_command[1]),float(path_command[2])]


            if command =='m':
                destination = rel_to_abs(start_point,destination)
            
            start_point = destination
            curve_start = destination
            with open(filename,"a") as f:
                Gcode_tests.retraction_move(f,draw_height,destination)
            
        elif command.upper() == "C":
            points,end_point = path_C(start_point,path_command,scalers,6)

            #print(points)

            xpoints,ypoints = split_lists(points)
            start_point = end_point

            #print(xpoints)
            #print(ypoints)
            #all curves are linked unless the M command is done
            Gcode_tests.arbitrary_curve(filename,xpoints,ypoints,draw_height,init_linked=True)
        elif command.upper() == "L":
            points,end_point = path_L(start_point,path_command,scalers,2)

            xpoints,ypoints = split_lists(points)
            start_point = end_point

            #all curves are linked unless the M command is done
            Gcode_tests.arbitrary_curve(filename,xpoints,ypoints,draw_height,init_linked=True)


        elif command.upper() == 'H':
            
            points,end_point = path_H(start_point,path_command,scalers,2)

            xpoints,ypoints = split_lists(points)
            start_point = end_point

            #all curves are linked unless the M command is done
            Gcode_tests.arbitrary_curve(filename,xpoints,ypoints,draw_height,init_linked=True)
        elif command.upper() == 'V':
            
            points,end_point = path_V(start_point,path_command,scalers,2)

            xpoints,ypoints = split_lists(points)
            start_point = end_point

            #all curves are linked unless the M command is done
            Gcode_tests.arbitrary_curve(filename,xpoints,ypoints,draw_height,init_linked=True)
        elif command.upper() == 'Z':
            #close the curve
            #print(f"curve start is {curve_start}")
            Gcode_tests.arbitrary_curve(filename,[start_point[0],curve_start[0]],[start_point[1],curve_start[1]],draw_height,init_linked=True)

            start_point = curve_start



def path_C(start_point,path_command,scalers,numpoints =15):
    """
    Creates a list of points for the path C or c commands

    Args:
    start_point: 
        list of two floats representing the x and y coordinates of the next command will start at
    path_command:
        a list containing 1 letter and a series of integers or floats determining the bezier curve
    scalers: 
        list of 2 ints representing how much to scale an image (unused)
    numpoints:
        an integer representing the number of points to draw of a curve
    
    Returns:
    point_list:
        a list of floats in the form [x1,y1,x2,y2,x3,y3,etc...]
    end_point:
        a list of floats representing the last x and y point of the drawn curve
    """
    
    #get just the coordinates, not the letter
    coordinates = path_command[1:7]

    #used to be int()
    coordinates = [float(i) for i in coordinates]

    if path_command[0] == 'c':


        coordinates = rel_to_abs(start_point,coordinates)
    

    #print(coordinates)
    #parameter for the curve
    t_list = np.linspace(0,1,numpoints)

    point_list = []

    #create the points
    for t in t_list:

        
        #print(coordinates)
        xcoord = (1-t)**3 *float(start_point[0]) + 3* (1-t)**2 *t*coordinates[0] + 3* (1-t) *(t**2)*coordinates[2] + (t**3)*coordinates[4]
        ycoord = (1-t)**3 *float(start_point[1]) + 3* (1-t)**2 *t*coordinates[1] + 3* (1-t) *(t**2)*coordinates[3] + (t**3)*coordinates[5]
        point_list.append([xcoord,ycoord])

    end_point = point_list[numpoints-1]
    return point_list,end_point

def path_L(start_point,path_command,scalers,numpoints =15):
    """
    Creates a list of points for the path L or l commands
    
    Args:
    start_point: 
        list of two floats representing the x and y coordinates of the next command will start at
    path_command:
        a list containing 1 letter and a series of integers or floats determining the bezier curve
    scalers: 
        list of 2 ints representing how much to scale an image (unused)
    numpoints:
        an integer representing the number of points to draw of a curve
    
    Returns:
    point_list:
        a list of floats in the form [x1,y1,x2,y2,x3,y3,etc...]
    end_point:
        a list of floats representing the last x and y point of the drawn curve
    """
    
    #get just the coordinates, not the letter
    coordinates = path_command[1:3]

    coordinates = [float(i) for i in coordinates]

    if path_command[0] == 'l':
        coordinates = rel_to_abs(start_point,coordinates)
    
    t_list = np.linspace(0,1,numpoints)

    point_list = []

    #create the points
    for t in t_list:
        #used to be int()
        xcoord = (1-t) *float(start_point[0]) + t*coordinates[0]
        ycoord = (1-t) *float(start_point[1]) + t*coordinates[1]
        point_list.append([xcoord,ycoord])

    end_point = point_list[numpoints-1]
    return point_list,end_point

def path_H(start_point,path_command,scalers,numpoints =15):
    """
    Creates a list of points for the path H or h commands
    
    Args:
    start_point: 
        list of two floats representing the x and y coordinates of the next command will start at
    path_command:
        a list containing 1 letter and a series of integers or floats determining the bezier curve
    scalers: 
        list of 2 ints representing how much to scale an image (unused)
    numpoints:
        an integer representing the number of points to draw of a curve
    
    Returns:
    point_list:
        a list of floats in the form [x1,y1,x2,y2,x3,y3,etc...]
    end_point:
        a list of floats representing the last x and y point of the drawn curve
    """
    #horizontal line
    end_point = path_command[1]
    if path_command[0] == 'h':
        #make it absolute
        #used to be int()
        end_point = float(path_command[1]) + float(start_point[0]) #0 bc horizontal line
    
    new_path_command = ['L',str(end_point),str(start_point[1])]
    return path_L(start_point,new_path_command,scalers,numpoints)

def path_V(start_point,path_command,scalers,numpoints =15):
    """
    Creates a list of points for the path V or v commands
    
    Args:
    start_point: 
        list of two floats representing the x and y coordinates of the next command will start at
    path_command:
        a list containing 1 letter and a series of integers or floats determining the bezier curve
    scalers: 
        list of 2 ints representing how much to scale an image (unused)
    numpoints:
        an integer representing the number of points to draw of a curve
    
    Returns:
    point_list:
        a list of floats in the form [x1,y1,x2,y2,x3,y3,etc...]
    end_point:
        a list of floats representing the last x and y point of the drawn curve
    """
    #vertical line
    end_point = path_command[1]
    if path_command[0] == 'v':
        #make it absolute
        end_point = float(path_command[1]) + float(start_point[1]) #1 bc vert line

    new_path_command = ['L',str(start_point[0]),str(end_point)]
    return path_L(start_point,new_path_command,scalers,numpoints)


def rel_to_abs(start_point,point_list):
    """
    Converts a list of points points from relative to absolute coordinates
    
    Args:
    start_point:
        list of two floats representing the x and y coordinates of the next command will start at
    point_list: 
        a list of floats in the form [x1,y1,x2,y2,x3,y3,etc...]
    
    Returns:
    new_coords:
        a list of floats in absolute coordinates in the form [x1,y1,x2,y2,x3,y3,etc...]
    """
    new_coords = []
    for i in range(len(point_list)):
        addend = start_point[i%2] #if 0 x coord, if 1 ycoord

        #used to be int()
        new_coords.append(float(addend) + float(point_list[i]))

    return new_coords

def split_lists(list):
    """
    Converts one list of points into two lists of x and y points
    
    Args:
    list: 
        a list of floats in the form [x1,y1,x2,y2,x3,y3,etc...]
    Returns:
    xlist: 
        a list of floats representing sequential x point components
    ylist: 
        a list of floats representing sequential y point components   
    """
    #list is a list of elements with an even number of elements

    #split list by odd and even
    xlist = []
    ylist = []
    for i in range(len(list)):
        xlist.append(list[i][0])
        ylist.append(list[i][1])
    return xlist,ylist

def scale_commands(command_list,scalers):
    """
    This function scales an image by a certain amount

    path_commands:
        list of strings containing the key letter and command arguments
    scalers: 
        list of 2 ints representing how much to scale an image by in the x and y direction
    Returns:
    new_command_list:
        list of strings containing the key letter and command arguments scaled by the specified amount
    """
    #scale all control points by the scalers

    xscale = scalers[0]
    yscale = scalers[1]

    new_command_list = []
    for command in command_list:

        if command[0] == 'c' or command[0] == 'C':
            new_command = [command[0],str(xscale*float(command[1])),str(yscale*float(command[2])),str(xscale*float(command[3])),str(yscale*float(command[4])),str(xscale*float(command[5])),str(yscale*float(command[6]))]
        elif command[0] == 'm' or command[0] == 'M':
            new_command = [command[0],str(xscale*float(command[1])),str(yscale*float(command[2]))]
        elif command[0] == 'l' or command[0] == 'L':
            new_command = [command[0],str(xscale*float(command[1])),str(yscale*float(command[2]))]
        elif command[0] == 'h' or command[0] == 'H':
            new_command = [command[0],str(xscale*float(command[1]))]
        elif command[0] == 'v' or command[0] == 'V':
            new_command = [command[0],str(yscale*float(command[1]))]
        elif command[0] == 'Z' or command[0] == 'Z':
            new_command = [command[0]]

        
        new_command_list.append(new_command)

    return new_command_list
