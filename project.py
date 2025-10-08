from tabulate import tabulate
import requests

from enum import Enum
import sys
import os
import textwrap
import configparser
import ast
import builtins
import csv
import xml.etree.ElementTree as ET
import re


def extFileCheck(file):
    return file.lower().endswith(".csv")


class Settings:

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
                return valueStr(None)
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
        self.regex = ITEM_ALIAS
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
            if isUrl(f):
                return Settings.FeedType.URL
            elif extFileCheck(f):
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
        if extFileCheck(r) == False:
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
        dict = {Step.ANALYTICS: self.analytics,
                Step.RESULT_FILE_NAME: self.resultFileName,
                Step.FIELD_WEIGHTS: self.fieldWeights,
                Step.COL_NAMES: self.columnNames,
                Step.REGEX: self.regex,
                Step.FEED: self.feed,
                Step.FEED_MAPPING: self.feedMapping
                }
        body = []
        fullRegex = None
        for key in Step:
            if (key == Step.FEED_MAPPING) & (self.feedType != Settings.FeedType.CSV_FILE):
                continue
            name = str(key)
            fieldValue = valueStr(dict[key])
            if key == Step.FIELD_WEIGHTS:
                name += " (Views - Users - Views/User_Rate - Avg.Time - Events - Key_Events)"
            elif key == Step.FEED:
                name += " (.csv file or link to Google Merchant Center .xml file)"
            elif key == Step.REGEX:
                if r := dict[key]:
                    if len(r) > 30:
                        fullRegex = f"(*) {key.value}. Full regex:\n{r}"
                        fieldValue = "You can find current regex\npattern below the table (*)"
            elif key == Step.FEED_MAPPING:
                fieldValue = str(dict[key])

            nameValue = "\n".join(textwrap.wrap(str(name), width=50))

            body.append([key.value,
                         nameValue,
                         fieldValue])
        print(tabulate(body, headers, "fancy_grid"))
        if f := fullRegex:
            print(fullRegex)


URL_RE = "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
ITEM_ALIAS = "^.*-([a-z]{1,7}[0-9]{1,9}[a-z]{1,9}(([0-9]{1,5}[a-z]{1,5}[0-9]?)|(-l))?|[a-z]{3,4}-[0-9]{3,6}|[0-9]{4,7}-[a-z]{1,4}|[a-z]{2}[0-9]{2,3}-[a-z]{2}-[0-9]{1,3})$"

class Step(Enum):
    ANALYTICS = 1
    RESULT_FILE_NAME = 2
    FIELD_WEIGHTS = 3
    COL_NAMES = 4
    REGEX = 5
    FEED = 6
    FEED_MAPPING = 7

    def __str__(self):
        match self:
            case self.ANALYTICS:
                return "(Required) GA4 analytics file (.csv)"
            case self.RESULT_FILE_NAME:
                return "Name of result file"
            case self.FIELD_WEIGHTS:
                return "Weights of metrics"
            case self.COL_NAMES:
                return "Name of columns in result file (2 columns)"
            case self.REGEX:
                return "Regular expression for filtering aliases in analytics file"
            case self.FEED:
                return "(Required) Feed with all items"
            case self.FEED_MAPPING:
                return "(Required) Feed file columns mapping"
        return self.name



settings = Settings()

def main():
    if len(sys.argv) == 2:
        analytics = sys.argv[1]
        try:
            if fileCheck(analytics):
                settings.analytics = analytics
        except:
            pass
    prnt("Rating Automator", MsgType.HEADER)
    while True:
        prnt("Settings:")
        settings.summary()
        prnt("To change any setting parameter, enter the appropriate Key number from the table,")
        print("or enter 9 to start calculations and generate the final file")
        print()
        code = raInpt(range=(1, len(Step)), exit=9)
        if code == 9:
            try:
                processCsvFor(settings)
                prnt("Success!")
                print(f"You can find the result in {settings.resultFileName} file")
                print()
                break
            except ValueError as ve:
                e = str(ve)
                prnt(e)
                match e[0]:
                    case "1":
                        promptFor(settings, Step.ANALYTICS)
                    case "6":
                        promptFor(settings, Step.FEED)
            except FileNotFoundError as fe:
                e = str(fe)
                prnt(e)
                match e[0]:
                    case "1":
                        settings.analytics = None
                        promptFor(settings, Step.ANALYTICS)
                    case "6":
                        settings.feed = None
                        promptFor(settings, Step.FEED)
        elif step := Step(code):
            promptFor(settings, step)

        settings.save()


def fileCheck(file):
    if extFileCheck(file):
        raise ValueError
    if not os.path.exists(file):
        raise FileNotFoundError
    return True


def isUrl(source):
    return isMatch(URL_RE, source)


def isMatch(pattern, source):
    rawPattern = r"{}".format(pattern)
    return re.search(rawPattern, source, re.IGNORECASE)


def valueStr(value):
    if value == None:
        return "<not_defined>"
    else:
        return shrink(str(value))


def shrink(source: str, maxLength: int = 30):
    if len(source) <= maxLength:
        return source
    elif maxLength <= 10:
        return source
    part = (maxLength - 3) // 2
    return source[:part] + "..." + source[len(source) - part:]

class MsgType(Enum):
    REGULAR = 0
    HEADER = 1
    STEP = 2
def prnt(msg: str, header = MsgType.REGULAR):
    def printOutlines(symb: str, times: int = 80):
        print(symb * times)

    print()
    match header:
        case MsgType.REGULAR:
            print(msg)
        case MsgType.HEADER:
            printOutlines("═")
            print(msg.upper())
            printOutlines("═")
        case MsgType.STEP:
            printOutlines("─")
            print(msg.upper())
            printOutlines("─")

class InputType(Enum):
    NUMBER = 0
    STRING = 1
    CSV_FILE = 2
    CSV_FILE_OR_XML_LINK = 3
def raInpt(title: str = "Input: ", 
           range: (int, int) = None, 
           exclude: int = None, 
           type = InputType.NUMBER, 
           exit: int = 0, 
           emptyAllowed = False):
    
    while True:
        inpt = input(title)
        if inpt == "":
            if emptyAllowed:
                return ""
            else:
                continue
        try:
            number = int(inpt)
            if number == exit:
                return number
            elif r := range:
                if r[0] <= number <= r[1]:
                    if e := exclude:
                        if e == number:
                            continue
                    return number
                else:
                    continue
            else:
                return number
        except:
            match type:
                case InputType.NUMBER:
                    continue
                case InputType.STRING:
                    return inpt
                case InputType.CSV_FILE:
                    try:
                        _ = fileCheck(inpt)
                        return inpt
                    except:
                        prnt("There is some problem with file")
                        continue
                case InputType.CSV_FILE_OR_XML_LINK:
                    try:
                        _ = fileCheck(inpt)
                        return inpt
                    except:
                        if isUrl(inpt):
                            return inpt
                        else:
                            continue


def promptFor(settings: Settings, step: Step):
    def cancelMsg():
        print("Type 0 to cancel")
        print()

    prnt(f"{step.value}. {str(step)}:", MsgType.STEP)
    match step:
        case Step.ANALYTICS:
            list = getCurrentCsvFiles(settings.feed)
            range = None
            if len(list) > 0:
                prnt("We found some file(s) in the current folder:")
                for i, f in enumerate(list):
                    print(f"{i + 1}. {f}")
                prnt("Select one by entering file's key number or enter file path")
                range = (1, len(list))
            else:
                prnt("Enter path to analytics file")

            cancelMsg()
            inpt = raInpt(range=range, type=InputType.CSV_FILE)
            match type(inpt):
                case builtins.int:
                    if inpt == 0:
                        return
                    else:
                        settings.analytics = list[inpt - 1]
                case builtins.str:
                    settings.analytics = inpt

        case Step.RESULT_FILE_NAME:
            cancelMsg()
            inpt = raInpt(type=InputType.STRING)
            match type(inpt):
                case builtins.str:
                    settings.resultFileName = inpt

        case Step.FIELD_WEIGHTS:
            settings.fieldWeights.views = raInpt(title="Views: ")
            settings.fieldWeights.users = raInpt(title="Users: ")
            settings.fieldWeights.viewsUserRate = raInpt(title="Views per User Rate: ")
            settings.fieldWeights.avgTime = raInpt(title="Avg. Time: ")
            settings.fieldWeights.events = raInpt(title="Events: ")
            settings.fieldWeights.keyEvents = raInpt(title="Key Events: ")

        case Step.COL_NAMES:
            cancelMsg()
            for i, t in enumerate(["ID: ", "Rate: "]):
                inpt = raInpt(title=t, type=InputType.STRING)
                colName = inpt
                match type(inpt):
                    case builtins.int:
                        if inpt == 0:
                            return
                        else:
                            colName = str(inpt)
                if i == 0:
                    settings.columnNames.sku = colName
                else:
                    settings.columnNames.rate = colName

        case Step.REGEX:
            prnt("You can use default regular expression:")
            print(ITEM_ALIAS)
            print("...or you can enter any regex on your own.")
            prnt("To use default regex - enter 'd'")
            print("If you do not want to use any regex - leave input empty (in this case it takes into account whole data from analytics file except headers).")
            print()
            cancelMsg()
            re = raInpt(type=InputType.STRING, emptyAllowed=True)
            match type(re):
                case builtins.str:
                    if re == "":
                        settings.regex = None
                    elif re[0] == "d":
                        settings.regex = ITEM_ALIAS
                    else:
                        settings.regex = re

        case Step.FEED:
            list = getCurrentCsvFiles(settings.analytics)
            range = None
            enterMsg = "Enter path to csv feed file or enter URL to xml of Google Feed for Merchant Center"
            if len(list) > 0:
                prnt("We found some file(s) in the current folder:")
                for i, f in enumerate(list):
                    print(f"{i + 1}. {f}")
                prnt(f"Select one by entering file's key number, {enterMsg.lower()}")
                range = (1, len(list))
            else:
                prnt(enterMsg)

            cancelMsg()
            inpt = raInpt(range=range, type=InputType.CSV_FILE_OR_XML_LINK)
            match type(inpt):
                case builtins.int:
                    if inpt == 0:
                        return
                    else:
                        settings.feed = list[inpt - 1]
                        promptFor(settings, Step.FEED_MAPPING)
                case builtins.str:
                    settings.feed = inpt
                    if not isUrl(inpt):
                        promptFor(settings, Step.FEED_MAPPING)

        case Step.FEED_MAPPING:
            prnt("Feed file preview:")
            h, b = preview(settings.feed)
            finalHeader = [f"{i + 1}\n{t}" for i, t in enumerate(h)]
            print(tabulate(b, finalHeader, "fancy_grid"))
            prnt("Enter the table column number that corresponds to the value.")
            cancelMsg()
            for i, t in enumerate(["SKU: ", "Alias: "]):
                inpt = raInpt(title=t,
                              exclude=None if i == 0 else (settings.feedMapping.sku + 1),
                              range=(1, len(h)))
                match type(inpt):
                    case builtins.int:
                        if inpt == 0:
                            return
                        else:
                            index = inpt - 1
                            colTitle = h[index]
                            if i == 0:
                                settings.feedMapping.sku = index
                                settings.feedMapping.skuColName = colTitle
                            else:
                                settings.feedMapping.alias = index
                                settings.feedMapping.aliasColName = colTitle


class Item():
    views = 0.0
    users = 0.0
    vuRate = 0.0
    avgTime = 0.0
    events = 0.0
    kEvents = 0.0

    def __init__(self, *args):
        if len(args) == 6:
            self.views = float(args[0])
            self.users = float(args[1])
            self.vuRate = float(args[2])
            self.avgTime = float(args[3])
            self.events = float(args[4])
            self.kEvents = float(args[5])

    def __add__(self, other):
        result = Item()
        result.views = self.views + other.views
        result.users = self.users + other.users
        result.vuRate= self.vuRate + other.vuRate
        result.avgTime = self.avgTime + other.avgTime
        result.events = self.events + other.events
        result.kEvents = self.kEvents + other.kEvents
        return result

    def __truediv__(self, other):
        result = Item()
        result.views = self.views / other
        result.users = self.users / other
        result.vuRate = self.vuRate / other
        result.avgTime = self.avgTime / other
        result.events = self.events / other
        result.kEvents = self.kEvents / other
        return result


def getCurrentCsvFiles(ignore=None):
    all_files = os.listdir(".")

    def filterRule(f):
        flag = (os.path.isfile(f)) & (extFileCheck(f))
        if i := ignore:
            return flag & (f != i)
        return flag

    result = [file for file in all_files if filterRule(file)]
    return result


def processCsvFor(settings: Settings):
    if a := settings.analytics:
        if not os.path.isfile(a):
            raise FileNotFoundError("1. There is some problem with analytics file")
    else:
        raise ValueError("1. You did not set analytics file")
    if f := settings.feed:
        if settings.feedType == Settings.FeedType.CSV_FILE:
            if not os.path.isfile(a):
                raise FileNotFoundError("6. There is some problem with feed file")
    else:
        raise ValueError("6. You did not set any feed source")
    avgTotal = Item()
    totalCounter = 0
    itemsDict = {}
    with open(settings.analytics) as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                a, v, u, vu, t, e, ke, _ = row
                if key := fetchKeyAlias(a):
                    if r := settings.regex:
                        if isMatch(r, key):
                            pass
                        else:
                            continue
                    currentItem = Item(v, u, vu, t, e, ke)
                    if key in itemsDict.keys():
                        currentItem += itemsDict[key]
                    itemsDict[key] = currentItem

                    avgTotal += currentItem
                    totalCounter += 1
            except:
                continue
    avgTotal /= totalCounter

    resultData = [[settings.columnNames.sku, settings.columnNames.rate]]

    def calculateRate(sku, alias):
        rating = 0.0
        if key := fetchKeyAlias(alias):
            if key in itemsDict:
                def calculate(current, avg, weight):
                    if (current == 0.0) | (avg == 0.0) | (weight == 0.0):
                            return 0.0
                    return current / avg * weight 
                item: Item = itemsDict[key]
                rating = calculate(item.views, avgTotal.views, settings.fieldWeights.views)
                rating += calculate(item.users, avgTotal.users, settings.fieldWeights.users)
                rating += calculate(item.avgTime, avgTotal.avgTime, settings.fieldWeights.avgTime)
                rating += calculate(item.events, avgTotal.events, settings.fieldWeights.events)
                rating += calculate(item.kEvents, avgTotal.kEvents, settings.fieldWeights.keyEvents)
                rating /= settings.fieldWeights.totalWeights()
                rating *= 100.0    
                        
        return [sku, rating]

    if settings.feedType == Settings.FeedType.URL:
        response = requests.get(settings.feed)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            items = root.find("channel").findall("item")
            ns = {"g": "http://base.google.com/ns/1.0"}
            for item in items:
                sku = item.find("g:id", ns).text
                alias = item.find("g:link", ns).text
                resultData.append(calculateRate(sku, alias))
        else:
            raise FileNotFoundError("6. There is some problem with link you have provided")

    else:
        with open(settings.feed) as file:
            reader = csv.reader(file)
            for row in reader:        
                alias = row[settings.feedMapping.alias]
                if isUrl(alias):
                    sku = row[settings.feedMapping.sku]
                    resultData.append(calculateRate(sku, alias))
                
    
    with open(settings.resultFileName, "w") as file:
        writer = csv.writer(file)
        writer.writerows(resultData)



def fetchKeyAlias(source):
    elems = source.split("/")
    if len(elems) >= 3:
        return elems[-2]
    return None


def preview(path: str, rowsPreview = 2):
    header = []
    body = []
    if rowsPreview > 0:
        with open(path) as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                match i:
                    case 0:
                        header = row
                    case _:
                        body.append([shrink(item, 30) for item in row])
                if i == rowsPreview:
                    break
        body.append(["..." for _ in range(len(header))])
    return (header, body)                                


if __name__ == "__main__":
    main()
