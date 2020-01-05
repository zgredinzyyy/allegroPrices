from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

#TODO:
#- Scrap Likes, Overall Grade X
#- Add Confidence Precentage X
#- Credits System
#- (Buying Option?)
#- Exporting to JSON
#- Show best option = MAX(confidence), MIN(price)

print('Please enter what would you like to look for:')
userWanted = input()
constructed = 'https://allegro.pl/listing?string=' + str(userWanted)

url = Request(constructed, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(url).read()
web = webpage.decode('utf-8')
soup = BeautifulSoup(web, 'html.parser')

#FIXME Nie działa kiedy nic nie ma #aboutSeller ex. https://allegro.pl/oferta/steam-f12015-f12017-gtav-rfactor2-project-cars-1-2-8326238065
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

def calcConfidence(likes,dislikes):
    likes = int(likes)
    disLikes = int(dislikes)
    summed = likes + disLikes
    confidencePoints = 0
    if summed >= 10000:
        confidencePoints += 5
    elif summed >= 5000:
        confidencePoints += 4
    elif summed >= 2000:
        confidencePoints += 3
    elif summed >= 1000:
        confidencePoints += 2
    elif summed >= 100:
        confidencePoints += 1

    approvalPrecentage = round(((likes / summed) * 0.05) * 100)
    confidencePoints += approvalPrecentage
    return str(confidencePoints)

def getPrice(href):
    url = urlopen(href).read()
    soup = BeautifulSoup(url, 'html.parser')
    for redirect in soup.select('div[aria-label*=cena]'):
        return redirect.get_text()

for link in soup.select('a[href*=".pl/oferta"]'):
    if link.get_text() is not '':
        title = link.get_text()
        href = link.get('href')
        likes = getLikes(href,True)
        disLikes = getLikes(href, False)
        price = getPrice(href)
        print('Title: ' + title)
        print('URL: ' + href)
        print('Likes: ' + likes)
        print('Dislikes: ' + disLikes)
        print('Price: ' + price)
        print('Confidence: ' + calcConfidence(likes,disLikes) + '/10')
        print('\n')