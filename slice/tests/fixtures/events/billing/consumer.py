def start(consumer):
    consumer.subscribe("order-created")
