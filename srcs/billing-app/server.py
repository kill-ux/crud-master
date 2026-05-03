from dotenv import load_dotenv
load_dotenv()

from app import get_env_variable, create_app

HOST = get_env_variable("BILLING_HOST")
PORT = get_env_variable("BILLING_PORT")
DEBUG = get_env_variable("BILLING_DEBUG").lower() in ("true", "1", "t")

app = create_app()

if __name__ == "__main__":
    app.run(host=HOST,port=PORT,debug=DEBUG)