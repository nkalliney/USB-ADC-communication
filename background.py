import time
import serial

import adafruit_board_toolkit.circuitpython_serial

def setup_serials():
    #get the data comports names- this works for windows or mac!
    #I understand there may be issues with Linux with serial communication (check your permissions)
    comports = adafruit_board_toolkit.circuitpython_serial.data_comports()
    if not comports:
        raise Exception("No CircuitPython boards found")

    serials = {}

    #setup serial lines: create a serial line, ask it which one it is, and assign that number to it as a dictionary key
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
        #    raise Exception("We have timed out waiting for a response!")  #debug greg
        if ser.in_waiting > 0: # if there's a new char...
            a = ser.read()
            if a == b'\r': #end the message if it is this
                return reply
            else: # or keep adding to the current message
                reply += a
