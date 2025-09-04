from enum import Enum

class Constants:

    class Step(Enum):
        ANALYTICS = (1, "GA4 analytics file (.csv)")
        RESULT_FILE_NAME = (2, "Name of result file")
        FIELD_WEIGHTS = (3, "Weights of metrics")
        COL_NAMES = (4, "Name of columns in result file (2 columns)")
        REGEX = (5, "Regular expression for filtering analytics file by alias")
        FEED = (6, "(Optional) Feed with all items")
        FEED_MAPPING = (7, "Feed mapping")

        def __init__(self, code, message):
            self._value_ = code
            self.message = message

        @classmethod
        def get(cls, step: int):
            for i in Constants.Step:
                if i.value == step:
                    return i
            return None

    @classmethod
    def valueStr(cls, value):
        if value == None:
            return "<not_defined>"
        else:
            return str(value)


    class MsgType(Enum):
        REGULAR = 0
        HEADER = 1
        STEP = 2

    @classmethod
    def prnt(cls, msg: str, header = MsgType.REGULAR):
        def printOutlines(symb: str, times: int):
            print(symb * times)

        print()
        match header:
            case Constants.MsgType.REGULAR:
                print(msg)
            case Constants.MsgType.HEADER:
                printOutlines("=", 50)
                print(msg.upper())
                printOutlines("=", 50)
            case Constants.MsgType.STEP:
                printOutlines("-", 50)
                print(msg.upper())
                printOutlines("-", 50)

    @classmethod
    def inpt(cls, range: (int, int) = None, exit: int = 0):
        while True:
            try:
                inpt = int(input("Input: "))
                if inpt == exit:
                    return inpt
                elif r := range:
                    if r[0] <= int(inpt) <= r[1]:
                        return inpt
                    else:
                        continue
                else:
                    continue
            except:
                continue
