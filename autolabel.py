import requests

from selenium import webdriver

import pandas as pd

from scrapy.selector import Selector

df = pd.read_csv("data.csv", encoding= "unicode_escape")

names = df['Description'].loc[df['Description'].notna()].str.lower().unique().tolist()

def find_nav(url):
    global CUR,N
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server={}'.format(proxy[CUR%N]))
    CUR += 1
    chrome = webdriver.Chrome(driver_path)
    
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
    global CUR,N
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server={}'.format(proxy[CUR%N]))
    CUR += 1
    chrome = webdriver.Chrome(driver_path)
                                
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
        