import random


class AdsCards ():
    """ Manage card ads (images and links) """

    def __init__(self):
        """ Contructor of class """

        self.ads = [
            {
                "type": "video",
                "path": "ebay-up-to-70-off-apple-watches-239x347px.mp4",
                "link": "https://www.ebay.com/e/_electronics/ebay-refurbished-apple-watches?mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339011126&toolid=20014&customid=&mkevt=1"
            },
            {
                "type": "video",
                "path": "share-price-checker-239x347px.mp4",
                "link": "https://www.referral-fifty-fifty.com/register/"
            },
            {
                "type": "video",
                "path": "shop-hot-deal-at-aliexpress-239x347px.mp4",
                "link": "https://s.click.aliexpress.com/e/_DmAf2NN?bz=300*250"
            },
            {
                "type": "video",
                "path": "try-amazon-audible-plus-239x347px.mp4",
                "link": "https://www.amazon.com/hz/audible/mlp/membership/plus?ref_=assoc_tag_ph_1524216631897&_encoding=UTF8&camp=1789&creative=9325&linkCode=pf4&tag=pricecheck06a-20&linkId=c3a3982e85003c64068c1ebf67d8e8b2"
            },
            {
                "type": "video",
                "path": "up-to-69-off-amazon-gift-card-239x347px.mp4",
                "link": "https://go.nordvpn.net/aff_c?offer_id=15&aff_id=96425&url_id=902"
            },
            {
                "type": "image",
                "path": "ebay-up-to-70-off-apple-watches-239x347px.png",
                "link": "https://www.ebay.com/e/_electronics/ebay-refurbished-apple-watches?mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339011126&toolid=20014&customid=&mkevt=1"
            },
            {
                "type": "image",
                "path": "share-price-checker-239x347px.png",
                "link": "https://www.referral-fifty-fifty.com/register/"
            },
            {
                "type": "image",
                "path": "shop-hot-deal-at-aliexpress-239x347px.png",
                "link": "https://s.click.aliexpress.com/e/_DmAf2NN?bz=300*250"
            },
            {
                "type": "image",
                "path": "try-amazon-audible-plus-239x347px.png",
                "link": "https://www.amazon.com/hz/audible/mlp/membership/plus?ref_=assoc_tag_ph_1524216631897&_encoding=UTF8&camp=1789&creative=9325&linkCode=pf4&tag=pricecheck06a-20&linkId=c3a3982e85003c64068c1ebf67d8e8b2"
            },
            {
                "type": "image",
                "path": "up-to-69-off-amazon-gift-card-239x347px.png",
                "link": "https://go.nordvpn.net/aff_c?offer_id=15&aff_id=96425&url_id=902"
            },

        ]

    def get_random_add(self) -> dict:
        """ Select a random add from the list and return it

        Returns:
            dict: The add selected

            Structure:
            {
                "type": str ("image" or "video"),
                "path": str
                "link": str
            }
        """

        random_ad = random.choice(self.ads)
        return random_ad