# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 19:46:31 2019

@author: User
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
% matplotlib notebook

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])
                  
fig,((ax1),(ax2)) = plt.subplots(2,1,figsize=(9,12))
mean = np.round(df.mean(axis=1),1)
std = df.std(axis=1)
C = 1.96
standard_error = std / np.sqrt(df.shape[1])
yerr = standard_error * C
ax2.set_position([0.13,0.48,0.75,0.02])
ax2.yaxis.set_ticks_position('none') 
ax2.set_xticks([0,128,255])
ax2.set_xticklabels(['Definetely Lower','Equal to y','Definetely Higher'])
ax2.set_yticklabels([])
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))
ax2.imshow(gradient, aspect='auto', cmap=plt.get_cmap('RdBu'))

def plot_bar(y):
    ax1.cla()
    ax1.bar(np.arange(0.5,df.shape[0]),mean,edgecolor='Black',color=get_color(y),width=0.75)
    ax1.errorbar(np.arange(0.5,df.shape[0]),mean,yerr=yerr,color='Black',capsize=12,ls='none')
    ax1.axhline(y,color='Red',alpha=0.7,linestyle='--')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    #ax.spines['left'].set_visible(False)
    #ax.spines['bottom'].set_visible(False)
    ax1.set_xticks([0.5,1.5,2.5,3.5])
    ax1.set_xticklabels(['1992','1993','1994','1995'])
    ax1.set_ylabel('Sample Mean',fontsize=12)
    ax1.annotate('y = {}'.format(y),[1.5,50000],fontsize=14)
    ax1.xaxis.set_ticks_position('none') 
    ax1.yaxis.set_ticks_position('none') 
    ax1.set_title('Sample Mean By Year, CI = 95%',fontsize=15)
    
def get_color(y):
    
    diff = y - mean
    sign = [1 if d > 0 else -1 for d in diff]
    prev_range = diff.abs().min(),diff.abs().max()
    new_range = 0.5,1
    blue = cm.Blues
    red = cm.Reds
    interpolation = np.interp(diff.abs(),prev_range,new_range) 
    colors = []
    for i,d in zip(interpolation.tolist(),diff):
        if d == 0:
            colors.append('White')
        elif d < 0:
            colors.append(blue(abs(i)))
        elif d > 0:
            colors.append(red(abs(i)))
            
    return colors

def onpick(event):
    y = np.round(event.ydata,1)
    plot_bar(y)
    

plot_bar(41000)
fig.canvas.mpl_connect('button_press_event', onpick)
fig.savefig('SampleBasedVisualization.png') 