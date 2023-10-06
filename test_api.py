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
    
    # Wait to api loads
    sleep (5)
    
    # Get words from json file
    current_folder = os.path.dirname (__file__)
    json_path = os.path.join (current_folder, "test_api_keywords.json")
    with open (json_path) as json_file:
        keywords = json.load (json_file)

    # Request each keyword
    for keyword in keywords:

        # Generate pai url
        url = f"{TEST_HOST}:{TEST_PORT}/keyword/"

        # Send keyword to api
        payload = json.dumps({
            "keyword": keyword,
            "api-key": TEST_API_KEY
        })
        headers = {
            'Content-Type': 'application/json'
        }

        # Get response from api
        requests.request("POST", url, headers=headers, data=payload)
        
        sleep (30)

if __name__ == "__main__":

    # Requestto api in background
    thread_request_api = Thread (target=request_api)
    thread_request_api.start ()

    # Start api
    app.run (debug=True, port=TEST_PORT)