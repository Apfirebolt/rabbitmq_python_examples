import pika
import sys

# --- Configuration ---
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
EXCHANGE_NAME = 'message_exchange'
EXCHANGE_TYPE = 'topic' # We'll use a topic exchange for flexible routing

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


# declare a new exchange with fanout type
def declare_exchange(exchange_name, exchange_type):
    connection = None
    try:
        # Establish a connection to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        try:
            # Try passive declare to check if exchange exists
            channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=exchange_type,
            passive=True
            )
            print(f"Exchange '{exchange_name}' already exists.")
        except pika.exceptions.ChannelClosedByBroker as e:
            pass

    except pika.exceptions.AMQPConnectionError as e:
        print(f"Failed to connect to RabbitMQ: {e}")
    except pika.exceptions.AMQPChannelError as e:
        print(f"Failed to declare exchange: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if connection and connection.is_open:
            connection.close()
            print("Connection closed.")


if __name__ == "__main__":
    declare_exchange('custom_exchange', 'fanout')