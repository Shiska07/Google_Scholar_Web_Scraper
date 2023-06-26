import sys
import helpers

def get_user_input():

    # start_url = str(input('Enter your Google Scholar Search result url: '))
    input_url = "https://scholar.google.com/scholar?start=0&q=(%22Machine+Learning%22%7C%22Deep+Learning%22)(%22Radiation+oncology%22%7C%22cancer+detection%22)&hl=en&as_sdt=0,44"

    # create a list to store sorting preferences
    sorting_pref = []
    aesc_pref = []

    print("Please enter attribute you would like to sort by in the decreasing order of priority.Your options are:\n")
    print("number of citations: 1\nyear published: 2\nfirst author name: 3\njournal name: 4\nno criteria: 0\n")

    for i in range(1, 4):
        val = input(f"Enter attribute no {i} to sort by or 'exit' to end program: ")

        if val == "exit":
            sys.exit(0)

        # keep asking for input if valid value is not entered
        while (not val.isdigit()) or (int(val) not in helpers.sorting_fields.keys()):
            print("\nPlease enter a valid number.Your options are:\n")
            print("number of citations: 1\nyear published: 2\nfirst author name: 3\njournal name: 4\nno criteria: 0\n")
            val = input(f"Enter attribute no {i} to sort by or 'exit' to end program: ")

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
    no_of_pages = int(input('Enter number of pages to use from the search result (max: 10): '))
    no_of_res = int(input('Enter the total number of search results to return: '))
    # return starting url and sorting preferences
    return input_url, [sorting_pref, aesc_pref], no_of_pages, no_of_res

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # get url and sorting prefs from user
    url, sorting_prefs, n_pages, n_res = get_user_input()
    helpers.get_sorted_results(url, sorting_prefs, n_pages, n_res)




'''
TO DO:
1. Timing and optimization
2. Error and edge case handling
'''
