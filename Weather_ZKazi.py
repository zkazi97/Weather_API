"""
Python Assignment: Weather Forecast
Due September 5th, 2020
Zain Kazi
"""

#%% Import relevant packages
import pprint
import requests 
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import statistics as st
import datetime
from datetime import timedelta 
from collections import OrderedDict

#%% Read in Locations and Draw Data using API 

#Read in Location names
locationNames = [
'Anchorage, USA',
'Buenos Aires, Argentina',
'São José dos Campos, Brazil',
'San José, Costa Rica',
'Nanaimo, Canada',
'Ningbo, China',
'Giza, Egypt',
'Mannheim, Germany',
'Hyderabad, India',
'Tehran, Iran',
'Bishkek, Kyrgyzstan',
'Riga, Latvia',
'Quetta, Pakistan',
'Warsaw, Poland',
'Dhahran, Saudia Arabia',
'Madrid, Spain',
'Oldham, England']

#Create column names
categNames = []
rows = []
for x in range(5):
    minandmax = ["Min "+str(x+1),"Max "+str(x+1)]
    categNames=categNames+minandmax
categNames = [["City"] + categNames + ["Min Avg"] + ["Max Avg"]]

#Loop through each city's data
for locs in range(len(locationNames)):
    
    #Call API to pull city data
    api_key = '286331138561bf58e5a83321b563f742' 
    URL = 'https://api.openweathermap.org/data/2.5/forecast?' 
    URL = URL + 'q=' + locationNames[locs] +'&appid=' + api_key 
    response = requests.get( URL ) 
    
    if response.status_code == 200: 
        data = response.json() 
        printer = pprint.PrettyPrinter( width=80, compact=True ) 
        printer.pprint( data[ 'list' ][ 0 ] ) 
    else:
        print( 'Error:', response.status_code )
         
    #Define lists to store mins, maxs, and dates 
    l = data['list']
    mins = []
    maxs= []
    dates= []
    
    #Loop through next 40 observations 
    for day in range(len(data['list'])):
        date = datetime.datetime.strptime(l[day]['dt_txt'],
                                         '%Y-%m-%d %H:%M:%S').date()
       
        #Create list of daily mins and maxs
        todayinfo = l[day]['main']
        mins.append(round(todayinfo['temp_min']-273.15,2))
        maxs.append(round(todayinfo['temp_max']-273.15,2))
        dates.append(date)
    
    #Create dataframe and determine mins, maxs for dates and avg
    forecastDict = {'Location': locationNames[locs], 'dates':dates,'mins':mins, 'maxs':maxs}
    forecastFrame = pd.DataFrame(data = forecastDict)
    
    #Define daily mins/maxs
    dailyInfo = forecastFrame.groupby('dates').min().tail()
    dailyMaxs = forecastFrame.groupby('dates').max().tail()
    
    # Add info to dailyInfo and find min/max averages
    dailyInfo['maxs'] = dailyMaxs['maxs']
    dailyInfo['min_avg'] = round(dailyInfo['mins'].mean(),2)
    dailyInfo['max_avg'] = round(dailyInfo['maxs'].mean(),2)
    
    # Use last 5 obs for 5 days 
    forecast = dailyInfo.tail()
    forecast.index = range(len(forecast))
    row=pd.DataFrame({'City' : [locationNames[locs]]})
    rowinfo =[]
    
    #Loop through dataframe to store row info and append to row list
    for x,y in forecast.iterrows():
        r = [y.loc['mins'], y.loc['maxs']]
        rowinfo=rowinfo+r
    rowinfo = [locationNames[locs]] + rowinfo + [y.loc['min_avg']] + [y.loc['max_avg']]        
    rows.append(rowinfo)
    
#Create CSV from forecast dataframe
finalForecast = pd.DataFrame(rows,columns = categNames[0])
finalForecast.to_csv("forecast.csv",float_format='%.2f', index = False)

#Plot temp maxs and mins
sns.barplot(x = "Max Avg", y = "City", data = finalForecast, orient = 'h')
plt.title("Max Average Temperature Over Next 5 Days Forecasted in Celsius by City", fontsize = 8)
plt.figure()







