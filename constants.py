from enum import Enum

class Constants:

    class Step(Enum):
        ANALYTICS = (1, "GA4 analytics file (.csv)")
        RESULT_FILE_NAME = (2, "Name of result file")
        FIELD_WEIGHTS = (3, "Weights of fields (usrs-avg_tm-evnts-eng_rt)")
        COL_NAMES = (4, "Name of columns in result file (2 columns)")
        REGEX = (5, "Regular expression for filtering analytics file")
        FEED = (6, "(Optional) Feed with all items (.csv or url of )")

        def __init__(self, code, message):
            self._value_ = code
            self.message = message

    @classmethod
    def valueStr(cls, value):
        if value == None:
            return "<not_defined>"
        else:
            return str(value)