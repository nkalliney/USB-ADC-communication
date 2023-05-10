import time
import serial

import adafruit_board_toolkit.circuitpython_serial
import background as bg
import time

serials = bg.setup_serials() #establish serial lines. This dictionary is in the format num : serialobject
command_list = ["real##", "readall", "which", "readmpall", "info"]
instructions = "Enter commands in the format processor_num [space] command [space] filename (if desired, and leave off .txt)\n\
    ex. 0 read01 data\n\
List of possible commands below."


def write_then_response(com, ser):
    # this method sends a command and receives a response
    com = com + "\r" # add a \r to signify the end of the command
    ser.write(bytearray(com.encode())) # write the command
    response = bg.response(ser).decode("utf-8") # wait for the response
    return response # then return it

def write2(com, ser):
    # this method sends a command and receives a response
    com = com + "\r" # add a \r to signify the end of the command
    ser.write(bytearray(com.encode())) # write the command

def response2(ser):
    response = bg.response(ser).decode("utf-8") # wait for the response
    return response # then return it

def write_data_into_file(name, data):
    #this takes a file name and a string of data and writes it to a text file
    name = name + '.txt' #add the .txt for the user
    with open(name, 'w') as f: # write output into a text file
        f.write(data)
        f.close()

def send_to_processor(com_parts):
    #This receives the parts of the command and sends the command to the processor designated
    #This is only called if the first char is not an x, which should mean it is a number
    try:
        processor_num = int(com_parts[0]) # find the processor number, should be first element in list
    except ValueError:
        return "First char must be a number or an x!" #The first char wasn't a number or an x, that's a problem
    if processor_num not in serials:
        return "The processor you selected is not available."
    response = write_then_response(com_parts[1], serials[processor_num]) # get the response
    if "read" in com_parts[1]: # if "read" in command, we want to save the response in a file.
       write_data_into_file(com_parts[2], response)
    return response # return the response

def other_commands(com_parts):
    # commands that don't go directly to a processor
    com = com_parts[1] # get the command
    if com == "info": # respond to info
        print(instructions)
        print(command_list)
        return "No response required from processor." # break out before we write to a file since we don't need to
    elif com == "readall": # if we want to read all of them
        to_return = readall(com_parts)
    file_name = com_parts[2]
    write_data_into_file(file_name, to_return)
    return to_return

def command_manager(): # This filters commands based on whether or not they need a response, or if
    # the command is readall, which requires a little more work on our end
    # and sends the response along to be printed
    user_input = input("Enter a command.\n")
    com_parts = user_input.split(" ")
    if len(com_parts) != 3: # if they did not provide a file name, add the default one
        com_parts.append("data")
    if com_parts[0] != 'x':
        to_return  = send_to_processor(com_parts)
    else:
        to_return = other_commands(com_parts)
    return to_return


def readall(com_parts):
    data_string = ''
    for serial in serials:
        write2("readmpall", serials[serial])
    for serial in serials:
        data = response2(serials[serial])
        data_string+=data
    return data_string
    write_data_into_file(com_parts[2], data_string)
    return data_string

print(instructions)
print(command_list)
while True:
    print(command_manager())

