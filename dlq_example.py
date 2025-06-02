import pika
import time

EXCHANGE_NAME = "example_fanout_exchange"
QUEUE_NAMES = ["fanout_one", "fanout_two", "fanout_three"]

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
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key="",
        body=msg,
        properties=pika.BasicProperties(expiration="3000")  # expiration in ms
    )
    print(f"Sent: {msg}")


def fast_consumer(queue_name):
    print(f"\nConsuming from {queue_name} with a fast consumer:")
    # Check if the queue has any messages before consuming
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
            # print acknowledgment
            print(f"  Acknowledged message with delivery tag: {method_frame.delivery_tag}")
        else:
            break
    # Cancel the consumer and requeue unacknowledged messages
    channel.cancel()


# Function to consume all messages from a queue
def consume_all(queue_name):
    # slow consumer
    fast_consumer(queue_name)


# Give RabbitMQ a moment to route messages
time.sleep(1)

# Read messages from all queues
for queue in QUEUE_NAMES:
    consume_all(queue)

# --- Cleanup ---
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
