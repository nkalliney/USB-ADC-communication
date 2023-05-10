# Write your code here :-)
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

# There does not seem to be an inherent ID for each processor. Therefore, assign a unique ID to each processor
# you are working with. I suggest numbering from 0 - n.
#########
setup.my_id = 0
#########

#  while not i2c.try_lock(): pass    #For future use only ... ignore for now ....

#====================================================
def reply(response):
    response = str(response) + "\r"
    serial.write(bytearray(response.encode()))

# This returns data in the format channel + ' ' + data + \n
def process_command(command):
    com2 = command.decode("utf-8")
    if com2 == "which\r": # Which channel am I talking to?
        reply(setup.my_id) # ME!
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

def read_all():
    data_string = ""
    for chan_name in setup.ordered_ids: # get the value of every channel
        val = read(setup.chan_dict[chan_name])
        data_string += (str(setup.my_id) + chan_name + " " + str(val) + "\n")
    return data_string

def read_dec(command): #this will receive a command in the format read##\r
    chan_name = command[-3:-1] #this is the string name of the channel we want to read
    if chan_name not in setup.chan_dict.keys():
        return "Error: This channel ID is not available."
    val = read(setup.chan_dict[chan_name])
    return str(setup.my_id) + chan_name + ' ' + str(val) + '\n' #val is differential output in V, to find field in Gauss, for this detector, 0.5 G / 1 V

def read(chan): # get the value of this channel
    return chan.voltage

while True:
    # Check for incoming data periodically ....
    if serial.in_waiting > 0:
            # At least one byte in serial input buffer
            byte = serial.read(1)
            if byte == b'\r':
                # A carriage return (<CR>) character has been received ...
                out_data = in_data #copy In_Data to Out_Data
                out_data += b'\r'       #append a <CR> to Out_Data
                process_command(out_data)
                in_data = bytearray()   #Clear In_Data for next command
                out_index = 0
            else:
                # Received character is NOT a <CR> so append this character to a growing in_data bytearray.
                in_data += byte
                #if len(in_data) == 100:
                #    raise Exception("Command lengths can not exceed 100!")
