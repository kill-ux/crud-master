from app.config import get_env_variable
import pika, json
from app.database import Session
from app.models import Orders

RABBITMQ_USERNAME = get_env_variable("RABBITMQ_USERNAME")
RABBITMQ_PASSWORD = get_env_variable("RABBITMQ_PASSWORD")
RABBITMQ_PORT = get_env_variable("RABBITMQ_PORT", int)
RABBITMQ_HOST = get_env_variable("RABBITMQ_HOST")
RABBITMQ_QUEUE = get_env_variable("RABBITMQ_QUEUE")


def callback(ch, method, properties, body):
    data = json.loads(body)
    session = Session()
    try:
        order = Orders(
            user_id=data["user_id"],
            number_of_items=data["number_of_items"],
            total_amount=data["total_amount"],
        )
        session.add(order)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    conn = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=pika.PlainCredentials(
                username=RABBITMQ_USERNAME, password=RABBITMQ_PASSWORD
            ),
        )
    )

    channel = conn.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True, arguments={"x-queue-type": "quorum"})

    channel.basic_consume(
        queue=RABBITMQ_QUEUE, on_message_callback=callback
    )
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
