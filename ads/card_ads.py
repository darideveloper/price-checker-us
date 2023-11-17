import random

class AdsCards ():
    """ Manage card ads (images and links) """
    
    def __init__ (self):
        """ Contructor of class """
        

        self.ads = {
            "nordvpn.jpeg":  "https://go.nordvpn.net/aff_c?offer_id=15&aff_id=96425&url_id=902",
            "ebay.jpeg": "https://www.ebay.com/e/_electronics/ebay-refurbished-apple-watches?mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339011126&toolid=20014&customid=&mkevt=1",
            "aliexpress.jpeg": "https://s.click.aliexpress.com/e/_De4zf2T?bz=300*250",
        }
        
    def get_random_add (self) -> dict:
        """ Select a random add from the list and return it
        
        Returns:
            dict: The add selected
            
            Structure:
            {
                path: str,
                link: str   
            }
        """
        
        random_add_image = random.choice(list(self.ads.keys()))
        random_add_link = self.ads[random_add_image]
        
        return {
            "path": random_add_image,
            "link": random_add_link            
        }
        
        

