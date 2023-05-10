# USB-ADC-communication
This code creates communication between a computer and a microprocessor over USB using Python, and then between the microprocessor and analog-digital convertor over I2C, using CircuitPython. This particular system uses ADS1115s from Adafruit, but it'd be pretty easy to swap them out.
This is my first time uploading to Github so... lmk what I can improve but don't be mean please!
Here's some more detail on the code.

COMPUTER'S END:
I will start with the user interface code here, as it's the base of everything else. Wait til the very end for the module and graphing code information!
Using commands, you can request things from the microprocessors.
Each microprocessor has an ID (more detail later) so to ask something from one specific microprocessor, you can do this: 
ID + [space] + command + [space] + file name for saved response (optional)
Each command is terminated with a "\r" but you don't need to worry about this, it is added on automatically by the code. This char is what the microprocessor looks for to signify the end of a command.
This code is designed to work for differential channels on the ADCs.
Each differential channel has a two-digit ID. Here's how that's assigned: on each microprocessor, each ADC is numbered, and then on each ADC each channel is numbered. So there might be two channels called "01" but on different microprocessors.
Here are the commands and how to use them:
read##: this reads a specific channel on one microprocessor. For example, 1 read01 reads the channel 01 on microprocessor 1; you can think of that channel as "101" but the digits are split up here so the code can process it more easily. The code on the computer does not need to know what channel on the ADC needs to be read, just the microprocessor the command must be sent to.
which: you probably won't need to use this. When the code is establishing communication in background.py, it gets the computer-assigned USB port names, and then sends the "which" command along each port. The microprocessor responds with its ID ("0", "1", etc.) and that is then linked to the USB port name through the dictionary called serials. When you type in the microprocessor ID when sending a command, the code automatically retrieves the USB port name using this dictionary.
readmpall: this reads all the channels on one microprocessor
info: this responds with some info about the system.
readall: this reads all the channels on the system, by sending "readmpall" to every microprocessor on the system. Since this isn't sent to a specific microprocessor, don't type in a microprocessor ID when sending a command. Instead, use an "x" (ex. "x readall").
If you type in a command such as 0 read01, you will get a response like this:
001 + [space] + 0.9430920 + [newline]
001 is the full ID (microprocessor ID + channel ID) and 0.9430920 is the differential channel reading in Volts.
readmpall and readall use the same structure, but with more lines. Say microprocessor 0 has the channels 00, 01, 10, and 11. If you say "0 readmpall", you will get the response:
000 value0
001 value1
010 value2
011 value3

This brings us to what code goes on on the microprocessor's end.
boot.py: All of this communication between the microprocessor and computer takes place over the data port on the microprocessor. It has a serial port, which is used for the REPL, and a data port for user-specific communication. What this code does is enable the data port because we want this user-specific communication.
In setup.py, all the ADC and channel objects are created (this part is the I2C communication). Retrieving the readings using the ADC and channel objects is over I2C and passing them to the computer is over USB (this uses usb_cdc). This is boring. One thing: there are a few dictionaries up top in case you need them. The adc_to_address links an ADC's address to its actual I2C address, and the chan_to_pins links a channel ID with what pins the actual wires are conected to on the ADC.
adc_dict and chan_dict link the adc and channel IDs to their objects, respectively. 
If you want to use this system with something other than these specific Adafruit ADCs, you can switch out the ADC code here.
Ok, now on to code.py.
IMPORTANT!!!! Each microprocessor that's connected to your system must have a unique my_id! Otherwise there are problems. When you download code.py on to each microprocessor, change it for each one!
This code is just filtering each command that's received and finding the correct response, and taking readings from the channels if needed.
If you want to change the commands your microprocessors respond to, you should do it in process_command(command).

The last thing I want to mention are the processor interface module code and the continuous graphing code. The module code can be imported as module into any of your code, and calling its functions will be just like using the user interface, but all automated! The continuous graphing file graphs all the readings from all the differential channel lines with respect to time, with a beautiful scrolling display and a start and stop button.

There were a lot of attributions for the code that I combined to make this project, and I don't know if I have to add them, but here are the links to my key influences!
https://learn.adafruit.com/welcome-to-circuitpython/overview
https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/overview
https://docs.circuitpython.org/projects/board-toolkit/en/latest/examples.html
https://www.youtube.com/watch?v=0V-6pu1Gyp8
https://pyserial.readthedocs.io/en/latest/pyserial.html
