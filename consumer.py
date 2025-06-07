import sys

import pika

# --- Configuration ---
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
EXCHANGE_NAME = 'message_exchange'
EXCHANGE_TYPE = 'topic' # We'll use a topic exchange for flexible routing
QUEUE_NAME = 'message_queue'

def connect_rabbitmq():
    """Establishes a connection to RabbitMQ."""
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
        )
        channel = connection.channel()
        print(f"[*] Connected to RabbitMQ at {RABBITMQ_HOST}:{RABBITMQ_PORT}")
        return connection, channel
    except pika.exceptions.AMQPConnectionError as e:
        print(e)
        print(f"Error connecting to RabbitMQ: {e}")
        sys.exit(1)


def consume_messages(queue_name):
    connection, channel = connect_rabbitmq()
    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, body):
        print(f"Received message: {body.decode()}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("Ack sent.")

    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    print(f"[*] Waiting for messages in '{queue_name}'. To exit press CTRL+C")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        if connection and connection.is_open:
            connection.close()
            print("Connection closed.")

if __name__ == "__main__":
    consume_messages(QUEUE_NAME)
