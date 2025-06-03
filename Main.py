from machine import I2C, Pin, PWM
import machine
import time
import random as rand
from Defs import *
import utime
from Speaker import *
from Sensor import *
from Rung import *

pin1 = machine.Pin(2,Pin.OUT)
pin2 = machine.Pin(3,Pin.OUT)
pin3 = machine.Pin(4,Pin.OUT)
scalepin = machine.Pin(5,Pin.IN)
pin1.off()
pin2.off()
pin3.off()
scale = 0
rand.seed()

pin1.on()
rung = Rung(0x18,SP_0,Rung1)
pin1.off()
pin2.on()
rung2 = Rung(0x18,SP_1,Rung2)
pin2.off()
pin3.on()
rung3 = Rung(0x18,SP_2,Rung3)
rung3.song(5)
utime.sleep_ms(150)
pin3.off()

try:
    while True:
            utime.sleep_ms(5)
            pin1.on()
            rung.play()
            pin1.off()
            
            pin2.on()
            rung2.play()
            pin2.off()
            
            pin3.on()
            rung3.play()
            pin3.off()
            
            while scalepin.value() == 1:
                scale += 1
                pin1.on()
                rung.scale(scale)
                rung.off()
                pin1.off()
                
                pin2.on()
                rung2.scale(scale)
                rung2.off()
                pin2.off()
                        
                pin3.on()
                rung3.scale(scale)
                rung3.off()
                rung3.song((scale-1)%5)#rand.randint(0,4))
                utime.sleep_ms(150)
                pin3.off()
                
                
except KeyboardInterrupt:
    print("beep")
    pin1.on()
    rung.off()
    pin1.off()
    
    pin2.on()
    rung2.off()
    pin2.off()
            
    pin3.on()
    rung3.off()
    pin3.off()
