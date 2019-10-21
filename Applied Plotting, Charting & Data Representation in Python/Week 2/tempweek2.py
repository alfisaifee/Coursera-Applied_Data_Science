# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 11:59:03 2019

@author: User
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def get_data():
    
    df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
    df['Data_Value'] = df['Data_Value'] / 10
    
    #To group data based on day and month
    month_day = []
    for element in df['Date']:
        dm = element.split('-')
        month_day.append(str(dm[1])+'-'+str(dm[2]))    
    df['month_day'] = month_day
    
    
    #To exclude data from year 2015
    ind_2015 = []
    for x in range(0,len(df)):
        if pd.Timestamp(df['Date'][x]).year == 2015:
            ind_2015.append(x)
    df_2015 = df.iloc[ind_2015]   
    df_n = df.drop(ind_2015)
    
    
    #To remove data of 29th Feb
    df_n = df_n.drop(df_n[df_n['month_day'] == '02-29'].index.values.tolist())  
    
    df_g = df_n.groupby('month_day')['Data_Value'].agg({'max':max,'min':min})
    df_g = df_g.reset_index()
    
    #To get 2015 datapoints for scatter plot
    df_g2015 = df_2015.groupby('month_day')['Data_Value'].agg({'max_2015':max,'min_2015':min})
    df_g['max_2015'] = df_g2015['max_2015'].values.tolist()
    df_g['min_2015'] = df_g2015['min_2015'].values.tolist()
    df_2015_max = df_g[df_g['max'] < df_g['max_2015']]
    df_2015_min = df_g[df_g['min'] > df_g['min_2015']]
    
    
    return df_g,  df_2015_max, df_2015_min

def plot_minmax():
    df, df_2015_max, df_2015_min = get_data()
    ax = plt.figure()
    fig,ax = plt.subplots(figsize = (15,10))
    plt.title('Max & Min Temp. in 2015 above and below Max & Min. from 2005-2014')
    
    ax.scatter(df_2015_max.index.values.tolist(),df_2015_max['max_2015'].values.tolist(),color='darkblue',label='Max. Temp. in 2015 greater than Max. from 2005-2014')
    ax.scatter(df_2015_min.index.values.tolist(),df_2015_min['min_2015'].values.tolist(),color='orange',label='Min. Temp. in 2015 less than Min. from 2005-2014')
    ax.plot(df['max'].values,color='gray',label='Max Temp. from 2005-2014 for day')
    ax.plot(df['min'].values,color='black',label='Min Temp. from 2005-2014 for day',alpha=0.25)
    ax.set_xticks(np.arange(15,350,30))
    ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec'])
    ax.set_xlim([-2,366])
    ax.set_ylim([-50,50])
    ax.set_yticks([-40,-20,0,20,40])
    ax.set_ylabel(u'Temperature in \N{DEGREE SIGN}C')
    ax.fill_between(range(len(df['max'].values)), 
                       df['max'].values, df['min'].values, 
                       facecolor='blue', alpha=0.08)
    ax.legend(loc='lower center')
    
    ax2 = ax.twinx()
    ax2.set_yticks([-40,-4,32,68,104])
    ax2.set_ylim([-58,122])
    ax2.set_ylabel(u'Temperature in \N{DEGREE SIGN}F')
    fig.savefig('temp.png')
    
plot_minmax()    