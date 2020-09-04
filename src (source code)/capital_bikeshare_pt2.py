#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 19:13:39 2020

@author: mcgaritym
"""

# load required libraries
import requests
import io
from io import BytesIO
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime
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
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import calendar
import matplotlib.dates as mdates
import numpy as np

# import folium
# from folium import plugins
# from folium.plugins import HeatMap
# import holoviews as hv
# from holoviews import opts
# hv.extension('bokeh')

# gather files in local directory, create empty dataframe, and concatenate data
files = glob.glob('20*')
files.sort()
df = pd.DataFrame()
for f in files:
    data = pd.read_csv(f)
    df = pd.concat([df, data], axis=0, sort='False')

# reindex data 
# df = df.reindex()


# # ## 3. Data Cleaning/Processing:

# # In[88]:


# # fill columns (different names) with same values
# df.reset_index(level=0, inplace=True)
# df['start_station_name'].update(df.pop('Start station'))
# df['end_station_name'].update(df.pop('End station'))
# df['started_at'].update(df.pop('Start date'))
# df['ended_at'].update(df.pop('End date'))
# df['member_casual'].update(df.pop('Member type'))

# # drop unnecessary, redundant or blank columns
# df = df.drop(columns = ['Duration', 'is_equity', 'rideable_type', 'Bike number', 'start_station_id', 'end_station_id'])

# # convert to numeric, categorical or datetime data types
# df[['start_lat', 'end_lat', 'start_lng', 'end_lng', 'Start station number', 'End station number']] = df[['start_lat', 'end_lat', 'start_lng', 'end_lng', 'Start station number', 'End station number']].apply(pd.to_numeric)
# df[['start_station_name', 'end_station_name']] = df[['start_station_name', 'end_station_name']].apply(pd.Categorical)
# df['started_at'] = pd.to_datetime(df['started_at'])
# df['ended_at'] = pd.to_datetime(df['ended_at'])

# # create new duration and number of rides column
# df['duration'] = df['ended_at'] - df['started_at']
# df['number_rides'] = 1

# # fill in missing start and end station numbers based on other rows (same station name) that have start and end station numbers
# df['Start station number'] = df['Start station number'].fillna(df.groupby('start_station_name')['Start station number'].transform('mean'))
# df['End station number'] = df['End station number'].fillna(df.groupby('end_station_name')['End station number'].transform('mean'))

# # fill in missing latitude/longitude data based on other rows (same station number) that have latitude/longitude numbers
# df['start_lat'] = df['start_lat'].fillna(df.groupby('Start station number')['start_lat'].transform('mean'))
# df['end_lat'] = df['end_lat'].fillna(df.groupby('End station number')['end_lat'].transform('mean'))
# df['start_lng'] = df['start_lng'].fillna(df.groupby('Start station number')['start_lng'].transform('mean'))
# df['end_lng'] = df['end_lng'].fillna(df.groupby('End station number')['end_lng'].transform('mean'))

# # rename columns
# df = df.rename(columns={'Start station number': 'start_station_id', 'End station number': 'end_station_id'})

# # print sample of data
# print('\n Data Sample: \n')
# df.head()