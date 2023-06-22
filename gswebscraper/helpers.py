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
sorting_fields = {1: 'total_citations',
                  2: 'publication_year',
                  3: 'first_author_name',
                  4: 'journal_name',
                  0: 'no_criteria'}

domain_url = "https://scholar.google.com"

# given a starting url and a value of n, returns a list of urls for next pages of the result
def get_urls_to_consequtive_n_pages(start_url, soup, n = 9):

    # create list to store urls
    url_list = [start_url]

    # url's pointing to the next pages are defined by id 'gs_ml'
    result_set = soup.select('#gs_ml')[0].find_all('a')

    # add all url's in the result set to the list
    for i in range(0, 9):
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
    first_authors_list = [item.find_all('a')[0].get_text() for item in res_list]
    return first_authors_list

# returns a list of publication years for each search result article
def get_publication_years(soup):

    res_list = list(soup.select('.gs_a'))
    years_list = []

    years_list = [item.get_text().split() for item in res_list]
    for value in res_list:
        terms = value.get_text().split()
        value = [item for item in terms if item.isnumeric()]
        years_list.append(value[0])

    return years_list

# returns a 2D list containing different attributes of the search results for a single page
def get_search_results(request_url):

    # get soup
    soup = get_response_soup(request_url)

