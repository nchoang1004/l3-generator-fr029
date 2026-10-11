# Source input for static analysis only; do not execute this sample.
import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda value: json.dumps(value).encode())

def place_order():
    producer.send('order-created', {'order_id': 1})
