#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
basic operation for a game(like a user does)
'''

import os

from airtest import base
from appium import webdriver
from PIL import Image

import airtest

DEBUG = os.getenv("DEBUG")=="true"
log = base.getLogger('ios')

# from zope.interface.declarations import implementer
# from airtest import interface

#@implementer(interface.IDevice)
class Device(object):
    def __init__(self, serialno=None):
        self.url = 'http://127.0.0.1:4723/wd/hub'
        self.driver = webdriver.Remote(
            command_executor=self.url,
            desired_capabilities={
                'platformName': 'iOS',
                # after appium 1.2.0, deviceName is required
                'deviceName': 'ios device',
                'autoLaunch': False
            }
        )
        self._scale = None
        self.start()
        self._init()

    def _init(self):
        rw, rh = self._getShapeReal()
        w, h = self._getShapeInput()
        w, h = min(w, h), max(w, h)
        print (rw, rh), (w, h)
        self._scale = float(w)/rw
        print 'SCALE:', self._scale

    def start(self):
        self.driver.launch_app()

    def stop(self):
        self.driver.close_app()

    def clear(self):
        self.stop()

    def snapshot(self, filename):
        ''' save screen snapshot '''
        log.debug('start take snapshot')
        self.driver.save_screenshot(filename)
        log.debug('finish take snapshot and save to '+filename)
        return filename

    def _cvtXY(self, x, y):
        """convert x,y from device real resolution to action input resolution"""
        x_input = x * self._scale #self.width / self.width_real
        y_input = y * self._scale #self.height / self.height_real
        log.debug("cvt %s,%s to %s,%s" % (x, y, x_input, y_input))
        return (int(x_input), int(y_input))

    def touch(self, x, y, eventType=airtest.EV_DOWN_AND_UP):
        '''
        touch screen at (x, y)
        multi finger operation not provided yet
        FIXME: not supported down_and_up in android
        '''
        x, y = self._cvtXY(x, y)
        log.debug('touch position %s', (x, y))
        self.driver.tap([(x, y)])

    def drag(self, (x1, y1), (x2, y2), duration=0):
        '''
        Simulate drag from (x1, y1) to (x2, y2)
        multi finger operation not provided yet
        '''
        x1, y1 = self._cvtXY(x1, y1)
        x2, y2 = self._cvtXY(x2, y2)
        log.debug('drag from (%s, %s) to (%s, %s)' % (x1, y1, x2, y2))
        self.driver.swipe(x1, y1, x2, y2, duration)

    def _getShapeReal(self):
        '''
        Get screen real resolution
        '''
        screen_shot = self.snapshot("screen_shot.png")
        img = Image.open(screen_shot)
        self.width_real, self.height_real = img.size
        log.debug('IosDevice real resolution: width:{width}, height:{height}'.format(
            width=self.width_real, height=self.height_real))
        return img.size

    def _getShapeInput(self):
        '''
        Get screen shape for x, y Input
        '''
        screen_size = self.driver.get_window_size()
        self.width, self.height = screen_size["width"], screen_size["height"]
        log.debug('IosDevice input resolution: width:{width}, height:{height}'.format(
            width=self.width, height=self.height))
        return (self.width, self.height)

    def shape(self):
        ''' 
        Get screen width and height 
        '''
        return map(int, [p/self._scale for p in self._getShapeInput()])
        #return (self.width_real, self.height_real)

    def type(self, text):
        '''
        Input some text

        @param text: string (text want to type)
        '''
        print "not provided yet on ios"

    def getMem(self, appname):
        print "not provided yet on ios"
        return {}

    def getCpu(self, appname):
        print "not provided yet on ios"
        return 0.0
    
    def getdevinfo(self):
        return {
                'mem_free': 0,
                'mem_total': 1,
                'cpu_count': 2,
                'product_model': 'ios',
                'product_brand': 'ios',
                }

if __name__ == '__main__':
    d = Device()
    d.snapshot("test.png")
    d.touch(180, 720)
    print d.shape()
    width, height = d.shape()
    d.drag((width * 0.5, height * 0.5), (width * 0.1, height * 0.5))
    
