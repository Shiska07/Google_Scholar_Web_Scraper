import sys
import helpers

def get_user_input():

    input_url = str(input('Enter the https url to your Google Scholar Search result: '))

    # check validity of url provided by the user
    input_url = helpers.check_url_validity(input_url)

    # create a list to store sorting preferences
    sorting_pref = []
    aesc_pref = []

    options_dict = {0 : "no criteria:",
                    1 : "citations  :",
                    2 : "year       :",
                    3 : "author(s)  :",
                    4 : "journal    :" }

    print("\nPlease enter attribute you would like to sort by in the decreasing order of priority. 1Your options are:")
    for key, value in options_dict.items():
        if key not in sorting_pref:
            print(f'{value} {key}')
    print("\nEnter 'exit' anytime to quit.\n")

    for i in range(1, 4):
        val = input(f"\nEnter attribute no {i} for sorting: ")

        if val == "exit":
            sys.exit(0)

        # keep asking for input if valid value is not entered
        while (not val.isdigit()) or (int(val) not in helpers.sorting_fields.keys() or int(val) in sorting_pref):
            print("\nPlease enter a valid number. Your options are:\n")

            for key, value in options_dict.items():
                if key not in sorting_pref:
                    print(f'{value} {key}')

            val = input(f"\nEnter attribute no {i} for sorting: ")

            if val == "exit":
                sys.exit(0)

         # exit loop if user inputs 0
        if int(val) == 0:
            break

        sorting_pref.append(int(val))

        aesc_val = input("Ascending? (Enter T/F): ")
        if aesc_val == "exit":
            sys.exit(0)

        while aesc_val not in ['T', 'F']:
            aesc_val = input("Ascending? (Enter T/F): ")
            if aesc_val == "exit":
                sys.exit(0)

        if aesc_val == 'T':
            aesc_pref.append(True)
        else:
            aesc_pref.append(False)


    # enter number of pages and search results from the search result to use
    no_of_pages = int(input('Enter number of pages you would like to pull results from(max: 10): '))
    no_of_res = int(input(f'Enter the total number of search items to return(max: {no_of_pages*10}): '))
    # return starting url and sorting preferences
    return input_url, [sorting_pref, aesc_pref], no_of_pages, no_of_res

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # get url and sorting prefs from user
    url, sorting_prefs, n_pages, n_res = get_user_input()
    helpers.get_sorted_results(url, sorting_prefs, n_pages, n_res)

    # link to article not being properly extracted
    