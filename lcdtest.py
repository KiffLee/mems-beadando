import os
import RPi_I2C_driver
import time
import glob
import subprocess
import socket
import fcntl
import struct
mylcd = RPi_I2C_driver.lcd()

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

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

def read_temp_raw():
    catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = catdata.communicate()
    out_decode = out.decode('utf-8')
    lines = out_decode.split('\n')
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c




mylcd.lcd_display_string("Connecting WiFi",1)

while (check_wifi() == 1):
    mylcd.lcd_display_string("Please wait",2)

mylcd.lcd_clear()

mylcd.lcd_display_string("Connected to:",1)
mylcd.lcd_display_string(check_wifi(),2)

time.sleep(2)
mylcd.lcd_clear()

mylcd.lcd_display_string("IP: %s" % get_ip_address('wlan0'), 1)
mylcd.lcd_display_string("CPU: ",2)

while True:
    mylcd.lcd_display_string_pos("%.2f" % measure_cpu_temp(), 2, 4)
    mylcd.lcd_display_string_pos("%.2f" % read_temp(),2, 11)
    time.sleep(1)


