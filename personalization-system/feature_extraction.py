from random import sample
from data_loading import ExperienceData, ArticlesData
#from bin.data_preprocessing import TagsCleaning
import pandas as pd
import os, sys



def FinalData():
    try:
        headers = {'chocco':'banna'}
        experiences = ExperienceData(headers)
        articles = ArticlesData(headers)
        #articles = TagsCleaning(articles)
        #experiences = TagsCleaning(experiences)
        

        #Creating Duration Column
        for i in range(0, experiences.shape[0]):
            if(pd.isna(experiences.iloc[i]['startCsExp']) == False and pd.isna(experiences.iloc[i]['endCsExp']) == False):
                experiences.at[i,'Duration'] = experiences.iloc[i]['endCsExp'] - experiences.iloc[i]['startCsExp']
            else:
                experiences.at[i,'Duration'] = ''
        

        #Creating classification_Name and pricePerPass columns
        articles['classification_Name'] = 'Articles'
        articles['pricePerPass'] = 0


        #Dropping Columns
        articles.drop(['city','tags','status','media'], axis=1, inplace=True)
        experiences.drop(['city','tags','whatsIncluded','hostImage',
                          'hostDescription','bookingUrl','rating','classification_id',
                          'slots','venue','accessibility','whatsNotIncluded','offers',
                          'minPeopleRequired','startCsExp','endCsExp','vendorAccountId','vendorAmount'], axis=1, inplace=True)


        #Renaming Columns
        articles.rename(columns = {'author':'Author/Host','timeToRead':'Experiences Duration/Article Reading Time'}, inplace=True)
        experiences.rename(columns={'longDescription':'content','coverMedia':'coverImage',
                                    'adminHost':'Author/Host','Duration':'Experiences Duration/Article Reading Time'},inplace=True)
        

        #FinalDataCleaning(articles,experiences)
        df = pd.concat([articles,experiences]).sort_values(by = 'updatedAt')#.reset_index(inplace=True)
        #print(df)
        df_copy = FinalDataCleaning(df)

        #Returning merged data
        return df_copy
    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error in Final Data Function", e, exc_tb.tb_lineno)
        return e





def FinalDataCleaning(df):
    try:
        df_copy = df.copy()
        df_copy.reset_index(inplace=True)
        df_copy['Tags2'] = df_copy['Tags']

        for i in range(0, df_copy.shape[0]):
            #print(df_copy2.iloc[i]['Tags'])
            #print("Hello", df_copy.iloc[i]['Tags'], df_copy.iloc[i]['Tags2'], i)
            df_copy.at[i, 'Tags2'] = tuple(df.iloc[i]['Tags'])
        return df_copy

    except Exception as e:
        print("Error in Final Data Cleaning Function", e)
        return e

    
def TagsList(df):
    try:
        Tags = []
        for i in range(0, df.shape[0]):
            for j in df.iloc[i]['Tags']:
                if j not in Tags:
                    Tags.append(j)
        return Tags
    
    except Exception as e:
        print("Error in Tag List Function", e)
        return e
    

def RecommendedFeaturedContent():
    try:
        recommendedContent = []
        df = FinalData()
        df = df[df['isFeatured'] == True]
        df = df.sample(n=30)
        #print([df['title'].values[0]])
        #print(df['title'])
        #indexList = df.index
        #print(indexList)
        for i in range(0, df.shape[0]):
            #print(i)
            #print(df['title'].iloc[i])
            recommendedContent.append((df['id'].iloc[i], df['classification_Name'].iloc[i]))
        return recommendedContent #[df['title'].iloc[:]]

    except Exception as e:
        print("Error in RecommendedFeaturedContent", e)
        return e




if(__name__ == '__main__'):
    test = RecommendedFeaturedContent()
    print(test)
