# Source input for static analysis only; do not execute this sample.
import json
from kafka import KafkaConsumer

consumer = KafkaConsumer('order-created', bootstrap_servers='kafka:9092', value_deserializer=json.loads)
