from dotenv import load_dotenv
load_dotenv()

import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("API_GATEWAY_PORT", 5000))
    debug = os.getenv("DEBUG", "FALSE").lower() in ("true", "1", "t")
    app.run(debug=debug, host="0.0.0.0", port=port)