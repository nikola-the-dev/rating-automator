from constants import Constants
from settings import Settings
from wizard import Wizard
from csvFileHelper import CsvFileHelper

import sys


settings = Settings()

def main():
    Constants.prnt("Rating Automator", Constants.MsgType.HEADER)
    while True:
        Constants.prnt("Settings:")
        settings.summary()
        Constants.prnt("To change any setting parameter, enter the appropriate Key number from the table,")
        print("or enter 9 to start calculations and generate the final file")
        print()
        code = Constants.inpt(range=(1, len(Constants.Step)), exit=9)
        if code == 9:
            if settings.analytics == None:
                Wizard.promptFor(settings, Constants.Step.ANALYTICS)
            else:
                CsvFileHelper.processFor(settings)
                break
        elif step := Constants.Step(code):
            Wizard.promptFor(settings, step)


if __name__ == "__main__":
    main()