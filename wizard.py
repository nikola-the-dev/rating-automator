from dataclasses import field

from settings import Settings
from csvFileHelper import CsvFileHelper
from enum import Enum

class Wizard:

    class Step(Enum):
        FINISHED = -1
        ANALYTICS = 0
        RESULT_FILE_NAME = 1
        FIELD_WEIGHTS = 2

    @classmethod
    def stepFor(cls, settings):
        if settings.analytics == None:
            return Wizard.Step.ANALYTICS
        elif settings.resultFileName == None:
            return Wizard.Step.RESULT_FILE_NAME
        elif settings.fieldWeights == None:
            return  Wizard.Step.FIELD_WEIGHTS
        return Wizard.Step.FINISHED

    @classmethod
    def promptFor(cls, settings: Settings):
        step = cls.stepFor(settings)
        Wizard.promptAt(step, settings)

    @classmethod
    def promptAt(cls, step: Step, settings: Settings):
        match step:
            case Wizard.Step.ANALYTICS:
                print()
                print("You didn't specify the analytics file name in the input arguments.")
                list = CsvFileHelper.getCurrentFiles(settings.feed)
                def fileErrMsg():
                    print()
                    print("Some problems with file path you've provided")
                    print()
                if len(list) > 0:
                    print()
                    print("But we found some file(s) in the current folder:")
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
                        print()
                        file = input("Enter file path: ")
                        try:
                            CsvFileHelper.fileCheck(file)
                            settings.analytics = file
                            break
                        except:
                            fileErrMsg()
                            continue

            case Wizard.Step.RESULT_FILE_NAME:
                print()
                print("(Optional) You can define result file name or leave empty for default value.")
                print(f"By default it's: {Settings.defaultResultName}")
                print()
                settings.resultFileName = input("Input: ")

            case Wizard.Step.FIELD_WEIGHTS:
                fieldWeights = Settings.FieldWeight()
                print()
                print("(Optional) You can define field weights in the following format:")
                print("xx-xx-xx-xx")
                print(", where xx is a value of weight for Number of Users, Average Time, Number of Events and Engagement Rate respectively.")
                print("Or leave empty for default values.")
                print("By default it's:")
                fieldWeights.printWeights()
                print()
                while True:
                    inpt = input("Input: ")
                    if inpt == "":
                        settings.fieldWeights = fieldWeights
                        break
                    else:
                        list = inpt.split("-")
                        if len(list) != 4:
                            print("There are should be 4 weights integer values in following format: xx-xx-xx-xx")
                            continue
                        else:
                            newWeights = Settings.FieldWeight()
                            flag = True
                            for i, item in enumerate(list):
                                if item.isdigit():
                                    match i:
                                        case 0:
                                            newWeights.user = int(item)
                                        case 1:
                                            newWeights.avgTime = int(item)
                                        case 2:
                                            newWeights.events = int(item)
                                        case 1:
                                            newWeights.engagement = int(item)
                                else:
                                    flag = False
                                    continue
                            settings.fieldWeights = newWeights
                            if flag:
                                break

            case 3:
                print("2")