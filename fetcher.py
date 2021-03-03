from bs4 import BeautifulSoup
import re
import requests
import html5lib
import datetime




months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
current_date = datetime.datetime.now()
current_date = current_date.strftime('%b') + '  ' + current_date.strftime('%d').lstrip('0')


# source = requests.get('https://gainesville.craigslist.org/search/bip?purveyor-input=all&hasPic=1&bundleDuplicates=1&searchNearby=2&nearbyArea=238&nearbyArea=80&nearbyArea=638&nearbyArea=333&nearbyArea=39&nearbyArea=331&nearbyArea=557&nearbyArea=186&nearbyArea=37')

# soup = BeautifulSoup(source.content)

bike_patterns = ['rack', 'carrier', 'wheel', 'bars', 'bag', '1x', 'hub']
camp_patterns = ['tent', 'big agnes','kelty', 'light', '2p' ,'2 person']
my_items = {('tent', 'sga'): ['big agnes', 'kelty', 'light', '2p', '2 person', 'ultralight', 'rei', 'zpacks', 'north face', 'nemo', 'msr', 'marmot', 'mammuts', 'backpack',]}
my_bike_items = {('bag', 'bip'): ['frame', 'pack', 'revelate', 'arkel', 'ortlieb', 'pannier', 'bikepack', 'seat pack']}
parts_list = {('bar', 'bip'): ['frame', 'pack', 'revelate', 'arkel', 'ortlieb', 'pannier', 'bikepack', 'seat pack']}

# data is (item, categoriy) : [list of things to search for under this query]

# camp_soup = BeautifulSoup(requests.get('https://gainesville.craigslist.org/search/sga?bundleDuplicates=1&nearbyArea=238&nearbyArea=80&nearbyArea=638&nearbyArea=333&nearbyArea=39&nearbyArea=331&nearbyArea=557&nearbyArea=186&nearbyArea=37&hasPic=1&searchNearby=2').content)
# https://gainesville.craigslist.org/search/sga?query=tent&purveyor-input=all&hasPic=1&bundleDuplicates=1&searchNearby=2&nearbyArea=238&nearbyArea=80&nearbyArea=638&nearbyArea=333&nearbyArea=39&nearbyArea=331&nearbyArea=557&nearbyArea=186&nearbyArea=37
categories = {'all': 'sss', 'sporting goods': 'sga', 'bikes': 'bia', 'bike parts' : 'bip'}

class CraigslistObject():

    def __init__(self):
        self.price = '0'
        self.title = 'NONE'
        self.date = '1/1/01'
        self.link = 'http://'


def find_matches(patterns, ob_list):
    matched_names = []
    for each in ob_list:
        for pattern in patterns:
            if re.search(pattern, each.title, re.IGNORECASE) is not None:
                matched_names.append(each)
    return matched_names
    




def search_craigslist(soup, patterns):
        cl_rows = soup.findAll('div', {'class': "result-info"})

        cl_patterns = patterns

        cl_object_list = []
        for each in cl_rows:
            temp = CraigslistObject()
            temp.price = each.find('span', {'class': 'result-price'}).text
            temp.title = each.find('a', {'class': 'result-title'}).text
            temp.date = each.find('time', {'class': 'result-date'}).text
            temp.link = each.find('a', {'class': 'result-title'})['href']
            cl_object_list.append(temp)




        craigslist_matches = find_matches(cl_patterns, cl_object_list)

        for match in craigslist_matches:
            print(match.price.ljust(6) + ' | ' + match.date + ' | ' + match.title + ' | ' + match.link)

        print('---------------------------------------------------')
        for match in craigslist_matches:
            if match.date == current_date:
                print(match.price.ljust(6) + ' | ' + match.date + ' | ' + match.title + ' | ' + match.link)
        print('---------------------------------------------------')



def search_item(item_dict):


    for item, value in item_dict.items():
        print(item[0])
        print(item[1])
        print(value)
        req = requests.get('https://gainesville.craigslist.org/search/'+ item[1] + '?bundleDuplicates=1&query=' + item[0] + '&nearbyArea=238&nearbyArea=80&nearbyArea=638&nearbyArea=333&nearbyArea=39&nearbyArea=331&nearbyArea=557&nearbyArea=186&nearbyArea=37&hasPic=1&searchNearby=2')
        print(req.url)
        soup = BeautifulSoup(req.content, features='html5lib')
        data = search_craigslist(soup, value) # item 1 is a list of patterns for that item

def broad_search_item(item_tuple):

        req = requests.get('https://gainesville.craigslist.org/search/'+ item_tuple[1] + '?bundleDuplicates=1&query=' + item_tuple[0] + '&nearbyArea=238&nearbyArea=80&nearbyArea=638&nearbyArea=333&nearbyArea=39&nearbyArea=331&nearbyArea=557&nearbyArea=186&nearbyArea=37&hasPic=1&searchNearby=2')
        soup = BeautifulSoup(req.content, features='html5lib')
        search_craigslist(soup, [item_tuple[0]])




broad_search_item(('trek', categories['bikes']))
broad_search_item(('cannondale', categories['bikes']))
broad_search_item(('specialized', categories['bikes']))
broad_search_item(('salsa', categories['bikes']))
broad_search_item(('surly', categories['bikes']))
broad_search_item(('bars', categories['bike parts']))
search_item(my_items)
search_item(my_bike_items)