from cloudscraper import create_scraper
import pandas as pd
from bs4 import BeautifulSoup
import concurrent.futures
import time

scraper = create_scraper()
book_items = []

start_time = time.time()

with open(r'links.txt', 'r') as f:
    links = f.readlines()
    links = [link.replace('\n', '') for link in links]

def transform(url):
    response = scraper.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.select_one('h1').text
    price = soup.select_one('p.price_color').get_text(strip=True, separator='£')[-1]
    book_item = {
        'Title': title,
        'Price': price
    }
    book_items.append(book_item)
    print(f'Title: {title}\nPrice: {price}\nCurrency: £uro')
    print('--------------------')

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(transform, links)

print("--- %s seconds ---" % (time.time() - start_time))

print(len(book_items))
df = pd.DataFrame(book_items)
df.to_csv('book_data.csv', index=False)