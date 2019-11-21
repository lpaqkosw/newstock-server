#-*- coding:utf-8 -*-

import sys
import pandas as pd
import datetime as dt
import html5lib
import json
import io
import requests
from bs4 import BeautifulSoup


def findCode(compname):
    with io.open('stock_data_eng.txt','rt', encoding='utf-8-sig') as f:
        compjson = json.load(f)
    for dict in compjson['Sheet1']:
        if dict['compName'] == compname.decode("utf-8"):
            return dict['compCode']

def findPage(date):
    dateObj = dt.datetime.strptime(date,"%Y.%m.%d")
    today = dt.datetime.today()
    delta = today - dateObj
    pageDelta = int(delta.days/14)
    pageNumber = 1 + pageDelta
    return pageNumber

'''
def todayInfo(code):
    url = "https://finance.naver.com/item/main.nhn?code="+ code
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")

    no_today = bs_obj.find("p", {"class": "no_today"}) 
    blind = no_today.find("span", {"class": "blind"}) 
     
    no_exday = bs_obj.find("p", {"class": "no_exday"})
    comp = no_exday.find_all("span", {"class": "blind"})
     
    no_info = bs_obj.find("table", {"class": "no_info"})
    infoTable = no_info.find_all("span", {"class": "blind"})
      

    todayData = [{
        "closingPrice" : blind.text,
        "comparedValue" : comp[0].text,
        "comparedPercent" : comp[1].text,
        "prevClosingPrice" : infoTable[0].text,
        "highPrice" : infoTable[1].text,
        "highLimit" : infoTable[2].text,
        "tradedAmount" : infoTable[3].text,
        "sikka" : infoTable[4].text,
        "lowPrice" : infoTable[5].text
    }]

    
    return todayData
'''


def pastInfo(code, page):
    url = ('https://finance.naver.com/item/sise_day.nhn?code='+code+'&page='+str(page))

    data = pd.read_html(url, encoding = 'utf-8')
    data = data[0]
    data.columns = ['date','closingPrice','comparedValue','sikka', 'highPrice', 'lowPrice', 'tradedAmount']
    price_data = data.dropna(axis=0, how='any')
    # price_data = price_data.drop(price_data.index[0])
    price_data = price_data.reset_index(drop=True)
    price_data['date'] = pd.to_datetime(price_data['date'], format='%Y-/%m-/%d', errors ='ignore')
    return price_data.to_json(orient='records')
