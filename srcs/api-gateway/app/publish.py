import pika, os

INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL")
BILLING_SERVICE_URL = os.getenv("BILLING_SERVICE_URL")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", int)
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")

def publish_message():
    conn = pika.BlockingConnection(
        pika.ConnectionParameters(
            RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=pika.PlainCredentials(
                username=RABBITMQ_USERNAME, password=RABBITMQ_PASSWORD
            ),
        )
    )
    channel = conn.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=RABBITMQ_QUEUE,
        body="""{
            "user_id": "3",
            "number_of_items": "5",
            "total_amount": "180"
        }""",
        properties=pika.BasicProperties(
            content_type="application/json", delivery_mode=2
        ),
    )
    print(" [x] Sent 'Hello World!'")
    conn.close()