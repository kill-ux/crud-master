from flask import Blueprint, request
import requests
import os

gateway_bp = Blueprint("gateway_bp", __name__)
INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL")
API_MOVIES_URL = "/api/movies"


@gateway_bp.route(API_MOVIES_URL + "/", methods=["GET", "POST", "DELETE"])
@gateway_bp.route(
    API_MOVIES_URL + "/<path:subpath>", methods=["GET", "POST", "PUT", "DELETE"]
)
def proxy_to_inventory(subpath=""):
    """Proxy endpoint to forward requests to the inventory service"""
    base_url = INVENTORY_SERVICE_URL.rstrip("/") + API_MOVIES_URL
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


import pika

conn = pika.BlockingConnection(pika.ConnectionParameters("192.168.56.11"))
channel = conn.channel()


@gateway_bp.route("/")
def sent():
    return {"status": "sent"}
