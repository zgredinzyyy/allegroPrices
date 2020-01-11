from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from webbrowser import open_new

#TODO:
#- Credits System
#- (Buying Option?)
#- Exporting to JSON
#- Put that shit into class already
#- Limiting possible to select pages
#- Checking if selected thing even has request in title

print('Please enter what would you like to look for:')
#Professional handling space before and after
allegroSpace = '%20'
userWanted = input()
userWanted = userWanted.split(' ')
if userWanted[0] is '': del userWanted[0]
if userWanted[len(userWanted)-1] is '': del userWanted[len(userWanted)-1]
userWanted = allegroSpace.join(userWanted)

print('Enter how many pages you want to scan:')
userPages = input()

bestTITLE = ''
bestLIKES = 0
bestDISLIKES = 0
bestPRICE = 9999999
bestCONF = 0
bestURL = ''

constructed = 'https://allegro.pl/listing?string=' + str(userWanted)
try:
    for i in range(int(userPages)+1):
        newConstructed = constructed + '&p=' + str(i+1)
        url = Request(newConstructed, headers={'User-Agent': 'Mozilla/5.0'})
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

        def newBest(title,likes,dislikes,price,conf,url):
            if price is not None and conf is not None:
                # Converting price from string value to float
                price = price[0:-3]
                price = price.replace(',', '.')
                price = float(price)

                conf = int(conf)

                global bestTITLE
                global bestLIKES
                global bestDISLIKES
                global bestCONF
                global bestPRICE
                global bestURL

                if conf >= bestCONF and price <= bestPRICE:
                    bestTITLE = title
                    bestLIKES = likes
                    bestDISLIKES = disLikes
                    bestCONF = conf
                    bestPRICE = price
                    bestURL = url

        for link in soup.select('a[href*=".pl/oferta"]'):
            if link.get_text() is not '' and 'https://allegrolokalnie.pl' not in link.get('href'):
                title = link.get_text()
                href = link.get('href')
                likes = getLikes(href,True)
                disLikes = getLikes(href, False)
                price = getPrice(href)
                conf = calcConfidence(likes,disLikes)
                newBest(title,likes,disLikes,price,conf,href)
                print('Watching:')
                print('Title: ' + checkNone(title))
                print('URL: ' + checkNone(href))
                print('Likes: ' + checkNone(likes))
                print('Dislikes: ' + checkNone(disLikes))
                print('Price: ' + checkNone(price))
                print('Confidence: ' + checkNone(conf) + "/10")
                print('---------------------------')
                print('Currently Best:')
                print('Title: ' + str(bestTITLE))
                print('URL: ' + str(bestURL))
                print('Likes: ' + str(bestLIKES))
                print('Dislikes: ' + str(bestDISLIKES))
                print('Price: ' + str(bestPRICE) + ' zł')
                print('Confidence: ' + str(bestCONF)+ "/10")
                print('\n')

except KeyboardInterrupt:
    open_new(bestURL)
else:
    open_new(bestURL)
