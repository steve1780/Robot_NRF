#===========================================
# np_rx.py  PantherBotics Radio Reciever
#
# With RP Pico2 and ESP32-S3 capabilities
#===========================================

import sys
import struct
import utime
from machine import Pin, SPI, I2C
from machine import Timer, ADC, PWM
from nrf24l01 import NRF24L01
from micropython import const
import ssd1306

#def_pico holds pin definitions
#def_esp use for alternate dev board
from def_pico import PLED, PSDA, PSCL, PCE, PCSN, PMOSI, PMISO, PSCK, PADC0, PADC1, PPWM1, PPWM2

# NRF24L01 Constants
_RX_POLL_DELAY = const(50)
_RESPONDER_SEND_DELAY = const(2)


led1 = Pin(PLED, mode=Pin.OUT, value=0)   # internal LED on RP2040

# Radio addresses are in little-endian format. They correspond to big-endian
# 0xf0f0f0f0e1, 0xf0f0f0f0d2
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

# timer callback routine ===================================================
def status_update(t0):
    global cmd
    global oled
    global t_interval
    oled.fill(0)
    oled.text("cmd/s: ",0,0)
    oled.text(str(int(cmd/t_interval)), 50, 0)
    oled.show()
    cmd = 0
    
def flash_led(times:int=None):
    for _ in range(times):
        led1.value(1)
        utime.sleep(.25) # time 
        led1.value(0)
        utime.sleep(.25)

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


# New helper: send a single byte (for reference only) ==========================
def send_byte(nrf, b: int, c: int, inter_byte_ms: int = 50):
    payload = struct.pack(',hh', b, c)
    # stop listening so we can transmit
    nrf.stop_listening()
    
    try:
        # send a single-byte payload
        #nrf.send(bytes([b]))
        nrf.send(payload)
        
    except OSError:
        # on failure just continue; caller can decide retry policy
        pass
    # return to listening so ack/response can be received
    nrf.start_listening()
    utime.sleep_ms(inter_byte_ms)


def send_cmd(cmd, dbyte):		# here for reference only
    nrf.stop_listening()
    send_byte(nrf, cmd, dbyte, inter_byte_ms=2)

    

# responder receives commands from nrf pipes ================================    
def responder():
    global cmd
    global commands      
    #if nrf.any():
    while nrf.any():
            buf = nrf.recv()
            #print("buf ", buf)
            c1, d1 = struct.unpack("ii", buf)
            cmd = cmd + 1
            #print(c1, d1)
            # command decode
            if c1 == 10 :
                commands["xStick1"] = d1
                #map_range(x, in_min, in_max, out_min, out_max)
                pw1 = map_range(d1, 0, 255, 1000, 9000)
                pw2 = map_range(d1, 0, 255, 9000, 1000)
                
                if pw1<170 or 
                
                serv1.duty_u16(pw1)
                serv2.duty_u16(pw2)
                    
                pass   
            elif c1 == 11 :
                commands["yStick1"] = d1
                pass

            utime.sleep_ms(_RX_POLL_DELAY)
            x = commands["xStick1"]
            y = commands["yStick1"]
            
            
            
            oled.fill(0)
            oled.text("cmd/s: ",0,0)
            #oled.text(str(int(cmd/t_interval)), 50, 0)
            oled.text(str(x), 10, 12)
            oled.text(str(y), 40, 12)
            oled.show()
    nrf.start_listening()

# setup code ==================================================================

cmd = 0				# reset command count
t_interval = 10		# interval time in seconds
commands = {"xStick1": 0, "yStick1": 0, "xStick2": 0, "yStick2": 0}

# For RP2350 default SPI(0)
spi = SPI(0, sck=Pin(PSCK), mosi=Pin(PMOSI), miso=Pin(PMISO))
cfg = {"spi": spi, "csn": PCSN, "ce": PCE}


# lookup the spi object and create the pins from the dict data
csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
spi = cfg["spi"]
nrf = NRF24L01(spi, csn, ce, payload_size=8)
    

print("PantherBotics Receiver")
#t0 = Timer(period=t_interval*1000, mode=Timer.PERIODIC, callback=status_update)
nrf.open_tx_pipe(pipes[1])
nrf.open_rx_pipe(1, pipes[0])
nrf.start_listening()

serv1 = PWM(Pin(PPWM1))
serv2 = PWM(Pin(PPWM2))
serv1.freq(50)
serv2.freq(50)
serv1.duty_u16(0)
serv2.duty_u16(0)
            
            
i2c = I2C(0, scl=PSCL, sda=PSDA)   # pico2 parameters
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
oled.fill(0)
oled.text("cmd/s: ",0,0)
oled.show()


flash_led(2)    
cmd = 0


# main() loop ================================================================

while True:
    responder()
    #print("Loop on respnder")
    


 
        
        
