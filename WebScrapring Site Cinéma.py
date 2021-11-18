movie_names = []
movie_years = []
movie_rates = []
movie_metas = []
movie_votes = []

from requests import get
from time import sleep
from random import randint
from time import time
from IPython.display import clear_output
from warnings import warn
from bs4 import BeautifulSoup
import pandas as pd

pages = [str(n) for n in range(1,5)]
years = [str(n) for n in range(2000,2018)]

url_first ="https://www.imdb.com/search/title/?release_date="
url_second = "&sort=num_votes,desc&page="

start_time = time()
requests = 0

for year in years:
    for page in pages:
        if requests > 72:
            warn('Attention')
            break
        else:
            requests +=1
            url = url_first + year + url_second + page
            response = get(url)
            sleep(randint(8,15))
            elapsed_time = time() - start_time
            print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
            clear_output(wait = True)
            soup = BeautifulSoup(response.text, 'html.parser')
            movie_container = soup.find_all(class_="lister-item mode-advanced")
            for n in movie_container:
                if n.find('div', class_='ratings-metascore') is not None:
                     # Extraction des noms de films
                    movie_names.append(n.h3.a.text)

                    # Extraction année
                    movie_years.append(n.h3.find('span', class_='lister-item-year text-muted unbold').get_text())

                    # Extraction note IMDB
                    rate = n.select('.ratings-imdb-rating')
                    movie_rates.append(float(rate[0].text))

                    #Extraction metacritic
                    meta =n.select('.metascore')
                    movie_metas.append(int(meta[0].text))

                    # Extraction Votes
                    vote = n.find('span', attrs={'name':'nv'})
                    movie_votes.append(int(vote['data-value']))


movies_pandas=pd.DataFrame({
    'Name': movie_names,
    'Year': movie_years,
    'Note IMDB': movie_rates,
    'Metascore': movie_metas,
    'Votes': movie_rates
})
print(movies_pandas.info())
print(movies_pandas.head(50))
