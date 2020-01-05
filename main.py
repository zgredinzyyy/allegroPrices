from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

#TODO:
#- Scrap Likes, Overall Grade
#- Add Confidence Precentage
#- Credits System
#- (Buying Option?)
#- Exporting to JSON

print('Please enter what would you like to look for:')
userWanted = input()
constructed = 'https://allegro.pl/listing?string=' + str(userWanted)

url = Request(constructed, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(url).read()
web = webpage.decode('utf-8')
soup = BeautifulSoup(web, 'html.parser')

def getLikes(given_URL, choice):
    newURL = given_URL + '#aboutSeller'
    url = urlopen(newURL).read()
    soup = BeautifulSoup(url, 'html.parser')
    if choice == True:
        for link in soup.select('a[href*="/oceny?recommend=true"] > p'):
            if link.get_text() is not '':
                return link.get_text()
    else:
        for link in soup.select('a[href*="/oceny?recommend=false"] > p'):
            if link.get_text() is not '':
                return link.get_text()

for link in soup.select('a[href*=".pl/oferta"]'):
    if link.get_text() is not '':
        title = link.get_text()
        href = link.get('href')
        print(title)
        print(href)
        #FIXME Nie działa kiedy nic nie ma #aboutSeller ex. https://allegro.pl/oferta/steam-f12015-f12017-gtav-rfactor2-project-cars-1-2-8326238065
        print('Likes: ' + getLikes(href,True))
        print('Dislikes: ' + getLikes(href,False))
        url = urlopen(href).read()
        soup = BeautifulSoup(url, 'html.parser')
        for redirect in soup.select('div[aria-label*=cena]'):
            print(redirect.get_text() + '\n')