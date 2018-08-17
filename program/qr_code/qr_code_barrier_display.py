# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 16:36:09 2018

@author: Jannis
"""

import tkinter as tk
from PIL import ImageTk
import time

#if car:
flag = 0
tim = time.time()
tim_2 = 0
root = tk.Tk()
root.geometry('%sx%s+%s+%s'%(1500,1100,-1100,-100)) #(w,h,a,b)
img = ImageTk.PhotoImage(file="IOTA/qr_code.png")
panel = tk.Label(image = img)
panel.configure(bg='black')
panel.pack(side = "bottom", fill = "both", expand = "yes")
def callback():
    img2 = ImageTk.PhotoImage(file='IOTA/safe_drive.png')
    panel.configure(image=img2)
    panel.image = img2
    #root.after(5000, lambda: root.destroy())

#root.after(5000, lambda: callback())
#root.mainloop()

while flag != 2:
    root.update_idletasks()
    root.update()
    if flag == 0 and time.time() - tim > 5:
        callback()
        tim_2 = time.time()
        flag = 1
    if time.time() - tim_2 > 5 and tim_2 != 0:
        root.destroy()
        flag = 2
