"""
Code for reading and writing (unused) SVG files.
"""

import csv

#code for writing svgs


def initialize_drawing(filename,bed_size,drawing_scale):
    """
    Code for initializing an SVG Drawing (unused)

    Args:
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
    """
    add the final line to an svg (unused)
    
    Args:
    filename:
        a string representing the name of a file
    """
    with open(filename,"a") as f: f.write("</svg>")

def polyline_svg(filename,pointlist):
    """
    Write a polyline to an SVG file (unused)
    Args:
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

#code for reading svgs. only works for path commands currently

def parse_svg(filename):
    """
    Read all relevant commands and arguments from an SVG file

    Args:
    filename:
        a string representing the name of a file
    
    Returns:
    command_list:
        a list of lists of strings and arguments containing the letter command to parse and that commands
        float or integer arguments
    viewBox:
        a list of integers representing the bounding box for the image
    
    """
    #its a list of lists
    command_list =[]
    with open(filename,"r") as f:

        
        viewBox = [0,0,0,0]
        #for row in reader:

        #first split into an array starting with <
        file_commands = f.read().split("<")
        #replace all new lines with spaces
        file_commands = [command.replace("\n"," ") for command in file_commands]
        #delete commas, kittykat.svg has commas instead of spaces in some places
        file_commands = [command.replace(","," ") for command in file_commands]
        file_commands = [command.replace("-"," -").replace('e -','e-') for command in file_commands]


        #clean up the created junk
        file_commands.remove('')
        #not used?
        file_command = [command[1:-1] for command in file_commands]

        #we now have a list of commands
        #print(file_commands)
        for command in file_commands:
            
            #find the command
            #print(command)
        
            
            temp_end = command.find(" ")

            #print(temp_end)
            start_word = command[0:temp_end]
            #print(start_word)

            #only parsing paths right now

            #we need to find the viewbox
            if start_word == "svg":
                
                if "height=" not in command:
                    continue 
                temp_start = command.find("height=") +8
                temp_end = command.find("\"",temp_start)

                #print(temp_start)
                #print(temp_end)

                #print(command)
                viewBox[3] = command[temp_start:temp_end]

                temp_start = command.find("width=") +7
                temp_end = command.find("\"",temp_start)

                viewBox[2] = command[temp_start:temp_end]
                
                print(viewBox)

                
                #height_start = command.find("height")

                if "px" in viewBox[2]:
                    viewBox[2] = viewBox[2][0:-2] 
                viewBox[2] = float(viewBox[2])
                if "px" in viewBox[3]:
                    viewBox[3] = viewBox[3][0:-2] 
                viewBox[3] = float(viewBox[3])


            if start_word == "path":
                #print("parsing")

                #print(f"command is {command}")
                parse_pathline(command,command_list)
    return command_list,viewBox






def parse_pathline(line,command_list):
    """
    Iterates through the path string in an svg file and picks out individual commands
    from it, adding them to a list of commands

    Args:
    line:
        a string representing all information that occurs within a "path" line within an svg
    command_list:
        a list of lists of strings and arguments containing the letter command to parse and that commands
        float or integer arguments

    """

    #command_list is a list of lists

    #may need to do additional pre-processing of the file

    #find where the path line starts

    temp_start = line.find(" d=") +4
    temp_end = line.find("\"",temp_start)

    
    path_data = line[temp_start:temp_end]

    #print(f"path data is {path_data}")

    #from here we should be able to get everything we need

    #need to split it into segments

    stop_codes_abs = ['M',"L","H","V","C","S","Q","T","A","Z"]
    stop_codes_rel = ['m',"l","h","v","c","s","q","t","a","z"]
    stop_codes = stop_codes_abs + stop_codes_rel

    #Im realizing I should have made those lists a dictionary the whole time
    #whoops. i can fix it later, but for now we're gonna have both

    stopcode_dict = {'M':2,"L":2,"H":1,"V":1,"C":6,"S":4,"Q":4,"T":2,"A":7,"Z":0, \
    'm':2,"l":2,"h":1,"v":1,"c":6,"s":4,"q":4,"t":2,"a":7,"z":0}



    #we're parsing until we're not
    run = True
    i =0
    while run:
        #this is because im in a while loop and im scared... removing, should work now
        '''
        i+=1
        if i > 250:
            break
        '''
        #we care about the start letter because it defines what kind of command we're doing
        temp_start,start_letter = find_first_occurence_of_multiple(path_data,stop_codes)

        #print(f"start letter is {start_letter}")

        #print(f"next search path is {path_data[temp_start+1:-1]}")

        #print("searched string is")
        #print(path_data[temp_start+1:len(path_data)])
        temp_end, end_letter = find_first_occurence_of_multiple(path_data[temp_start+1:len(path_data)],stop_codes)
        
        #print(f"end letter is {end_letter}")

        #print(f"end index is {temp_end}")

        #stop parsing if we're at the end

        #deals with a bug for parsing the last command of the list
        if temp_end == -1:
            run = False
            single_letter_command = path_data[temp_start:len(path_data)]
        else:
            #this will almost always run
            single_letter_command = path_data[temp_start:temp_end+1]

        #print(single_letter_command)

        #if '' in single_letter_command:
        #    single_letter_command.remove('')

        #print(f"single letter command is {single_letter_command}")
        #take a single line of of 1 letter commands and parse it, add it to the main list
        parse_single_command(command_list,single_letter_command,start_letter,stopcode_dict)

        
        #print(f"command list: {command_list}")

        #print(single_letter_command)

        path_data = path_data[temp_end+1:len(path_data)]
        #print(f"new path is {path_data}")

    #return command_list

def parse_single_command(list_of_lists,command,letter,letter_dict):
    """
    Parses a single string command into a list of SVG commands with easily readable
    arguments. Also deals with the command chaining problem.

    Args:
    command:
        a string representing all information that occurs within the scope of a letter in a path line
    list_of_lists:
        a list of lists of strings and arguments containing the letter command to parse and that commands
        float or integer arguments
    letter:
        a string containing a single character with the command being parsed
    letter_dict:
        a dictionary with strings as keys and integers as values representing the
        number of arguments per command.
        
    """
    #could have multiple individual curves in it
    num_arguments = letter_dict[letter]

    if letter == 'Z' or letter =='z':
        #if the letter is z then there are no arguments
        list_of_lists.append(["Z"])

        #print("got here")
        #print(list_of_lists)
        return

    #print(letter)
    command = command.split(" ")

    if '' in command:
        command.remove('')
    #print(type(command))
    #print(command)

    #command is a list
    if letter in command:
        command.remove(letter)
    elif letter in command[0]:
        #if the letter has no space after its number in the command
        command[0] = command[0][1:len(command[0])]

    #print(command)


    #print(command)

    #print(len(command))
    #the number of command we're adding
    for i in range(len(command)//num_arguments):
        
        #print(i)
        #in the format
        # letter arg 1 arg2 etc..
        
        temp_list = [letter]
        for j in range(num_arguments):
            temp_list.append(command[i*num_arguments + j])
            
        list_of_lists.append(temp_list)
    
    #print(list_of_lists)




def find_first_occurence_of_multiple(string,list_strings):

    """
    Searches a string for multiple possible strings and outputs the one that
    occurrs first.

    Args:
    string:
        the string being in
    list_strings:
        a list of strings representing the possible letter commands in the SVG path
    
    Returns:
        a list containing best_index and best_letter
    best_index:
        the first index at which one of the searched strings occurs
    best_letter
        the first string of those searched that occurs

    """

    #print(string)
    best_index = -1
    best_letter = False
    for letter in list_strings:

        if string == 0:
            break
    
        if letter in string:

            temp_index = string.find(letter)

            if best_index ==-1 or temp_index < best_index:

                best_letter = letter
                best_index = temp_index
    
    return [best_index,best_letter]


#unused redundant partial function

def find_scale(viewBox,bed_dimensions,max_scale=-1,stretch_scale =False):

    """
    Find the maximum amount by which you can scale an SVG in x and y directions

    Args:
    viewBox:
        a list with 2 integers: x and y image size maximum in terms of steps
    bed_dimensions:
        a list with 2 integers: x and y bed size maximum in terms of steps
    max_scale:
        an integer representing the maximum amount you can scale an image,
        -1 if uncapped
    stretch_scale:
        a boolean representing whether x and y can be scaled independently

    Returns:
        a list containing xscale and yscale
    xscale: 
        an integer representing the amount by which to scale x
    yscale: 
        an integer representing the amount by which to scale y

    """
    #assume viewBox[0,1] are 0
    xscale = bed_dimensions[0]/viewBox[2]
    yscale = bed_dimensions[1]/viewBox[3]
    
    #stop the image from getting stretched out
    if not stretch_scale:

        if xscale <= yscale:
            yscale = xscale
        else:
            xscale = yscale
    
    #prevent the image from getting scaled too much
    if max_scale != -1:

        if xscale > max_scale:
            xscale = max_scale
        if yscale > max_scale:
            yscale = max_scale
    
    #return scaling factors 

    return [xscale,yscale]

