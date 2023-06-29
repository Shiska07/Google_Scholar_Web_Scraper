import sys
import os
import requests
import bs4
import pandas as pd
import time
import numpy as np
from datetime import datetime

# create a dictionary to store sorting attributes
sorting_fields = {1: 'citations',
                  2: 'year',
                  3: 'first_author',
                  4: 'journal',
                  0: 'no_criteria'}

domain_url = "https://scholar.google.com"

# writes the url and the search query in a .txt file
def write_search_metadata(soup, request_url, n_items, fname):

    search_query_list = []
    res_set = soup.select('.gs_in_txt')
    for i in range(0, int(len(res_set) / 2)):
        search_query_list.append(res_set[i]['value'])

    search_query = ''.join(search_query_list)

    with open(fname+'/metadata.txt', 'w') as f:
        f.write(f'filename    : {fname}.csv\n')
        f.write(f'Timestamp   : {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n')
        f.write(f'Search query: {search_query}\n')
        f.write(f'Total items : {n_items}\n')
        f.write(f'url         : {request_url}\n')
        f.write('\nAttribute description:\n')
        f.write('title       : Title of the paper\n')
        f.write('year        : Publication year\n')
        f.write('first_author: Name of the first author\n')
        f.write('citations   : Number of times the paper has been cited\n')
        f.write('journal     : Publication journal name\n')
        f.write('url         : link to the paper\n')
        f.write('search_page : Page number of the search result on GoogleScholar\n')

    print("Search metadata saved in file 'metadata.csv'")


# converts url value to hyperlink
def create_hyperlink(url_value):

    if len(url_value) < 255:
        hyperlink = '=HYPERLINK("{}", "{}")'.format(url_value, "link")
    else:
        return url_value

    return hyperlink


# saves dataframe as an excel file
def save_df_as_csv(df, n_res):

    # get filename from user
    fname = input('Enter filename to save results: ')

    # save top 'n' values as a .csv file
    df_final = df.head(n_res).copy()
    df_final['url'] = df_final['url'].apply(create_hyperlink)

    while True:
        try:
            # create a directory with the same name as the file
            os.mkdir(fname)
        except:
            fname = input("Invalid filename. Please pick a different filename: ")
        else:
            # destination string
            dest = fname + '/' + fname + '.csv'
            df_final.to_csv(dest, index=False)
            print(f'Results saved in file {fname}.csv.\n')
            break

    return fname


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


# gets intial response for url provided by the user and returns soup object
def get_response_soup(request_url):

    # check if the provided url is a valid url
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
    article_urls = []
    for item in res_list:
        if 'https:' in item.find_all('a')[1]['href']:
            article_urls.append(item.find_all('a')[1]['href'])
        else:
            article_urls.append(item.find_all('a')[0]['href'])
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
        if len(value) > 0:
            years_list.append(int(value[0]))
        else:
            years_list.append(np.NaN)

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
    total_citations_list = []
    for item in valid_res_list:
        value = item.find_all('a')[2].get_text().split()[-1]
        if value.isnumeric():
            total_citations_list.append(int(value))
        else:
            total_citations_list.append(np.NaN)

    return total_citations_list

# returns a 2D list containing different attributes of the search results for a single page
def get_search_results_as_2Dlist(request_url):

    # get soup
    soup = get_response_soup(request_url)

    # get search result attributes and convert each to series
    res_list_2D = [get_titles(soup), get_publication_years(soup), get_first_auther_names(soup),
                   get_number_of_citations(soup), get_journal_names(soup), get_article_urls(soup)]

    return res_list_2D

def create_sorted_dataframe(request_url, sorting_prefs, n):

    # create list to store results
    titles_list = []        # Title of the paper
    year_list = []          # Published year
    authors_list = []       # First author
    citations_list = []     # No. of citations
    journal_list = []       # Name of the journal
    urls_list = []          # url/link to the article/paper
    search_page = []        # page number of the search result on GoogleScholar

    # get urls for upto 'n' pages
    search_urls_list = get_urls_to_consequtive_n_pages(request_url, get_response_soup(request_url), n)

    start_time = time.time()

    for i, search_url in enumerate(search_urls_list):

        res = get_search_results_as_2Dlist(search_url)

        # unpack and append results
        titles_list.extend(res[0])
        year_list.extend(res[1])
        authors_list.extend(res[2])
        citations_list.extend(res[3])
        journal_list.extend(res[4])
        urls_list.extend(res[5])
        search_page.extend([i+1]*10)

    # create a pandas dataframe to store values
    final_df = pd.DataFrame(list(zip(titles_list, year_list, authors_list, citations_list, journal_list, urls_list, search_page)),
                                columns=['title', 'year', 'first_author', 'citations', 'journal', 'url', 'search_page'])

    end_time = time.time()

    print(f'Total scraping time : {end_time - start_time:0.3f}s.\n')

    # sort df if preferences are provided
    if len(sorting_prefs[0]) == len(sorting_prefs[1]) != 0:
        # get column names for sorting
        sorting_pref_cols = [sorting_fields[item] for item in sorting_prefs[0]]

        # sort the df according to user preferences
        final_df.sort_values(by = sorting_pref_cols, ascending = sorting_prefs[1], inplace = True)

    else:
        # sory by decreasing order of citations, then year
        final_df.sort_values(by=['citations', 'year'], ascending=[False, False], inplace=True, na_position='first')

    return final_df

# check's if the url provided by the user is valid for the program
def check_url_validity(request_url):

    try:
        test_resp = requests.get(request_url)
    except:
        print("Provided url is not valid. Please re-run the program.\n")
        sys.exit(0)
    else:
        if domain_url in request_url:
            return request_url
        else:
            print("Provided url is out of the program's scope. Please re-run the program.\n")
            sys.exit(0)

def get_sorted_results(request_url, sorting_prefs, n, n_res):

    # create sorted dataframe out of search results
    df = create_sorted_dataframe(request_url, sorting_prefs, n)

    # save as a .csv file
    fname = save_df_as_csv(df, n_res)

    # write search metadata
    write_search_metadata(get_response_soup(request_url), request_url, n_res, fname)

