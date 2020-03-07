import os
import os.path
import time
import PySimpleGUI as sg
import sys

def formatline(line):
    line = line.split()
    line = [float(line[0]), line[1], float(line[2])]
    return line

def displayalt(alt):
    pass

with open(sys.argv[1], 'r') as logfile:
    popcount = 0
    firstline = logfile.readline()
    firstline = formatline(firstline)
    assert firstline[1][0]=='S','logfile has no start'
    offset = firstline[0] - time.time()
    for line in logfile:
        line = formatline(line)
        while line[0]>(time.time()+offset):
            pass
        displayalt(line[2])
        if (line[1][0] == 'G') or (line[1][0]=='N') or (line[1][0]=='T'):
            sg.PopupNoButtons(line[1] + ' Drop!','Altitude: ' + str(line[2]) + 'M', non_blocking=True, no_titlebar=True, font=('Arial', 25), keep_on_top=True, location=[4+270*(popcount//7),700-(110*popcount)%770])
            popcount += 1
input()

