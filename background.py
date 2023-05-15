import time
import serial

import adafruit_board_toolkit.circuitpython_serial

def setup_serials():
    """
    This gets the data comports names- this works for windows or mac!
    There may be issues with Linux with serial communication. According to https://alknemeyer.github.io/embedded-comms-with-python/,
    it's probably an issue with your permissions. The author suggests, and I quote...
    
   "From the same terminal instance where you intend on running your Python program, run the following command beforehand,
    replacing /dev/ttyACM0 with the port where your device is:
    'sudo chmod 666 /dev/ttyACM0'"
    """
    comports = adafruit_board_toolkit.circuitpython_serial.data_comports()
    if not comports:
        raise Exception("No CircuitPython boards found")

    serials = {}

    #setup serial lines: create a serial line, ask it what its ID is, and assign that ID to it as a dictionary key for easy reference
    for comport in comports:
        current_serial = serial.Serial(comport.device, 115200)
        current_serial.write(bytearray("which\r".encode()))
        i = int(response(current_serial))
        print(str(i) + ": " + comport.device) # print out the number and data port for user checks
        serials[i] = current_serial


    return serials

def response(ser): # wait for a response on designated serial line
    reply = b''
    start = time.time()
    while True:
        #add this in if you want but be careful about your timing! It can create issues
        #if (time.time()-start) > 0.02:   
        #    raise Exception("We have timed out waiting for a response!")
        if ser.in_waiting > 0: # if there's a new char...
            a = ser.read()
            if a == b'\r': #end the message if it \r
                return reply
            else: # or keep adding to the current message
                reply += a
