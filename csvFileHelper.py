import os
import csv
from sys import flags

from constants import Constants
from settings import Settings


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
        avgTotal = CsvFileHelper.Item()
        itemsDict = {}
        with open(settings.analytics) as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    a, v, u, vu, t, e, ke, _ = row
                    elems = a.split("/")
                    if len(elems) >= 3:
                        key = elems[-2]
                        currentItem = CsvFileHelper.Item(v, u, vu, t, e, ke)
                        if key in itemsDict.keys():
                            currentItem += itemsDict[key]
                        itemsDict[key] = currentItem

                        flag = avgTotal.users != 0
                        avgTotal += currentItem
                        if flag:
                            avgTotal /= 2
                except:
                    continue

