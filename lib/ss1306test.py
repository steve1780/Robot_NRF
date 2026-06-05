import machine
import ssd1306

import network
import utime

spi = machine.SPI(1, baudrate=8000000, polarity=0, phase=0)
oled = ssd1306.SSD1306_SPI(128, 64, spi, machine.Pin(15), machine.Pin(0), machine.Pin(16))

s = network.WLAN(network.STA_IF)
print('connecting to network...')

s.connect('caseservices2', 'booboo42')
s.active(True)
utime.sleep(1.0)
print('Boot WLAN Config:', s.ifconfig())


oled.fill(0)
oled.show()
utime.sleep(0.5)
oled.invert(0)
oled.text('WLAN:', 0, 0)
ifConfig = ''.join(s.ifconfig()[0])
oled.text(ifConfig, 0, 10)
#ifConfig = ''.join(s.ifconfig()[1])
#oled.text(ifConfig, 0, 20)
#ifConfig = ''.join(s.ifconfig()[2])
#oled.text(ifConfig, 0, 30)
#ifConfig = ''.join(s.ifconfig()[3])
#oled.text(ifConfig, 0, 40)

oled.show()
