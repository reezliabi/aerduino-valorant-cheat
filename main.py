import cv2
from mss import mss
import numpy as np
import win32api
import serial
import keyboard
import time
import configparser
import sys
import platform
import os
import hashlib
from datetime import datetime

print("License loading from Config.ini. If you don't have one you can ask for a free one on Discord.")
print(' ')
config = configparser.ConfigParser()
config.read('Config.ini')


print(' ')
print("You can't use Silent, Aim Assistant and Flick together, only one of them at time. We suggest to use No Recoil only alone or with Aim Assistant.")
print(' ')
print('SETTINGS LOADED FROM Config.ini. Please carefully read options and usage on that file.')
print(' ')
aammbbtt = False
rkil = False
sylnt = False
flyk = False
chst_offsst = 2
ncck_offsst = 6
hedd_offsst = 8
a1m_offsst = 0
ffoovv = int(config['Options']['FOV'])
com = config['Options']['COM']
mouse_type = config['Options']['MouseType']
purple_mode = config['Options']['ColorPurpleMode']
xspd = float(config['Options']['Xspeed'])
yspd = float(config['Options']['Yspeed'])
flyk_sylnt_speed = float(config['Options']['FlickSilentSpeed'])
reolad_settings_key = config['Options']['ReloadSettingsKey']
aammbbtt_key = config['Options']['AimAssistOnOff']
rkil_key = config['Options']['RecoilOnOff']
sylnt_key = config['Options']['SilentOnOff']
sylnt_activ_key = config['Options']['SilentInGameButton']
flyk_key = config['Options']['FlickOnOff']
flyk_activ_key = config['Options']['FlickInGameButton']
exit_key = config['Options']['ExitKey']
trgt = config['Options']['AimTarget']
ass_aim = config['Options']['AssistOnlyAiming']
flyk_plus_aim = config['Options']['FlickNormalAssistAiming']
flyk_delay = float(config['Dev']['FlickDelay'])
performance_delay = float(config['Dev']['PerformanceBoost'])
high_cpu = config['Dev']['HighCPUinUse']
set_custom_color = config['Dev']['SetCustomColor']
tmp_hsv_lower = config['Dev']['HSVCustomLower']
tmp_hsv_upper = config['Dev']['HSVCustomUpper']
indq1 = tmp_hsv_lower.find('[')
indq2 = tmp_hsv_lower.find(']')
ind1 = tmp_hsv_lower.find(',')
ind2 = tmp_hsv_lower.find(',', ind1 + 1, indq2 - 1)
ind3 = tmp_hsv_lower.find(',', ind2 + 1, indq2 - 1)
h_lower = int(tmp_hsv_lower[indq1 + 1:ind1].strip())
s_lower = int(tmp_hsv_lower[ind1 + 1:ind2].strip())
v_lower = int(tmp_hsv_lower[ind2 + 1:indq2].strip())
indq1 = tmp_hsv_upper.find('[')
indq2 = tmp_hsv_upper.find(']')
ind1 = tmp_hsv_upper.find(',')
ind2 = tmp_hsv_upper.find(',', ind1 + 1, indq2 - 1)
ind3 = tmp_hsv_upper.find(',', ind2 + 1, indq2 - 1)
h_upper = int(tmp_hsv_upper[indq1 + 1:ind1].strip())
s_upper = int(tmp_hsv_upper[ind1 + 1:ind2].strip())
v_upper = int(tmp_hsv_upper[ind2 + 1:indq2].strip())
sct = mss()
arduino_part = serial.Serial(com, 115200, timeout=0)
sscrnshtt = sct.monitors[1]
sscrnshtt['left'] = int(sscrnshtt['width'] / 2 - ffoovv / 2)
sscrnshtt['top'] = int(sscrnshtt['height'] / 2 - ffoovv / 2)
temp_w = int(sscrnshtt['width'])
temp_h = int(sscrnshtt['height'])
sscrnshtt['width'] = ffoovv
sscrnshtt['height'] = ffoovv
mid = ffoovv / 2
if purple_mode == 'STRONG' and set_custom_color == 'False':
    lower = np.array([
        127,
        76,
        123], dtype='uint8')
    upper = np.array([
        162,
        197,
        255], dtype='uint8')
if purple_mode == 'SOFT' and set_custom_color == 'False':
    lower = np.array([
        140,
        111,
        160], dtype='uint8')
    upper = np.array([
        148,
        154,
        194], dtype='uint8')
if purple_mode == 'ALTERNATIVE' and set_custom_color == 'False':
    lower = np.array([
        40,
        50,
        50], dtype='uint8')
    upper = np.array([
        80,
        255,
        255], dtype='uint8')
if purple_mode != 'STRONG' and purple_mode != 'SOFT' and purple_mode != 'ALTERNATIVE' and set_custom_color == 'False':
    lower = np.array([
        127,
        76,
        123], dtype='uint8')
    upper = np.array([
        162,
        197,
        255], dtype='uint8')
if set_custom_color == 'True':
    lower = np.array([
        h_lower,
        s_lower,
        v_lower], dtype='uint8')
    upper = np.array([
        h_upper,
        s_upper,
        v_upper], dtype='uint8')
if trgt == 'NECK':
    a1m_offsst = ncck_offsst
if trgt == 'CHEST':
    a1m_offsst = chst_offsst
if trgt == 'HEAD':
    a1m_offsst = hedd_offsst
if trgt != 'NECK' and trgt != 'CHEST' and trgt != 'HEAD':
    a1m_offsst = 6
print('Config:')
print(' ')
print('COM = ', com)
print('Mouse library used (you must reload arduino library and ch33t0 to change it) = ', mouse_type)
print('FOV = ', ffoovv)
print('Purple Mode = ', purple_mode)
print('Aim Target = ', trgt)
print('X Speed = ', xspd)
print('Y Speed = ', yspd)
print('Flick and Silent Speed = ', flyk_sylnt_speed)
print('Aim Assistant On/Off Key = ', aammbbtt_key)
print('No Recoil On/Off Key = ', rkil_key)
print('Flick On/Off Key = ', flyk_key)
print('Silent On/Off Key = ', sylnt_key)
print('Use this button to Flick in game = ', flyk_activ_key)
print('Use this button to Silent kill in game = ', sylnt_activ_key)
print('Aim Assistant Activated only while aiming = ', ass_aim)
print('Flick without aiming, aim assistant while aiming = ', flyk_plus_aim)
print('Aim Assistant = ', aammbbtt)
print('No Recoil = ', rkil)
print('Silent = ', sylnt)
print('Flick = ', flyk)
print('To Reload Settings from Config.ini press = ', reolad_settings_key)
print('Press the following key to exit = ', exit_key)
print(' ')
print('Dev Settings: ')
print(' ')
print('Performance Boost = ', performance_delay)
print('Use more cpu while tracking = ', high_cpu)
print('Set Custom Color = ', set_custom_color)
print('HSV Lower = ', tmp_hsv_lower)
print('HSV Upper = ', tmp_hsv_upper)
print('Flick delay = ', flyk_delay)
print(' ')
print('READY!')

def mvmnt(x, y):
    if mouse_type == 'ANIMALI' and mouse_type == 'DOGESIMPLE' or mouse_type == 'DOGE':
        x = int(x)
        y = int(y)
        x = x + 127
        y = y + 127
        if x > 254:
            x = 254
        if x < 0:
            x = 0
        if y > 254:
            y = 254
        if y < 0:
            y = 0
        data = bytearray([
            126,
            x,
            y,
            126])
        arduino_part.write(data)
    if mouse_type == 'HIDMOUSEREPORT':
        data = f'''{int(x)}:{int(y)}'''
        arduino_part.write(data.encode())
        return None


def smovv(x, y):
    if mouse_type == 'ANIMALI' and mouse_type == 'DOGESIMPLE' or mouse_type == 'DOGE':
        x = int(x)
        y = int(y)
        x = x + 127
        y = y + 127
        if x > 254:
            x = 254
        if x < 0:
            x = 0
        if y > 254:
            y = 254
        if y < 0:
            y = 0
        data = bytearray([
            126,
            x,
            y,
            126])
        arduino_part.write(data)
        pkts = bytearray([
            94,
            94,
            94,
            94])
        arduino_part.write(pkts)
        inverso = bytearray([
            123,
            x,
            y,
            123])
        arduino_part.write(inverso)
    if mouse_type == 'HIDMOUSEREPORT':
        data = f'''syl3nt{int(x)}:{int(y)}'''
        arduino_part.write(data.encode())
        return None


def mflyck():
    if mouse_type == 'ANIMALI' and mouse_type == 'DOGESIMPLE' or mouse_type == 'DOGE':
        pkts = bytearray([
            94,
            94,
            94,
            94])
        arduino_part.write(pkts)
    if mouse_type == 'HIDMOUSEREPORT':
        arduino_part.write('shttt'.encode())
        return None


def lclc():
    if win32api.GetAsyncKeyState(1) < 0:
        return True


def rclc():
    if win32api.GetAsyncKeyState(2) < 0:
        return True


def basik_rkoil():
    if lclc():
        time.sleep(0.1)
        if not lclc():
            return None


def assist():
    img = np.array(sct.grab(sscrnshtt))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=5)
    thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
    (contours, hierarchy) = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        M = cv2.moments(thresh)
        pta = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        cX = pta[0]
        cY = pta[1] - a1m_offsst
        x = int(cX - mid)
        y = int(cY - mid)
        x2 = x * xspd
        y2 = y * yspd
        mvmnt(x2, y2)
        return None


def fliccare():
    if flyk_activ_key == 'LCLICK':
        if lclc():
            img = np.array(sct.grab(sscrnshtt))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower, upper)
            kernel = np.ones((3, 3), np.uint8)
            dilated = cv2.dilate(mask, kernel, 5, iterations=5)
            thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
            (contours, hierarchy) = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            if len(contours) != 0:
                M = cv2.moments(thresh)
                pta = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                cX = pta[0]
                cY = pta[1] - a1m_offsst
                x = int(cX - mid)
                y = int(cY - mid)
                x2 = x * flyk_sylnt_speed
                y2 = y * flyk_sylnt_speed
                mvmnt(x2, y2)
                return None
            return None
        return None
    if None.is_pressed(flyk_activ_key):
        img = np.array(sct.grab(sscrnshtt))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(mask, kernel, iterations=5)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        (contours, hierarchy) = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            M = cv2.moments(thresh)
            pta = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
            cX = pta[0]
            cY = pta[1] - a1m_offsst
            x = int(cX - mid)
            y = int(cY - mid)
            x2 = x * flyk_sylnt_speed
            y2 = y * flyk_sylnt_speed
            mvmnt(x2, y2)
            time.sleep(flyk_delay)
            mflyck()
            return None
        return None


def silenziare():
    img = np.array(sct.grab(sscrnshtt))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=5)
    thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
    (contours, hierarchy) = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        M = cv2.moments(thresh)
        pta = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        cX = pta[0]
        cY = pta[1] - a1m_offsst
        x = int(cX - mid)
        y = int(cY - mid)
        x2 = x * flyk_sylnt_speed
        y2 = y * flyk_sylnt_speed
        smovv(x2, y2)
        return None


while True:
    if keyboard.is_pressed(reolad_settings_key):
        print(' ')
        print('Reloading Settings (Except COM and License): ')
        print(' ')
        time.sleep(0.5)
        config = configparser.ConfigParser()
        config.read('Config.ini')
        aammbbtt = False
        rkil = False
        sylnt = False
        flyk = False
        chst_offsst = 2
        ncck_offsst = 6
        hedd_offsst = 8
        a1m_offsst = 0
        ffoovv = int(config['Options']['FOV'])
        com = config['Options']['COM']
        mouse_type = config['Options']['MouseType']
        purple_mode = config['Options']['ColorPurpleMode']
        xspd = float(config['Options']['Xspeed'])
        yspd = float(config['Options']['Yspeed'])
        flyk_sylnt_speed = float(config['Options']['FlickSilentSpeed'])
        reolad_settings_key = config['Options']['ReloadSettingsKey']
        aammbbtt_key = config['Options']['AimAssistOnOff']
        rkil_key = config['Options']['RecoilOnOff']
        sylnt_key = config['Options']['SilentOnOff']
        sylnt_activ_key = config['Options']['SilentInGameButton']
        flyk_key = config['Options']['FlickOnOff']
        flyk_activ_key = config['Options']['FlickInGameButton']
        exit_key = config['Options']['ExitKey']
        trgt = config['Options']['AimTarget']
        ass_aim = config['Options']['AssistOnlyAiming']
        flyk_plus_aim = config['Options']['FlickNormalAssistAiming']
        flyk_delay = float(config['Dev']['FlickDelay'])
        performance_delay = float(config['Dev']['PerformanceBoost'])
        high_cpu = config['Dev']['HighCPUinUse']
        set_custom_color = config['Dev']['SetCustomColor']
        tmp_hsv_lower = config['Dev']['HSVCustomLower']
        tmp_hsv_upper = config['Dev']['HSVCustomUpper']
        indq1 = tmp_hsv_lower.find('[')
        indq2 = tmp_hsv_lower.find(']')
        ind1 = tmp_hsv_lower.find(',')
        ind2 = tmp_hsv_lower.find(',', ind1 + 1, indq2 - 1)
        ind3 = tmp_hsv_lower.find(',', ind2 + 1, indq2 - 1)
        h_lower = int(tmp_hsv_lower[indq1 + 1:ind1].strip())
        s_lower = int(tmp_hsv_lower[ind1 + 1:ind2].strip())
        v_lower = int(tmp_hsv_lower[ind2 + 1:indq2].strip())
        indq1 = tmp_hsv_upper.find('[')
        indq2 = tmp_hsv_upper.find(']')
        ind1 = tmp_hsv_upper.find(',')
        ind2 = tmp_hsv_upper.find(',', ind1 + 1, indq2 - 1)
        ind3 = tmp_hsv_upper.find(',', ind2 + 1, indq2 - 1)
        h_upper = int(tmp_hsv_upper[indq1 + 1:ind1].strip())
        s_upper = int(tmp_hsv_upper[ind1 + 1:ind2].strip())
        v_upper = int(tmp_hsv_upper[ind2 + 1:indq2].strip())
        if purple_mode == 'STRONG' and set_custom_color == 'False':
            lower = np.array([
                127,
                76,
                123], dtype='uint8')
            upper = np.array([
                162,
                197,
                255], dtype='uint8')
        if purple_mode == 'SOFT' and set_custom_color == 'False':
            lower = np.array([
                140,
                111,
                160], dtype='uint8')
            upper = np.array([
                148,
                154,
                194], dtype='uint8')
        if purple_mode == 'ALTERNATIVE' and set_custom_color == 'False':
            lower = np.array([
                40,
                50,
                50], dtype='uint8')
            upper = np.array([
                80,
                255,
                255], dtype='uint8')
        if purple_mode != 'STRONG' and purple_mode != 'SOFT' and purple_mode != 'ALTERNATIVE' and set_custom_color == 'False':
            lower = np.array([
                127,
                76,
                123], dtype='uint8')
            upper = np.array([
                162,
                197,
                255], dtype='uint8')
        if set_custom_color == 'True':
            lower = np.array([
                h_lower,
                s_lower,
                v_lower], dtype='uint8')
            upper = np.array([
                h_upper,
                s_upper,
                v_upper], dtype='uint8')
        if trgt == 'NECK':
            a1m_offsst = ncck_offsst
        if trgt == 'CHEST':
            a1m_offsst = chst_offsst
        if trgt == 'HEAD':
            a1m_offsst = hedd_offsst
        if trgt != 'NECK' and trgt != 'CHEST' and trgt != 'HEAD':
            a1m_offsst = 6
        sct = mss()
        sscrnshtt = sct.monitors[1]
        sscrnshtt['left'] = int(temp_w / 2 - ffoovv / 2)
        sscrnshtt['top'] = int(temp_h / 2 - ffoovv / 2)
        sscrnshtt['width'] = ffoovv
        sscrnshtt['height'] = ffoovv
        mid = ffoovv / 2
        print('Config:')
        print(' ')
        print('Mouse library used (you must reload arduino library and ch33t0 to change it) = ', mouse_type)
        print('FOV = ', ffoovv)
        print('Purple Mode = ', purple_mode)
        print('Aim Target = ', trgt)
        print('X Speed = ', xspd)
        print('Y Speed = ', yspd)
        print('Flick and Silent Speed = ', flyk_sylnt_speed)
        print('Aim Assistant On/Off Key = ', aammbbtt_key)
        print('No Recoil On/Off Key = ', rkil_key)
        print('Flick On/Off Key = ', flyk_key)
        print('Silent On/Off Key = ', sylnt_key)
        print('Use this button to Flick in game = ', flyk_activ_key)
        print('Use this button to Silent kill in game = ', sylnt_activ_key)
        print('Aim Assistant Activated only while aiming = ', ass_aim)
        print('Flick without aiming, aim assistant while aiming = ', flyk_plus_aim)
        print('Aim Assistant = ', aammbbtt)
        print('No Recoil = ', rkil)
        print('Silent = ', sylnt)
        print('Flick = ', flyk)
        print('To Reload Settings from Config.ini press = ', reolad_settings_key)
        print('Press the following key to exit = ', exit_key)
        print(' ')
        print('Dev Settings: ')
        print(' ')
        print('Performance Boost = ', performance_delay)
        print('Use more cpu while tracking = ', high_cpu)
        print('Set Custom Color = ', set_custom_color)
        print('HSV Lower = ', tmp_hsv_lower)
        print('HSV Upper = ', tmp_hsv_upper)
        print('Flick delay = ', flyk_delay)
        print(' ')
        print('READY!')
    if keyboard.is_pressed(aammbbtt_key):
        time.sleep(1)
        aammbbtt = not aammbbtt
        print('Aim Assistant = ', aammbbtt)
    if keyboard.is_pressed(rkil_key):
        time.sleep(1)
        rkil = not rkil
        print('No Recoil = ', rkil)
    if keyboard.is_pressed(sylnt_key):
        time.sleep(1)
        sylnt = not sylnt
        print('Silent = ', sylnt)
    if keyboard.is_pressed(flyk_key):
        time.sleep(1)
        flyk = not flyk
        print('Flick = ', flyk)
    if keyboard.is_pressed(exit_key):
        time.sleep(1)
        exit()
    if rkil == True and lclc():
        if high_cpu == 'True':
            if lclc():
                basik_rkoil()
                if not lclc():
                    pass
                else:
                    basik_rkoil()
    if aammbbtt == True and sylnt == False:
        if flyk == False or flyk_plus_aim == 'True':
            if ass_aim != 'True' or rclc():
                if high_cpu == 'True' and ass_aim == 'True':
                    if rclc():
                        assist()
                        if not rclc():
                            pass
                        else:
                            assist()
    if (aammbbtt == False or flyk_plus_aim == 'True') and sylnt == False and flyk == True:
        if high_cpu == 'True' and flyk_activ_key == 'LCLICK':
            if lclc():
                fliccare()
                if not lclc():
                    pass
                else:
                    fliccare()
    if aammbbtt == False and sylnt == True and flyk == False and keyboard.is_pressed(sylnt_activ_key):
        if high_cpu == 'True' and keyboard.is_pressed(sylnt_activ_key):
            if keyboard.is_pressed(sylnt_activ_key):
                silenziare()
                if not keyboard.is_pressed(sylnt_activ_key):
                    pass
                else:
                    silenziare()
    time.sleep(performance_delay)
    
