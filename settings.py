from tabulate import tabulate
from enum import Enum

from constants import Constants
from regexHelper import RegexHelper

import textwrap


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

    class FeedMapColumnNames:
        sku = None
        alias = None

        skuColName = ""
        aliasColName = ""

        def __str__(self):
            parts = []
            if s := self.sku:
                parts.append(f"{self.skuColName} ({s}) is for SKU values")
            if a := self.alias:
                parts.append(f"{self.aliasColName} ({a}) is for item alias values")
            return "; ".join(parts)


    class FieldWeight:

        def __init__(self):
            self.views = 0
            self.users = 5
            self.viewsUserRate = 5
            self.avgTime = 10
            self.events = 20
            self.keyEvents = 30

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
        self.resultFileName = ""
        self.fieldWeights = Settings.FieldWeight()
        self.columnNames = Settings.ColumnNames()
        self.regex = RegexHelper.ITEM_ALIAS
        self.feedMapping = None


    # Variables

    @property
    def feedType(self):
        if f := self.feed:
            if RegexHelper.isUrl(f):
                return Settings.FeedType.URL
            elif Constants.extFileCheck(f):
                return Settings.FeedType.CSV_FILE
        return Settings.FeedType.UNDEFINED

    @property
    def resultFileName(self):
        return self._resultFileName
    @resultFileName.setter
    def resultFileName(self, result):
        r = result
        if r == "":
            r = "result"
        if Constants.extFileCheck(r) == False:
            r += ".csv"
        self._resultFileName = r


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
        fullRegex = None
        for key in Constants.Step:
            if (key == Constants.Step.FEED_MAPPING) & (self.feedType != Settings.FeedType.CSV_FILE):
                continue
            name = str(key)
            fieldValue = Constants.valueStr(dict[key])
            if key == Constants.Step.FIELD_WEIGHTS:
                name += " (Views - Users - Views/User_Rate - Avg.Time - Events - Key_Events)"
            elif key == Constants.Step.FEED:
                name += " (.csv file or link to Google Merchant Center .xml file)"
            elif key == Constants.Step.REGEX:
                if r := dict[key]:
                    if len(r) > 30:
                        fullRegex = f"(*) {key.value}. Full regex:\n{r}"
                        fieldValue = "You can find current regex pattern below the table (*)"

            nameValue = "\n".join(textwrap.wrap(str(name), width=50))

            body.append([key.value,
                         nameValue,
                         fieldValue])
        print(tabulate(body, headers, "fancy_grid"))
        if f := fullRegex:
            print(fullRegex)

