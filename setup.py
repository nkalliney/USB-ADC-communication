# Write your code here :-)
# Write your code here :-)
import time
import board
import neopixel
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

adc_dict = {}
chan_dict = {}
ordered_ids = []
adc_to_address = {}
my_id = 0 # processor specific
chan_to_pins = {}

def setup_dicts(i2c_freq=100000, adc_data_rate=128, adc_gain=1):
    global adc_dict
    global chan_dict
    global ordered_ids
    global adc_to_address
    global chan_to_pins

    # Specify default data rate in SPS (default is 128 samples per second)
    # Legal values: 8,16,32,64,128,250,475,860

    # Specific PGA gain:
    # Legal values:
    #   2/3 (+/-6.144v),
    #    1  (+/-4.096v),
    #    2  (+/-2.048v),
    #    4  (+/-1.024v),
    #    8  (+/-0.512v),
    #    16 (+/-0.256v)

    i2c = busio.I2C(board.SCL, board.SDA, frequency=i2c_freq)
    # Create the ADC objects using the I2C bus
    try:
        ad = 0x48
        adc_id = "0"
        ads0 = ADS.ADS1115(i2c, data_rate=adc_data_rate, gain=adc_gain, address = ad)
        adc_dict[adc_id] = ads0
        adc_to_address[adc_id] = ad
    except:
        pass

    try:
        ad = 0x49
        adc_id = "1"
        ads1 = ADS.ADS1115(i2c, data_rate=adc_data_rate, gain=adc_gain, address= ad)
        adc_dict[adc_id] = ads1
        adc_to_address[adc_id] = ad
    except:
        pass

    try:
        ad = 0x4A
        adc_id = "2"
        ads2 = ADS.ADS1115(i2c, data_rate=adc_data_rate, gain=adc_gain, address= ad)
        adc_dict[adc_id] = ads2
        adc_to_address[adc_id] = ad
    except:
        pass

    try:
        ad = 0x4B
        adc_id = "3"
        ads3 = ADS.ADS1115(i2c, data_rate=adc_data_rate, gain=adc_gain, address= ad)
        adc_dict[adc_id] = ads3
        adc_to_address[adc_id] = ad
    except:
        pass

    keys = sorted(adc_dict) # make sure we're doing everything in the order it was added in, which is ascending order
    for adc_id in keys:
        chan = AnalogIn(adc_dict[adc_id], ADS.P0, ADS.P1)
        id1 = adc_id + str(0) # create the ID manually
        chan2 = AnalogIn(adc_dict[adc_id], ADS.P2, ADS.P3)
        id2 = adc_id + str(1) # create the ID manually
        chan_dict[id1] = chan # add it to the dictionary right now
        chan_dict[id2] = chan2

        chan_to_pins[id1] = "0 1"
        chan_to_pins[id2] = "2 3"

    ordered_ids = sorted(chan_dict) # for future possible use
