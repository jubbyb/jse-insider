import requests # for making standard html requests
from bs4 import BeautifulSoup # magical tool for parsing html data

import re #regex

# to do :
#  Supreme Ventures Limited (SVL) has advised that the Company has acquired an additional 29% shareholding
#  interest in Posttopost Betting Limited, bringing its total shareholding to 80%.

def get_trades():
    page_prefix = "https://www.jamstockex.com/page/"
    page_number = 1
    page_suffix = "/?s=Trading+in+Shares&tag&cat=-1&start&end" # filters for articles category and keyword "shares"

    tradeTotal = []
    # loop through recent x pages 
    for i in range(1,4):
        
        URL = page_prefix+str(i)+page_suffix
        page = requests.get(URL)
        soup = BeautifulSoup(page.text, 'html.parser')

        # find all entries on page
        trade_list = soup.find_all(class_ = 'entry-summary')


        for i in trade_list:
            
        
            cont = i.contents[1].text
            
            # clean data and replace with commas for csv 
            cont = re.sub(',', '',cont, flags=re.IGNORECASE)
            # print(cont)
            cont = re.sub('has.*sold', ',sold',cont, flags=re.IGNORECASE)
            cont = re.sub('has.*purchased', ',purchased',cont, flags=re.IGNORECASE)
            cont = re.sub('shares.*purchased', ',purchased',cont, flags=re.IGNORECASE)
            cont = re.sub('shares.*bought', ',purchased',cont, flags=re.IGNORECASE)
            cont = re.sub('advises.*sold', ',sold',cont, flags=re.IGNORECASE)
            cont = re.sub('acquired', ',acquired,',cont, flags=re.IGNORECASE)
            cont = re.sub('a total of', '',cont, flags=re.IGNORECASE)
            cont = re.sub('a total', '',cont, flags=re.IGNORECASE)
            cont = re.sub('shares on', ',',cont, flags=re.IGNORECASE)
            cont = re.sub('and a connected party purchased a total of', ' purchased',cont, flags=re.IGNORECASE)
            cont = re.sub('shares. The transactions were carried out between', ',',cont, flags=re.IGNORECASE)
            cont = re.sub('has advised that a purchase of', ',purchased',cont, flags=re.IGNORECASE)
            cont = re.sub('sold', 'sold ,',cont, flags=re.IGNORECASE)
            cont = re.sub('purchased', 'purchased ,',cont, flags=re.IGNORECASE)
            cont = re.sub('shares during the period', ',',cont, flags=re.IGNORECASE)
            cont = re.sub('shares held under the Employee Share Ownership Plan of the Company', '',cont, flags=re.IGNORECASE)
            cont = re.sub('has advised that a director exercised their stock options and', '',cont, flags=re.IGNORECASE)
            cont = re.sub('shared during the period', ',',cont, flags=re.IGNORECASE)
            cont = re.sub('shares by two directors was completed', ',',cont, flags=re.IGNORECASE)

            cont = re.sub('on', '',cont, flags=re.IGNORECASE)
            
            
            tradeTotal.append(cont.split(','))


    for i in tradeTotal :
        # for a in len(i):
        length = len(i)
        # formatting
        if len(i) == 3:
            print(f"{'| ' + i[0]:<70} | {i[1]:<10} | {i[2]:<20} |")
        elif len(i) == 4 :
            print(f"{'| ' + i[0]:<70} | {i[1]:<10} | {i[2]:<20} | {i[3]:<25} |")
        elif len(i) == 5:
            print(f"{'| ' + i[0]:<70} | {i[1]:<10} | {i[2]:<20} | {i[3]:<25} | {i[4]:<25} |")
        elif len(i) == 6:
            print(f"{'| ' + i[0]:<70} | {i[1]:<10} | {i[2]:<20} | {i[3]:<25} | {i[4]:<25} | {i[4]:<25} |")  
        else :
            print(i)
    
    return tradeTotal
