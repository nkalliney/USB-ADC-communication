import time
import serial

import adafruit_board_toolkit.circuitpython_serial

def setup_serials():
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
        #if (time.time()-start) > 0.02:    #debug greg
        #    raise Exception("We have timed out waiting for a response!")  #debug greg
        if ser.in_waiting > 0:
            a = ser.read()
            if a == b'\r':
                return reply
            else:
                reply += a
