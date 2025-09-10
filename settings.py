from tabulate import tabulate
from enum import Enum

from constants import Constants
from regexHelper import RegexHelper

import textwrap
import configparser
import os
import ast


class Settings:

    # Constants

    class FeedType(Enum):
        UNDEFINED = 0
        CSV_FILE = 1
        URL = 2


    _configFile = "config.ini"
    class ConfigKey(Enum):
        USER_DEF = 0
        FEED = 1
        RESULT_FILE = 2
        FIELD_WEIGHTS = 3
        FW_VIEWS = 31
        FW_USERS = 32
        FW_VU_RATE = 33
        FW_TIME = 34
        FW_EVENTS = 35
        FW_K_EVENTS = 36
        COLUMN_NAMES = 4
        COL_NAME_SKU = 41
        COL_NAME_RATE = 42
        REGEX = 5
        FEED_MAPPING = 6
        FM_SKU_INDEX = 61
        FM_SKU_NAME = 611
        FM_ALIAS_INDEX = 62
        FM_ALIAS_NAME = 621


    class ColumnNames:
        sku = "ID"
        rate = "Popularity"

        def __str__(self):
            return f"{self.sku} & {self.rate}"
        
        def userDefDict(self):
            return {Settings.ConfigKey.COL_NAME_SKU.name: self.sku,
                    Settings.ConfigKey.COL_NAME_RATE.name: self.rate}
                
        def parseUserDef(self, userDef):
            if userDef != None:
                key = Settings.ConfigKey.COLUMN_NAMES.name
                if key in userDef:
                    colNames = ast.literal_eval(userDef[key])
                    self.sku = colNames[Settings.ConfigKey.COL_NAME_SKU.name]
                    self.rate = colNames[Settings.ConfigKey.COL_NAME_RATE.name]

        

    class FeedMapColumnNames:
        sku = None
        alias = None

        skuColName = ""
        aliasColName = ""

        def __str__(self):
            parts = []
            if self.skuColName != "":
                parts.append(f"{self.skuColName} ({self.sku + 1}) -> SKU")
            if self.aliasColName != "":
                parts.append(f"{self.aliasColName} ({self.alias + 1}) -> Alias")
            if len(parts) == 0:
                return Constants.valueStr(None)
            else:
                return "\n".join(parts)
            
        def userDefDict(self):
            return {Settings.ConfigKey.FM_SKU_INDEX.name: self.sku,
                    Settings.ConfigKey.FM_ALIAS_INDEX.name: self.alias,
                    Settings.ConfigKey.FM_SKU_NAME.name: self.skuColName,
                    Settings.ConfigKey.FM_ALIAS_NAME.name: self.aliasColName}
        
        def parseUserDef(self, userDef):
            if userDef != None:
                key = Settings.ConfigKey.FEED_MAPPING.name
                if key in userDef:
                    mapping = ast.literal_eval(userDef[key])
                    self.sku = mapping[Settings.ConfigKey.FM_SKU_INDEX.name]
                    self.alias = mapping[Settings.ConfigKey.FM_ALIAS_INDEX.name]
                    self.skuColName = mapping[Settings.ConfigKey.FM_SKU_NAME.name]
                    self.aliasColName = mapping[Settings.ConfigKey.FM_ALIAS_NAME.name]


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
            list = self.allElems()
            return sum(list)
        
        def userDefDict(self):
            return {Settings.ConfigKey.FW_VIEWS.name: self.views,
                    Settings.ConfigKey.FW_USERS.name: self.users,
                    Settings.ConfigKey.FW_VU_RATE.name: self.viewsUserRate,
                    Settings.ConfigKey.FW_TIME.name: self.avgTime,
                    Settings.ConfigKey.FW_EVENTS.name: self.events,
                    Settings.ConfigKey.FW_K_EVENTS.name: self.keyEvents}

        def parseUserDef(self, userDef):
            if userDef != None:
                key = Settings.ConfigKey.FIELD_WEIGHTS.name
                if key in userDef:
                    weights = ast.literal_eval(userDef[key])
                    self.views = weights[Settings.ConfigKey.FW_VIEWS.name]
                    self.users = weights[Settings.ConfigKey.FW_USERS.name]
                    self.viewsUserRate = weights[Settings.ConfigKey.FW_VU_RATE.name]
                    self.avgTime = weights[Settings.ConfigKey.FW_TIME.name]
                    self.events = weights[Settings.ConfigKey.FW_EVENTS.name]
                    self.keyEvents = weights[Settings.ConfigKey.FW_K_EVENTS.name]


    # Instance initialization

    def __init__(self):
        self.analytics = None
        self._feed = None
        self.resultFileName = ""
        self.fieldWeights = Settings.FieldWeight()
        self.columnNames = Settings.ColumnNames()
        self.regex = RegexHelper.ITEM_ALIAS
        self.feedMapping = Settings.FeedMapColumnNames()

        if os.path.isfile(self._configFile):            
            config = configparser.ConfigParser()
            config.read(self._configFile)

            userDefs = config[Settings.ConfigKey.USER_DEF.name]
            def getUserDef(key, default):
                if key in userDefs:
                    return userDefs[key]
                return default
            self.feed = getUserDef(Settings.ConfigKey.FEED.name, self.feed)
            self.resultFileName = getUserDef(Settings.ConfigKey.RESULT_FILE.name, self.resultFileName)
            self.regex = getUserDef(Settings.ConfigKey.REGEX.name, self.regex)
            self.regex = None if self.regex == "" else self.regex

            self.columnNames.parseUserDef(userDefs)
            self.feedMapping.parseUserDef(userDefs)
            self.fieldWeights.parseUserDef(userDefs)


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

    @property
    def feed(self):
        return self._feed
    @feed.setter
    def feed(self, source):
        if self._feed != source:
            self.feedMapping = Settings.FeedMapColumnNames()
        self._feed = source


    # Interface methods

    def save(self):
        config = configparser.ConfigParser()
        userDef = {}

        if f := self.feed:
            userDef[Settings.ConfigKey.FEED.name] = f
        userDef[Settings.ConfigKey.RESULT_FILE.name] = self.resultFileName
        userDef[Settings.ConfigKey.REGEX.name] = "" if self.regex == None else self.regex

        userDef[Settings.ConfigKey.FEED_MAPPING.name] = self.feedMapping.userDefDict()
        userDef[Settings.ConfigKey.COLUMN_NAMES.name] = self.columnNames.userDefDict()
        userDef[Settings.ConfigKey.FIELD_WEIGHTS.name] = self.fieldWeights.userDefDict()

        config[Settings.ConfigKey.USER_DEF.name] = userDef
        with open(self._configFile, "w") as file:
            config.write(file)


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
                        fieldValue = "You can find current regex\npattern below the table (*)"
            elif key == Constants.Step.FEED_MAPPING:
                fieldValue = str(dict[key])

            nameValue = "\n".join(textwrap.wrap(str(name), width=50))

            body.append([key.value,
                         nameValue,
                         fieldValue])
        print(tabulate(body, headers, "fancy_grid"))
        if f := fullRegex:
            print(fullRegex)

