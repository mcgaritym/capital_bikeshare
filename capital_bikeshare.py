#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 08:29:20 2020

@author: mcgaritym
"""
# STEP 1: load required libraries
import requests
import io
from io import BytesIO
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import date, datetime
import re
import time
from urllib.request import urlopen
import zipfile
from zipfile import ZipFile
import glob
import os
from urllib.request import urlopen, Request
import seaborn as sns
import textwrap
from matplotlib import pyplot as plt
import matplotlib as mpl
import folium
from folium import plugins
from folium.plugins import HeatMap
import numpy as np

# STEP 2: set driver options, request options, and url
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--headless')
# options.add_argument('--incognito')
# driver = webdriver.Chrome(ChromeDriverManager().install())
# headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.39 Safari/537.36', 
#             "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
# url = 'https://s3.amazonaws.com/capitalbikeshare-data/index.html'
# driver.get(url)
# time.sleep(2)
# driver.execute_script("window.scrollTo(0, 500000)")
# time.sleep(2)
# page_source = driver.page_source
# soup = BeautifulSoup(page_source, "html.parser")

# ## get links for data and filter for 2018-2020 (current)
# links = []
# for link in soup.findAll('a'):
#     link_text = link.get('href')
#     str(link_text)
#     if ('2020' in link_text) or ('2019' in link_text) or ('2018' in link_text):
#         links.append(link_text)
# print(links)


# ## get data from links, and save zip to disk/folder or convert zip directly to DataFrame
# df = pd.DataFrame()
# for url in links:

#     ## METHOD 1: save zip files to disk/folder
#     r = requests.get(url)
#     z = zipfile.ZipFile(io.BytesIO(r.content))
#     z.extractall()
    
#     ## METHOD 2: dont save zip files to disk/folder
#     # remote_zip_file = urlopen(url)
#     # zipinmemory = BytesIO(remote_zip_file.read())
#     # zip_file = zipfile.ZipFile(zipinmemory)
#     # data = pd.read_csv(zip_file.open(zip_file.namelist()[0]))
#     # df = pd.concat([df, data], axis=0, sort=False)
#     # print(df.tail())

#----------------------------------------------------------------------------

files = glob.glob('20*')
files.sort()
#print(files)
df = pd.DataFrame()
for f in files:
    data = pd.read_csv(f)
    df = pd.concat([df, data], axis=0, sort='False')
    
df.reindex()

df['start_station_name'].update(df.pop('Start station'))
df['end_station_name'].update(df.pop('End station'))
df['started_at'].update(df.pop('Start date'))
df['ended_at'].update(df.pop('End date'))
df['member_casual'].update(df.pop('Member type'))
df['started_at'] = pd.to_datetime(df['started_at'])
df['ended_at'] = pd.to_datetime(df['ended_at'])
df['duration'] = df['ended_at'] - df['started_at']
df['number_rides'] = 1
df = df.drop(columns = ['Duration', 'is_equity', 'rideable_type', 'Bike number', 'start_station_id', 'end_station_id'])

df[['start_lat', 'end_lat', 'start_lng', 'end_lng', 'Start station number', 'End station number']] = df[['start_lat', 'end_lat', 'start_lng', 'end_lng', 'Start station number', 'End station number']].apply(pd.to_numeric)
df[['start_station_name', 'end_station_name']] = df[['start_station_name', 'end_station_name']].apply(pd.Categorical)

# alternate methods
#df['start_lat'] = df.groupby(['start_station_name'], sort=False)['start_lat'].fillna(pd.Series.mode)
#df["value"] = df.groupby("name").transform(lambda x: x.fillna(x.mean()))
#df = df.groupby('end_station_name').fillna(df.mode().iloc[0])
#df.D = df.groupby(['A','B','C'])['D'].apply(lambda x: x.fillna(x.mean()))

# filling in missing start and end station numbers and
df['Start station number'] = df['Start station number'].fillna(df.groupby('start_station_name')['Start station number'].transform('mean'))
df['End station number'] = df['End station number'].fillna(df.groupby('end_station_name')['End station number'].transform('mean'))

df['start_lat'] = df['start_lat'].fillna(df.groupby('Start station number')['start_lat'].transform('mean'))
df['end_lat'] = df['end_lat'].fillna(df.groupby('End station number')['end_lat'].transform('mean'))
df['start_lng'] = df['start_lng'].fillna(df.groupby('Start station number')['start_lng'].transform('mean'))
df['end_lng'] = df['end_lng'].fillna(df.groupby('End station number')['end_lng'].transform('mean'))

# rename columns
df = df.rename(columns={'Start station number': 'start_station_id', 'End station number': 'end_station_id'})

print('Shape of DataFrame before dropNA:', df.shape)

# drop rows with missing values
df = df.dropna(subset=['start_lat', 'end_lat', 'start_lng', 'end_lng', 'start_station_id', 'end_station_id', 'start_station_name', 'end_station_name'])

print('Shape of DataFrame after dropNA:', df.shape)

# print sample of columns
df1 = df.iloc[:1000]
df2 = df.iloc[-1000:]

# print(df.groupby('start_station_name')['number_rides'].count().nlargest(10))
# print(df.groupby('start_station_name')['number_rides'].count().nsmallest(10))


#df.groupby('start_station_name')['number_rides'].count().nlargest(10)
#df = df.set_index('started_at')

## PLOT 1: Barplot of Top 5 Stations
# sns.set(style="darkgrid")
# ax = sns.countplot(x="start_station_name", data=df, palette="Blues_d", order=df.start_station_name.value_counts().iloc[:5].index)
# ax.set(xlabel='ride stations', ylabel='number of rides', title = 'Top 5 ride stations in DC (2018-Present)')
# ax.set_xticklabels(ax.get_xticklabels(), fontsize=8)
# ax.set_xticklabels([textwrap.fill(t.get_text(), 11)  for t in ax.get_xticklabels()], fontsize=8)
#plt.savefig('top5_ride_stations_.png', dpi=300, bbox_inches='tight')



# ## PLOT 2: Barplot of Top 5 Stations During Virus 
# df_covid = df[(df['started_at'] >= '2020-03-01')]
# sns.set(style="darkgrid")
# ax = sns.countplot(x="start_station_name", data=df_covid, palette="Blues_d", order=df_covid.start_station_name.value_counts().iloc[:5].index)
# ax.set(xlabel='ride stations', ylabel='number of rides', title = 'Top 5 ride stations in DC during COVID-19 (March 2020-Present)')
# ax.set_xticklabels(ax.get_xticklabels(), fontsize=10)
# ax.set_xticklabels([textwrap.fill(t.get_text(), 11)  for t in ax.get_xticklabels()], fontsize=10)
# #plt.savefig('top5_ride_stations_.png', dpi=300, bbox_inches='tight')


# ## PLOT 3: Heatmap of Rides
# df = df.dropna(subset=['start_lat', 'start_lng'])
# #m = folium.Map([38.8977, -77.0365], zoom_start=14)
# def generateBaseMap(default_location=[38.8977, -77.0365], default_zoom_start=13):
#     base_map = folium.Map(location=default_location, control_scale=True, zoom_start=default_zoom_start)
#     return base_map
# base_map = generateBaseMap()
# m = HeatMap(data=df[['start_lat', 'start_lng', 'number_rides']].groupby(['start_lat', 'start_lng']).sum().reset_index().values.tolist(), radius=8, max_zoom=13).add_to(base_map)
# m.save('map2.html')