import os

class CsvFileHelper:

    @classmethod
    def getCurrentFiles(cls, ignore=None):
        all_files = os.listdir(".")

        def filterRule(f):
            flag = (os.path.isfile(f)) & (CsvFileHelper.extFileCheck(f))
            if i := ignore:
                return flag & (f != i)
            return flag

        result = [file for file in all_files if filterRule(file)]
        return result

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
