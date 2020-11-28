# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import tkinter as tk


class app_window():
    
    def __init__(self, w=1200, h=900):
        self.w = w
        self.h = h
        self.num = 0
        self.window = tk.Tk()
        button = tk.Button(self.window, text = 'quit', command=self.quit)
        button.pack()
        button = tk.Button(self.window, text = '1', command=self.add(1))
        button.pack()
        button = tk.Button(self.window, text = '2', command=self.add(2))
        button.pack()
        button = tk.Button(self.window, text = '3', command=self.add(3))
        button.pack()
        self.window.geometry(str(self.w)+'x'+str(self.h))
        self.window.mainloop()
        
    def quit(self):
        self.window.destroy()
        
    def add(self, x):
        self.num += x
        print(self.num)


a=app_window()




