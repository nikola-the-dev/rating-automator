import builtins

from tabulate import tabulate

from settings import Settings
from csvFileHelper import CsvFileHelper
from constants import Constants
from regexHelper import RegexHelper


class Wizard:

    @classmethod
    def promptFor(cls, settings: Settings, step: Constants.Step):
        def cancelMsg():
            print("Type 0 to cancel")
            print()

        Constants.prnt(f"{step.value}. {str(step)}:", Constants.MsgType.STEP)
        match step:
            case Constants.Step.ANALYTICS:
                list = CsvFileHelper.getCurrentFiles(settings.feed)
                range = None
                if len(list) > 0:
                    Constants.prnt("We found some file(s) in the current folder:")
                    for i, f in enumerate(list):
                        print(f"{i + 1}. {f}")
                    Constants.prnt("Select one by entering file's key number or enter file path")
                    range = (1, len(list))
                else:
                    Constants.prnt("Enter path to analytics file")

                cancelMsg()
                inpt = Constants.inpt(range=range,
                                      type=Constants.InputType.CSV_FILE)
                match type(inpt):
                    case builtins.int:
                        if inpt == 0:
                            return
                        else:
                            settings.analytics = list[inpt - 1]
                    case builtins.str:
                        settings.analytics = inpt

            case Constants.Step.RESULT_FILE_NAME:
                cancelMsg()
                inpt = Constants.inpt(type=Constants.InputType.STRING)
                match type(inpt):
                    case builtins.str:
                        settings.resultFileName = inpt

            case Constants.Step.FIELD_WEIGHTS:
                settings.fieldWeights.views = Constants.inpt(title="Views: ")
                settings.fieldWeights.users = Constants.inpt(title="Users: ")
                settings.fieldWeights.viewsUserRate = Constants.inpt(title="Views per User Rate: ")
                settings.fieldWeights.avgTime = Constants.inpt(title="Avg. Time: ")
                settings.fieldWeights.events = Constants.inpt(title="Events: ")
                settings.fieldWeights.keyEvents = Constants.inpt(title="Key Events: ")

            case Constants.Step.COL_NAMES:
                cancelMsg()
                for i, t in enumerate(["ID: ", "Rate: "]):
                    inpt = Constants.inpt(title=t, type=Constants.InputType.STRING)
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

            case Constants.Step.REGEX:
                Constants.prnt("You can use default regular expression:")
                print(RegexHelper.ITEM_ALIAS)
                print("...or you can enter any regex on your own.")
                Constants.prnt("To use default regex - enter 'd'")
                print("If you do not want to use any regex - leave input empty (in this case it takes into account whole data from analytics file except headers).")
                print()
                cancelMsg()
                re = Constants.inpt(type=Constants.InputType.STRING, emptyAllowed=True)
                match type(re):
                    case builtins.str:
                        if re == "":
                            settings.regex = None
                        elif re[0] == "d":
                            settings.regex = RegexHelper.ITEM_ALIAS
                        else:
                            settings.regex = re

            case Constants.Step.FEED:
                list = CsvFileHelper.getCurrentFiles(settings.analytics)
                range = None
                enterMsg = "Enter path to csv feed file or enter URL to xml of Google Feed for Merchant Center"
                if len(list) > 0:
                    Constants.prnt("We found some file(s) in the current folder:")
                    for i, f in enumerate(list):
                        print(f"{i + 1}. {f}")
                    Constants.prnt(f"Select one by entering file's key number, {enterMsg.lower()}")
                    range = (1, len(list))
                else:
                    Constants.prnt(enterMsg)

                cancelMsg()
                inpt = Constants.inpt(range=range,
                                      type=Constants.InputType.CSV_FILE_OR_XML_LINK)
                match type(inpt):
                    case builtins.int:
                        if inpt == 0:
                            return
                        else:
                            settings.feed = list[inpt - 1]
                            cls.promptFor(settings, Constants.Step.FEED_MAPPING)
                    case builtins.str:
                        settings.feed = inpt
                        if not RegexHelper.isUrl(inpt):
                            cls.promptFor(settings, Constants.Step.FEED_MAPPING)

            case Constants.Step.FEED_MAPPING:
                Constants.prnt("Feed file preview:")
                h, b = CsvFileHelper.preview(settings.feed)
                h = [f"{i + 1}\n{t}" for i, t in enumerate(h)]
                print(tabulate(b, h, "fancy_grid"))
                Constants.prnt("Enter the table column number that corresponds to the value.")
                cancelMsg()
                inpt = Constants.inpt(title="SKU: ",
                                      range=(1, len(h)),
                                      type=Constants.InputType.CSV_FILE_OR_XML_LINK)
                