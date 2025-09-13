import os
import csv
import requests
import xml.etree.ElementTree as ET

from constants import Constants
from settings import Settings
from regexHelper import RegexHelper


class CsvFileHelper:

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
            result = CsvFileHelper.Item()
            result.views = self.views + other.views
            result.users = self.users + other.users
            result.vuRate= self.vuRate + other.vuRate
            result.avgTime = self.avgTime + other.avgTime
            result.events = self.events + other.events
            result.kEvents = self.kEvents + other.kEvents
            return result

        def __truediv__(self, other):
            result = CsvFileHelper.Item()
            result.views = self.views / other
            result.users = self.users / other
            result.vuRate = self.vuRate / other
            result.avgTime = self.avgTime / other
            result.events = self.events / other
            result.kEvents = self.kEvents / other
            return result


    @classmethod
    def getCurrentFiles(cls, ignore=None):
        all_files = os.listdir(".")

        def filterRule(f):
            flag = (os.path.isfile(f)) & (Constants.extFileCheck(f))
            if i := ignore:
                return flag & (f != i)
            return flag

        result = [file for file in all_files if filterRule(file)]
        return result


    @classmethod
    def processFor(cls, settings: Settings):
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
        avgTotal = CsvFileHelper.Item()
        totalCounter = 0
        itemsDict = {}
        with open(settings.analytics) as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    a, v, u, vu, t, e, ke, _ = row
                    if key := cls.fetchKeyAlias(a):
                        if r := settings.regex:
                            if RegexHelper.isMatch(r, key):
                                pass
                            else:
                                continue
                        currentItem = CsvFileHelper.Item(v, u, vu, t, e, ke)
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
            if key := cls.fetchKeyAlias(alias):
                if key in itemsDict:
                    def calculate(current, avg, weight):
                        if (current == 0.0) | (avg == 0.0) | (weight == 0.0):
                                return 0.0
                        return current / avg * weight 
                    item: CsvFileHelper.Item = itemsDict[key]
                    rating = calculate(item.views, avgTotal.views, settings.fieldWeights.views)
                    rating += calculate(item.users, avgTotal.users, settings.fieldWeights.users)
                    rating += calculate(item.avgTime, avgTotal.avgTime, settings.fieldWeights.avgTime)
                    rating += calculate(item.events, avgTotal.events, settings.fieldWeights.events)
                    rating += calculate(item.kEvents, avgTotal.kEvents, settings.fieldWeights.keyEvents)
                    rating /= settings.fieldWeights.totalWeights()
                    rating *= 100.0    
                            
            return [sku, round(rating)]

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
                    if RegexHelper.isUrl(alias):
                        sku = row[settings.feedMapping.sku]
                        resultData.append(calculateRate(sku, alias))
                    
        
        with open(settings.resultFileName, "w") as file:
            writer = csv.writer(file)
            writer.writerows(resultData)



    @classmethod
    def fetchKeyAlias(cls, source):
        elems = source.split("/")
        if len(elems) >= 3:
            return elems[-2]
        return None


    @classmethod
    def preview(cls, path: str, rowsPreview = 2):
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
                            body.append([Constants.shrink(item, 30) for item in row])
                    if i == rowsPreview:
                        break
            body.append(["..." for _ in range(len(header))])
        return (header, body)