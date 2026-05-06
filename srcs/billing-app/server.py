from dotenv import load_dotenv
load_dotenv()
from app import init_db
import sys
from app.consumer import start_consumer


if __name__ == "__main__":
    try:
        init_db()
        start_consumer()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit()
