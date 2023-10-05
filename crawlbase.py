import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv ()
CROWLBASE_TOKEN = os.getenv ("CROWLBASE_TOKEN")
CURRENT_FOLDER = os.path.dirname(__file__)

def requests_page (link:str, html_name:str="") -> BeautifulSoup:
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

    # Create html file
    if html_name:
        res = requests.request("GET", url)
        file_path = os.path.join (CURRENT_FOLDER, "html", f"{html_name}.html")
        with open (file_path, "w", encoding='UTF-8') as file:
            file.write (res.text)
    
    # Get soup
    soup = BeautifulSoup (requests.get (url).text, "html.parser")
    return soup    

# requests_page ("https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=protein&_sacat=0", html_name="sample ebay")
