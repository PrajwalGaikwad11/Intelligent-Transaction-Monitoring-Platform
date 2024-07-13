from confluent_kafka import Producer
import random
import time
import json

# Kafka broker configuration
bootstrap_servers = 'localhost:9092'
topic = 'transactions'

# Function to generate sample transaction data
def generate_transaction():
    transaction_id = random.randint(1, 1000)
    amount = round(random.uniform(10.0, 1000.0), 2)
    timestamp = int(time.time() * 1000)  # current timestamp in milliseconds

    transaction = {
        'transaction_id': transaction_id,
        'amount': amount,
        'timestamp': timestamp
    }
    return transaction

# Kafka producer configuration
conf = {
    'bootstrap.servers': bootstrap_servers,
}

# Create Kafka producer
producer = Producer(conf)

# Produce sample transaction data to Kafka topic
try:
    while True:
        transaction_data = generate_transaction()
        # Convert transaction_data to JSON string before producing
        json_data = json.dumps(transaction_data)
        producer.produce(topic, key=str(transaction_data['transaction_id']), value=json_data)
        producer.flush()
        print(f"Produced: {json_data}")
        time.sleep(1)  # simulate delay between transactions
except KeyboardInterrupt:
    pass
finally:
    producer.flush()  # Ensure all messages are delivered
