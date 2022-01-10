
#%%载入需要的包
import requests as rq
from bs4 import BeautifulSoup as bs
import json

#读取站点数据
def read_data(name):
    railway = {}
    with open('data/train_'+name+'.txt') as f:
        for line in f.readlines():
            rail_name, station = line.split(':')
            railway[rail_name] = station[:-1].split(',')
    return railway
railway_type = ['g','d','k','t','c','z','n']
railway = {r_type:read_data(r_type) for r_type in railway_type}

station_list = set()
for k,v in railway.items():
    for k,u in v.items():
        station_list = station_list | set(u)
station_list

#%%使用高德地图API获取站点的地理位置
def getloc(key,headers,station):
    url = 'https://restapi.amap.com/v3/geocode/geo?address='+station+'站&poitype=火车站&output=XML&key=' + key
    rx = rq.get(url,headers = headers)
    rx.raise_for_status
    rx.encoding = 'UTF-8'
    tx = rx.text
    so = bs(tx,'html.parser')
    if so.find('location') is None:
        return dict()
    else:
        loc = str(so.find('location').string)
        coords = dict()
        coords['lng'] = float(loc.split(',')[0])
        coords['lat'] = float(loc.split(',')[1])
        return coords

#站点经纬度字典
key = 'd06ff6e614baadc4e5aa3689d5c3c3f5'   # need to change the key to your own key
headers = {'User-Agent':'Chrome/72.0'}
loc_dict = {}
station_list=list(station_list)
for station in station_list:
    loc_dict[station] = getloc(key,headers,station)

#没有找到对应的经纬度位置的站点
loc_none_list = []
for k,v in loc_dict.items():
    if v=={}:
        loc_none_list.append(k)
len(loc_none_list)  #249个

#%% 更改匹配方式再匹配一次
def getloc1(key,headers,station):
    url = 'https://restapi.amap.com/v3/geocode/geo?address='+station+'站&poitype=高铁站&output=XML&key=' + key
    rx = rq.get(url,headers = headers)
    rx.raise_for_status
    rx.encoding = 'UTF-8'
    tx = rx.text
    so = bs(tx,'html.parser')
    if so.find('location') is None:
        return dict()
    else:
        loc = str(so.find('location').string)
        coords = dict()
        coords['lng'] = float(loc.split(',')[0])
        coords['lat'] = float(loc.split(',')[1])
        loc_none_list.remove(station)
        return coords
    
for station in loc_none_list:
    loc_dict[station] = getloc1(key,headers,station)   
len(loc_none_list)  


#%% 使用百度地图API获取没有匹配到的站点的经纬度信息（可能存在匹配不准确的问题）
def getloc2(station):
    url = 'http://api.map.baidu.com/geocoding/v3/'
    params = { 'address' : station+'高铁站', 
               'ak' : 'FC8BnAES6zAWTSxQLN2N254fLRujSwKS', 
               'output': 'json'} 
    res = rq.get(url,params)
    jd = json.loads(res.text)
    if jd['status'] == 1:
        return ''
    else:
        loc_none_list.remove(station)
        coords = jd['result']['location']
        return coords

#如果匹配不到，则使用县的地理位置信息
"""def getloc3(station):
    url = 'http://api.map.baidu.com/geocoding/v3/'
    params = { 'address' : station+'县',  
               'ak' : 'FC8BnAES6zAWTSxQLN2N254fLRujSwKS', 
               'output': 'json'} 
    res = rq.get(url,params)
    jd = json.loads(res.text)
    if jd['status'] == 1:
        return ''
    else:
        loc_none_list.remove(station)
        coords = jd['result']['location']
        return coords
for station in loc_none_list:
    loc_dict[station] = getloc3(station)   
len(loc_none_list)"""

#%% 剩下一些匹配不到的手动匹配
loc_dict['二道桥'] = {'lng':87.623703,'lat':43.787407}
loc_dict['上高镇'] = {'lng':117.183014,'lat':36.181897}
loc_dict['乌兰胡同'] = {'lng':109.874717,'lat':41.616407}
loc_dict['新固镇'] = {'lng':116.330216,'lat':39.430955}

#%% 导出数据
import pandas as pd
pd.DataFrame(loc_dict).to_csv('coords.csv',encoding='utf-8-sig')

