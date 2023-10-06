import os
import json
import requests
from time import sleep
from app import app
from threading import Thread
from dotenv import load_dotenv

load_dotenv ()

TEST_HOST = os.getenv ("TEST_HOST")
TEST_PORT = os.getenv ("TEST_PORT")
TEST_API_KEY = os.getenv ("TEST_API_KEY")

def request_api ():
    
    sleep (5)

    # Generate pai url
    url = f"{TEST_HOST}:{TEST_PORT}/keyword/"

    # Send keyword to api
    payload = json.dumps({
        "keyword": "protein",
        "api-key": TEST_API_KEY
    })
    headers = {
        'Content-Type': 'application/json'
    }

    # Get response from api
    requests.request("POST", url, headers=headers, data=payload)

if __name__ == "__main__":

    # Requestto api in background
    thread_request_api = Thread (target=request_api)
    thread_request_api.start ()

    # Start api
    app.run (debug=True, port=TEST_PORT)