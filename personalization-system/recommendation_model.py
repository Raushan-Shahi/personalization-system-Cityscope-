from __future__ import division
import traceback
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
from data_preprocessing import TextCleaning
from feature_extraction import FinalData, RecommendedFeaturedContent, TagsList

# Cache to store computed results
cache = {}

def TagsScore(df, tags, cosine_sim, indexDict):
    try:
        Tags = TagsList(df)

        for i in range(0, df.shape[0]):
            indexDict[i] = len(set(tags) & set(df.iloc[i]['Tags'])) / float(
                len(set(tags) | set(df.iloc[i]['Tags']))) * 100

        sorted_dt = {key: value for key, value in sorted(indexDict.items(), key=lambda item: item[1], reverse=True)}
        sorted_dt = {key: value for key, value in sorted_dt.items() if value != 0.0}

        for i in sorted_dt.keys():
            sorted_dt[i] = sorted(list(enumerate(cosine_sim[i])), key=lambda x: x[1], reverse=True)[0:20]

        return sorted_dt

    except Exception as e:
        print("Error in Tags Score Function", e)
        return e





# Suggested for you section
def SuggestedForYou(tags):
    try:
        # Check if results are already computed for given tags
        if tuple(tags) in cache:
            return cache[tuple(tags)]

        final_list = []
        df = FinalData()
        df = TextCleaning(df)

        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['New Text'])
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        tagScore_dt = TagsScore(df, tags, cosine_sim, dict.fromkeys(df.index, None))

        for keys in tagScore_dt.keys():
            for i in range(0, len(tagScore_dt[keys])):
                if (df.iloc[tagScore_dt[keys][i][0]]['title'] not in final_list and tagScore_dt[keys][i][1] != 0.0):
                    final_list.append(df.iloc[tagScore_dt[keys][i][0]]['title'])

        # Store computed results in cache
        cache[tuple(tags)] = final_list

        return final_list

    except Exception as e:
        print("Error in SuggestedForYou Function", e)
        return e

# Recommended for you section
def RecommendedForYou(id):
    try:
        # Check if results are already computed for given ID

        final_list = []
        new_sim_scores = []
        df = FinalData()
        df = TextCleaning(df)

        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['New Text'])
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        indices = pd.Series(df.index, index=df['id']).drop_duplicates()

        if id in indices.index:
            idx = indices[id]
            sim_scores = list(enumerate(cosine_sim[idx]))

            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            new_sim_scores = [i for i in sim_scores if i[1] != 0 and df['City Name'].iloc[i[0]] == df['City Name'].iloc[sim_scores[0][0]]]
            new_sim_scores = new_sim_scores[1:21]

            content_indices = [i[0] for i in new_sim_scores]

            recommendedContent = []
            for i in content_indices:
                recommendedContent.append((df['id'].iloc[i], df['classification_Name'].iloc[i]))

            # Store computed results in cache
            cache[id] = recommendedContent

            return recommendedContent

        else:
            print("Recommending Featured Content")
            recommendedFeaturedContent = RecommendedFeaturedContent()

            # Store computed results in cache
            cache[id] = recommendedFeaturedContent

            return recommendedFeaturedContent

    except Exception as e:
        print("Error in RecommendedForYou Function", e, traceback.format_exc())
        return e

if __name__ == '__main__':
    tags = ['Sports', 'Adventure', 'Workshop', 'Startups', 'Fitness', 'Food', 'Covid-19', 'Gaming', 'Getaways', 'Environment']
    print(SuggestedForYou(tags))
    print("Recommended Content")
    title = "Key health schemes to take note of in Rajasthan"
    print(RecommendedForYou(title))
