#!/usr/bin/env python
'''
Example Module
Peter Barker, September 2016

This module simply serves as a starting point for your own MAVProxy module.

1. copy this module sidewise (e.g. "cp mavproxy_example.py mavproxy_coolfeature.py"
2. replace all instances of "example" with whatever your module should be called
(e.g. "suav")

3. trim (or comment) out any functionality you do not need
'''

import os
import os.path
import sys
from pymavlink import mavutil
import errno
import time
import PySimpleGUI as sg

from MAVProxy.modules.lib import mp_module
from MAVProxy.modules.lib import mp_util
from MAVProxy.modules.lib import mp_settings


class suav(mp_module.MPModule):
    def __init__(self, mpstate):
        """Initialise module"""
        super(suav, self).__init__(mpstate, "suav", "")

        self.example_settings = mp_settings.MPSettings(
            [ ('verbose', bool, False),
          ])
        self.add_command('suav', self.cmd_suav, "suav module", ['status','set (LOGSETTING)','test (alt)'])
        self.cvsfile = open('eggs.csv', 'w', newline='')
        self.popcount = 0

    def usage(self):
        '''show help on command line options'''
        return "Usage: suav <status/set>"

    def cmd_suav(self, args):
        '''control behaviour of the module'''
        if len(args) == 0:
            print(self.usage())
        elif args[0] == "status":
            print(self.status())
        elif args[0] == "set":
            self.example_settings.command(args[1:])
        elif args[0] == "test":
            sg.PopupNoButtons('Test drop!','Altitude: ' + args[1]+'ft', non_blocking=True, no_titlebar=True, font=('Arial', 25), keep_on_top=True, location=[4+255*(self.popcount//7),700-(110*self.popcount)%770])
            self.popcount += 1
        else:
            print(self.usage())

    def status(self):
        '''returns information about module'''
        return()

    def idle_task(self):
        '''called rapidly by mavproxy'''
        '''now = time.time()'''

    def mavlink_packet(self, m):
        '''handle mavlink packets'''
        //print(m.get_type())
        if m.get_type() == 'GLOBAL_POSITION_INT':
            pass
        elif m.get_type() == 'STATUS_ALT_REQ':
            print(m.cur_alt)
            print(m.dist_alt)
        elif m.get_type() == 'DROP_POPUP':
            print('Message Received: Glider DROPPED!')
            print(m.value)
            sg.PopupNoButtons('Glider Drop!','Altitude: ' + str(m.value) + 'ft', non_blocking=True, no_titlebar=True, font=('Arial', 25), keep_on_top=True, location=[4+255*(self.popcount//7),700-(110*self.popcount)%770])
            self.popcount += 1
        elif m.get_type() == 'DATA16':
            if m.type == 150:
                print('Message Received: Glider DROPPED!')
            

def init(mpstate):
    '''initialise module'''
    return suav(mpstate)
