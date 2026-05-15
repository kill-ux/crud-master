import pika
import json
from .models import db, Order

def start_order_consumer(app):
    """Background worker to consume order messages from RabbitMQ"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=app.config['RABBITMQ_HOST']))
    channel = connection.channel()
    channel.queue_declare(queue=app.config['RABBITMQ_QUEUE'], durable=True)

    def callback(ch, method, properties, body):
        with app.app_context():
            data = json.loads(body)
            # Create the order in the Billing DB
            new_order = Order(user_id=data['user_id'], movie_id=data['movie_id'])
            db.session.add(new_order)
            db.session.commit()
            print(f" [x] Order recorded for User {data['user_id']}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=app.config['RABBITMQ_QUEUE'], on_message_callback=callback)
    channel.start_consuming()