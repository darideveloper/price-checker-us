import os
import requests
from dotenv import load_dotenv

load_dotenv ()

REFERRAL_HOST = os.getenv ("REFERRAL_HOST")
REFERRAL_API_KEY = os.getenv ("REFERRAL_API_KEY")

class Referral ():
    
    def __init__(self):
        pass
    
    def get_by_hash (self, hash:str) -> dict:
        """ Query a user form referral api by hash

        Args:
            hash (str): user hash

        Returns:
            dict: store data
            
            Structure:
            {
                "store_1": "store_ref_link",
                "store_2": "store_ref_link",
            }
        """
        
        headers = {
            "token": REFERRAL_API_KEY
        }
        
        params = {
            "hash": hash
        }
        
        res = requests.get (f"{REFERRAL_HOST}/referral", headers=headers, params=params)
        json_data = res.json ()
        if res.status_code == 200:
            return json_data["data"]
        else:
            return {}


if __name__ == "__main__":
    ref = Referral ()
    referral_links = ref.get_by_hash ("ce913808c307c0abf4161bc0c99d27244d8ea1e6de41bf2633a40a4adc657ae5")
    print ()