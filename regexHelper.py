import re

class RegexHelper:

    URL_RE = "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
    ITEM_ALIAS = "^.*-([a-z]{1,7}[0-9]{1,9}[a-z]{1,9}(([0-9]{1,5}[a-z]{1,5}[0-9]?)|(-l))?|[a-z]{3,4}-[0-9]{3,6}|[0-9]{4,7}-[a-z]{1,4}|[a-z]{2}[0-9]{2,3}-[a-z]{2}-[0-9]{1,3})$"

    @classmethod
    def isUrl(cls, source):
        return cls.isMatch(cls.URL_RE, source)

    @classmethod
    def isMatch(cls, pattern, source):
        rawPattern = r"{}".format(pattern)
        return re.search(rawPattern, source, re.IGNORECASE)