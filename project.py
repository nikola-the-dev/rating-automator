import sys

from constants import Constants
from settings import Settings
from wizard import Wizard
from csvFileHelper import CsvFileHelper


settings = Settings()

def main():
    if len(sys.argv) == 2:
        analytics = sys.argv[1]
        try:
            if Constants.fileCheck(analytics):
                settings.analytics = analytics
        except:
            pass
    Constants.prnt("Rating Automator", Constants.MsgType.HEADER)
    while True:
        Constants.prnt("Settings:")
        settings.summary()
        Constants.prnt("To change any setting parameter, enter the appropriate Key number from the table,")
        print("or enter 9 to start calculations and generate the final file")
        print()
        code = Constants.inpt(range=(1, len(Constants.Step)), exit=9)
        if code == 9:
            try:
                CsvFileHelper.processFor(settings)
                Constants.prnt("Success!")
                print(f"You can find the result in {settings.resultFileName} file")
                print()
                break
            except ValueError as ve:
                e = str(ve)
                Constants.prnt(e)
                match e[0]:
                    case "1":
                        Wizard.promptFor(settings, Constants.Step.ANALYTICS)
                    case "6":
                        Wizard.promptFor(settings, Constants.Step.FEED)
            except FileNotFoundError as fe:
                e = str(fe)
                Constants.prnt(e)
                match e[0]:
                    case "1":
                        settings.analytics = None
                        Wizard.promptFor(settings, Constants.Step.ANALYTICS)
                    case "6":
                        settings.feed = None
                        Wizard.promptFor(settings, Constants.Step.FEED)
        elif step := Constants.Step(code):
            Wizard.promptFor(settings, step)
        
        settings.save()


if __name__ == "__main__":
    main()