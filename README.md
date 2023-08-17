This is a web scraping program written in Python to help students and researchers like myself extract information from a GoogleScholar search for filtering more relevant journal articles. Just as I was getting started with my master's thesis and deciding to pick a more specific topic, I found the number of research articles and publications on the application of Machine Learning in Radiation Oncology to be overwhelming. In order to filter articles that are more relevant to my research interests(and also learn about web-scraping) I decided to create this program.

To use the program:-

1. Open command prompt and run: python main.py
2. When prompted, provide the http link of your google scholar search result
3. Provide the first, second and third criteria to sort results by. For example: citations, year, journal, etc.

The sorted list will be stored in a .csv file and the search metadata will be stored in 'metadata.csv' within a folder created by the program. The program will prompt the user to provide the folder name. Check folder 'gswebscraper/transfer_learning_nedical_imaging' for search results example.
