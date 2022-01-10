import bs4
import requests
import re
import html2text
from tqdm import tqdm

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

def crawl_train(train):
    try:
        web = 'https://www.jt2345.com/huoche/checi/'+train+'.htm'
        info = requests.get(web,headers=headers)
        info.raise_for_status()
        info.encoding = "GBK"
    
        info = bs4.BeautifulSoup(info.text, "html.parser")
        info = html2text.html2text(str(info))
    
        info = info[info.index('\n1')+1:].split('\n')
        info = [i for i in info if len(i)>0 and '[' in i]
        info = [i for i in info if i[0].isdigit()]
    
        info = [i[i.index('[')+1:i.index(']')] for i in info]
        return info
    except:
        #print(train+'download failed')
        return train
    
def crawl_list(train_list):
    download_failed = []
    trains = []

    for train in tqdm(train_list):
        station = crawl_train(train)
        if type(station) == str:
            download_failed.append(station)
        else:
            trains.append(train+':'+','.join(station))
          
    return trains, download_failed