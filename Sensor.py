
from machine import I2C, Pin, PWM
import machine
import time
from Defs import *
import utime
from Speaker import *



class Sensor:
    #ADD is the adress of the I/O and channel is the I2C channel we are comunicating with
    def __init__(self, sda_pin, scl_pin,ADD,channel):
        self.DEV_ADDR = ADD

        # create two I2C pins one for each 
        self.I2C = machine.I2C(channel,scl = Pin(scl_pin),sda = Pin(sda_pin))

        # D1-D7 are inputs, D0 is output
        self.I2C.writeto(self.DEV_ADDR,bytearray([CONF_PORT0,0b11111111]))
        self.I2C.writeto(self.DEV_ADDR,bytearray([CONF_PORT1,0b01111111]))     

        # set polarity of inputs; D1-D7 flip polarity, D0 retain original polarity
        self.I2C.writeto(self.DEV_ADDR,bytearray([POLARITY_PORT0,0b11111111]))
        self.I2C.writeto(self.DEV_ADDR,bytearray([POLARITY_PORT1,0b00000011]))

        # Set D0 off (LEDs off)
        self.I2C.writeto(self.DEV_ADDR,bytearray([OUTPUT_PORT1,0b00000000]))
        
    def read(self):

        # Turn on the LEDs in the line sensor
        self.I2C.writeto(self.DEV_ADDR,bytearray([OUTPUT_PORT1,0b10000000]))
        # allow time for sensors to turn on
        time.sleep_ms(20)
        
        # Read one byte of data from the I/O expander, this data is D0 = LED control pin; D1-D7 = reflectance sensor signals
        self.I2C.writeto(self.DEV_ADDR,bytearray([INPUT_PORT0]))
        byte0 = self.I2C.readfrom(self.DEV_ADDR,1)[0]
        self.I2C.writeto(self.DEV_ADDR,bytearray([INPUT_PORT1]))
        byte1 = self.I2C.readfrom(self.DEV_ADDR,1)[0]

        # turn off the LEDs in the line sensor
        self.I2C.writeto(self.DEV_ADDR,bytearray([OUTPUT_PORT1,0b00000000]))
        time.sleep_ms(20)

        #needs to be updated to combine both bites into one
        byte1 = ((byte1<<6)>>6) | (byte1<<7)
        

        return byte0>>1     

if __name__ == "__main__":
        pin1 = machine.Pin(28,Pin.OUT)
        pin2 = machine.Pin(27,Pin.OUT)
        pin3 = machine.Pin(26,Pin.IN)
        pin2.off()
        pin1.on()
        utime.sleep_ms(1000)
        print(pin3.value())
        utime.sleep_ms(1000)
        pin2.on()
        utime.sleep_ms(1000)
        print(pin3.value())