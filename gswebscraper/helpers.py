import requests
import bs4
import numpy as np
import pandas as pd

# create object for initial webpage to create metadata
class Webpage:
    def __int__(self, url):
        self.url = url
        self.search_query = None

    def set_search_query(self, soup):
        # extract search_query from soup object
        pass


# create a dictionary to store sorting attributes
sorting_fields = {1: 'citations',
                  2: 'year',
                  3: 'first_author',
                  4: 'journal',
                  0: 'no_criteria'}

domain_url = "https://scholar.google.com"

# given a starting url and a value of n, returns a list of urls for next pages of the result
def get_urls_to_consequtive_n_pages(start_url, soup, n):

    # create list to store urls
    url_list = [start_url]

    # url's pointing to the next pages are defined by id 'gs_ml'
    result_set = soup.select('#gs_nml')[0].find_all('a')

    # add all url's in the result set to the list
    for i in range(0, n - 1):
        url_raw = result_set[i]['href']
        url_final = domain_url + url_raw
        url_list.append(url_final)

    return url_list

# writes the url and the search query in a .txt file
def write_search_metadata(soup, request_url):
    pass


# gets intial response for url provided by the user and returns soup object
def get_response_soup(request_url):

    req_response = requests.get(request_url)
    soup = bs4.BeautifulSoup(req_response.content, "lxml")
    return soup

# returns a list of journal article titles for all search results on the page
def get_titles(soup):

    res_list = list(soup.select('[data-lid]'))
    titles = [item.select('h3')[0].get_text() for item in res_list]
    return titles

# returns a list of url to article for all search results on the page
def get_article_urls(soup):

    res_list = list(soup.select('[data-lid]'))
    article_urls = [item.find_all('a', href = True)[0]['href'] for item in res_list]
    return article_urls

# returns a list of first authors for all search results on the page
def get_first_auther_names(soup):

    res_list = soup.select('.gs_a')
    first_authors_list = [item.get_text().split(', ')[0] for item in res_list]
    return first_authors_list

# returns a list of publication years for each search result article
def get_publication_years(soup):

    res_list = list(soup.select('.gs_a'))
    years_list = []

    for value in res_list:
        terms = value.get_text().split()
        value = [item for item in terms if item.isnumeric()]
        years_list.append(int(value[0]))

    return years_list

# returns a list containing name of the journal where each paper was published
def get_journal_names(soup):

    res_list = list(soup.select('.gs_a'))
    journal_names_list = [item.get_text().split()[-1].split('.')[0] for item in res_list]
    return journal_names_list

# returns a list containing the number of citations on each search result article
def get_number_of_citations(soup):

    res_list = list(soup.select('.gs_fl'))
    valid_res_list = valid_res_list = [item for item in res_list if len(item["class"]) == 1]

    # the 'gs_fl' class containing citation for each search item = (i*2)+1 ( i = 0, the index is 1)
    total_citations_list = [int(item.find_all('a')[2].get_text().split()[-1]) for item in valid_res_list]
    return total_citations_list

# returns a 2D list containing different attributes of the search results for a single page
def get_search_results_as_df(request_url):

    # get soup
    soup = get_response_soup(request_url)

    # get search result attributes and convert each to series
    titles_ser = pd.Series(get_titles(soup), name = "title")
    urls_ser = pd.Series(get_article_urls(soup), name = "url_to_article")
    authors_ser = pd.Series(get_first_auther_names(soup), name = "first_author")
    year_ser = pd.Series(get_publication_years(soup), name = "year", dtype = int)
    journal_ser = pd.Series(get_journal_names(soup), name = "journal")
    citations_ser = pd.Series(get_number_of_citations(soup), name = "citations", dtype = int)

    # create dataframe
    df = pd.concat([titles_ser, year_ser, authors_ser, citations_ser, journal_ser, urls_ser], axis = 1)
    return df

def get_sorted_dataframe(request_url, sorting_prefs, n):

    # create a pandas dataframe to store values
    final_df = pd.DataFrame(columns = ['title', 'year', 'first_author', 'citations', 'journal', 'url_to_article'])

    # get urls for upto 'n' pages
    search_urls_list = get_urls_to_consequtive_n_pages(request_url, get_response_soup(request_url), n)

    # for each up to 'n' result pages
    for search_url in search_urls_list:

        # get df for search result
        single_page_res_df = get_search_results_as_df(search_url)

        # append to final df
        final_df = pd.concat([final_df, single_page_res_df], axis = 0, ignore_index = True)
        final_df.reset_index(drop = True, inplace = True)

    # sort df if preferences are provided
    if len(sorting_prefs[0]) == len(sorting_prefs[1]) != 0:
        # get column names for sorting
        sorting_pref_cols = [sorting_fields[item] for item in sorting_prefs[0]]

        # sort the df according to user preferences
        final_df.sort_values(by = sorting_pref_cols, ascending = sorting_prefs[1], inplace = True)

    return final_df

# converts url value to hyperlink
def create_hyperlink(url_value):
    return '=HYPERLINK("{}", "{}")'.format(url_value, url_value)


# saves dataframe as an excel file
def save_df_as_csv(df, n_res):

    # get filename from user
    f_name = input('Enter filename for saving:')

    # save top 'n' values as a .csv file
    df_final = df.head(n_res).copy()
    df_final['url_to_article'] = df_final['url_to_article'].apply(create_hyperlink)
    df_final.to_csv(f_name + '.csv', index = False)
    print(f'Results saved in file {f_name}.csv.\n')


def get_sorted_results(request_url, sorting_prefs, n, n_res):
    df = get_sorted_dataframe(request_url, sorting_prefs, n)
    save_df_as_csv(df, n_res)
