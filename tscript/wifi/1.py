import os

def create_access_point(ssid, password):
    os.system(f'nmcli dev wifi hotspot ifname wlan0 ssid {ssid} password {password}')

# Замените 'MySSID' и 'MyPassword' на имя и пароль вашей точки доступа
create_access_point('MySSID', 'MyPassword')
