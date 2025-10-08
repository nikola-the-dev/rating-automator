import sys
import os

import project

CONFIG = "config.ini"

def main():
    if len(sys.argv) == 2 and project.fileCheck(sys.argv[1]) and os.path.exists(CONFIG):
        if not project.runCalculations(sys.argv[1]):
            project.main()
    else:
        project.main()



if __name__ == "__main__":
    main()