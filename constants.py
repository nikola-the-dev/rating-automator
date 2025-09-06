import os

from enum import Enum
from regexHelper import RegexHelper

class Constants:

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


    @classmethod
    def valueStr(cls, value):
        if value == None:
            return "<not_defined>"
        else:
            return Constants.shrink(str(value))


    @classmethod
    def shrink(cls, source: str, maxLength: int = 30):
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

    @classmethod
    def prnt(cls, msg: str, header = MsgType.REGULAR):
        def printOutlines(symb: str, times: int = 80):
            print(symb * times)

        print()
        match header:
            case cls.MsgType.REGULAR:
                print(msg)
            case cls.MsgType.HEADER:
                printOutlines("═")
                print(msg.upper())
                printOutlines("═")
            case cls.MsgType.STEP:
                printOutlines("─")
                print(msg.upper())
                printOutlines("─")

    class InputType(Enum):
        NUMBER = 0
        STRING = 1
        CSV_FILE = 2
        CSV_FILE_OR_XML_LINK = 3
    @classmethod
    def inpt(cls, title: str = "Input: ",
             range: (int, int) = None,
             type = InputType.NUMBER,
             exit: int = 0,
             emptyAllowed = False
             ):
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
                    if r[0] <= int(inpt) <= r[1]:
                        return number
                    else:
                        continue
                else:
                    return number
            except:
                match type:
                    case Constants.InputType.NUMBER:
                        continue
                    case Constants.InputType.STRING:
                        return inpt
                    case Constants.InputType.CSV_FILE:
                        try:
                            _ = cls.fileCheck(inpt)
                            return inpt
                        except:
                            Constants.prnt("There is some problem with file")
                            continue
                    case Constants.InputType.CSV_FILE_OR_XML_LINK:
                        try:
                            _ = cls.fileCheck(inpt)
                            return inpt
                        except:
                            if RegexHelper.isUrl(inpt):
                                return inpt
                            else:
                                continue

    @classmethod
    def fileCheck(cls, file):
        if cls.extFileCheck(file):
            raise ValueError
        if not os.path.exists(file):
            raise FileNotFoundError
        return True

    @classmethod
    def extFileCheck(cls, file):
        return file.lower().endswith(".csv")