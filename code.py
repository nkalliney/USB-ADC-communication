import time
import board
import neopixel
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import setup
import usb_cdc

setup.setup_dicts()

if __name__ == '__main__':
  # Get the USB data feed object
    serial = usb_cdc.data             #Create instance of 'data' USB port object
    in_data = bytearray()             #Initialize In_Data to an empty bytearray.
    out_data = b''
    out_index = 0

# Required to control LED colors of NeoPixel
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)

# Assign a unique ID to each processor
# I suggest numbering from 0 - n.
setup.my_id = 0

#====================================================
def reply(response):
    response = str(response) + "\r"
    serial.write(bytearray(response.encode()))

def process_command(command):
    com2 = command.decode("utf-8")
    if com2 == "which\r": # if asked, "which microprocessor am I talking to?"
        reply(setup.my_id) # respond with unique ID
    elif com2 == "info\r":
        reply(info())
    elif com2 == "readmpall\r": # if the command is read all of the channels
        reply(read_all())
    elif "read" in com2: # if not, read the single channel asked for
        reply(read_dec(com2))
    else:
        serial.write(command) # just echo (this still has the \r on it)

def info():
    info_string = "ID: " + str(setup.my_id) + "\n" + "Number of connected ADCs: " + str(len(setup.adc_dict)) + "\n" + "Number of channels: " + str(len(setup.chan_dict)) + "\n"
    return info_string

# This returns data in the format: channel + ' ' + data + \n
def read_all():
    data_string = ""
    for chan_name in setup.ordered_ids: # get the value of every channel
        val = read(setup.chan_dict[chan_name])
        data_string += (str(setup.my_id) + chan_name + " " + str(val) + "\n")
    return data_string

# This returns data in the format: channel + ' ' + data + \n
def read_dec(command): #this will receive a command in the format read##\r
    chan_name = command[-3:-1] #this is the string name of the channel we want to read (##)
    if chan_name not in setup.chan_dict.keys():
        return "Error: This channel ID is not available."
    val = read(setup.chan_dict[chan_name])
    return str(setup.my_id) + chan_name + ' ' + str(val) + '\n' #val is differential output in V

def read(chan): # get the differential voltage on this channel
    return chan.voltage

while True:
    # Check for incoming data ...
    if serial.in_waiting > 0:
            # At least one byte in serial input buffer
            byte = serial.read(1)
            if byte == b'\r':
                # A carriage return character (end of message) has been received ...
                full_message = in_data #copy In_Data to full_message
                full_message += b'\r'       #append a carriage return to full_message
                process_command(full_message)
                in_data = bytearray()   #Clear In_Data for next command
            else:
                # Received character is NOT a carriage return so append this character to a growing in_data bytearray.
                in_data += byte
