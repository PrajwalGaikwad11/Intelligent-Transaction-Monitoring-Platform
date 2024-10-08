# Intelligent Transaction Monitoring Platform

## Overview
This project implements an intelligent transaction monitoring platform focusing on real-time monitoring and fraud detection. It leverages Kafka for real-time data streaming, Spark for data processing, and an Isolation Forest model for fraud detection. The platform also includes a Flask app to display the results.

## Features
- Real-time transaction monitoring using Kafka.
- Fraud detection using an Isolation Forest model.
- Smooth data pipeline and real-time streaming.
- API integration using Flask.
- User-friendly web interface with color-coded transactions (red for fraud, green for normal).

## Prerequisites
- Python 3.8+
- Apache Kafka
- Apache Spark
- Scikit-learn
- Flask
- Pandas
- Confluent Kafka Python client

## Setup Instructions

### 1. Install Dependencies
First, install the necessary Python packages:
```bash
pip install confluent_kafka pandas scikit-learn flask joblib
```
### 2. Setup kafka
Download and setup kafka in your system
2.1 start zookeper
```bash
.\bin/zookeeper-server-start.sh config/zookeeper.properties
```
2.2 start kafka server
```bash
.\bin/kafka-server-start.sh config/server.properties
```
2.3 create kafka topic of your choice
```bash
bin/kafka-topics.sh --create --topic transactions --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```
### 3. Kafka Producer and Kafka Consumer
- Producer: Generates and Sends transaction data to the Kafka topic.
- Consumer: Reads transaction data from the Kafka topic and process it for model prediction.
### 4. Build An Isolation Forest Model Using Pyspark and Sk-learn
- Used PySpark to process the data and train the model for differentiating between fraud transaction data and normal transaction data.
- Save the model 
### 5. Build Flask App for displayig and monitoring the anamolies
- Data present at the consumer is feeded to the model for prediction and the results are displayed through flask app
- run the flask_app_script and see the results on 'http://localhost:5000/transactions'

