# coding:utf-8
import requests
from bs4 import BeautifulSoup
import json
import time



brands_dict = {} #source text from web
brand_dict = {} #cleaned brand
series_dict = {} #source text from web 
serie_dict = {} #cleaned serie
hedges_dict = {} #source text from web
hedge_dict ={} #cleaned hedge
series = ""

requests.packages.urllib3.disable_warnings()
'''
#get brand
URL1 = "https://www.iautos.cn/car/brands-group-by-pinyin/?_ajax=1&_=1565081024964"
response = requests.get(url=URL1, timeout=30, verify=False)
sour_brand = response.text
#load & dump brand_json
brands_dict = json.loads(sour_brand)
with open("brand.json", "w") as brand:
    json.dump(brands_dict, brand)
    #datas up there just get it for once and load it back below
'''
#dump brand and get series
with open("brand.json", "r") as brand:
    brands_dict = json.load(brand)
for alfa in brands_dict:
    for brands in brands_dict[alfa]:
        brand_dict[brands['id']] = brands
'''
#get serie_id
number = 1565081024965
count = 1
for brand_id in brand_dict:
    #forge url
    URL2 = "https://www.iautos.cn/car/ajax-series/?brand_id=%s&_ajax=1&_=%s" % (brand_id, str(number+count))
    
    #use different sequence bumber
    count += 1
    response = requests.get(url=URL2, timeout=30, verify=False)
    sour_series = response.text

    #clean serie_id
    series_dict = json.loads(sour_series)
    serie_dict[brand_id] = {}
    for mfrs in series_dict:
        serie_dict[brand_id][mfrs["car_mfrs"]["iautos_name"]] = {}
        for serie in mfrs["car_series"]:
            serie_dict[brand_id][mfrs["car_mfrs"]["iautos_name"]][serie["id"]]= serie
    time.sleep(1)
    print(brand_id)
print(serie_dict)
#dump series
with open("serie.json", "w") as serie:
    json.dump(serie_dict, serie)
    #datas up there just get it for once and load it back below
'''
number = 1565082124965
count = 1
with open("serie.json", "r") as serie:
    serie_dict = json.load(serie)
for serie in serie_dict:
    for mfrs in serie_dict[serie]:
        for serie_info in serie_dict[serie][mfrs]:
            serie_id = serie_dict[serie][mfrs][serie_info]['id']
            print(serie_id)
            
            #get hedge_ratio
            #forge url
            URL3 = "https://www.iautos.cn/?c=ajax&a=ratio&series_id=%s&_ajax=1&_=%s" % (serie_id, str(number+count))
            
            #use different sequence bumber
            count += 1
            response = requests.get(url=URL3, timeout=30, verify=False)
            sour_hedges = response.text
        
            #clean serie_id
            hedges_dict = json.loads(sour_hedges)
            hedge_dict[serie_id] = {}
            if hedges_dict["status"] == 1 :
                hedge_dict[serie_id] = hedges_dict["data"]
            else:
                hedge_dict[serie_id] = {"hedge_ratio":[0,0,0,0,0,0,0,0]}
            
            time.sleep(1)
                           
with open("hedge.json", "w") as hedge:
    json.dump(hedge_dict, hedge)
'''
sour = response.text
root = BeautifulSoup(sour, "html.parser")
flow = root.find("div", "iSelectList")
upnum = flow.find("a")
print(upnum)

#load json
with open("ssq.json", 'r') as ssq_f:
    count = 1
    dict = json.load(ssq_f)
    #write new upnum
    dict[upnum.string] = {"ssq" : upnum["href"]}
    #get red ssq
    ball_red = root.find_all("li", "ball_red")
    for red in ball_red:
        dict[upnum.string]["red" + str(count)] = red.string
        count += 1
    #get blue ssq
    ball_blue = root.find("li", "ball_blue")
    dict[upnum.string]["blue"] = ball_blue.string

#dump ssq
with open("ssq.json", 'w') as ssq:
    json.dump(dict, ssq)
'''










