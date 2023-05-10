"""
This module can be used in any higher-level code that requires communicating with a microprocessor to ADC to ADS1115.
-> import r_processor_interface_mod as pim

ex. pim.read_detector("101")
ex. pim.read_mp("1")
ex. pim.read_all()

The data that send(command) returns can be reformatted in many ways, such as a dictionary, and the structure will be preserved in your code
since the data is not being sent over a serial line.

Though all the IDs are numbers, they are data type string for easy slicing. Always input IDs as strings.

Each detector has an ID, formatted as such:
The first digit is the microprocessor ID, hard-coded into each code.py
The second digit is the ADC ID on EACH microprocessor. ADC 0, therefore, exists on every processor
The third digit is the detector ID on EACH ADC. Therefore, detector 0 is repeated on every ADC

The data returned by a read command other than fastread is as such:
ID + [space] + data (actual magnetic field reading) + <\n><\CR>
plus more lines of the same if it's several detectors

Fast read is formatted:
f + [space] + ID + <\n>
data + [space] + timestamp_since_start_of_reading

Possible commands: ["real##", "readall", "which", "readmpall"]

The commands sent to processors should be of the format:
ID + [space] + command + [space] + filename (if desired, leave off .txt)
if the command is readall, the ID should be 'x' to indicate it is not going to a single microprocessor

"""


import time
import serial

import adafruit_board_toolkit.circuitpython_serial
import background as bg
import time

serials = bg.setup_serials() #establish serial lines. This dictionary is in the format num : serialobject


def write_then_response(com, ser):
    # this method sends a command and receives a response
    com = com + "\r" # add a \r to signify the end of the command
    ser.write(bytearray(com.encode())) # write the command
    response = bg.response(ser).decode("utf-8") # wait for the response
    return response # then return it

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
    # commands that don't go directly to a processor
    com = com_parts[1] # get the command
    if com == "info": # respond to info
        print(instructions)
        print(command_list)
        return "No response required from processor." # break out before we write to a file since we don't need to
    elif com == "readall": # if we want to read all of them
        to_return = read_all2(com_parts)
    file_name = com_parts[2]
    return to_return

def send(command): # This filters commands based on whether or not they need a response, or if
    # the command is readall, which requires a little more work on our end
    # and sends the response along to be printed
    com_parts = command.split(" ")
    if len(com_parts) != 3: # if they did not provide a file name, add the default one
        com_parts.append("data")
    if com_parts[0] != 'x': # if it is being sent to a processor...
        to_return  = send_to_processor(com_parts) # sends a command like ["1", "read11"]
    else:
        to_return = other_commands(com_parts)
    return to_return


def read_all2(com_parts):
    data_string = ''
    for serial in serials:
        data = write_then_response("readmpall", serials[serial])
        data_string += data
    return data_string

# Here are what you actually want to use, I'm guessing:

def read_detector(d_id):
    processor_id = d_id[0:1]
    id2 = d_id[1:]
    command = processor_id + " " + "read" + id2
    return send(command)

def read_mp(mp_id):
    command = mp_id + " readmpall"
    return send(command)

def read_all():
    command = "x readall"
    return send(command)
