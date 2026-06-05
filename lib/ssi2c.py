import machine
import ssd1306

import network
import utime

#spi = machine.SPI(1, baudrate=8000000, polarity=0, phase=0)

#i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)

i2c = machine.I2C(machine.Pin(5), machine.Pin(4), freq=100000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
#oled = ssd1306.SSD1306_I2C(128, 32, i2c)

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
