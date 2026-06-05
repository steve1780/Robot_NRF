from machine import Pin
import time
l=Pin(25, Pin.OUT)

for i in range(5):
    l.toggle()
    time.sleep(.2)
    l.toggle()
    time.sleep(.6)
    
import nnrf
#import k_demo
