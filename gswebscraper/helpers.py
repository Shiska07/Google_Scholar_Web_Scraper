import requests
import bs4
import numpy as np
import pandas as pd

# create a dictionary to store sorting attributes
sorting_fields = {1: 'total_citations',
                  2: 'publication_year',
                  3: 'first_author_name',
                  4: 'journal_name',
                  0: 'no_criteria'}
