import random


class AdsCards ():
    """ Manage card ads (images and links) """

    def __init__(self):
        """ Contructor of class """

        self.ads = [
            {
                "type": "video",
                "path": "limited-time-luxe-handbags-deals-239x347px (1).mp4",
                "link": "https://www.ebay.com/e/fashion/luxe-handbag-deals-082823?mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339089849&toolid=20014&customid=&mkevt=1",
            },
            {
                "type": "video",
                "path": "up-to-40%off-musical-instruments-239x347px.mp4",
                "link": "https://www.ebay.com/e/lifestyle-media/musical-instruments-and-gear?mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339089849&toolid=20014&customid=&mkevt=1",
            },
            {
                "type": "video",
                "path": "up-to-60%-off-TVs-239x347px.mp4",
                "link": "https://www.ebay.com/e/_electronics/new-and-ebay-refurbished-tv-home-audio-savings?mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339089849&toolid=20014&customid=&mkevt=1",
            },
            {
                "type": "video",
                "path": "up-to-70%-off-apple-watches-239x347px.mp4",
                "link": "https://www.ebay.com/e/_electronics/refurbished-smartwatches?mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339089849&toolid=20014&customid=&mkevt=1",
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