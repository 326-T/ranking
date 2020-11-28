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

import numpy as np
import pandas as pd
import random
import copy


class Player():
    
    def __init__(self, name):
        self.win = 0
        self.lose = 0
        self.score = 0
        self.name = name
        self.rank = 0

        self.power = 0
        
    def __str__(self):
        return "Player:" + self.name + ", Rank:" + str(self.rank) + ", Win:" + str(self.win) + ", Lose:" + str(self.lose) + ", Score:" + str(self.score) + ", Power:" + str(self.power)


class Swiss_System_Tournament():
    
    def __init__(self, data_size):
        self.players = []
        names = []
        for i in range(data_size):
            self.players.append(Player('選手'+str(i+1)))
            names.append('選手'+str(i+1))
        if data_size%2 == 1:
            self.players.append(Player('Bye'))
            names.append('Bye')
        self.vs_table = pd.DataFrame(np.zeros((len(self.players), len(self.players))), index=names, columns=names, dtype='int')
        self.ranking = np.array(range(len(self.players)))
        self.end = False
        
    def Print(self):
        for r in self.ranking:
            print(self.players[r])
        print('score sheet')
        print(self.vs_table)
        
    def Save(self, path):
        self.vs_table.to_csv(path)
        
    def Load(self, path):
        self.vs_table = pd.read_csv(path, index_col=0)
        names = self.vs_table.index.values
        self.players.clear()
        for name1 in names:
            self.players.append(Player(name1))
            for name2 in names:
                if self.vs_table.at[name1, name2] > 0:
                    self.players[-1].win += 1
                elif self.vs_table.at[name1, name2] < 0:
                    self.players[-1].lose += 1
        self.Calc_Score()
        self.Update_Rank()
            
    def Update_Rank(self):
        ranking = []
        for p in self.players:
            ranking.append(-p.win-p.score*0.001)
        self.ranking = np.argsort(ranking)
        rank_list = []
        for i, r in enumerate(self.ranking):
            self.players[r].rank = i
            rank_list.append(self.players[r].name)
        # sort vs_table by rank
        self.vs_table = self.vs_table.reindex(index=rank_list, columns=rank_list)
        print(self.vs_table)
        self.Check_End()
        print(self.flag)
            
    def Make_Match(self):
        match_list = []
        ranking = copy.deepcopy(self.ranking)
        while len(ranking) > 1:
            for i in range(1, len(ranking)):
                if (self.vs_table.at[self.players[ranking[0]].name, self.players[ranking[i]].name] == 0
                    or self.players[ranking[i]].name == "Bye"):
                    match_list.append([self.players[ranking[0]].name, self.players[ranking[i]].name])
                    ranking = np.delete(ranking, [0, i])
                    break
                elif (i == len(ranking) - 1 or i == 3):
                    ranking = np.delete(ranking, 0)
        
        return match_list
    
    def Report_Match(self, match_list, result):
        for i, (m, r) in enumerate(zip(match_list, result)):
            if r[0] > 0:
                self.players[call_player(self.players, m[0])].win += 1
                self.players[call_player(self.players, m[1])].lose += 1
            else:
                self.players[call_player(self.players, m[0])].lose += 1
                self.players[call_player(self.players, m[1])].win += 1
        
            self.vs_table.at[m[0], m[1]] += r[0]
            self.vs_table.at[m[1], m[0]] += r[1]
        self.Calc_Score()
        self.Update_Rank()
        
    def Delete_Match(self, match_list, result):
        for i, (m, r) in enumerate(zip(match_list, result)):
            if r[0] > 0:
                self.players[call_player(self.players, m[0])].win -= 1
                self.players[call_player(self.players, m[1])].lose -= 1
            else:
                self.players[call_player(self.players, m[0])].win -= 1
                self.players[call_player(self.players, m[1])].lose -= 1
        
            self.vs_table.at[m[0], m[1]] -= r[0]
            self.vs_table.at[m[1], m[0]] -= r[1]
        self.Calc_Score()
        self.Update_Rank()
        
    def Calc_Score(self):
        for p1 in self.players:
            if p1.name == 'Bye':
                p1.score = -1e6
            else:
                score = 0
                for p2 in self.players:
                    if self.vs_table.at[p1.name, p2.name] > 0:
                        score += self.vs_table.at[p1.name, p2.name] * p2.win
                    elif self.vs_table.at[p1.name, p2.name] < 0:
                        score += self.vs_table.at[p1.name, p2.name] * p2.lose

                p1.score = score
            
    def Check_End(self):
        names = self.vs_table.index.values
        flag = True
        for i in range(len(names)):
            for j in range(i+1,len(names)):
                if self.vs_table.at[names[i], names[j]] == 2:
                    flag = True
                    break
                elif self.vs_table.at[names[i], names[j]] <= 0:
                    flag = False
                    break
            for j in range(i-1, -1, -1):
                if self.vs_table.at[names[i], names[j]] == -2:
                    flag = True
                    break
                elif self.vs_table.at[names[i], names[j]] >= 0:
                    flag = False
                    break

            if flag == False:
                break
        self.flag = flag
        return self.flag


class judge():
    def __init__(self):
        pass
    
    def entry(self, players):
        for p in players:
            if p.name == "Bye":
                p.power = 0
            else:
                p.power = random.randint(1,10)
    
    def match(self, players, match_list):
        result = []
        for m in match_list:
            power_m0 = players[call_player(players, m[0])].power
            power_m1 = players[call_player(players, m[1])].power
            r0 = random.choices([1,-1], weights=[power_m0, power_m1])
            result.append([r0[0], -r0[0]])
        return result


def call_player(players, name):
    index = -1
    for i, p in enumerate(players):
        if p.name == name:
            index = i
    if index == -1:
        print("invalid name: "+str(name))
    return index


def test_system():
    a = Swiss_System_Tournament(11)
    b = judge()
    b.entry(a.players)
    for i in range(10):
        match = a.Make_Match()
        result = b.match(a.players, match)
        a.Report_Match(match, result)
        a.Update_Rank()
    a.Print()
    a.Save('../../result/test.csv')
    c = Swiss_System_Tournament(0)
    c.Load('../../result/test.csv')
    c.Print()

# +
#test_system()
# -


