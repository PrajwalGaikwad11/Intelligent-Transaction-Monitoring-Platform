from flask import Flask, jsonify, render_template
from confluent_kafka import Consumer, KafkaException, KafkaError
import json
import joblib
import pandas as pd
from threading import Thread

app = Flask(__name__)

# Load the trained Isolation Forest model
model_path = "C:/Users/prajw/OneDrive/Documents/Assignment5/isolation_forest_model.pkl"
model = joblib.load(model_path)

# Kafka consumer configuration
bootstrap_servers = 'localhost:9092'
group_id = 'transaction-monitoring-group'
topic = 'transactions'

# Kafka consumer configuration
conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe([topic])

transactions = []

def consume_transactions():
    global transactions
    try:
        while True:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise KafkaException(msg.error())

            transaction_data = json.loads(msg.value().decode('utf-8'))
            transformed_data = transform_data(transaction_data)
            prediction = model.predict(transformed_data)

            result = {
                'transaction': transaction_data,
                'fraud': True if prediction[0] == -1 else False
            }

            transactions.append(result)
            transactions = transactions[-60:]  # Keep only the last 60 transactions
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

def transform_data(transaction):
    data = {'transaction_id': [transaction['transaction_id']], 'amount': [transaction['amount']]}
    return pd.DataFrame(data)

@app.route('/transactions', methods=['GET'])
def get_transactions():
    return render_template('transactions.html', transactions=transactions)

if __name__ == '__main__':
    thread = Thread(target=consume_transactions)
    thread.start()
    app.run(host='0.0.0.0', port=5000)
