import os
from dotenv import load_dotenv
from scraper import Scraper
from db import Database
from crawlbase import requests_page

# read .env file
load_dotenv ()
MAX_PRODUCTS = int(os.getenv ("MAX_PRODUCTS"))

class ScraperAmazon (Scraper):
    
    def __init__ (self, keyword:str, db:Database):
        """ Start scraper for amazon

        Args:
            keyword (str): product to search
            db (Database): database instance
        """
        
        # Css self.selectors
        self.selectors = {
            'product': 'div[data-asin][data-uuid]',
            'image': 'img',
            'title': 'h2',
            'rate_num': '.a-spacing-top-micro span[aria-label]:nth-child(1)',
            'reviews': '.a-spacing-top-micro span[aria-label]:nth-child(2)',
            'sponsored': '[aria-label~="Sponsored"]',
            'best_seller': '.a-row.a-badge-region',
            'price': 'a.a-size-base span[aria-hidden]:nth-child(2)',
            'sales': '.a-row.a-size-base > span.a-color-secondary:only-child',
            'link': 'a',
            "search_bar": '',
            "search_btn": '',
        }
        
        self.store = "amazon"
        self.start_product = 7
        
        # Send data to scraper
        super().__init__ (keyword, db)
        
    def __load_page__ (self, product:str):
        """ Load amazon search page

        Args:
            product (str): product to search
        """
        
        # Load search page
        link = f"https://www.amazon.com/s?k={product}&s=review-rank"
        self.soup = requests_page (link, html_name="sample amazon")

    def __get_is_sponsored__ (self, text:str) -> str:
        """ Get if the product is sponsored in amazon

        Args:
            text (str): sponsored text

        Returns:
            bool: True if the product is sponsored
        """
        
        return text != ""
    
    def __get_clean_price__ (self, text:str) -> str:
        """ Get product clean price in aliexpress

        Args:
            text (str): price as text

        Returns:
            str: clean price
        """
        
        price = self.clean_text (text, ["$", "US "])
        price = price.replace ("\n", ".")
        return price
        
    def get_reviews (self, selector:str) -> str:
        """ Get product reviews number as text
        
        Args:
            selector (str): css selector

        Returns:
            str: reviews number as text
        """
        
        reviews = self.soup.select_one (selector).attrs ["aria-label"]
        return reviews
    
    def get_product_link (self, selector:str) -> str:
        """ Get product link with selector, from href

        Args:
            selector (str): css selector

        Returns:
            str: product link in store
        """
        
        prefix = "https://www.amazon.com"
        link = self.soup.select_one (selector).attrs["href"]
        if prefix not in link:
            link = prefix + link
        return link
    
    def get_rate_num (self, selector:str) -> float:
        """ Get product rate number with selector

        Args:
            selector (str): css selector

        Returns:
            float: product rate as float
        """
        
        rate_num = self.soup.select_one (selector).attrs["aria-label"]
        
        if rate_num:
            rate_num = float(rate_num.split (" ")[0])
        else:
            rate_num = 0.0
            
        return rate_num