from dotenv import load_dotenv

load_dotenv()
import pika
# from app import get_env_variable
import sys

# HOST = get_env_variable("BILLING_HOST")
# PORT = get_env_variable("BILLING_PORT")
# DEBUG = get_env_variable("BILLING_DEBUG").lower() in ("true", "1", "t")

# app = create_app()

# if __name__ == "__main__":
#     app.run(host=HOST,port=PORT,debug=DEBUG)


def main():
    conn = pika.BlockingConnection(
        pika.ConnectionParameters(
            credentials=pika.PlainCredentials(
                username="billing_user", password="billing_user"
            ),
        )
    )
    channel = conn.channel()
    channel.queue_declare(queue="hello", durable=True)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue="hello", auto_ack=True, on_message_callback=callback)
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit()
