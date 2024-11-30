# Stage 1: Python Environment
FROM python:3.12 as python-env

WORKDIR /app

# Copy the data ingestion script
COPY ./data_ingestion/sentiment_ingest.py /app/sentiment_ingest.py

# Organize UI files in a way Flask can easily find them
RUN mkdir templates static

COPY ./ui/index.html /app/templates/index.html
COPY ./ui/style.css /app/static/style.css
COPY ./ui/app.js /app/static/app.js

# Install required Python packages
RUN pip install google-api-python-client textblob elasticsearch flask pymongo spacy torch torchvision pyvim

# Download the spaCy model needed
RUN python -m spacy download en_core_web_sm

# Run the Python ingestion script
CMD ["python", "sentiment_ingest.py"]
