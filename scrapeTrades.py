import requests # for making standard html requests
from bs4 import BeautifulSoup, element # magical tool for parsing html data

import re #regex




def get_trades():
    page_prefix = "https://www.jamstockex.com/page/"
    page_number = 1
    page_suffix = "/?s=Trading+in+Shares&tag&cat=-1&start&end" # filters for articles category and keyword "shares"

    tradeTotal = []
    ticker=''
    # loop through recent x pages 
    for i in range(1,4):
        
        URL = page_prefix+str(i)+page_suffix
        page = requests.get(URL)
        soup = BeautifulSoup(page.text, 'html.parser')

        articles = soup.find_all('article')
        
        for article in articles:
            # print(article)

             # find all entries on page
            trade_summary = article.find(class_ = 'entry-summary')

            #
            trade_date = article.find(class_ = 'text-muted')
            trade_date = trade_date.text
            trade_date = re.sub(r'Posted: ', '',trade_date, flags=re.IGNORECASE)
            
            # print('trade_list',trade_summary.text)
            summary = trade_summary.text
            # search for content between brackets and return value without brackets 
            ticker = re.search(r'\(([^()]*)\)',summary)
            ticker = ticker.group(1).strip()
            
            # clean data and replace with commas for csv 
            cont = re.sub(',', '',summary, flags=re.IGNORECASE)
            
            # print(cont)
            qty = re.search(r'[0-9]+',cont)
            qty = qty.group().strip()
            # print('summary : ', summary)
            # print('date : ',trade_date)
            # print('ticker : ',ticker)
            # print('qty : ',qty)

            

            if (cont.find('purchase') !=-1 and cont.find('sold') !=-1):
                salestatus = 'Transferred'
            elif (cont.find('purchase') !=-1 or cont.find('acquired') !=-1):
                salestatus = 'Purchased'
            elif (cont.find('sold') !=-1 ):
                salestatus = 'sold'
            else:
                salestatus = 'unknown'

            print('side : ',salestatus)
         
            
            arr=[ticker,salestatus,qty,trade_date,summary]
            tradeTotal.append(arr)
            
    print(tradeTotal)

    
    
    return tradeTotal

get_trades()