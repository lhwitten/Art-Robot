"""
printbed 5x5 inches


bed_range_y = 5 #inches
bed_range_x = 5 #inches
drawing_scale = 100 #incriments per inch
point_range_y = bed_range_y*drawing_scale
point_range_x = bed_range_x*drawing_scale
"""

import csv

#code for writing svgs


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

#code for reading svgs. only works for path commands currently

def parse_svg(filename):

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
        
        #clean up the created junk
        file_commands.remove('')
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

            if start_word == "path":
                #print("parsing")

                #print(f"command is {command}")
                parse_pathline(command,command_list)
    return command_list






def parse_pathline(line,command_list):

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
        i+=1
        if i > 250:
            break
        #we care about the start letter because it defines what kind of command we're doing
        temp_start,start_letter = find_first_occurence_of_multiple(path_data,stop_codes)

        #print(f"start letter is {start_letter}")

        #print(f"next search path is {path_data[temp_start+1:-1]}")

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
            single_letter_command = path_data[temp_start:temp_end]


        #print(f"single letter command is {single_letter_command}")
        #take a single line of of 1 letter commands and parse it, add it to the main list
        parse_single_command(command_list,single_letter_command,start_letter,stopcode_dict)

        #print(f" testing command interpretation should have 2 c commands{command_list}")

        #print(single_letter_command)

        path_data = path_data[temp_end+1:len(path_data)]
        #print(f"new path is {path_data}")

    #return command_list

def parse_single_command(list_of_lists,command,letter,letter_dict):

    #could have multiple individual curves in it
    num_arguments = letter_dict[letter]

    command = command.split(" ")

    #print(command)
    command.remove(letter)

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
    returns the first index a string in the list of strings occurs as 
    well as the relevant string
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