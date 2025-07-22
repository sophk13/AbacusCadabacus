~~from machine import I2C, Pin, PWM
import machine
import time
from Defs import *
import utime
from Speaker import *
from Sensor import *

class Rung:
    #takes device adress speaker 1 adress, which rung it is, and any aditional speaker adresses up to 2
    def __init__(self, m_Add, s_Add0, rung, s_Add1 = -1,s_Add2 = -1):
        #speaker 2 and 3 adresses saved for logic reasons
        self.s_Add1 = s_Add1
        self.s_Add2 = s_Add2
        
        #sets scale based on rung to Cmaj
        self.scale_list = rung_scales[rung]
        self.scale_cur = self.scale_list[0]
        
        #sets up speaker and sensor
        self.sensor = Sensor(SDA,SCL,m_Add,0)
        self.speaker0 = Speaker(s_Add0)
        
        #sets up aditional speakers if present
        if s_Add1 == -1:
            return
        self.speaker1 = Speaker(s_Add1)
        if s_Add2 == -1:
            return
        self.speaker2 = Speaker(s_Add2)
        
    #set your current scale   
    def scale(self,scale):
        self.scale_cur = self.scale_list[scale%3]
    
    #Plays a note apropriote to the sensor reading
    def play(self):
        number = self.sensor.read()
        #print(number)
        if bin(number).count("1") == 10:
            self.off()
        elif number >= 512:
            self.tone(8)
        elif number >= 256:
            self.tone(7)
        elif number >= 128:
            self.tone(6)
        elif number >= 64:
            self.tone(5)
        elif number >= 32:
            self.tone(4)
        elif number >= 16:
            self.tone(3)
        elif number >= 8:
            self.tone(2)
        elif number >= 4:
            self.tone(1)
        elif number >= 2:
            self.tone(0)
        else:
            self.tone(9)
            #print("test")
        
                
    #plays a song from ones defined in Defs            
    def song(self,num):
        i = 0
        song = songs[num]
        wait = times[num]
        for j in song:
            self.speaker0.set(j)
            utime.sleep_ms(wait[i])
            self.speaker0.off()
            utime.sleep_ms(25)
            i += 1
            
    #plays a song on associated speaker depending on the key you are in    
    def tone(self,num):
        try:
            if num == -1:
                self.speaker0.set(0)
                #print("yay")
                if self.s_Add1 == -1:
                    return
                self.speaker1.set(0)
                if self.s_Add2 == -1:
                    return
                self.speaker2.set(0)
            else:
                if self.s_Add1 == -1 and self.s_Add2 == -1:
                    #print(self.scale_cur[num])
                    self.speaker0.set(self.scale_cur[num])
                else:
                    self.speaker0.set(self.scale_cur[num][0]) 
                    if self.s_Add1 == -1:
                        return
                    self.speaker1.set(self.scale_cur[num][1])
                    if self.s_Add2 == -1:
                        return
                    self.speaker2.set(self.scale_cur[num][2])
        except:
            #print("oops!")
            return
    
    #turn off the speakers
    def off(self):
        self.tone(-1)
        
    
if __name__ == "__main__":
    try:
        onpin1 = machine.Pin(2,Pin.OUT)
        onpin2 = machine.Pin(3,Pin.OUT)
        onpin3 = machine.Pin(4,Pin.OUT)
        onpin2.off()
        onpin1.off()
        onpin3.on()
        
        rung = Rung(0x18,SP_2,Rung3)
        onpin3.off()
#         onpin1.off()
#         rung2 = Rung(0x18,21,Rung2)
#         onpin2.off()
        #rung.scale(3)
        #rung.song(0)
        #utime.sleep_ms(1000)
        #rung.song(1)
        #utime.sleep_ms(1000)
        #rung.song(3)
        #utime.sleep_ms(1000)
        while True:
            utime.sleep_ms(50)
            onpin3.on()
            rung.play()
            onpin3.off()
#             onpin2.on()
#             rung2.play()
#             onpin2.off()
    except KeyboardInterrupt:
        print("beep")
        onpin3.on()
        rung.off()
        onpin3.off()
#         onpin2.on()
#         rung2.off()
#         onpin2.off()
                
        