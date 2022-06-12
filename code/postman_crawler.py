import pandas as pd
import numpy as np
import os
import requests
from bs4 import BeautifulSoup
from lxml import html

headers = {
    'Content-Type': 'application/x-www-form-urlencoded;',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  + 'AppleWebKit/537.36 (KHTML, like Gecko) '
                  + 'Chrome/102.0.0.0 Safari/537.36',
    'referer': 'https://goodinfo.tw/tw/StockFinDetail.asp?'
               + 'RPT_CAT=BS_M_QUAR&STOCK_ID=2332',
    'Cookie': 'CLIENT%5FID=20220604002816788%5F101%2E10%2E6%2E162'
}

TEMPATH = os.path.join('.', 'template.html')
SEASON = [20214, 20201, 20182]


def genUrlnPayload(sticker, stype, session):
    """Generate URL and Payload"""
    url = 'https://goodinfo.tw/tw/StockFinDetail.asp?STEP=DATA&STOCK_ID=%d&RPT_CAT=%s&QRY_TIME=%d' % (sticker, stype, session)
    payload = 'STEP=DATA&STOCK_ID=%d&RPT_CAT=%s&QRY_TIME=%d' % (sticker, stype, session)
    
    return url, payload


def postReq(url, payload):
    """Get HTML"""
    res = requests.request('POST', url, headers=headers, data=payload)
    res.encoding = 'utf-8'

    return res.text


def resHandler(text):
    """Discard first table tag and insert into HTML template"""
    soup = BeautifulSoup(text, 'html.parser')
    
    with open(TEMPATH, 'r') as temPage:
        temSoup = BeautifulSoup(temPage, 'html.parser')
        soup.find('table').decompose()
        temSoup.find('body').append(soup)
        tmpDfs = pd.read_html(str(temSoup))

        return tmpDfs


def cleanTrans(df):
    """Clean dataframe"""
    df.columns = ['', '金額', '%', '金額', '%', '金額', '%', '金額',
                  '%', '金額', '%', '金額', '%', '金額', '%']
    df.drop(['%'], axis=1, inplace=True)
    df = df.transpose()
    df.columns = df.iloc[0]
    df.drop(df.index[0], axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    ls = df.columns[df.columns.duplicated()].values.tolist()
    df.drop(ls, axis=1, inplace=True)
    
    return df


def addTimeNameIndux(df, sticker, season):
    """Add information to datasets"""
    switch = {
        20214: [
            ['2021', '2021', '2021', '2021', '2020', '2020', '2020'],
            ['Q4', 'Q3', 'Q2', 'Q1', 'Q4', 'Q3', 'Q2']
        ],
        20201: [
            ['2020', '2019', '2019', '2019', '2019', '2018', '2018'],
            ['Q1', 'Q4', 'Q3', 'Q2', 'Q1', 'Q4', 'Q3']
        ],
        20182: [
            ['2018', '2018', '2017', '2017', '2017', '2017', '2016'],
            ['Q2', 'Q1', 'Q4', 'Q3', 'Q2', 'Q1', 'Q4']
        ]
    }
    
    years = switch.get(season, '')[0]
    quarters = switch.get(season, '')[1]

    tmp = pd.DataFrame(columns=['公司', '股票代號', '產業', '年份', '季度'])
    name, indus = getNameIndus(sticker)
    tmp['公司'] = [name]*7
    tmp['股票代號'] = [sticker]*7
    tmp['產業'] = [indus]*7
    tmp['年份'] = years
    tmp['季度'] = quarters
    
    df = pd.concat([tmp, df], axis=1)

    return df


def getNameIndus(sticker):
    """Get company's name and industry"""
    url = 'https://goodinfo.tw/tw/StockDetail.asp?STOCK_ID=%d' % (sticker)
    
    res = requests.request('get', url, headers=headers)
    byte_data = res.content
    source_code = html.fromstring(byte_data)
    nameXp = '/html/body/table[2]/tr/td[3]/table/tr[1]/td/table/tr/td[1]/table/tr[1]/th/table/tr/td[1]/nobr/a/text()'
    indXp = '/html/body/table[2]/tr/td[3]/table/tr[2]/td[3]/table[1]/tr[3]/td[2]/text()'
    
    name = source_code.xpath(nameXp)[0][5:]
    indus = source_code.xpath(indXp)[0]
    
    return name, indus


def companyState(sticker, stype):
    """Aggregate one company's financial statements"""
    dfs = []
    
    for i in range(len(SEASON)):
        url, payload = genUrlnPayload(sticker, stype, SEASON[i])
        tmpDfs = resHandler(postReq(url, payload))
        df = cleanTrans(tmpDfs[0])
        dfs.append(addTimeNameIndux(df, sticker, SEASON[i]))

    dfs = pd.concat(dfs, ignore_index=True)[:-1]
    
    return dfs


def wholeState(companies, stype):
    """Aggregate all companies' financial statements"""
    dfs = []
    
    for c in companies:
        dfs.append(companyState(c, stype))

    wDf = pd.concat(dfs, ignore_index=True)
    wDf = wDf.replace('-', 0).replace(np.nan, 0)
    numColsName = wDf.columns[5:]
    wDf[numColsName] = wDf[numColsName].astype('float64')
    wDf['年份'] = wDf['年份'].astype('int')
    wDf['季度'] = wDf['季度'].astype('string')
    
    return wDf


if __name__ == '__main__':
    wholeState([2330, 2303, 5347], 'IS_M_QUAR').to_excel('IS_whole.xlsx')