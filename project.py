from settings import Settings
from wizard import Wizard
from csvFileHelper import CsvFileHelper

import sys


settings = Settings()

def main():
    while Wizard.stepFor(settings) != Wizard.Step.FINISHED:
        Wizard.promptFor(settings)

if __name__ == "__main__":
    main()