def place_order(producer, order_id):
    producer.send("order-created", {"order_id": order_id})


def replay(other_producer, order_id):
    other_producer.send("order-created", {"order_id": order_id})
