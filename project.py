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
        code = Constants.inpt((1, len(Constants.Step)), 9)
        if code == 9:
            print("Calculate")
            break
        elif step := Constants.Step.get(code):
            Wizard.promptFor(settings, step)


if __name__ == "__main__":
    main()