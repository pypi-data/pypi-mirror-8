#!/usr/bin/env python
# -*- coding: utf-8 -*-

#coding: utf-8
#
#__all__=['devsuit', 'android', 'image', 'base', 'patch', 'ios', 'device']

__version__ = '0.2.1.5'

ANDROID = 'android'
IOS = 'ios'
WINDOWS='windows'

EV_DOWN = 'down'
EV_UP = 'up'
EV_DOWN_AND_UP = 'down_and_up'

import os
import json
import subprocess
import signal, sys

# just import
import monitor

def _sig_handler(signum, frame):
    print >>sys.stderr, 'Signal INT catched !!!'
    sys.exit(1)
signal.signal(signal.SIGINT, _sig_handler)

from airtest import devsuit


defaultConfigFile = 'air.json'
defaultDevice = 'android'

def _safe_load_config(cfg_file):
    if os.path.exists(cfg_file):
        return json.load(open(cfg_file))
    return {}

#
# ==========================================================
#


def _android_start(serialno, params):
    package = params.get('package')
    activity = params.get('activity')
    subprocess.call(['adb', '-s', serialno, 'shell', 'am', 'start', '-n', '/'.join([package, activity])])


def _android_stop(serialno, params):
    package = params.get('package')
    subprocess.call(['adb', '-s', serialno, 'shell', 'am', 'force-stop', package])


def _windows_start(basename, params={}):
    dir_ = params.get('dir') or '.'
    os.system('cd /d %s && start %s' %(dir_, basename))


def _windows_stop(basename, params={}):
    basename = basename.lower()
    if not basename.endswith('.exe'):
        basename += '.exe'
    os.system('taskkill /t /f  /im %s' %(basename))


def _run_control(devno, device=None, action='start'):
    device = device or defaultDevice
    cfg = _safe_load_config(defaultConfigFile)
    func = '_%s_%s'%(device, action)
    if func not in globals():
        raise RuntimeError('device(%s) %s method not exists' % (device, action))
    return globals()[func](devno, cfg.get(device, {}))

def start(devno, device=None):
    _run_control(devno, device, 'start')

def stop(devno, device=None):
    _run_control(devno, device, 'stop')

#
# ----------------------------------------------------------
#


def connect(devno=None, appname=None, device=None, monitor=True, logfile='log/airtest.log'):
    """
    Connect device

    @param devno: If devno is None, then get device serialno from `adb devices`
    @param device: can be one of <android|windows|ios>
    @param monitor: wether to enable CPU monitor
    """
    if not devno:
        devs = getDevices()
        if not devs:
            sys.exit('adb: No devices found')
        if len(devs) != 1:
            sys.exit('adb: Too many devices, need to specify phone serialno')
        devno = devs[0][0]

    device = device or defaultDevice
    if device == ANDROID:
        from airtest.device import android
        subprocess.call(['adb', 'start-server'])
        if not devno:
            devno = [d for d, t in getDevices() if t == 'device'][0]
        devClass = android.Device
    elif device == IOS:
        from airtest.device import ios
        devClass = ios.Device
    elif device == WINDOWS:
        from airtest.device import windows
        devClass = windows.Device
    elif device == 'dummy': # this class is only for test
        from airtest.device import dummy
        devClass = dummy.Device 
    else:
        raise RuntimeError('device type not recognize')

    return devsuit.DeviceSuit(device, devClass, devno, 
            appname=appname, logfile=logfile, monitor=monitor)


def getDevices(device='android'):
    """
    @return devices list 
    """
    subprocess.call(['adb', 'start-server'])
    output = subprocess.check_output(['adb', 'devices'])
    result = []
    for line in str(output).splitlines()[1:]:
        ss = line.strip().split()
        if len(ss) == 2:
            (devno, state) = ss
            result.append((devno, state))
    return result
