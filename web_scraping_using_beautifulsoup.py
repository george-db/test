# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 09:59:38 2021

@author: geojo
"""

import bs4
from bs4 import BeautifulSoup
import csv
import requests
import time
import pandas as pd
import urllib
import re
import pickle
from datetime import datetime
from dateutil.parser import parse
from pandas.api.types import is_numeric_dtype, is_datetime64_dtype
import numpy as np


dr = pd.date_range('20110801','20110901',freq='MS')

def is_date(str_val):
    try:
        parse(str_val,fuzzy=False)
        return True
    except ValueError:
        return False

def convert_to_numeric(str_val):        
    repl_str = re.compile('\d+.?\d*')
    return ' '.join([str(x) for x in str_val.split() if re.search(repl_str,x)])



l1_datetime=[]
avg_temp=[]
avg_dewpoint=[]
avg_windspeed=[]
avg_direction=[]
rainfall_for_year=[]
max_temp=[]
max_humidity=[]
max_windspeed=[]
avg_humidity=[]
avg_barometer=[]
avg_gustspeed=[]
rainfall_for_month=[]
max_rain_per_minute=[]
min_temp=[]
min_humidity=[]
max_pressure=[]
min_pressure=[]
max_gustspeed=[]
max_heatindex=[]
for x in dr:
    str_url= "https://www.estesparkweather.net/archive_reports.php?date="+datetime.strftime(x,"%Y%m")
    print(str_url)
    print('^'*30)
    pg = requests.get(str_url)
    soup = BeautifulSoup(pg.content,'html.parser')
    #print(list(soup.children))
    main_header = soup.find_all('tr',class_='table-top')
    col_vals = soup.find_all('tr',class_='column-light')
    
    main_tables = soup.find_all('table')
    h1_val = soup.find_all('h1')[1]
    year_val_str = str(h1_val).replace('<h1>', '').replace('</h1>','')
    year_val = year_val_str.split(' ')[::-1][0]
    
    for i in range(0,len(main_tables)):
        #print(main_tables[i].find(class_='table-top').get_text())
        td_val = main_tables[i].find_all('td',colspan=2)
        if main_tables[i].find('td',colspan=2)==None:
            continue
        td_val0 = main_tables[i].find('td',colspan=2).get_text()
        td_val2 = main_tables[i].find_all('tr',class_="column-light")
        td_val3 = main_tables[i].find_all('tr',class_="column-dark")
        #td_val4 = main_tables[i].find_all('tr')        
        
            
        month_val_str=td_val0.split(' ')[0]
        day_val_str=td_val0.split(' ')[1]        
        print('---'*20)
        #print(day_val_str)
        #print(month_val_str)
        #print(year_val)
        idx_datetime=year_val+'-'+month_val_str+'-'+day_val_str
        #print('%%'*20)
        #print(idx_datetime)
        #print(is_date(idx_datetime))
        print('='*30)
        print(idx_datetime)
        print('='*30)
        if is_date(idx_datetime)==False:
            continue
        if datetime.strptime(idx_datetime,'%Y-%b-%d').date()>datetime.strptime('2018-Oct-28','%Y-%b-%d').date():
            break        
        
        #skipping the first header row
        for row in main_tables[i].find_all('tr')[1:]:            
            str_val1 = row.find_all('td')[1].get_text()  
            if row.find_all('td')[0].get_text()=="Average temperature":                            
               avg_temp.append(float(convert_to_numeric(str_val1).replace('°F','')))
            if row.find_all('td')[0].get_text()=="Average humidity":
               avg_humidity.append(int(convert_to_numeric(str_val1).replace('%','')))
            if row.find_all('td')[0].get_text()=="Average dewpoint":                            
               avg_dewpoint.append(float(convert_to_numeric(str_val1).replace('°F','')))
            if row.find_all('td')[0].get_text()=="Average barometer":
               avg_barometer.append(float(convert_to_numeric(str_val1)))
            if row.find_all('td')[0].get_text()=="Average windspeed":                            
               avg_windspeed.append(float(convert_to_numeric(str_val1)))
            if row.find_all('td')[0].get_text()=="Average gustspeed":
               avg_gustspeed.append(float(convert_to_numeric(str_val1)))
            if row.find_all('td')[0].get_text()=="Average direction":                            
               avg_direction.append(int(convert_to_numeric(str_val1).replace('°','')))
            if row.find_all('td')[0].get_text()=="Rainfall for month":
               rainfall_for_month.append(float(convert_to_numeric(str_val1)))
            if row.find_all('td')[0].get_text()=="Rainfall for year":
               rainfall_for_year.append(float(convert_to_numeric(str_val1)))
            if row.find_all('td')[0].get_text()=="Maximum rain per minute":
               max_rain_per_minute.append(float(convert_to_numeric(str_val1).split()[0]))
            if row.find_all('td')[0].get_text()=="Maximum temperature":
               max_temp.append(float(convert_to_numeric(str_val1).split()[0].replace('°F','')))
            if row.find_all('td')[0].get_text()=="Minimum temperature":
               min_temp.append(float(convert_to_numeric(str_val1).split()[0].replace('°F','')))
            if row.find_all('td')[0].get_text()=="Maximum humidity":                            
               max_humidity.append(int(convert_to_numeric(str_val1).split()[0].replace('%','')))
            if row.find_all('td')[0].get_text()=="Minimum humidity":
               min_humidity.append(int(convert_to_numeric(str_val1).split()[0].replace('%','')))
            if row.find_all('td')[0].get_text()=="Maximum pressure":
               max_pressure.append(float(convert_to_numeric(str_val1).split()[0]))
            if row.find_all('td')[0].get_text()=="Minimum pressure":
               min_pressure.append(float(convert_to_numeric(str_val1).split()[0]))
            if row.find_all('td')[0].get_text()=="Maximum windspeed":                            
               max_windspeed.append(float(convert_to_numeric(str_val1).split()[0]))
            if row.find_all('td')[0].get_text()=="Maximum gust speed":                            
               max_gustspeed.append(float(convert_to_numeric(str_val1).split()[0]))
            if row.find_all('td')[0].get_text()=="Maximum heat index":                            
               max_heatindex.append(float(convert_to_numeric(str_val1).split()[0].replace('°F','')))

        #print(datetime.strptime(idx_datetime,'%Y-%b-%d').date())        
        #l1_datetime.append(datetime.strptime(idx_datetime,'%Y-%b-%d').date().strftime("%Y-%m-%-d"))    
        l1_datetime.append(pd.to_datetime(idx_datetime,format='%Y-%b-%d'))
                    
        #print(idx_datetime)
        print('---'*20)
        #date_index = td_val0.split()[1] +''
        #rel_soup2 = BeautifulSoup(' '.join([str(x) for x in td_val2]),'html.parser')
        #rel_soup3 = BeautifulSoup(' '.join([str(x) for x in td_val3]),'html.parser')
        #rel_soup = BeautifulSoup(' '.join([str(x) for x in td_val]),'html.parser')
        #str_avg_temp = rel_soup2.find_all('td')[1].get_text().lstrip()
        #str_avg_dewpoint = rel_soup2.find_all('td')[3].get_text().lstrip()
        #str_avg_windspeed = rel_soup2.find_all('td')[5].get_text().lstrip()
        #str_avg_direction = rel_soup2.find_all('td')[7].get_text().lstrip()
        #str_rainfall_for_year = rel_soup2.find_all('td')[9].get_text().lstrip()
        #str_max_temp = rel_soup2.find_all('td')[11].get_text().lstrip()
        #str_max_humidity = rel_soup2.find_all('td')[13].get_text().lstrip()
        #str_max_windspeed = rel_soup2.find_all('td')[15].get_text().lstrip()
        
        #avg_temp.append(str_avg_temp)
        #avg_dewpoint.append(str_avg_dewpoint)
        #avg_windspeed.append(str_avg_windspeed)
        #avg_direction.append(str_avg_direction)
        #rainfall_for_year.append(str_rainfall_for_year)
        #max_temp.append(str_max_temp)
        #max_humidity.append(str_max_humidity)
        #max_windspeed.append(str_max_windspeed)
        
        #for c1 in rel_soup2.find_all('td'):
        #    print(c1)
        print('*'*40)
        

'''print(l1_datetime)
print(avg_temp)
print(avg_dewpoint)
print(avg_windspeed)
print(avg_direction)
print(rainfall_for_year)
print(max_temp)
print(max_humidity)
print(max_windspeed)'''
df = pd.DataFrame({'datetime':l1_datetime,
                   'Average temperature (°F)':avg_temp,
                   'Average humidity (%)':avg_humidity,
                   'Average dewpoint (°F)':avg_dewpoint,
                   'Average barometer (in)':avg_barometer,
                   'Average windspeed (mph)':avg_windspeed,
                   'Average gustspeed (mph)':avg_gustspeed,                   
                   'Average direction (°deg)':avg_direction,
                   'Rainfall for month (in)':rainfall_for_month,                   
                   'Rainfall for year (in)':rainfall_for_year,
                   'Maximum rain per minute':max_rain_per_minute,                   
                   'Maximum temperature (°F)':max_temp,
                   'Minimum temperature (°F)':min_temp,
                   'Maximum humidity (%)':max_humidity,
                   'Minimum humidity (%)':min_humidity,
                   'Maximum pressure':max_pressure,
                   'Minimum pressure':min_pressure,                   
                   'Maximum windspeed (mph)':max_windspeed,
                   'Maximum gust speed (mph)':max_gustspeed,
                   'Maximum heat index (°F)':max_heatindex
                   })
df.set_index('datetime',inplace=True)
print(df.info())

mean = round(np.mean(df["2011-08-01":"2011-08-20"]["Average windspeed (mph)"]), 2)
print('-'*30)
print(mean)
print('-'*30)
#for col in df.columns:    
#    print(is_numeric_dtype(df[col][datetime.strptime('2018-Oct-28','%Y-%b-%d').date()]))
#    print(is_datetime64_dtype(df[col][datetime.strptime('2018-Oct-28','%Y-%b-%d').date()]))
    #print(col+'====='+str(df[col][datetime.strptime('2018-Oct-28','%Y-%b-%d').date()]))
#print(df['Maximum rain per minute'])    
#for c1 in df.columns:
    #print(c1+'====='+df[c1])
