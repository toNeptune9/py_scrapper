#!/usr/bin/python3
from bs4 import BeautifulSoup
import re
import requests as req
import yaml
import sys
import traceback
import logging

def preparate_dictionary(name_key, d, l) :
    key = name_key
    d.setdefault(key, [])
    for item in l:
        d[key].append(item.text)
    return 

if __name__ == "__main__":
    try:
        input_user = input("Please enter a URL for scrapping: ")
        if not input_user:
            raise ValueError('Empty input!')
    except ValueError as e:
        print (e)
        sys.exit()
    valid = re.compile('https://www.milwaukeetool.com/Products')
    if not valid.search(input_user):
        print ("Can't to scrap this link. Exit")
        sys.exit()        
    resp = req.get(input_user)
    sp = BeautifulSoup(resp.text,'lxml')
    try:
        title = sp.title.text
        desc  = sp.find("meta",property="og:description")
        product_id = sp.find("div", {"data-bv-show": "reviews"})
        keys = sp.find("div",{"class":"product-features"}).find('ul').findAll('li')
        specs = sp.find("div",{"class":"product-specs__table"}).findAll("div",{"class":"product-specs__row"})
        #TODO : make parsed specs looks pretty without extra empty lines
        images = []
        for img in sp.findAll('img'):
            images.append(img.get('src'))
        dict_file = { 'scrapper output from' : input_user , 'information':{'title':title, 'description': desc['content'], 'id' : product_id['data-bv-product-id']}}
        #TODO: fix order of the dict_file
        preparate_dictionary("key_features",dict_file,keys) 
        preparate_dictionary("specs",dict_file,specs)
        with open(r'out.yaml','w') as file:
            documents = yaml.dump(dict_file,file)
        print("check the output file out.yaml, exit program")
    except Exception as e:
        logging.error(traceback.format_exc())