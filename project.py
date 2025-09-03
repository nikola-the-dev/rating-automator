from settings import Settings
from wizard import Wizard
from csvFileHelper import CsvFileHelper

import sys


settings = Settings()

def main():
    settings.summary()


if __name__ == "__main__":
    main()