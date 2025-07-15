from machine import I2C, Pin, PWM
import machine
import time
import random as rand
from Defs import *
import utime
from Speaker import *
from Sensor import *
from Rung import *


button = machine.Pin(BP,Pin.IN)
scale = 0
rand.seed()


rung = Rung(R_1,SP_0,0)
rung2 = Rung(R_2,SP_1,1)
rung3 = Rung(R_3,SP_2,2)
rung4 = Rung(R_4,SP_3,3)
rung5 = Rung(R_5,SP_4,4,SP_5,SP_6)
rungs = [rung,rung2,rung3,rung4,rung5]
rung3.song(5)

try:
    while True:
            utime.sleep_ms(5)
            
            for i in range(5):
                 rungs[i].play()
            
            while button.value() == 1:
                scale += 1

                for i in range(5):
                     rungs[i].off()
                     rungs[i].scale(scale)
                
                rung3.song((scale-1)%5)#rand.randint(0,4))
                utime.sleep_ms(150)
                
                
except KeyboardInterrupt:
    print("beep")
    for i in range(5):
         rungs[i].off()
