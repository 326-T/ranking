# -*- coding: utf-8 -*-
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

from modules.tournament import Player, Swiss_System_Tournament, call_player


class Log():
    def __init__(self):
        self.match_log = []
        self.result_log = []
        self.latest_match = []
        self.latest_result = []
        self.match_id = 0
        
    def Set_latest_match(self, latest_match):
        self.latest_match = latest_match
        self.match_id = 0
    
    def Get_next_match(self):
        if self.match_id >= len(self.latest_match):
            return []
        else:
            return self.latest_match[self.match_id]
    
    def Report_match_result(self, result):
        self.latest_result.append(result)
        self.match_id += 1
        
    def Save(self):
        self.match_log.append(self.latest_match)
        self.result_log.append(self.latest_result)
        self.latest_match = []
        self.latest_result = []
        
    def Back(self):
        if self.match_id == 0:
            self.latest_match = self.match_log.pop(-1)
            self.latest_result = self.result_log.pop(-1)
            self.latest_result.pop(-1)
            self.match_id = len(self.latest_match) - 1
        else:
            self.latest_result.pop(-1)
            self.match_id -= 1



class Swiss_App():
    def __init__(self, w=800, h=200):
        self.w = w
        self.h = h
        self.num = 0
        self.packs = []
        self.grids = []
        
        self.init_window(w, h)
        self.init_tournament()
        
    def init_window(self, w, h):
        self.root = tk.Tk()
        self.root.geometry(str(self.w)+'x'+str(self.h))
        quit_button = tk.Button(self.root, text = '中断', command=self.Quit)
        quit_button.grid(row = 2, column = 1, padx = 5, pady = 5)
        back_button = tk.Button(self.root, text = "戻る", command=self.Back)
        back_button.grid(row = 2, column = 2, padx = 5, pady = 5)
        
    def init_tournament(self):
        self.log = Log()
        self.tournament = Swiss_System_Tournament(11)
        self.log.Set_latest_match(self.tournament.Make_Match())
        self.Ask_Question(self.log.Get_next_match())
        
    def Set_Window(self):
        for pack in self.packs:
            pack.pack()
        
    def Reset_Window(self):
        for pack in self.packs:
            pack.pack_forget()
        self.packs.clear()
        for grid in self.grids:
            grid.grid_forget()
        self.grids.clear()
        
    def Quit(self):
        self.root.destroy()
        self.tournament.Save('../result/test.csv')
    
    def Ask_Question(self, p_names):
        self.Reset_Window()
        label = tk.Label(self.root, text = p_names[0] + 'と' + p_names[1] + 'ではどちらが上手ですか？')
        ans2_button = tk.Button(self.root, text = p_names[0] + 'の方が上手', command=lambda:self.Answer(2))
        ans1_button = tk.Button(self.root, text = p_names[0] + 'の方がやや上手', command=lambda:self.Answer(1))
        _ans1_button = tk.Button(self.root, text = p_names[1] + 'の方がやや上手', command=lambda:self.Answer(-1))
        _ans2_button = tk.Button(self.root, text = p_names[1] + 'の方が上手', command=lambda:self.Answer(-2))
        label.grid(row = 0, column = 0, columnspan = 4, padx = 5, pady = 5)
        ans2_button.grid(row = 1, column = 0, padx = 5, pady = 5)
        ans1_button.grid(row = 1, column = 1, padx = 5, pady = 5)
        _ans1_button.grid(row = 1, column = 2, padx = 5, pady = 5)
        _ans2_button.grid(row = 1, column = 3, padx = 5, pady = 5)
        self.grids.append(ans2_button)
        self.grids.append(ans1_button)
        self.grids.append(_ans1_button)
        self.grids.append(_ans2_button)
        
    def Answer(self, r):
        result = [r, -r]
        self.log.Report_match_result(result)
        next_match = self.log.Get_next_match()
        if len(next_match) > 0 and (next_match[0] == "Bye" or next_match[1] == "Bye"):
            self.log.Report_match_result([2,-2])
            next_match = self.log.Get_next_match()
        
        if len(next_match) == 0:
            self.tournament.Report_Match(self.log.latest_match, self.log.latest_result)
            self.log.Save()
            self.log.Set_latest_match(self.tournament.Make_Match())
            next_match = self.log.Get_next_match()
        
        self.Ask_Question(next_match)
        
    def Back(self):
        if len(self.log.result_log) == 0 and len(self.log.latest_result) == 0:
            pass
        else:
            if self.log.match_id == 0:
                self.tournament.Delete_Match(self.log.match_log[-1], self.log.result_log[-1])
            self.log.Back()
            next_match = self.log.Get_next_match()
            if (next_match[0] == "Bye" or next_match[1] == "Bye"):
                self.log.Back()
                next_match = self.log.Get_next_match()

            self.Ask_Question(next_match)
        
    def Mainloop(self):
        self.root.mainloop()


a = Swiss_App()

a.Mainloop()


