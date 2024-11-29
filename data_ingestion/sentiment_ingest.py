import googleapiclient.discovery
from textblob import TextBlob
from elasticsearch import Elasticsearch
import json
from flask import Flask, request, jsonify

# Flask app for API endpoint
app = Flask(__name__)

# YouTube API credentials
API_KEY = "AIzaSyDWXDVLvxb3lRGtN1reSXDZcV48M79-3rY"

# Elasticsearch connection (via HAProxy load balancer)
es = Elasticsearch("http://haproxy:5000")

# Search YouTube videos based on a keyword
def search_videos(keyword):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
    request = youtube.search().list(
        part="snippet",
        q=keyword,
        type="video",
        maxResults=5  # You can adjust the number of videos to fetch
    )
    response = request.execute()
    video_ids = [item["id"]["videoId"] for item in response.get("items", [])]
    return video_ids

# Get comments for a specific video ID
def get_comments(video_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100
    )
    response = request.execute()
    comments = [item["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for item in response.get("items", [])]
    return comments

# Analyze sentiment of comments
def analyze_sentiment(comment):
    analysis = TextBlob(comment)
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity == 0:
        return "neutral"
    else:
        return "negative"

@app.route('/analyze', methods=['POST'])
def analyze():
    keyword = request.json.get('keyword')
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    video_ids = search_videos(keyword)
    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}

    for video_id in video_ids:
        comments = get_comments(video_id)
        for comment in comments:
            sentiment = analyze_sentiment(comment)
            comment_data = {
                "video_id": video_id,
                "comment": comment,
                "sentiment": sentiment
            }
            es.index(index="youtube_sentiment", document=comment_data)
            sentiment_counts[sentiment] += 1

    return jsonify(sentiment_counts)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
