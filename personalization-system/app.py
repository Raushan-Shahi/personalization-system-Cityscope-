from flask import Flask, request
import json
from recommendation_model import SuggestedForYou,RecommendedForYou
from feature_extraction import RecommendedFeaturedContent
#import requests
#from flask import request

app = Flask(__name__)

@app.route('/')
def HelloWorld():
    print("Hi")
    return "Hi"

@app.route('/SuggestedForYou', methods=['POST'])
def SuggestedForYouContent():
    request_data = request.get_json()
    tagList = request_data['tags']
    print(tagList, "Hi again")
    recommendedContent = SuggestedForYou(tagList)
    if len(recommendedContent) == 0:
        print("No Recommended Content")
        raise "Empty List"
    else:
        return json.dumps(recommendedContent)

@app.route('/RecommendedForYou', methods=['POST'])
def RecommendedForYouContent():
    request_data = request.get_json()
    id = request_data['id']
    print(id, "Hi again")
    recommendedContent = []
    recommendedContent = RecommendedForYou(id)
    #print(recommendedContent)
    #if (len(recommendedContent) == 0):
    #    print("No Recommended Content")
    #    recommendedFeaturedContent = RecommendedFeaturedContent()
    #    return json.dumps(recommendedFeaturedContent)
    #    #raise Exception #as "Empty List"
    #else:
    return json.dumps(recommendedContent)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=True) #(debug= True)