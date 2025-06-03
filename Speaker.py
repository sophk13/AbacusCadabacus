
from machine import Pin, PWM
import machine
import utime
from Defs import *

class Speaker:
    def __init__(self, pwm_pin):
        self.PWM = PWM(pwm_pin, freq=10000, duty_u16=0)
        self.current_tone = 0;

    def set(self, freq):
        # set duty
        if freq == 0:
            self.off()
        elif freq == self.current_tone:
            return
        else:
            self.PWM.duty_u16(int(65535*0.5))
            self.PWM.freq(int(freq))
            self.current_tone = freq
        
    def off(self):
        self.PWM.duty_u16(0)
        self.current_tone = 0

        
# Write some code to test your motor here
if __name__ == "__main__":
    speaker1 = Speaker(SP_0)
    speaker2 = Speaker(SP_1)
    speaker1.off()
    speaker2.off()
    

