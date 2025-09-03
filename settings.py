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
            self.user = 10
            self.avgTime = 10
            self.events = 20
            self.engagement = 25

        def __str__(self):
            elems = [self.user, self.avgTime, self.events, self.engagement]
            return "-".join([str(item) for item in elems])

        def totalWeights(self):
            return self.user + self.avgTime + self.events + self.engagement


    # Instance initialization

    def __init__(self):
        self.analytics = None
        self.feed = None
        self.resultFileName = "result.csv"
        self.fieldWeights = Settings.FieldWeight()
        self.columnNames = Settings.ColumnNames()
        self.regex = None
        self.isRegexSimplified = False


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
                Constants.Step.REGEX: self.regex
                }
        body = []
        for key in Constants.Step:
            body.append([key.value,
                         key.message,
                         Constants.valueStr(dict[key])
                         ])
        print(tabulate(body, headers, "outline"))

