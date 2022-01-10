# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 14:43:29 2022

@author: 10951
"""
#%% 匹配车站所在省市县
import requests as rq
import pandas as pd
loc_dict = pd.read_csv('coords.csv',index_col='dim')
loc_dict = pd.DataFrame(loc_dict).to_dict()

loc_none_list = []
        
for station in loc_dict:    
    url = "http://restapi.amap.com/v3/geocode/regeo"  
    params = {'key':'d06ff6e614baadc4e5aa3689d5c3c3f5',
            'location': str(loc_dict[station]['lng'])+','+str(loc_dict[station]['lat']) }  #经度在前，维度在后              
    res = rq.get(url,params).json()
    if res['status']=='1':
        loc_dict[station]['province'] = res['regeocode']['addressComponent']['province']            
        loc_dict[station]['city'] = res['regeocode']['addressComponent']['city']            
        loc_dict[station]['district'] = res['regeocode']['addressComponent']['district'] 
        if len(loc_dict[station]['city'])==0:
            loc_dict[station]['city'] = loc_dict[station]['province']
    else:
        loc_none_list.append(station)
        
pd.DataFrame(loc_dict).to_csv('address.csv',encoding='utf-8-sig')  # 导出数据                  

#%% 计算车站之间的距离
from scipy.spatial.distance import cdist
from pyproj import Transformer

def loc_transform(station):
    lat = loc_dict[station]['lat']
    lng = loc_dict[station]['lng']
    transformer = Transformer.from_crs("epsg:4326","epsg:3857")
    x, y = transformer.transform(lat, lng)
    return [[x,y]]

def cal_distance(s1,s2):
    return cdist(loc_transform(s1),loc_transform(s2),metric='euclidean')

cal_distance('苏州北','上海虹桥')
