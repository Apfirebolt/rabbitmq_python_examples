import time

import pika

EXCHANGE_NAME = "fanout_example"
QUEUE_NAMES = ["slow", "medium", "fast"]
DLX_EXCHANGE_NAME = "dlx_exchange"
DLX_QUEUE_NAME = "dlx_queue"

MESSAGES = [
    "Hello, World!",
    "This is a test message.",
    "RabbitMQ is great for messaging.",
    "Fanout exchanges broadcast messages to all queues.",
    "Dead-letter exchanges handle unacknowledged messages.",
]

# Setup connection and channel\
# login with a different user if needed
connection_params = pika.ConnectionParameters(
    host="localhost",
    port=5672,
    virtual_host="/",
    credentials=pika.PlainCredentials("aspper", "pass12345"),
)
# connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Declare fanout exchange
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="fanout")

# Declare and bind queues
for queue in QUEUE_NAMES:
    channel.queue_declare(queue=queue, durable=True)
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue)

# Publish messages
for msg in MESSAGES:
    channel.basic_publish(exchange=EXCHANGE_NAME, routing_key="", body=msg)
    print(f"Sent: {msg}")


def slow_consumer(queue_name):
    print(f"\nConsuming from {queue_name} with a slow consumer:")
    for method_frame, properties, body in channel.consume(
        queue=queue_name, inactivity_timeout=1
    ):
        if method_frame:
            print(f"  Received: {body.decode()}")
            time.sleep(2)  # Simulate slow processing
            channel.basic_ack(method_frame.delivery_tag)
        else:
            break
    # Cancel the consumer and requeue unacknowledged messages
    channel.cancel()


def medium_consumer(queue_name):
    print(f"\nConsuming from {queue_name} with a medium consumer:")
    for method_frame, properties, body in channel.consume(
        queue=queue_name, inactivity_timeout=1
    ):
        if method_frame:
            print(f"  Received: {body.decode()}")
            time.sleep(1)  # Simulate medium processing
            channel.basic_ack(method_frame.delivery_tag)
        else:
            break
    # Cancel the consumer and requeue unacknowledged messages
    channel.cancel()


def fast_consumer(queue_name):
    print(f"\nConsuming from {queue_name} with a fast consumer:")
    for method_frame, properties, body in channel.consume(
        queue=queue_name, inactivity_timeout=1
    ):
        if method_frame:
            print(f"  Received: {body.decode()}")
            channel.basic_ack(method_frame.delivery_tag)
        else:
            break
    # Cancel the consumer and requeue unacknowledged messages
    channel.cancel()


# Function to consume all messages from a queue
def consume_all(queue_name):
    # slow consumer
    if queue_name == "slow":
        slow_consumer(queue_name)
    # medium consumer
    elif queue_name == "medium":
        medium_consumer(queue_name)
    # fast consumer
    elif queue_name == "fast":
        fast_consumer(queue_name)
    else:
        print(f"Unknown queue: {queue_name}")


# Give RabbitMQ a moment to route messages
time.sleep(1)

# Read messages from all queues
for queue in QUEUE_NAMES:
    consume_all(queue)

channel.close()
connection.close()
