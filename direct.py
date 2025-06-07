import random
import time

import pika

EXCHANGE_NAME = "example_direct_exchange"
QUEUE_NAMES = ["direct_one", "direct_two", "direct_three"]
ROUTING_KEYS = ["key_one", "key_two", "key_three"]

MESSAGES = [
    "Hello, World!",
    "This is a test message.",
    "RabbitMQ is great for messaging.",
    "Direct exchanges route messages by key.",
    "Dead-letter exchanges handle unacknowledged messages.",
]

connection_params = pika.ConnectionParameters(
    host="localhost",
    port=5672,
    virtual_host="/",
    credentials=pika.PlainCredentials("aspper", "pass12345"),
)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Declare direct exchange
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="direct")

# Declare and bind queues with routing keys
for queue, routing_key in zip(QUEUE_NAMES, ROUTING_KEYS, strict=False):
    channel.queue_declare(queue=queue, durable=True)
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue, routing_key=routing_key)


# randomly select a queue and routing key for publishing
for message in MESSAGES:
    queue = random.choice(QUEUE_NAMES)
    routing_key = ROUTING_KEYS[QUEUE_NAMES.index(queue)]
    print(f"\nPublishing to {queue} with routing key '{routing_key}': {message}")
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=routing_key,
        body=message,
    )
    print(f"Sent to {queue} with routing key '{routing_key}': {message}")

def fast_consumer(queue_name):
    print(f"\nConsuming from {queue_name} with a fast consumer:")
    queue_state = channel.queue_declare(queue=queue_name, passive=True)
    if queue_state.method.message_count == 0:
        print(f"  No messages to consume from {queue_name} (possibly expired).")
        return

    for method_frame, properties, body in channel.consume(
        queue=queue_name, inactivity_timeout=1
    ):
        time.sleep(1)
        if method_frame:
            print(f"  Received: {body.decode()}")
            channel.basic_ack(method_frame.delivery_tag)
            print(f"  Acknowledged message with delivery tag: {method_frame.delivery_tag}")
        else:
            break
    channel.cancel()

def consume_all(queue_name):
    fast_consumer(queue_name)

time.sleep(1)

for queue in QUEUE_NAMES:
    consume_all(queue)

print("\n--- Cleaning up RabbitMQ entities ---")
for queue in QUEUE_NAMES:
    try:
        channel.queue_delete(queue=queue)
        print(f"Deleted queue: {queue}")
    except pika.exceptions.ChannelClosedByBroker:
        print(f"Queue {queue} already deleted or empty during cleanup.")
try:
    channel.exchange_delete(exchange=EXCHANGE_NAME)
    print(f"Deleted exchange: {EXCHANGE_NAME}")
except pika.exceptions.ChannelClosedByBroker:
    print(f"Exchange {EXCHANGE_NAME} already deleted or empty during cleanup.")

channel.close()
connection.close()
print("\nConnection closed.")
