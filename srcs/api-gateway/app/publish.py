import pika, os, json
from flask import  request

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
    channel.queue_declare(
        queue=RABBITMQ_QUEUE, durable=True, arguments={"x-queue-type": "quorum"}
    )
    data = request.get_json()
    channel.basic_publish(
        exchange="",
        routing_key=RABBITMQ_QUEUE,
        body=json.dumps({
            'user_id': data['user_id'],
            'number_of_items': data['number_of_items'],
            'total_amount': data['total_amount'],
        }),
        properties=pika.BasicProperties(content_type="application/json"),
    )
    print(" [x] Sent 'Hello World!'")
    conn.close()
