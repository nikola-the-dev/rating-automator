from dataclasses import field

from settings import Settings
from csvFileHelper import CsvFileHelper
from constants import Constants

import builtins

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
                Constants.prnt("You can define the raw regular expression (regex)")
                print("or you can enter simplified version of it by starting 's'-symbol.")
                Constants.prnt("So, simplified regex starts with 's'-symbol.")
                print("Then in pattern you can mark 'x' for any symbol,")
                print("'n' is for digit,")
                print("and '*' is for any amount of symbols.")
                print("For example if your alias looks like:")
                print("https://somesite.com/target-item-sku5522-smth")
                print("You can define simplified regex as:")
                print("s*xxxnnnn-xxxx")
                Constants.prnt("Leave empty if you do not want to filter items by regex and take into account whole data.")
                print()
                cancelMsg()
                re = Constants.inpt(type=Constants.InputType.STRING, emptyAllowed=True)
                match type(re):
                    case builtins.str:
                        if re == "":
                            settings.regexSimplified = None
                            settings.regex = None
                        elif re[0] == "s":
                            settings.regexSimplified = re
                            settings.regex = re
                        else:
                            settings.regexSimplified = None
                            settings.regex = re

            case Constants.Step.FEED_MAPPING:
                print("2")