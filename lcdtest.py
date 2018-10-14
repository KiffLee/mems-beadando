import os
import I2C_LCD_driver
import time
import socket
import fcntl
import struct
mylcd = I2C_LCD_driver.lcd()

def measure_cpu_temp():
    f = open("/sys/class/thermal/thermal_zone0/temp")
    t = f.read()
    f.close()
    return (int(t)/1000.0)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915, 
        struct.pack('256s', ifname[:15])
    )[20:24])

def check_wifi():
    ssid = os.popen('iwgetid').readline()
    if ssid:
        return ssid[17:-2]
    else:
        return 1

mylcd.lcd_display_string("Connecting WiFi",1)

while (check_wifi() == 1):
    mylcd.lcd_display_string("Please wait",2)

mylcd.lcd_clear()

mylcd.lcd_display_string("Connected to:",1)
mylcd.lcd_display_string(check_wifi(),2)

time.sleep(2)
mylcd.lcd_clear()

mylcd.lcd_display_string("IP: %s" % get_ip_address('wlan0'), 1)

while True:
    mylcd.lcd_display_string("CPU Temp: %.2f C" % measure_cpu_temp(), 2)
    time.sleep(1)
