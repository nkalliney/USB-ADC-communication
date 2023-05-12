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
    # this method sends a command
    com = com + "\r" # add a \r to signify the end of the command
    ser.write(bytearray(com.encode())) # write the command

def response2(ser):
    # this reads a responds
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
    return response # return the response

def other_commands(com_parts):
    # commands that don't go directly to a signle processor
    com = com_parts[1] # get the command
    if com == "info": # respond to info
        print(instructions)
        print(command_list)
        return "No response required from processor."
    elif com == "readall": # if we want to read all of the channels
        to_return = readall(com_parts)
    return to_return

def command_manager(): # This filters commands based on whether or not they need a response from a microprocessor, or if
    # the command is readall, which requires a little more work on our end
    # and sends the response along to be printed
    user_input = input("Enter a command.\n")
    com_parts = user_input.split(" ")
    if com_parts[0] != 'x': # if the microprocessor ID is not x, it goes to a specific microporcessor
        to_return  = send_to_processor(com_parts)
    else:
        to_return = other_commands(com_parts)
    if len(com_parts) == 3: # if they provided a file name, write to file
        write_data_into_file(com_parts[2], to_return)
    return to_return


def readall(com_parts):
    # writing the command and listening for a response is split up here 
    # is to save time since the microprocessors take some time to get the readings and 
    # we want them all doing that at once instead of waiting for each one in turn
    data_string = ''
    for serial in serials:
        write2("readmpall", serials[serial])
    for serial in serials:
        data = response2(serials[serial])
        data_string+=data
    return data_string

print(instructions)
print(command_list)
while True:
    print(command_manager())

