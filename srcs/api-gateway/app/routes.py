from flask import Blueprint, request, jsonify
import requests
import os
import pika
import json

from app import get_env_variable

gateway_bp = Blueprint("gateway_bp", __name__)

INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL")
BILLING_SERVICE_URL = os.getenv("BILLING_SERVICE_URL")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")

API_MOVIES_URL = "/api/movies"
API_ORDERS_URL = "/api/orders"


@gateway_bp.route(
    API_MOVIES_URL + "/", methods=["GET", "POST", "DELETE"]
)
@gateway_bp.route(
    API_MOVIES_URL + "/<path:subpath>", methods=["GET", "POST", "PUT", "DELETE"]
)
def proxy_to_inventory(subpath=""):
    """Proxy endpoint to forward requests to the inventory service"""
    base_url = INVENTORY_SERVICE_URL.rstrip('/') + API_MOVIES_URL
    forwarded_url = f"{base_url}/{subpath}" if subpath else base_url

    try:
        resp = requests.request(
            method=request.method,
            url=forwarded_url,
            json=request.get_json() if request.is_json else None,
            params=request.args,
            headers={k: v for k, v in request.headers if k.lower() != "host"},
            cookies=request.cookies,
            allow_redirects=False,
        )

        excluded_headers = {
            "content-encoding",
            "content-length",
            "transfer-encoding",
            "connection",
        }
        
        headers = [
            (k, v)
            for k, v in resp.raw.headers.items()
            if k.lower() not in excluded_headers
        ]

        return resp.content, resp.status_code, headers
    except requests.exceptions.ConnectionError as e:
        print(f"Error connecting to inventory service: {e}")
        return {"error": "Inventory service is down"}, 503


# --- BILLING ROUTES ---
@gateway_bp.route(API_ORDERS_URL + "/", methods=["GET"])
def proxy_to_billing():
    """Directly proxy GET requests to the Billing Service"""
    forwarded_url = BILLING_SERVICE_URL.rstrip('/') + API_ORDERS_URL
    
    try:
        resp = requests.get(forwarded_url, params=request.args)
        return resp.content, resp.status_code
    except requests.exceptions.ConnectionError:
        return {"error": "Billing service is down"}, 503


@gateway_bp.route(API_ORDERS_URL + "/", methods=["POST"])
def queue_order():
    """Send POST requests to RabbitMQ for asynchronous processing"""
    if not RABBITMQ_HOST:
        return {"error": "RabbitMQ host not configured"}, 500

    try:
        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        
        # Ensure the queue exists
        channel.queue_declare(queue='order_queue', durable=True)
        
        # Publish the message
        message = request.get_json()
        channel.basic_publish(
            exchange='',
            routing_key='order_queue',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
        connection.close()
        return {"message": "Order request accepted"}, 202
        
    except Exception as e:
        print(f"RabbitMQ Error: {e}")
        return {"error": "Could not queue order"}, 503