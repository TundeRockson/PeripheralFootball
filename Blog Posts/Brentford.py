#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 18:31:26 2021

@author: tunderockson
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

#Scrape some information Transfermarkt.com
headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

page = "https://www.transfermarkt.com/brentford-fc/rekordabgaenge/verein/1148/plus/1/galerie/0?saison_id=&pos=&detailpos=&w_s="
pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

Players = pageSoup.find_all("a", {"class": "spielprofil_tooltip"})
Values = pageSoup.find_all("td", {"class": "rechts hauptlink"})
Seasons = pageSoup.find_all("a", string="saison_id")
PlayersList = []
ValuesList = []


#Get the first 10 players from the table
for i in range(0,10):
    PlayersList.append(Players[i].text)
    ValuesList.append(Values[i].text[1:-1])
    
ValuesList = [int(float(i))*1000000 for i in ValuesList]
    
#Dataframe with departure Fees
df = pd.DataFrame({"Player":PlayersList,"Fee (Million)":ValuesList,"Transfer Status":'Departure Fee'})

df.head()


#Dataframe with Arrival Fees
df2 = pd.DataFrame({"Player":PlayersList,"Fee (Million)":
                    [2000000, 1700000, 2000000, 0, 2850000, 620000, 950000, 1350000, 1500000, 100000],
                    "Transfer Status":'Arrival Fee'})
finalDf= pd.concat([df, df2], axis=0)
    



#Plotting the departure and arrival fees
fig, ax = plt.subplots(figsize=(12, 4))
sns.set_style('darkgrid')
splot = sns.barplot(data=finalDf, x='Player', y='Fee (Million)', ax=ax, hue='Transfer Status', palette="coolwarm")
for p in splot.patches:
    splot.annotate(format(p.get_height()/1000000, '.02f')+"M", 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', 
                   size=9,
                   xytext = (0, 5), 
                   textcoords = 'offset points')
    
ax.set(ylim=(0, 35000000))

#Reformatting y labels
ax.get_yaxis().set_major_formatter(
    FuncFormatter(lambda x, p: format(int(x), ',')))



fig.savefig('/Users/tunderockson/Desktop/Sports Data Science/PeripheralFootball/Blog Posts/brentford.png',facecolor='white', orientation='landscape', dpi=500)





