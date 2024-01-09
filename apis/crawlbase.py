import os
from time import sleep
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from database.db import Database

load_dotenv()
CROWLBASE_TOKEN = os.getenv("CROWLBASE_TOKEN")
CURRENT_FOLDER = os.path.dirname(__file__)
SAVE_HTML = os.getenv("SAVE_HTML") == "True"


def requests_page(link: str, db: Database,
                  selector_product: str, html_name: str = "") -> BeautifulSoup:
    """ Query page data from crawlbase api, and returns html response

    Args:
        link (str): link of the page to query
        db (Database): database object
        selector_product (str): css selector to validate if page is loaded
        html_name (str, optional): name of the html to save. Defaults to "".

    Returns:
        BeautifulSoup: html response from crawlbase api
    """

    chars = {
        "&": "%26",
        ":": "%3A",
        "/": "%2F",
        "?": "%3F",
        "=": "%3D",
        "+": "%2B",
        "#": "%23",
        " ": "%20"
    }

    # Scape link
    for old_char, new_char in chars.items():
        link = link.replace(old_char, new_char)

    # Get data from api

    url = (
        f"https://api.crawlbase.com/?token={CROWLBASE_TOKEN}"
        f"&country=US&url={link}&render=true&device=desktop&wait=10000"
    )

    # Try 3 times to request page
    for _ in range(5):

        # Restart control variables
        soup = None
        results_num = 0

        res = requests.request("GET", url)

        # Validate response
        if res.status_code == 200:
            # Save log
            db.save_log(f"Page rendered {link}", "crawlbase")
        else:
            # Try again
            sleep(5)
            continue

        # Get soup
        try:
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
        except Exception:
            sleep(5)
            continue

        # get the results in the page
        results_num = len(soup.select(selector_product))
        if results_num == 0:
            sleep(5)
            continue

        break

    # Validate if soup is created
    if not soup or results_num == 0:
        message = f"Page not rendered {link})"
        db.save_log(message, "crawlbase", log_type="error")
        raise Exception(f"Page not rendered {link}")

    # Create html file
    if html_name and SAVE_HTML:
        file_path = os.path.join(CURRENT_FOLDER, "html", f"{html_name}.html")
        with open(file_path, "w", encoding='UTF-8') as file:
            file.write(res.text)

    return soup, results_num
