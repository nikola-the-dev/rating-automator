from dataclasses import field

from settings import Settings
from csvFileHelper import CsvFileHelper
from constants import Constants

class Wizard:

    @classmethod
    def promptAt(cls, step: Constants.Step, settings: Settings):
        print()
        print(f"{step.value}. {step.message}:")
        print()
        match step:
            case Constants.Step.ANALYTICS:
                list = CsvFileHelper.getCurrentFiles(settings.feed)
                def fileErrMsg():
                    print()
                    print("Some problems with file path you've provided")
                    print()
                if len(list) > 0:
                    print("We found some file(s) in the current folder:")
                    while True:
                        for i, f in enumerate(list):
                            print(f"{i + 1}. {f}")
                        print()
                        print("Select one (specify file number) or enter file path:")
                        print()
                        inpt = input("Input: ")
                        if inpt.isdigit():
                            n = int(inpt)
                            if n < len(list):
                                settings.analytics = list[n]
                                break
                            else:
                                print("You enter wrong number of file")
                        else:
                            try:
                                CsvFileHelper.fileCheck(inpt)
                                settings.analytics = inpt
                                break
                            except:
                                fileErrMsg()
                                continue

                else:
                    while True:
                        for i, f in enumerate(list):
                            print(f"{i + 1}. {f}")
                        file = input("Enter file path: ")
                        try:
                            CsvFileHelper.fileCheck(file)
                            settings.analytics = file
                            break
                        except:
                            fileErrMsg()
                            continue

            case Constants.Step.RESULT_FILE_NAME:
                settings.resultFileName = input("Input: ")

            case Constants.Step.FIELD_WEIGHTS:
                print("You can define field weights in the following format:")
                print("xx-xx-xx-xx")
                print(", where xx is a value of weight for Number of Users (usrs), Average Time (avg_tm), Number of Events (evnts) and Engagement Rate (eng_rt) respectively.")
                print()
                while True:
                    inpt = input("Input: ")
                    list = inpt.split("-")
                    if len(list) != 4:
                        print("There are should be 4 weights integer values in following format: xx-xx-xx-xx")
                        continue
                    else:
                        fieldWeights = Settings.FieldWeight()
                        flag = True
                        for i, item in enumerate(list):
                            if item.isdigit():
                                match i:
                                    case 0:
                                        fieldWeights.user = int(item)
                                    case 1:
                                        fieldWeights.avgTime = int(item)
                                    case 2:
                                        fieldWeights.events = int(item)
                                    case 3:
                                        fieldWeights.engagement = int(item)
                            else:
                                flag = False
                                continue
                        settings.fieldWeights = fieldWeights
                        if flag:
                            break

            case 3:
                print("2")