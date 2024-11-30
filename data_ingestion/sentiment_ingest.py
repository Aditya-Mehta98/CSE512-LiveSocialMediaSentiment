import googleapiclient.discovery
import pymongo
import spacy
from textblob import TextBlob
from elasticsearch import Elasticsearch
from flask import Flask, request, jsonify, render_template
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# MongoDB connection
mongo_client = pymongo.MongoClient("mongodb://mongodb:27017/")
db = mongo_client["video_analysis"]
queries_collection = db["queries"]

# Elasticsearch connection
es = Elasticsearch("http://elasticsearch:9200")

# YouTube API Key (provided by user)
API_KEY = "AIzaSyDWXDVLvxb3lRGtN1reSXDZcV48M79-3rY"
nlp = spacy.load("en_core_web_sm")

# Search YouTube for video data and check MongoDB cache
def get_video_data(keyword):
    keyword_lower = keyword.lower()
    existing_data = queries_collection.find_one({"keyword": keyword_lower})
    
    if existing_data:
        return existing_data["video_details"]

    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
    # Change maxResults to 50 to get 50 videos for analysis
    request = youtube.search().list(part="snippet", q=keyword, type="video", maxResults=50)
    response = request.execute()

    video_details = []
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        description = item["snippet"].get("description", "")

        # Get popularity metrics
        video_request = youtube.videos().list(part="statistics", id=video_id)
        video_response = video_request.execute()
        video_stats = video_response["items"][0]["statistics"]
        popularity_metrics = {
            "view_count": video_stats.get("viewCount"),
            "like_count": video_stats.get("likeCount"),
            "comment_count": video_stats.get("commentCount")
        }

        # Store video metadata
        video_details.append({
            "video_id": video_id,
            "title": title,
            "url": video_url,
            "description": description,
            "popularity_metrics": popularity_metrics
        })

    # Store in MongoDB
    queries_collection.insert_one({
        "keyword": keyword_lower,
        "query_time": datetime.now().isoformat(),
        "video_details": video_details
    })

    return video_details

# Extract entities from video descriptions
def extract_entities(description):
    doc = nlp(description)
    entities = []
    for ent in doc.ents:
        if ent.label_ in [
            "ORG", "PRODUCT", "BRAND", "PERSON", "GPE", "LOC", "EVENT", "WORK_OF_ART", "LANGUAGE",
            "DATE", "TIME", "MONEY", "PERCENT", "CARDINAL"
        ]:
            entities.append(ent.text)
    return list(set(entities))


# Enhanced Analyze sentiments in comments or description
def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0.75:
        return "strongly positive"
    elif analysis.sentiment.polarity > 0.25:
        return "positive"
    elif analysis.sentiment.polarity > -0.25:
        return "neutral"
    elif analysis.sentiment.polarity > -0.75:
        return "negative"
    else:
        return "strongly negative"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze_video', methods=['POST'])
def analyze_video():
    try:
        keyword = request.json.get('keyword')
        if not keyword:
            return jsonify({"error": "Keyword is required"}), 400

        # Fetch video details, either from MongoDB or from YouTube API
        video_details = get_video_data(keyword)

        analyzed_data = []
        for video in video_details:
            sentiment = analyze_sentiment(video["description"])
            entities = extract_entities(video["description"])
            video["sentiment"] = sentiment
            video["entities"] = entities

            # Add current timestamp to avoid duplicate Elasticsearch entries on reanalysis
            video["timestamp"] = datetime.now().isoformat()
            es.index(index="youtube_sentiment", document=video)
            analyzed_data.append(video)

        return jsonify({
            "analyzed_data": analyzed_data[:10],
            "summary_data": analyzed_data
        })
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
