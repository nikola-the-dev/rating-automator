from settings import Settings
from quiz import Quiz

import sys
import os
import csv


settings = Settings()

def main():
    settings.analytics = "Сторінки_й_екрани_Шлях_до_сторінки_й_клас_екрана-3.csv"
    prompt_for_feed()


def prompt_for_feed():
    option = prompt_options("(Recommended) Do you want to add feed with all items in order to generate complete update list?",
                  "Yes, I want to add items from csv file",
                  "Yes, I want to add from URL (Google Feed for Merchant Center)",
                  "No, just generate list based on analytics file"
                            )
    match option:
        case 1:
            files = get_list_of_current_dir_csv_files(settings.analytics)
            files.append("Type path to file")
            selected = prompt_options("Which one you want to select?", *files)
            if selected == len(files):
                print("Type path to csv file")
            else:
                settings.feed = files[selected - 1]
        case 2:
            print("URL")
        case 3:
            print("Skip")


def prompt_options(msg, *args):
    while True:
        print(msg)
        for i, arg in enumerate(args):
            print(f"{i + 1}. {arg}")
        print()
        print("0. Exit")
        try:
            result = int(input("Input: "))
            if result == 0:
                sys.exit()
            else:
                if result > len(args):
                    continue
            return result
        except ValueError:
            continue


def get_list_of_current_dir_csv_files(ignore=None):
    all_files = os.listdir(".")
    def filter_rule(f):
        flag = (os.path.isfile(f)) & (f.lower().endswith(".csv"))
        if i := ignore:
            return flag & (f != i)
        return flag
    result = [file for file in all_files if filter_rule(file)]
    return result


if __name__ == "__main__":
    main()