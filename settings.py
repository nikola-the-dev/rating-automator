from tabulate import tabulate
from enum import Enum

from csvFileHelper import CsvFileHelper
from constants import Constants
from regexHelper import RegexHelper


class Settings:

    # Constants

    class FeedType(Enum):
        UNDEFINED = 0
        CSV_FILE = 1
        URL = 2


    class ColumnNames:
        sku = "ID"
        rate = "Popularity"

        def __str__(self):
            return f"{self.sku} & {self.rate}"


    class FieldWeight:

        def __init__(self):
            self.views = 0
            self.users = 20
            self.viewsUserRate = 5
            self.avgTime = 10
            self.events = 25
            self.keyEvents = 40

        def allElems(self):
            return [self.views, self.users, self.viewsUserRate, self.avgTime, self.events, self.keyEvents]

        def __str__(self):
            return "-".join([str(item) for item in self.allElems()])

        def totalWeights(self):
            return sum(self.allElems())


    # Instance initialization

    def __init__(self):
        self.analytics = None
        self.feed = None
        self.resultFileName = "result.csv"
        self.fieldWeights = Settings.FieldWeight()
        self.columnNames = Settings.ColumnNames()
        self.regex = None
        self.isRegexSimplified = False
        self.feedMapping = None


    # Variables

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


    # Interface methods

    def summary(self):
        headers = ["Key", "Name", "Value"]
        dict = {Constants.Step.ANALYTICS: self.analytics,
                Constants.Step.RESULT_FILE_NAME: self.resultFileName,
                Constants.Step.FIELD_WEIGHTS: self.fieldWeights,
                Constants.Step.COL_NAMES: self.columnNames,
                Constants.Step.REGEX: self.regex,
                Constants.Step.FEED: self.feed,
                Constants.Step.FEED_MAPPING: self.feedMapping
                }
        body = []
        for key in Constants.Step:
            if (key == Constants.Step.FEED_MAPPING) & (self.feedType != Settings.FeedType.CSV_FILE):
                continue
            body.append([key.value,
                         key.message,
                         Constants.valueStr(dict[key])
                         ])
            if key == Constants.Step.FIELD_WEIGHTS:
                body.append(["", "(Views - Users - Views/User Rate - Avg.Time - Events - Key Events)", ""])
            elif key == Constants.Step.FEED:
                body.append(["", "(.csv file or link to Google Merchant Center .xml file)", ""])
        print(tabulate(body, headers, "outline"))

