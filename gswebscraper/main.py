import os
import csv
import sys
import helpers





def get_user_input():

    # start_url = str(input('Enter your Google Scholar Search result url: '))
    input_url = "https://scholar.google.com/scholar?start=0&q=(%22Machine+Learning%22%7C%22Deep+Learning%22)(%22Radiation+oncology%22%7C%22cancer+detection%22)&hl=en&as_sdt=0,44"

    print("Please enter attribute you would like to sort by in the decreasing order of priority.Your options are:\n")
    print("number of citations(desc): 1\nyear published(desc): 2\nfirst author name: 3\njournal name: 4\nno criteria: 0\n")

    # create a list to store sorting preferences
    sorting_pref = []

    for i in range(1, 4):
        val = input(f"Enter attribute no {i} to sort by or 'exit' to end program: ")

        if val == "exit":
            sys.exit(0)

        # keep asking for input if valid value is not entered
        while (not val.isdigit()) or (int(val) not in helpers.sorting_fields.keys()):
            print("\nPlease enter a valid number.Your options are:\n")
            print("number of citations(desc): 1\nyear published(desc): 2\nfirst author name: 3\njournal name: 4\nno criteria: 0\n")
            val = input(f"Enter attribute no {i} to sort by or 'exit' to end program: ")

            if val == "exit":
                sys.exit(0)

        sorting_pref.append(int(val))

        # exit loop if user inputs 0
        if int(val) == 0:
            sorting_pref.append(int(val))
            break

    # return starting url and sorting preferences
    return input_url, sorting_pref

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # get url and sorting prefs from user
    url, sorting_prefs = get_user_input()


