import os

class Settings:

    # Instance initialization

    def __init__(self):
        self._feed = None
        self._analytics = None


    # Variables

    @property
    def analytics(self):
        return self._analytics
    @analytics.setter
    def analytics(self, analytics):
        if not os.path.exists(analytics):
            raise FileNotFoundError
        self._analytics = analytics

    @property
    def feed(self):
        return self._feed
    @feed.setter
    def feed(self, feed):
        if not os.path.exists(feed):
            raise FileNotFoundError
        self._feed = feed