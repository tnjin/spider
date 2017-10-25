# coding: utf-8

import time
import random
import os
import json
import re
from selenium import webdriver
import traceback


def get_company_urls(url, pages, filename,driver):
    pattern = re.compile('href="(.*?)/page/creditdetail')
    for i in range(6,27):
        #driver = webdriver.Chrome("D:/Program/chromdriver/chromedriver.exe")#PhantomJS()
        new_url = url+'&beginPage={}'.format(str(i+1))
        print(new_url)
        #driver.get(new_url)
        load_page(new_url)
        #time.sleep(10)
        comps = decodeListPage(driver)
        print(comps)
        with open(filename+'.txt','a+') as f:
            for j in comps:
                obj = json.dumps(j,encoding="utf-8")
                f.write(obj)
                f.write("\n")
        #enter_company_detail(filename+'.csv', url_sz, driver)
        #driver.close()
        # time.sleep(random.randrange(3, 7))
        #break


def decodeListPage(driver):
    comp_items = driver.find_elements_by_class_name("company-list-item")
    comps = []
    if comp_items:
        for item in comp_items:
            dic = {}
            name = item.find_element_by_class_name("list-item-title-text").text
            dic["name"] = name
            a = item.find_element_by_link_text(u"更多公司信息>")
            dic["detail_url"] = a.get_attribute("href")
            try:
                hot_div = item.find_element_by_class_name("list-item-itemsWrap")
                if hot_div:
                    lis = hot_div.find_elements_by_tag_name("li")
                    if lis:
                        items = []
                        for li in lis:
                            item = {}
                            a = li.find_element_by_tag_name("a")
                            span = li.find_element_by_class_name("item-offer-title")
                            span = span.find_element_by_tag_name("span")
                            item["url"] = a.get_attribute("href")
                            item["introduce"] = span.get_attribute("outerText")
                            items.append(item)
                        dic["hot"] = items
            except:
                print ("no hot")
            comps.append(dic)
    return comps




def enter_company_detail(fileName,baseUrl,driver):
    reg = re.compile('href="(.*?)gsda_huangye')
    with open(fileName) as urls:
        for url in urls:
            try:
                #driver.get(url)
                load_page(url)
                ul = reg.findall(driver.page_source)
                if not ul or len(ul) == 0:
                    write_to_error("错误-detail:%s"%url)
                    continue
                temp = ul[0].replace("&amp;","&")
                temp = temp+"gsda_huangye"
                print(temp)
                #driver.get(temp)
                #time.sleep(20)
                load_page(temp)
                decodePage(driver,temp)
            except Exception:
                f = open("exlog.txt", 'a+')
                traceback.print_exc(file=f)
                f.flush()
                f.close()





def decodePage(driver,curl):
    h1 = driver.find_element_by_xpath('//*[@id="site_content"]/div[1]/div/div[1]/div/div[2]/div[1]/div/h1')

    company_name = h1.text
    print(company_name)
    trs = driver.find_elements_by_tag_name("tr")
    if not trs:
        write_to_error(company_name,curl)
    else:
        with open(company_name,"w") as f:
            for tr in trs:
                print(tr.text)
                f.write(tr.text.encode("utf-8"))
                f.write("\n")






def write_to_error(name,url):
    with open(name,"a+") as f:
        f.write(name)
        f.write("|")
        f.write(url)
        f.write("\n")


def load_page(url):
    driver.get(url)
    time.sleep(10)
    if "wrongpage.html" in driver.current_url:
        driver.back()
        time.sleep(10)
        driver.get(url)
        time.sleep(10)
    return



driver = webdriver.Chrome("D:/Program/chromdriver/chromedriver.exe")
if __name__ == '__main__':
    url_sz = 'https://www.1688.com/'
    driver.get(url_sz)
    time.sleep(10)
    #get_company_urls(url_sz, 100, u'深圳',driver)
    url_sz = 'https://s.1688.com/company/company_search.htm?keywords=%B4%C9%C6%F7&city=%BE%B0%B5%C2%D5%F2&province=%BD%AD%CE%F7&n=y&filt=y'
    get_company_urls(url_sz, 100, u'景德镇',driver)
    #enter_company_detail(u'景德镇.csv',url_sz,driver)
