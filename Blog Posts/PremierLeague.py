#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 23:49:59 2021

@author: tunderockson
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import datetime

path = r'/Users/tunderockson/Desktop/Sports Data Science/english-premier-league_zip/archive'
all_files = glob.glob(path + "/*.csv")

#Combining all the datasets columnwise
li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)
    

frame = pd.concat(li, axis=0, ignore_index=True)

#Removing unnecessary columns from the dataset
pl_df = frame.drop(['Div','B365H', 'B365D', 'B365A', 'BWH', 'BWD',
       'BWA', 'IWH', 'IWD', 'IWA', 'LBH', 'LBD', 'LBA', 'PSH', 'PSD', 'PSA',
       'WHH', 'WHD', 'WHA', 'SJH', 'SJD', 'SJA', 'VCH', 'VCD', 'VCA', 'Bb1X2',
       'BbMxH', 'BbAvH', 'BbMxD', 'BbAvD', 'BbMxA', 'BbAvA', 'BbOU',
       'BbMx>2.5', 'BbAv>2.5', 'BbMx<2.5', 'BbAv<2.5', 'BbAH', 'BbAHh',
       'BbMxAHH', 'BbAvAHH', 'BbMxAHA', 'BbAvAHA', 'PSCH', 'PSCD', 'PSCA',
       'GBH', 'GBD', 'GBA', 'SBH', 'SBD', 'SBA', 'BSH', 'BSD', 'BSA'],axis=1)

#Adding additional columns to the dataset
pl_df["Goals"] = pl_df["FTHG"]+pl_df["FTAG"]
pl_df["TotalShots"] = pl_df["HS"]+pl_df["AS"]
pl_df["ShotsOnTarget"] = pl_df["HST"]+pl_df["AST"]
pl_df["Corners"] = pl_df["HC"]+pl_df["AC"]
pl_df["Fouls"] = pl_df["HF"]+pl_df["AF"]
pl_df["Bookings"] = pl_df["HY"]+pl_df["HR"]+pl_df["AY"]+pl_df["AR"]

pl_df['Date'] = pd.to_datetime(pl_df['Date'])

#Function for sorting the data by seasons
def season_sort(obs):
    if (obs > pd.to_datetime('08-01-2009')) & (obs < pd.to_datetime('05-31-2010')):
        Season = '2009/10'
    elif (obs > pd.to_datetime('08-01-2010')) & (obs < pd.to_datetime('05-31-2011')):
        Season = '2010/11'
    elif (obs > pd.to_datetime('08-01-2011')) & (obs < pd.to_datetime('05-31-2012')):
        Season = '2011/12'
    elif (obs > pd.to_datetime('08-01-2012')) & (obs < pd.to_datetime('05-31-2013')):
        Season = '2012/13'
    elif (obs > pd.to_datetime('08-01-2013')) & (obs < pd.to_datetime('05-31-2014')):
        Season = '2013/14'
    elif (obs > pd.to_datetime('08-01-2014')) & (obs < pd.to_datetime('05-31-2015')):
        Season = '2014/15'
    elif (obs > pd.to_datetime('08-01-2015')) & (obs < pd.to_datetime('05-31-2016')):
        Season = '2015/16'
    elif (obs > pd.to_datetime('08-01-2016')) & (obs < pd.to_datetime('05-31-2017')):
        Season = '2016/17'
    elif (obs > pd.to_datetime('08-01-2017')) & (obs < pd.to_datetime('05-31-2018')):
        Season = '2017/18'
    else:
        Season = '2018/19'
    return Season

pl_df['Season']=pl_df['Date'].apply(lambda x:season_sort(x))

#Function for getting the points from each game
def points_given(obs):
    if (obs == 'A'):
        home_points=0
        away_points=3
    elif (obs == 'H'):
        home_points=3
        away_points=0
    else:
        home_points=1
        away_points=1
    return [home_points, away_points]

pl_df['HomePoints']=pl_df['FTR'].apply(lambda x:points_given(x)[0])    
pl_df['AwayPoints']=pl_df['FTR'].apply(lambda x:points_given(x)[1])    

#correl = pl_df.corr()
        
#Applying the seasons function

#pl_df.rename(columns={"FTHG": "FullTime HomeGoals", "FTAG": "FullTime AwayGoals",
#                      "FTR": "FullTime Result", "HTHG": "HalfTime HomeGoals",
#                      "HTAG": "HalfTime AwayGoals", "HTR": "HalfTime Result",
#                      "HS": "HomeShots", "AS": "AwayShots", "HST": "HomeShotsOnTarget",
#                      "AST": "AwayShotsOnTarget", "HF": "HomeFouls", "AF": "AwayFouls",
#                      "HC": "HomeCorners", "AC": "AwayCorners", "HY":"HomeYellow",
#                      "AY": "AwayYellow", "HR": "HomeRed", "AR": "AwayRed"})
