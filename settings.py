from tabulate import tabulate
from enum import Enum

from csvFileHelper import CsvFileHelper
from regexHelper import RegexHelper


class Settings:

    # Constants

    defaultResultName = "result.csv"

    class FeedType(Enum):
        UNDEFINED = 0
        CSV_FILE = 1
        URL = 2

    class FieldWeight:

        def __init__(self):
            self.user = 10
            self.avgTime = 10
            self.events = 20
            self.engagement = 25

        def totalWeights(self):
            return self.user + self.avgTime + self.events + self.engagement

        def printWeights(self):
            table = [["Number of users", self.user],
                     ["Average time", self.avgTime],
                     ["Number of events", self.events],
                     ["Engagement rate", self.engagement],
                     ]
            print(tabulate(table, ["Field", "Weight"], "outline"))


    # Instance initialization

    def __init__(self):
        self.analytics = None
        self.feed = None
        self.resultFileName = None
        self.fieldWeights = None


    # Variables

    @property
    def analytics(self):
        return self._analytics
    @analytics.setter
    def analytics(self, analytics):
        self._analytics = analytics

    @property
    def feed(self):
        return self._feed
    @feed.setter
    def feed(self, feed):
        self._feed = feed

    @property
    def feedType(self):
        if f := self.feed:
            if RegexHelper.isUrl(f):
                return Settings.FeedType.URL
            elif CsvFileHelper.extFileCheck(f):
                return Settings.FeedType.CSV_FILE
        return Settings.FeedType.UNDEFINED

    @property
    def resultFileName(self):
        return self._resultFileName
    @resultFileName.setter
    def resultFileName(self, result):
        if r := result:
            if CsvFileHelper.extFileCheck(r) == False:
                r += ".csv"
            self._resultFileName = r
        self._resultFileName = result

    @property
    def fieldWeights(self):
        return self._fieldWeights
    @fieldWeights.setter
    def fieldWeights(self, weights):
        self._fieldWeights = weights

