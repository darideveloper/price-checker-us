import os
from time import sleep
from datetime import datetime
from database.mysql import MySQL
from email_manager.sender import EmailManager
from dotenv import load_dotenv

load_dotenv ()
EMAIL_USER = os.getenv ("EMAIL_USER")
EMAIL_PASSWORD = os.getenv ("EMAIL_PASSWORD")
TO_EMAILS = os.getenv ("TO_EMAILS").split (",")

class Database (MySQL):
    
    status = {}
    api_keys = {}
    stores = {}
    log_types = {}
    log_origins = {}
    
    def __init__ (self, server:str, database:str, username:str, password:str):
        """ Connect with mysql db

        Args:
            server (str): server host
            database (str): database name
            username (str): database username
            password (str): database password
        """
        
        # Connext to database
        super().__init__(server, database, username, password)
        
        # Loading initial data
        if not Database.status:
            Database.status = self.__get_status__ ()
        
        if not Database.api_keys:
            Database.api_keys = self.__get_api_keys__ ()
            
        if not Database.stores:
            Database.stores = self.__get_stores__ ()
    
        if not Database.log_types:
            Database.log_types = self.__get_log_types__ ()
            
        if not Database.log_origins:
            Database.log_origins = self.__get_log_origins__ ()
        
        # Log status
        self.log_origin = "database"
        
        # Connect to email
        self.email_manager = EmailManager (EMAIL_USER, EMAIL_PASSWORD)
    
    def __get_status__ (self) -> dict:
        """ Retuen status from database as dictionary

        Returns:
            dict: status
            {
                "to do": 1,
                "working": 2,
                "done": 3
            }
        """
        
        query = "SELECT * FROM status"
        data = self.run_sql (query)
        
        status = {}
        for row in data:
            status[row["name"]] = row["id"]
            
        return status
    
    def __get_api_keys__ (self) -> dict:
        """ Retuen api keys from database as dictionary

        Returns:
            dict: status
            {
                "api-key-1": 1,
                "api-key-2": 2,
            }
        """
        
        query = "SELECT * FROM apikeys"
        data = self.run_sql (query)
        
        status = {}
        for row in data:
            status[row["api_key"]] = row["id"]
            
        return status
    
    def __get_stores__ (self) -> dict:
        """ Query current stores in database 
        
        Returns:
            dict: stores (name and id)
            
            {
                "amazon": {
                    "id": 1,
                },
                "aliexpress": {
                    "id": 2,
                },
                "ebay": {
                    "id": 3,
                },
                ...
            }
        """
                
        # Query all stores 
        query = "select * from stores"
        results = self.run_sql(query)
        
        data = {}
        for row in results:
            data[row["name"]] = {
                "id": row["id"],
            }
        
        return data
    
    def __get_log_types__ (self) -> dict:
        """ Query current log types in database

        Returns:
            dict: log types (name and id)
            
            {
                "info": 1,
                "error": 2,
            }
        """
                
        # Query all stores 
        query = "select * from log_types"
        results = self.run_sql(query)
        
        data = {}
        for row in results:
            data[row["name"]] = row["id"]
        
        return data
    
    def __get_log_origins__ (self) -> dict:
        """ Query current log origins in database

        Returns:
            dict: log types (name and id)
            {
                "database": 1,
                "api": 2,
                "scraper": 3
            }
        """
                
        # Query all stores 
        query = "select * from log_origins"
        results = self.run_sql(query)
        
        data = {}
        for row in results:
            data[row["name"]] = row["id"]
        
        return data
    
    def save_products (self, products_data:list):
        """ Save products in database

        Args:
            products_data (list): list of dict with products data
        """
        
        for product in products_data:
            
            # Get product data
            image = product["image"]
            title = product["title"]
            rate_num = product["rate_num"]
            reviews = product["reviews"]
            price = product["price"]
            best_seller = 1 if product["best_seller"] else 0          
            sales = product["sales"]
            link = product["link"]
            id_store = product["id_store"]
            id_request = product["id_request"]
            
            # Generate sql query
            query = f"""
                INSERT INTO products (
                    image, 
                    title, 
                    rate_num, 
                    reviews, 
                    price, 
                    best_seller, 
                    sales, 
                    link, 
                    id_store,
                    id_request
                ) VALUES (
                    '{image}', 
                    '{title}', 
                    {rate_num}, 
                    {reviews}, 
                    {price}, 
                    {best_seller}, 
                    {sales}, 
                    '{link}',
                    {id_store},
                    {id_request}
                ); 
            """.replace ("\n", "")
                            
            # Save data
            self.run_sql(query)
            
    def delete_products (self):
        """ Delete all rows from products table """
        
        self.save_log ("Deleting all products from database", self.log_origin)
        
        query = "delete from products"
        self.run_sql(query)
        
    def validate_token (self, token:str):
        """ Validate if token exist in database and is active

        Args:
            token (str): api access token
        """
        
        token_cencured = token[:5] + "..."
        self.save_log (f"Validating token {token_cencured}", self.log_origin)
        
        token = self.get_clean_text (token)
        
        query = f"""
            SELECT id 
            FROM apikeys 
            WHERE 
                api_key = '{token}'
                AND
                is_active = 1
        """
        
        api_key_found = self.run_sql (query)
        
        if api_key_found:
            return True
        else:
            return False
                
    def create_new_request (self, api_key:str, keyword:str) -> int:
        """  Save a new request in database with status "to do" 
        
        Args:
            api_key (str): api access token
            keyword (str): keyword to search
            
        Returns:
            int: id of new request
        """
        
        self.save_log ("Creating new request in database", self.log_origin)
        
        # Get status for new requests
        status_todo_id = Database.status["to do"]
        
        # Get api key id
        api_key_id = Database.api_keys[api_key] 
        
        # get and fomat current datetime
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save new request
        query = f"""
            INSERT INTO requests (status, todo_datetime, api_key, keyword) 
            VALUES ({status_todo_id}, '{current_datetime}', {api_key_id}, '{keyword}')
        """
        self.run_sql (query)
        
        # Query id of new request
        query = f"""
            SELECT id 
            FROM requests
            WHERE
                status = {status_todo_id}
                AND
                api_key = {api_key_id}
                AND
                todo_datetime = '{current_datetime}'
        """
        id = self.run_sql (query)[0]["id"]
        return id
    
    def update_request_status (self, request_id:int, status_name:str):
        """ Update request status in db
        
        Args:
            request_id (int): request id
            status_name (str): status name
        """
        
        self.save_log (f"Updating request {request_id} status to {status_name}", self.log_origin)
        
        status_num = Database.status[status_name]
        
        # get current datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        query = f"""
            UPDATE requests
            SET 
                status = {status_num},
                {status_name}_datetime = '{now}'
            WHERE id = {request_id}
        """
        self.run_sql (query)
    
    def get_request_status (self, request_id:int) -> str:
        """ Get request status in db
        
        Args:
            request_id (int): request id
            
        Returns:
            str: status name
        """
        
        query = f""" 
            SELECT status
            FROM requests
            WHERE id = {request_id}
        """
        
        status_results = self.run_sql (query)
        
        if not status_results:
            return ""
        
        status_num = status_results[0]["status"]
        for status_name, status_id in Database.status.items ():
            if status_id == status_num:
                return status_name
            
        return ""
    
    def get_products (self, id_request:int) -> list:
        """ Get products from a request and all stores

        Args:
            id_request (int): request id from api

        Returns:
            list: list of dict with products data
            
        """
        
        # Get products from db
        query = f"""
            SELECT * 
            FROM products
            WHERE 
                id_request = {id_request}
        """
        
        products = self.run_sql (query)
        
        # Sort products by store
        products_store = {}
        for store_name, store_data in Database.stores.items():
            store_id = store_data["id"]
            
            # Filter products of the current store
            products_store[store_name] = list(filter(
                lambda product: product["id_store"] == store_id, products
            ))
        
        return products_store
    
    def save_log (self, message:str, origin:str, store:str="", id_request:int=0, api_key:str="", log_type:str="info"):
        """ Save log in database

        Args:
            message (str): logs details
            store (str): webn scraping log store
            id_request (int): id request from api
            api_key (str): api key from api
            log_type (str): type of log (info or error)
        """
        
        # Get and validate ids
        id_store = Database.stores[store]["id"] if store else "NULL"
        id_api_key = Database.api_keys[api_key] if api_key else "NULL"
        id_log_type = Database.log_types[log_type] if log_type else "NULL"
        id_log_origin = Database.log_origins[origin] if origin else "NULL"
        
        # Validate id request
        if not id_request:
            id_request = "NULL"
        
        # Save log in database
        query = f"""
        INSERT INTO `logs` 
            (id_log_type, id_log_origin,id_store, id_request, id_api_key, message) 
        VALUES 
            ({id_log_type}, {id_log_origin}, {id_store}, {id_request}, {id_api_key}, '{message}')
        """
        
        self.run_sql (query)
        
        # Print logs 
        extra_data = False
        print_message = f"{log_type}: {message} ("
        if store and store != "NULL":
            print_message += f"store: {store}, "
            extra_data = True
        if id_request and id_request != "NULL":
            print_message += f"request: {id_request}, "
            extra_data = True
        if api_key and api_key != "NULL":
            print_message += f"api_key: {api_key[:5]+'...'}, "
            extra_data = True
        
        print_message = print_message[:-2]
        if extra_data:
            print_message += ")"
        
        print (print_message)
        
        # Send error email
        if log_type == "error":
            
            # Wait for email to be sent
            while True:
                
                if self.email_manager.sending_email:
                    sleep (1)
                else:
                    break
            
            self.email_manager.send_email (TO_EMAILS, "Error in web scraping", print_message)
            