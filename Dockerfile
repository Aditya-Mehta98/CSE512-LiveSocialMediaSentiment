# Stage 1: Python Environment
FROM python:3.12 as python-env

WORKDIR /app

# Copy the data ingestion script
COPY ./data_ingestion/sentiment_ingest.py /app/sentiment_ingest.py

# Install required Python packages
RUN pip install google-api-python-client textblob elasticsearch flask

# Run the Python ingestion script
CMD ["python", "sentiment_ingest.py"]
