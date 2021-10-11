from selenium import webdriver

import pandas as pd

from scrapy.selector import Selector

import sys 

import pickle

import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

df = pd.read_csv("data.csv", encoding= "unicode_escape")

names = df['Description'].loc[df['Description'].notna()].str.lower().unique().tolist()

BASE_URL = r'https://www.amazon.com/s?k='

#driver_path = "./drivers/chromedriver.exe"

def find_nav(url):
    chrome = webdriver.Chrome()
    #chrome = webdriver.Chrome(driver_path)   
    chrome.get(BASE_URL[:-5] + url)
    
    response = Selector(text = chrome.page_source)
    chrome.quit()
    re = response.xpath("//div/@data-category").get()
    if re:
        return re
    re = response.xpath("//div[@id = 'wayfinding-breadcrumbs_container']//li//a//text()")
    try:
        final_re = re.getall()[:3]
    except:
        final_re = re.getall()[:2]
    return list(set(final_re))

def query_product(name,page_num = "1"):
    chrome = webdriver.Chrome()
    #chrome = webdriver.Chrome(driver_path)  
    chrome.get(BASE_URL + name + "&page=" + page_num)
    response = Selector(text = chrome.page_source)
    if response.xpath("//ul[@class = 'a-pagination']").get() == None:
        
        chrome.quit()
        return ""
    relative_urls = response.xpath("//span[@data-component-type = 's-search-results']//h2//a//@href").getall()
    chrome.quit()
    for url in relative_urls:
        re = find_nav(url)
        if re:
            return re
        
    #return query_product(name, page_num = str(int(page_num) + 1))
    return ""

if __name__ == '__main__':
    d = {}
    num = sys.argv[-1]
    try:
        for i,name in enumerate(names):
            if i <= num:
                continue
            d[name] = query_product(name)
            print(i)
            print(name, d[name].__str__())
            
            if (i + 1)%100 == 0:
                with open("./output/out{}".format(i),"wb") as f: pickle.dump(d,f)
                d = {}
    except:
        print("python autolabel [on going number e.g]")    
    