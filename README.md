# CSE512-LiveSocialMediaSentiment

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/Aditya-Mehta98/CSE512-LiveSocialMediaSentiment)

## Overview

CSE512-LiveSocialMediaSentiment is an advanced system designed for sentiment analysis and video metadata retrieval using the YouTube API. The project extracts video data based on user-supplied keywords, conducts a thorough analysis of the content, and displays the sentiment analysis results via a Flask-based web interface. It integrates MongoDB, Elasticsearch, and Kibana to create a distributed data system (DDS) for efficient data indexing, querying, and visualization.

## Features

- **YouTube Video Search**: Retrieves metadata for up to 50 YouTube videos corresponding to a specific keyword.
- **Sentiment Analysis**: Utilizes TextBlob to classify video descriptions into categories: Positive, Neutral, Negative, Strongly Positive, and Strongly Negative.
- **Entity Extraction**: Uses spaCy to identify key entities such as brands, products, and organizations from video descriptions.
- **Efficient Data Management**: Caches video metadata in MongoDB to reduce redundant API calls and improve retrieval performance.
- **Distributed Search & Indexing**: Indexes the sentiment analysis results in Elasticsearch, enabling scalable querying.
- **Visualization**: Employs pie charts in the web UI to represent sentiment trends and uses Kibana for advanced data visualization.
- **Interactive Dashboard**: A user-friendly web interface developed with Flask and Bootstrap, offering a simple interaction flow and intuitive data visualization.

## Technologies Used

- **Flask**: A Python micro web framework to serve the web application.
- **YouTube API**: Extracts video data based on user-provided keywords.
- **MongoDB**: A NoSQL database used to cache video metadata, reducing redundant requests to the YouTube API and optimizing data retrieval.
- **Elasticsearch**: A distributed search and analytics engine used for indexing and querying the analyzed data.
- **Kibana**: Visualization tool to gain insights from data indexed in Elasticsearch.
- **spaCy**: An NLP library used for named entity recognition (NER).
- **TextBlob**: Python library for performing sentiment analysis on textual data.
- **Chart.js**: JavaScript library to generate dynamic pie charts for sentiment visualization.

## Project Structure

- `data_ingestion/sentiment_ingest.py`: Contains the core logic for fetching YouTube video data, conducting sentiment analysis, extracting entities, and indexing data.
- `ui/index.html`: Defines the user interface, allowing users to input keywords and visualize analysis outcomes.
- `ui/style.css`: Custom CSS to enhance the UI appearance.
- `ui/app.js`: JavaScript responsible for managing UI interactions, AJAX requests, and rendering dynamic content.
- `docker-compose.yml`: Docker configuration file to set up and orchestrate Flask, MongoDB, Elasticsearch, and Kibana containers.
- `Dockerfile`: Configuration for setting up the Python environment and running the Flask application within a Docker container.

## Setup Instructions

### Prerequisites

- Docker
- Docker Compose
- Python 3.8+

### Running the Project

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Aditya-Mehta98/CSE512-LiveSocialMediaSentiment.git
   cd CSE512-LiveSocialMediaSentiment
   ```

2. **Set up API Keys**
   - Replace the `API_KEY` variable in `sentiment_ingest.py` with your YouTube Data API Key.

3. **Build and Start Docker Containers**
   ```bash
   docker-compose up --build
   ```

   This command will build and start containers for the Flask server, MongoDB, Elasticsearch, and Kibana.

4. **Access the Application**
   - **Web Application**: Navigate to `http://localhost:5000` in your web browser to interact with the sentiment analysis dashboard.
   - **Kibana Dashboard**: Access `http://localhost:5601` to visualize data using Kibana.

5. **MongoDB Access**
   - Connect to the MongoDB instance using MongoDB Compass or any other client via the connection string: `mongodb://localhost:27017/`.

### Usage

- Enter a **keyword** (e.g., "cosmetics") in the web interface.
- Click the **Analyze Video** button to analyze the top 50 videos related to the keyword.
- View sentiment analysis, detected entities, and video popularity metrics in the dashboard.
- Sentiment analysis is visually represented in a pie chart summarizing the distribution for all **50 videos**, while detailed results for only the top **10 videos** are displayed.

### Cleaning the Database

To clear all data from MongoDB, run the following command in the Docker environment:
```bash
docker exec -it <mongodb_container_name> mongo video_analysis --eval "db.queries.remove({})"
```
Replace `<mongodb_container_name>` with the name of your MongoDB container (typically `cse512-livesocialmediasentiment-mongodb`).

## Components of a Distributed Data System (DDS)

This project integrates multiple components typical of a Distributed Data System (DDS):

1. **Data Storage & Querying**
   - **MongoDB**: Stores metadata for each video, enabling efficient retrieval and serving as a caching layer to reduce redundant API calls to YouTube.
2. **Data Fragmentation**
   - **MongoDB and Elasticsearch**: MongoDB stores the video metadata, while Elasticsearch indexes the analysis results. This separation allows effective data fragmentation across storage engines, enhancing scalability and performance.
3. **Data Indexing & Search**
   - **Elasticsearch**: Provides powerful indexing and complex querying, facilitating efficient access to sentiment analysis results and supporting large-scale analysis requirements.
4. **Data Visualization**
   - **Kibana**: Allows visualization of indexed data from Elasticsearch for intuitive analysis.
   - **Chart.js**: Utilized in the front-end to produce interactive pie charts, providing a clear overview of sentiment distributions.
