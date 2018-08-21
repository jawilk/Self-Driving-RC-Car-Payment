# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 15:20:52 2018

@author: Jannis
"""
### CREDITS: https://github.com/indrekots/rc-car-controller ###

import time
import tkinter as tk
from tkinter import messagebox
import bluetooth

class Controller:
    def __init__(self):
        self.pressed = {}
        self.prevPressed = {}
        self.time = []
        self.press_release = []
        self._initPresses()
        self._create_ui()

    def _initPresses(self):
        self.pressed["q"] = False
        self.pressed["w"] = False
        self.pressed["e"] = False
        self.pressed["a"] = False
        self.pressed["s"] = False
        self.pressed["d"] = False
        self.pressed["y"] = False
        self.pressed["x"] = False
        self.pressed["k"] = False
        self.pressed["0"] = False
        self.pressed["1"] = False
        self.pressed["2"] = False
        self.pressed["3"] = False
        self.pressed["4"] = False
        self.prevPressed["q"] = False
        self.prevPressed["w"] = False
        self.prevPressed["e"] = False
        self.prevPressed["a"] = False
        self.prevPressed["s"] = False
        self.prevPressed["d"] = False
        self.prevPressed["y"] = False
        self.prevPressed["x"] = False
        self.prevPressed["k"] = False
        self.prevPressed["0"] = False
        self.prevPressed["1"] = False
        self.prevPressed["2"] = False
        self.prevPressed["3"] = False
        self.prevPressed["4"] = False


    def start(self):
        self._check_key_press()
        self.root.protocol("WM_DELETE_WINDOW", self.closing)
        self.root.mainloop()
        
    def closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            with open('time_press_release/time_p_r.txt', 'w') as time_file:  
                for time_stamp in self.time:
                    time_file.write('%s\n' % time_stamp)           
            with open('time_press_release/press_release.txt', 'w') as press_release_file:  
                for key in self.press_release:
                    press_release_file.write('%s\n' % key)
            self.root.destroy()


    def _check_for_press(self, key, command):
        if self._is_pressed(key):
            self.prevPressed[key] = True
            sock.send(command)
            self.press_release.append(key+'_press')
            self.time.append(time.time())
            print(key + " pressed")

    def _check_for_release(self, key, command):
        if self._is_released(key):
            self.prevPressed[key] = False
            self.press_release.append(key+'_release')
            self.time.append(time.time())
            print(key + " released")

    def _check_key_press(self):
        self._check_for_press("q", b"Q")
        self._check_for_release("q", b"Q")
        self._check_for_press("w", b"W")
        self._check_for_release("w", b"W")
        self._check_for_press("e", b"E")
        self._check_for_release("e", b"E")
        self._check_for_press("a", b"R")
        self._check_for_release("a", b"R")
        self._check_for_press("s", b"T")
        self._check_for_release("s", b"T")
        self._check_for_press("d", b"F")
        self._check_for_release("d", b"F")
        self._check_for_press("y", b"J")
        self._check_for_release("y", b"J")
        self._check_for_press("x", b"I")
        self._check_for_release("x", b"I")
        self._check_for_press("k", b"O")
        self._check_for_release("k", b"O")
        self._check_for_press("0", b"0")
        self._check_for_release("0", b"0")
        self._check_for_press("1", b"1")
        self._check_for_release("1", b"1")
        self._check_for_press("2", b"2")
        self._check_for_release("2", b"2")
        self._check_for_press("3", b"3")
        self._check_for_release("3", b"3")
        self._check_for_press("4", b"4")
        self._check_for_release("4", b"4")


        self.root.after(10, self._check_key_press)

    def _is_pressed(self, key):
        return self.pressed[key] and self.prevPressed[key] == False

    def _is_released(self, key):
        return self.pressed[key] == False and self.prevPressed[key]

    def _create_ui(self):
        self.root = tk.Tk()
        self.root.geometry('400x300')
        self._set_bindings()

    def _set_bindings(self):
        for char in ["q","w","e","a","s","d","y","x","k","0","1","2","3","4"]:
            self.root.bind("<KeyPress-%s>" % char, self._pressed)
            self.root.bind("<KeyRelease-%s>" % char, self._released)
            self.pressed[char] = False

    def _pressed(self, event):
        self.pressed[event.char] = True

    def _released(self, event):
        self.pressed[event.char] = False
        
def get_device():
    return bluetooth.discover_devices()[0] # '00:13:EF:00:0D:FE'; Neeeds to connect from PC before; PW=1234

if __name__ == "__main__":
    bd_addr = get_device()
    port = 1
    sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))
    
    p = Controller()
    p.start()
