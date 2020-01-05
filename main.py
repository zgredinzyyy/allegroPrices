from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

print('Please enter what would you like to look for:')
userWanted = input()
constructed = 'https://allegro.pl/listing?string=' + str(userWanted)

url = Request(constructed, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(url).read()
web = webpage.decode('utf-8')
soup = BeautifulSoup(web, 'html.parser')

for link in soup.select('a[href*=".pl/oferta"]'):
    if link.get_text() is not '':
        print(link.get_text())
        print(link.get('href'))
        url = urlopen(link.get('href')).read()
        soup = BeautifulSoup(url, 'html.parser')
        for redirect in soup.select('div[aria-label*=cena]'):
            print(redirect.get_text() + '\n')

    