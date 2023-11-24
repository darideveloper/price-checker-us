import os
from time import sleep
from functools import wraps
from threading import Thread
from database.db import Database
from dotenv import load_dotenv
from scraper.scraper import Scraper
from scraper.amazon import ScraperAmazon
from scraper.ebay import ScraperEbay
from scraper.walmart import ScraperWalmart
from apis.referral import Referral
from ads.card_ads import AdsCards
from flask import (
    Flask,
    request,
    render_template,
    session,
    redirect,
    url_for,
    send_file
)

app = Flask(__name__)

# Load env variables
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
USE_THREADING = os.getenv("USE_THREADING") == "True"
PORT = int(os.environ.get('PORT', 5000))
app.secret_key = os.environ.get('SECRET_KEY')
ROTATTION_LINKS_SYSTEM = int(os.getenv("ROTATTION_LINKS_SYSTEM"))
ROTATION_LINKS_USER = int(os.getenv("ROTATION_LINKS_USER"))
REFERRAL_HOST = os.getenv("REFERRAL_HOST")
ADS_RELATION = int(os.getenv("ADS_RELATION"))
RECENT_SEARCHES_NUM = int(os.getenv("RECENT_SEARCHES_NUM"))

# Connect with database
db = Database(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)

log_origin = "api"

# Connect to referral api
referral_api = Referral()


def start_scraper(scraper_class: Scraper, keyword: str, request_id: int):
    """ Start an specific scraper and extract data

    Args:
        scraper_class (Scraper): Scraper class
        keyword (str): keyword to search
        request_id (int): request id
    """

    scraper = scraper_class(keyword, db)

    try:
        scraper.get_results(request_id)
    except Exception as error:

        # Clean error message
        error = str(error).replace("'", "").replace("\"", "")

        # Save error in db
        error_message = f"store: {scraper.store}, keyword: {keyword}, error: {str(error)}"
        db.save_log(error_message, log_origin, id_request=request_id, log_type="error")
        quit()

    # random_wait_time = random.randint (30, 60)
    # sleep (random_wait_time)


def start_scrapers(keyword: str, request_id: int):
    """ Start all scrapers

    Args:
        keyword (str): keyword to search
        request_id (int): request id
    """

    classes = [ScraperAmazon, ScraperEbay, ScraperWalmart]

    # Update request status to working
    db.update_request_status(request_id, "working")

    # Start scraping threads
    threads = []
    for class_elem in classes:

        # Run functions with and without threads
        if USE_THREADING:
            thread_scraper = Thread(target=start_scraper, args=(
                class_elem, keyword, request_id))
            thread_scraper.start()
            threads.append(thread_scraper)
        else:
            start_scraper(class_elem, keyword)

    # Wait for all threads to finish
    while True:

        alive_threads = list(filter(lambda thread: thread.is_alive(), threads))
        if not alive_threads:
            break

        else:
            sleep(2)

    # Update request status to done
    db.update_request_status(request_id, "done")


def wrapper_validate_api_key(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        # Get json data
        json_data = request.get_json()
        api_key = json_data.get("api-key", "")

        # Validate required data
        if not api_key:

            status_code = 400
            db.save_log(f"({status_code}) Api-key is required", log_origin)

            return ({
                "status": "error",
                "message": "Api-key is required",
                "data": {}
            }, status_code)

        # Validate if token exist in db
        api_key_valid = db.validate_token(api_key)
        if not api_key_valid:

            status_code = 401
            db.save_log(
                f"({status_code}) Invalid api-key {api_key}", log_origin)

            return ({
                "status": "error",
                "message": "Invalid api-key",
                "data": {}
            }, status_code)

        return function(*args, **kwargs)

    return wrap


def wrapper_validate_request_id(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        # Get json data
        json_data = request.get_json()
        request_id = json_data.get("request-id", "")

        # Validate required data
        if not request_id:

            status_code = 400
            db.save_log(f"({status_code}) Request-id is required", log_origin)

            return ({
                "status": "error",
                "message": "Request-id is required",
                "data": {}
            }, status_code)

        # Get request status
        request_status = db.get_request_status(request_id)

        if not request_status:

            status_code = 404
            message = f"({status_code}) Invalid request-id {request_status}"
            db.save_log(message, log_origin)

            return ({
                "status": "error",
                "message": "Invalid request-id",
                "data": {}
            }, status_code)

        return function(*args, **kwargs)

    return wrap


@app.get('/')
def index():
    """ Home page """

    # Get api key for web
    api_key_web = ""
    for api_key, data in db.api_keys.items():
        if data["name"] == "web":
            api_key_web = api_key
            break

    return render_template("index.html", api_key=api_key_web)


@app.get('/legals/')
def legals():
    """ Legals page """

    return render_template("legals.html")


@app.get('/legal-framework/')
def legal_framewok():
    """ Legal framework page """

    return render_template("legal-framework.html")


@app.post('/keyword/')
@wrapper_validate_api_key
def keyword():
    """ Initilize scraper in background """

    # Get json data
    json_data = request.get_json()
    keyword = json_data.get("keyword", "")
    api_key = json_data.get("api-key", "")

    # Validate required data
    if not keyword:

        status_code = 400
        db.save_log(f"({status_code}) Keyword is required",
                    log_origin, api_key=api_key)

        return ({
            "status": "error",
            "message": "Keyword is required",
            "data": {}
        }, status_code)

    # save request in db
    request_id = db.create_new_request(api_key, keyword)

    # initialize web scraper in background
    thread_scrapers = Thread(target=start_scrapers, args=(keyword, request_id))
    thread_scrapers.start()

    status_code = 200
    db.save_log(f"({status_code}) Scraper started in background",
                log_origin, api_key=api_key, id_request=request_id)

    return {
        "status": "success",
        "message": "Scraper started in background",
        "data": {
            "request-id": request_id
        }
    }


@app.post('/status/')
@wrapper_validate_api_key
@wrapper_validate_request_id
def status():
    """ Get request status """

    # Get json data
    json_data = request.get_json()
    request_id = json_data.get("request-id", "")

    # Get request status
    request_status = db.get_request_status(request_id)

    status_code = 200
    db.save_log(f"({status_code}) Request status",
                log_origin, id_request=request_id)

    return ({
        "status": "success",
        "message": "Request status",
        "data": {
            "status": request_status
        }
    })


@app.post('/results/')
@wrapper_validate_api_key
@wrapper_validate_request_id
def results():

    # Get json data
    json_data = request.get_json()
    request_id = json_data.get("request-id", "")

    # Get products from db
    products, keyword = db.get_products(request_id)

    status_code = 200
    db.save_log(f"({status_code}) Products found",
                log_origin, id_request=request_id)

    # TODO: Add keyword to response
    return ({
        "status": "success",
        "message": "Products found",
        "data": {
            "products": products
        }
    })


@app.get('/preview/')
def recent_searches():
    """ Return a table of the recent results """

    searches = db.get_last_requests(RECENT_SEARCHES_NUM)

    # Format links and dates
    searches = list(map(lambda search: {
        **search,
        "link": f"/preview/{search['id']}",
        "date": search["date"].strftime("%m/%d/%Y")
    }, searches))

    # Split results in two columns
    split_index = int(len(searches) / 2)
    columns = [
        searches[:split_index],
        searches[split_index:]
    ]

    return render_template("preview.html", columns=columns)


@app.get('/preview/<int:request_id>')
def preview_request_id(request_id):
    """ Render basic preview products page """

    # Get referral session
    referral_hash = session.get("hash", "")
    referral_links = {}
    if referral_hash:
        referral_links = referral_api.get_by_hash(referral_hash)

    valid_request_id = db.get_request_status(request_id)

    if not valid_request_id:

        status_code = 401
        db.save_log(f"({status_code}) Invalid api token or request id",
                    log_origin, id_request=request_id)

        return ({
            "status": "error",
            "message": "invalid api token or request id",
            "data": []
        }, status_code)

    # Get products from db
    products, keyword, working_datetime = db.get_products(request_id)

    # Add referral code
    current_referral = "user"
    links_num_user = 0
    links_num_system = 0
    links_total_user = 0
    links_total_system = 0
    for product in products:

        # Get product data
        link = product["link"]
        store = product["store"]

        # Get referral links and increase counter
        referral_link_user = referral_links.get(store, "")
        referral_link_system = Database.stores[store]["referral_link"]
        if current_referral == "user":
            links_num_user += 1

            if referral_link_user:
                links_total_user += 1
            elif referral_link_system:
                referral_link_user = referral_link_system
                links_total_system += 1

        else:
            links_num_system += 1

            if referral_link_system:
                links_total_system += 1
            elif referral_link_user:
                referral_link_system = referral_link_user
                links_total_user += 1

        # Save referral link
        conector = "&" if "?" in link else "?"
        if current_referral == "user":
            link = f"{link}{conector}{referral_link_user}"
        else:
            link = f"{link}{conector}{referral_link_system}"

        product["link"] = link

        # Change referral current user
        if links_num_user == ROTATION_LINKS_USER:
            current_referral = "system"
            links_num_user = 0
        elif links_num_system == ROTATTION_LINKS_SYSTEM:
            current_referral = "user"
            links_num_system = 0

    # Sort products by price
    product_sort = sorted(products, key=lambda product: product["price"])

    # Add product ads
    ads_cards = AdsCards()
    products_ads = []
    for product in product_sort:

        product_index = product_sort.index(product)

        # Save add
        if product_index % ADS_RELATION == 0:
            add_data = ads_cards.get_random_add()
            add_data["id"] = f"{product_index} add"
            products_ads.append(add_data)

        # Save product
        products_ads.append(product)

    status_code = 200
    db.save_log(f"({status_code}) Products rendered",
                log_origin, id_request=request_id)

    # Format date like MM/DD/YYYY
    search_date = working_datetime.strftime("%m/%d/%Y")

    return render_template(
        "preview-request-id.html",
        products=products_ads,
        links_total_user=links_total_user,
        links_total_system=links_total_system,
        referral_host=REFERRAL_HOST,
        keyword=keyword,
        search_date=search_date,
        request_id=request_id
    )


@app.get('/referral/<hash>/')
def referral(hash):
    """ Save referral hash as session """

    # Save cookie
    session["hash"] = hash

    # Redirect to home
    return redirect(url_for("index"))


@app.get('/sitemap.xml')
def sitemap():
    """ Return sitemap """

    # Redirect to home
    return send_file("static/sitemap.xml")


@app.get('/robots.txt')
def robots():
    """ Return robots """

    # Redirect to home
    return send_file("static/robots.txt")


@app.errorhandler(404)
def template_404(error):
    """ Return 404 template """

    return (render_template("404.html"), 404)


if __name__ == "__main__":
    app.run(debug=True, port=PORT)
