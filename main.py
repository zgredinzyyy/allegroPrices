from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from webbrowser import open_new

#TODO:
#- Scrap Likes, Overall Grade X
#- Add Confidence Precentage X
#- Credits System
#- (Buying Option?)
#- Exporting to JSON
#- Show best option = MAX(confidence), MIN(price)
#- Put that shit into class already
#- Accept Spaces in 'what' input
#- KeyboardInterrupt causes to open latest best choice
#- Add support for multiple pages

print('Please enter what would you like to look for:')
userWanted = input()
constructed = 'https://allegro.pl/listing?string=' + str(userWanted)

url = Request(constructed, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(url).read()
web = webpage.decode('utf-8')
soup = BeautifulSoup(web, 'html.parser')

bestPRICE = 9999999
bestCONF = 0
bestURL = ''

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
    if likes is not None and dislikes is not None:
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
    else:
        return None

def getPrice(href):
    url = urlopen(href).read()
    soup = BeautifulSoup(url, 'html.parser')
    for redirect in soup.select('div[aria-label*=cena]'):
        return redirect.get_text()

def checkNone(toCheck):
    if toCheck is None:
        return 'Brak Danych'
    else:
        return str(toCheck)

def newBest(price,conf,url):
    if price is not None and conf is not None:
        # Converting price from string value to float
        price = price[0:-3]
        price = price.replace(',', '.')
        price = float(price)

        conf = int(conf)

        global bestCONF
        global bestPRICE
        global bestURL

        if conf >= bestCONF and price <= bestPRICE:
            bestCONF = conf
            bestPRICE = price
            bestURL = url

for link in soup.select('a[href*=".pl/oferta"]'):
    if link.get_text() is not '':
        title = link.get_text()
        href = link.get('href')
        likes = getLikes(href,True)
        disLikes = getLikes(href, False)
        price = getPrice(href)
        conf = calcConfidence(likes,disLikes)
        newBest(price,conf,href)
        print('Title: ' + checkNone(title))
        print('URL: ' + checkNone(href))
        print('Likes: ' + checkNone(likes))
        print('Dislikes: ' + checkNone(disLikes))
        print('Price: ' + checkNone(price))
        print('Confidence: ' + checkNone(conf) + "/10")
        print('---------------------------')
        print('Best NOW:')
        print('URL: ' + str(bestURL))
        print('Price: ' + str(bestPRICE))
        print('Confidence: ' + str(bestCONF))
        print('\n')

open_new(bestURL)
