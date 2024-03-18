import json
import requests
import pandas as pd
import numpy as np
from datetime import datetime, date
import matplotlib.pyplot as plt
import re
import random
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')


def TimeCleaning(data):

    try:
        #Cleaning dates
        #Formatting the dates
        for i in range(0, data.shape[0]):
            data.at[i, 'createdAt'] = datetime.strptime(data.iloc[i]['createdAt'][:10], '%Y-%m-%d').date()
            data.at[i, 'updatedAt'] = datetime.strptime(data.iloc[i]['updatedAt'][:10], '%Y-%m-%d').date()

        #Converting string to datetime
        data['createdAt'] = pd.to_datetime(data['createdAt'])
        data['updatedAt'] = pd.to_datetime(data['updatedAt'])

        #Sorting according to recently updated
        data.sort_values(by = 'updatedAt')
        return data

    except Exception as e:
        print("Error in Time Cleaning Function", e)
        return e



def TagsCleaning(data):
    try:
        data['Tags']=[list() for x in range(len(data.index))]

        #Cleaning tags and city column
        for i in range(0, data.shape[0]):
            data.at[i, 'City Name'] = data.iloc[i]['city']['name']
            for j in range(0, len(data.iloc[i]['tags'])):
                #if experiences_final.iloc[i]['tags'][j]['name'] not in experiences_final.iloc[i]['Tags']:
                data.iloc[i]['Tags'].append(data.iloc[i]['tags'][j]['name'])
        return data
    except Exception as e:
        print("Error in Tags Cleaning Function", e)
        return e



def TextCleaning(data):
    try:
        newText = []
        for i in range(0, data.shape[0]):
            #print(df.iloc[i]['content'])
            #print(type(df_copy.iloc[i]['content']))
            if(data.iloc[i]['content'] != [] and type(data.iloc[i]['content']) != float):
                #print(df.iloc[i]['content'])
                newText.append(BeautifulSoup(data.iloc[i]['content']).get_text())
                data.at[i, 'New Text'] = BeautifulSoup(data.iloc[i]['content']).get_text().replace('\n','').replace('\xa0','')
            else:
                data.at[i, 'New Text'] = ' '
        return data
    
    except Exception as e:
        print("Error in Text Cleaning Function", e)
        return e