# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 13:33:23 2019

@author: User
"""

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
%matplotlib inline

max_temp = pd.read_excel('MaxTemp90-16.xlsx')
max_temp = max_temp.iloc[:31,:13]
min_temp = pd.read_excel('MinTemp90-16.xlsx')
precipitaion = pd.read_excel('Precipitaion90-16.xlsx')
rainfall_days = pd.read_csv('seattleWeather_1990-2016.csv')
snowfall_depth = pd.read_excel('SnowfallDepth90-16.xlsx')

max_temp['Day'] = max_temp['Day'].astype('int')
max_temp = max_temp.set_index('Day')
max_temp = max_temp.replace('-',np.nan)
max_temp = max_temp.mean(skipna=True)
max_temp = np.round(max_temp,1)

min_temp = min_temp.set_index('Day')
min_temp = min_temp.replace('-',np.nan)
min_temp = min_temp.mean(skipna=True)
min_temp = np.round(min_temp,1)

precipitaion = precipitaion.set_index('Day')
precipitaion = precipitaion.replace('-',np.nan)

snowfall_depth = snowfall_depth.set_index('Day')
snowfall_depth = snowfall_depth.replace('-',np.nan)

rainfall_days = pd.read_csv('seattleWeather_1990-2016.csv')
rainfall_days['month_day'] = rainfall_days['DATE'].apply(lambda x : str(x.split('-')[1]) + '-' + str(x.split('-')[0]))
rainfall_days['RAIN_days'] = [1 if x == True else 0 for x in rainfall_days['RAIN']]
rainfall_days = rainfall_days.groupby('month_day')['RAIN_days'].sum()
rainfall_days = rainfall_days.reset_index() 
rainfall_days['month'] = [x.split('-')[0] for x in rainfall_days['month_day']]
rainfall_days = rainfall_days.groupby('month')['RAIN_days'].mean()
rainfall_days = np.round(rainfall_days.values)

precipitation = precipitaion.mean(skipna=True)
precipitation = np.round(precipitation,2)

snowfall_depth = snowfall_depth.mean(skipna=True)
snowfall_depth = np.round(snowfall_depth,2)
x = np.arange(1,13)

plt.style.use('default')
fig,(ax1,ax2)= plt.subplots(2,1,figsize=(10,8),sharex=True)
fig.subplots_adjust(top=0.4,bottom=0.2,wspace=None)

ax2.plot(x,rainfall_days.tolist(),'black',linestyle='--',label = 'Avg. Rainfall days per month',marker='s')
ax2.set_ylim([-10,20])
ax2.set_xlim([0,13])
ax2.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec'])
ax2.set_yticks([])
ax2.tick_params(axis=u'both', which=u'both',length=0)
for a,b,data in zip(x,rainfall_days.tolist(),rainfall_days.tolist()):
    ax2.annotate(s=str(int(data))+' days',xy=(a,b+1.2),xytext=(a-0.2,b+1.2),fontsize=8) 
ax2.axvline(6,ls='--',alpha=0.2)   
ax2.axvline(9,ls='--',alpha=0.2)    
ax2.axvline(3,ls='--',alpha=0.2) 
ax2.axvline(10,ls='--',alpha=0.2) 
ax2.legend(loc=(0.48, 0.85),fontsize=8)

ax3 = ax2.twinx()
ax3.bar(x,height=precipitation.values,alpha=0.5,align='center',label='Avg. Precipitation (IN)',color='red')
for a,b,data in zip(x,precipitation.tolist(),precipitation.tolist()):
    ax3.annotate(s=data,xy=(a,b-0.01),xytext=(a-0.2, b-0.01),fontsize=8)
ax3.bar(x,snowfall_depth,color='DarkBlue',align='center',label='Avg. Snowfall Depth (IN)',alpha=0.3)
for a,b,data in zip(x,snowfall_depth.tolist(),snowfall_depth.tolist()):
    ax3.annotate(s=data,xy=(a,b-0.006),xytext=(a-0.2, b-0.007),fontsize=8)
ax3.set_yticks(np.linspace(0,0.30,7))
ax3.set_yticks([])
ax3.legend(loc=(0.48, 0.75),fontsize=8)

ax1.plot(np.arange(1,13),max_temp,marker='o',color='red',label='Avg. Max Temp. per month')
ax1.plot(np.arange(1,13),min_temp,marker='o',color='blue',label='Avg. Min Temp. per month')
ax1.set_xticks(np.arange(1,14))
for a,b,data in zip(np.arange(1.4,13),max_temp.tolist(),max_temp.tolist()):
    ax1.annotate(s=str(int(data))+ u'\N{DEGREE SIGN}F' ,xy=(a,b+1.2),xytext=(a-0.4,b+2),fontsize=8)
for a,b,data in zip(np.arange(1.4,13),min_temp.tolist(),min_temp.tolist()):
    ax1.annotate(s=str(int(data))+ u'\N{DEGREE SIGN}F' ,xy=(a,b+1.2),xytext=(a-0.4,b+2),fontsize=8)  
ax1.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec'])    
ax1.set_yticks([])
ax1.set_ylim([35,85])
ax1.set_xlim([0,13])
ax1.legend(fontsize=8,loc=(0.75,0.75))
ax1.axvline(6,ls='--',alpha=0.2)   
ax1.axvline(9,ls='--',alpha=0.2)   
ax1.axvline(3,ls='--',alpha=0.2) 
ax1.axvline(10,ls='--',alpha=0.2)
ax1.tick_params(axis=u'both', which=u'both',length=0)
ax1.text(7,82,'Best',fontsize=8)
ax1.text(4,82,'Average',fontsize=8)
ax1.text(9.2,82,'Average',fontsize=8)
ax1.text(11.5,82,'Worst',fontsize=8)
ax1.text(1,82,'Worst',fontsize=8)
ax1.set_title('Best time to visit Seattle based on Weather Data from 1990-2016',fontsize=12)

for a in [ax1,ax2,ax3]:
    a.spines["top"].set_visible(False)
    a.spines["right"].set_visible(False)
    a.spines["bottom"].set_visible(False)
    a.spines["left"].set_visible(False)
plt.tight_layout()

fig.savefig('seattleweather.png')