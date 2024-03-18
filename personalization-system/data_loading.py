import sys,os
import json
import requests
import pandas as pd
import numpy as np
from datetime import datetime, date
import matplotlib.pyplot as plt
import re
import random
from data_preprocessing import TimeCleaning, TagsCleaning



def ExperienceData(headers):
    try:
        experience_response = requests.get('http://api2.cityscope.media/experiences?limit=1000',headers = headers)
        experiences = experience_response.json()['data']
        experiences = pd.DataFrame(experiences)
        experiences = TimeCleaning(experiences)
        for i in range(0, experiences.shape[0]):
            
            # Start and end field date conversion
            if(pd.isna(experiences.iloc[i]['startCsExp']) == False):
                experiences.at[i, 'startCsExp'] = datetime.strptime(experiences.iloc[i]['startCsExp'][:10], '%Y-%m-%d').date()
            if(pd.isna(experiences.iloc[i]['endCsExp']) == False):
                experiences.at[i, 'endCsExp'] = datetime.strptime(experiences.iloc[i]['endCsExp'][:10], '%Y-%m-%d').date()
            
            #removing start end missing values
            if(pd.isna(experiences.iloc[i]['classification'])):
                experiences.iloc[i]['classification'] = {'name': '', 'id':''}
        

        #Cleaning Classification Column
        explodedExperience = experiences['classification'].apply(pd.Series)
        explodedExperience.rename(columns = {'name':'classification_Name', 'id':'classification_id'}, inplace=True)
        experiences = pd.concat([experiences.drop('classification', axis = 1), explodedExperience],axis=1)

        #Only taking data which is Active
        experiences = experiences[experiences['isActive'] == True]
        experiences = TagsCleaning(experiences)
        return experiences.copy()
    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error in Experience Data Function", e, exc_tb.tb_lineno)
        return e


def ArticlesData(headers):
    try:
        article_response = requests.get('http://api2-dev.cityscope.media/articles?limit=10000',headers = headers)
        articles = article_response.json()['data']
        articles = pd.DataFrame(articles)
        articles = TimeCleaning(articles)
        articles = TagsCleaning(articles)
        return articles.copy()
    except Exception as e:
        print("Error in Articles Data Function", e)
        return e
    

if __name__ == '__main__':
    c = ExperienceData({'chocco':'banna'})
    print(c['classification_Name'].isna())
