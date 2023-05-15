# most of this I didn't write tbh- see the youtube video in the credits

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure


import tkinter as tk    #tkinter permits manipulation of GUI widgets
import numpy as np
import adafruit_board_toolkit.circuitpython_serial
import background as bg
import time
import numpy as np
import random


serials = bg.setup_serials() #establish serial lines. This dictionary is in the format "ID" : serialobject
all_readings = {} # keeps track of all of the data points we've collected
time_list = [] # keeps track of all the times we've collected data
start_time = time.time()
cond = False # whether we are plotting or not
lines = [] # These will hold all the line objects that go on the plot

def write_then_response(com, ser):
    # this method sends a command and receives a response
    com = com + "\r" # add a \r to signify the end of the command
    ser.write(bytearray(com.encode())) # write the command
    response = bg.response(ser).decode("utf-8") # wait for the response
    return response # then return it

def readall():
    data_string = '' # collects the response from all the processors
    for serial in serials: #for each serial line,
        data = write_then_response("readmpall", serials[serial]) # ask for a reading on every detector
        data_string += data # add it to our running total
    return data_string

def add_to_list(li, val):
    if li != None: # if the list exists
        if len(li) >= 100: #and it is too long
            li[0:99] = li[1:100] #wrap the data around
            li[99] = val #and add the new value
        else:
            li.append(val) # if it's still short, just add the new value
    else:
        li = [val] # if the list doesn't exist, create a new one with our first value
    return li

def process_data(result, now):
    global all_readings, time_list
    sep = result.split("\n") # this splits it into a line from each detector
    sep.pop() # because of the final new line, the last member of sep is empty, so just delete it
    i = 0
    for det in sep: # for each detector line
        sp = det.split(" ") # split it into an ID and a value ['id', 'value']
        sp[1] = float(sp[1]) + 0.1*i #add an offset
        all_readings[sp[0]] = add_to_list(all_readings.get(sp[0]), sp[1])
        # the above line finds the list that in the all_readings dictionary corresponds to the ID
        # whether it is None or not. It then sets the list to itself with the new value added.
        i = i+1
    time_list = add_to_list(time_list, now-start_time) # add the current time to the list as well

def setup_lines(num): # set up each individual line (corresponding to a detector) on the plot
    global ax, lines
    for i in range(num):
        r = lambda: random.randint(0,255)
        color_str = '#%02X%02X%02X' % (r(),r(),r()) # make a random color for each line
        line = ax.plot([],[], '-o', color = color_str)[0] # create a currently empty line
        lines.append(line) # add it to the list of lines

#---- plot data -----
def plot_data():
    global cond, all_readings, time_list, canvas, start_time, lines, ax

    if (cond == True):

        result = readall()
        now = time.time()
        process_data(result, now)

        #Updata x & y values to be plotted....
        i = 0
        for key in all_readings:
            lines[i].set_xdata(time_list)
            lines[i].set_ydata(all_readings[key])
            i = i + 1

        #Update canvas ...
        ax.set_xlim(time_list[0], time_list[-1])
        canvas.draw()

    #after 1mS, call plot_data() function again
    root.after(1, plot_data)

def plot_start():
    global cond
    cond = True

def plot_stop():
    global cond
    cond = False

#---- Main GUI Code ----
root = tk.Tk()
root.title('Real Time Plot')  #label given popup window
root.configure(background = 'light blue')
root.geometry("1200x1000")  #set the window size

#------create Plot object on GUI----------
# add figure canvas
# The Figure class represents the drawing area on which
# matplotlib charts will be drawn.
fig = Figure();

#See: https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.add_subplot
#Also: https://stackoverflow.com/questions/3584805/what-does-the-argument-mean-in-fig-add-subplot111
#Note: subplot grid parameters may be encoded as a single integer.
#      For example, "111" means "1x1 grid, first subplot" and
#      "234" means "2x3 grid, 4th subplot".
ax = fig.add_subplot(111)

ax.set_title('Serial Data');
ax.set_xlabel('Time')
ax.set_ylabel('Values')
ax.set_xlim(0,10)
ax.set_ylim(-2,2)
ax.grid()
setup_lines(16) # Here is where we input how many detectors we're expecting

# create FigureCanvasTkAgg object
# The FigureCanvasTkAgg class is an interface between the Figure
# and Tkinter Canvas.
# Note that the FigureCanvasTkAgg object is not a Canvas object
# but contains a Canvas object.
canvas = FigureCanvasTkAgg(fig, master=root)   # A tk.DrawingArea.

#specific upper right corner (x,y) and size (width,height) of TkAgg canvas
canvas.get_tk_widget().place(x=10,y=20,width=1000,height=800)

#Enable the built-in toolbar for the figure on the graph.
toolbar = NavigationToolbar2Tk(canvas)

canvas.draw()


root.update();
start = tk.Button(root, text="Start", command = lambda: plot_start())
start.place(x=25,y=825)

root.update();
stop = tk.Button(root, text="Stop", command = lambda: plot_stop())
stop.place(x=100,y=825)

root.after(1, plot_data)   #after 1mS, execute function
root.mainloop()
