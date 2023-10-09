import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from db import Database

load_dotenv ()
CROWLBASE_TOKEN = os.getenv ("CROWLBASE_TOKEN")
CURRENT_FOLDER = os.path.dirname(__file__)

def requests_page (link:str, db:Database, html_name:str="") -> BeautifulSoup:
    """ Query page data from crawlbase api, and returns html response 
    
    Args:
        link (str): link of the page to query
        html_name (str, optional): name of the html file to save. Defaults to "".
    
    Returns:
        BeautifulSoup: html response from crawlbase api
    """
    
    # Scape link
    link = link.replace ("&", "%26").replace (":", "%3A").replace ("/", "%2F").replace ("?", "%3F").replace ("=", "%3D").replace ("+", "%2B").replace ("#", "%23").replace (" ", "%20")

    # Get data from api
    url = f"https://api.crawlbase.com/?token={CROWLBASE_TOKEN}&country=US&url={link}&render=true&device=desktop&wait=10000"
    res = requests.request("GET", url)
    
    if res.status_code == 200:
        db.save_log (f"Page rendered {link}", "crawlbase")
    else:
        db.save_log (f"Page not rendered {link} ({res.status_code})", "crawlbase", log_type="error")
        
    # Raise error if the status code is not 200
    res.raise_for_status ()

    # Create html file
    if html_name:
        file_path = os.path.join (CURRENT_FOLDER, "html", f"{html_name}.html")
        with open (file_path, "w", encoding='UTF-8') as file:
            file.write (res.text)
    
    # Get soup
    try:
        soup = BeautifulSoup (requests.get (url).text, "html.parser")
    except Exception as error:
        db.save_log (f"Page not rendered {link} ({error})", "crawlbase", log_type="error")
        soup = None
    else:
        return soup    