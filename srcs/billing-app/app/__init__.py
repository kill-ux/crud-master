from flask import Flask

def create_app():
    app = Flask(__name__)
    
    return app

import os

def get_env_variable(name, cast_type=str):
    """
    Retrieves an environment variable. 
    Raises a Detailed RuntimeError if the variable is missing.
    """
    
    value = os.getenv(name)
    if name is None:
        raise RuntimeError(f"CRITICAL ERROR: Environment variable '{name}' is not set.")
    try:
        return cast_type(value)
    except ValueError:
        raise RuntimeError(f"CRITICAL ERROR: Variable '{name}' must be of type {cast_type.__name__}.")