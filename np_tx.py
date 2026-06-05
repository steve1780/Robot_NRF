#===========================================
# np_tx.py  PantherBotics Radio Transmitter
#
# With RP Pico2 and ESP32-S3 capabilities
#===========================================

import sys
import struct
import utime
from machine import Pin, SPI, I2C
from machine import Timer, ADC
from nrf24l01 import NRF24L01
from micropython import const

#def_pico holds pin definitions
#def_esp use for alternate dev board
from def_pico import PLED, PSDA, PSCL, PCE, PCSN, PMOSI, PMISO, PSCK, PADC0, PADC1

# NRF24L01 Constants
_RX_POLL_DELAY = const(10)
_RESPONDER_SEND_DELAY = const(2)

cmd = 0				# reset command count
t_interval = 10		# interval time in seconds


led1 = Pin(PLED, mode=Pin.OUT, value=0)   # internal LED on RP2040
xPot = ADC(Pin(PADC0))
yPot = ADC(Pin(PADC1))


# Radio addresses are in little-endian format. They correspond to big-endian
# 0xf0f0f0f0e1, 0xf0f0f0f0d2
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")


# timer callback routine ===================================================
def status_update(t0):		# not used presently
    global cmd
    global xPot
    global yPot
    xV = xPot.read_u16()
    yV = yPot.read_u16()
    #def map_range(x, in_min, in_max, out_min, out_max):
    xP = map_range(xV, 0, 65534, 0, 255)
    send_cmd(10, xP)
    yP = map_range(yV, 0, 65534, 0, 255)
    send_cmd(11, yP)
    #print("Xmit: ", xP, yP)
    
def flash_led(times:int=None):
    for _ in range(times):
        led1.value(1)
        utime.sleep(.25) # time 
        led1.value(0)
        utime.sleep(.25)

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


# Transmit byte ==========================================================
def send_byte(nrf, b: int, c: int, inter_byte_ms: int = 50):
    payload = struct.pack('<ii', b, c)
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
    

# setup code ==================================================================

# For RP2350 default SPI(0)
spi = SPI(0, sck=Pin(PSCK), mosi=Pin(PMOSI), miso=Pin(PMISO))
cfg = {"spi": spi, "csn": PCSN, "ce": PCE}

# lookup the spi object and created the pins from the dict data
csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
spi = cfg["spi"]
nrf = NRF24L01(spi, csn, ce, payload_size=8)
    

print("PantherBotics Transmitter")
#t0 = Timer(period=200, mode=Timer.PERIODIC, callback=status_update)
nrf.open_tx_pipe(pipes[0])
nrf.open_rx_pipe(1, pipes[1])
nrf.start_listening()

flash_led(2)    
cmd = 0


# main() loop ================================================================

while True:
    led1.toggle()
    xV = xPot.read_u16()
    yV = yPot.read_u16()
    #def map_range(x, in_min, in_max, out_min, out_max):
    xP = map_range(xV, 0, 65534, 0, 255)
    send_byte(nrf, 10, xP, 2)
    yP = map_range(yV, 0, 65534, 0, 255)
    send_byte(nrf, 11, yP, 2)
    #print("Xmit: ", xP, yP)
 
 
 
 

        