import urllib.request
from bs4 import BeautifulSoup
import http.cookiejar
import chardet
import os


def load_html(openner, url):
    res = openner.open(url)
    page = res.read()
    html_str = page.decode("utf8")
    res.close()
    # print(html)
    return html_str




def decodeIndexPage(html,opener):
    #print(html)
    soup = BeautifulSoup(html,"html.parser")
    alist = soup.find_all(name="a", attrs={"rel":"bookmark"})
    titleSet = []
    #print(alist)
    for a in alist:
        print(a.get("title"))
    for a in alist:
        if a.get("title") in titleSet:
            continue
        else:
            titleSet.append(a.get("title"))
        print("%s---------------------------------------------------------------------------------------------------------"%a.get("title"))
        folder = createFolder(a.get("title"))
        secHtml = load_html(openner,a.get("href"))
        decodeSecPage(secHtml,folder)



def decodeSecPage(html,folder):
    soupSec = BeautifulSoup(html,"html.parser")
    main = soupSec.find(name="div", attrs={"class": "td-post-featured-image"})
    img = main.find(name="img", attrs={"class": "entry-thumb"})
    imgs = soupSec.find_all(name="img",attrs={"class":"alignnone"})
    imgs.append(img)
    i = 1
    for img in imgs:
    #print(imglist)
        set = img.get("srcset")
        if not set:
            set = img.get("src")
            if not set:
                continue
            else:
                urllib.request.urlretrieve(set, os.path.join(folder, "%s.jpg" % i))
                i=i+1
                continue
        item = set.split(",")
        #print(item)
        urls =item[-1]
        #print(urls)
        urls = urls.split(" ")
        #print(urls)
        url = urls[1]
        url = fromatUrl(url)
        #print(url)
        urllib.request.urlretrieve(url, os.path.join(folder, "%s.jpg"%i))
        i=i+1
    print("total:%s" % i)


def fromatUrl(url):
    if url[-12] == "-":
      return  url[:-12]+url[-4:]
    else:
        return url

def createFolder(title):
    path = os.getcwd()
    path = os.path.join(path,title)
    if os.path.exists(path):
        return path
    else:
        os.makedirs(path)
        return path

if __name__ == '__main__':
    urls = [r"http://www.coserspark.com/index.php/category/%E7%BE%8E%E5%9B%BE/",
            r"http://www.coserspark.com/index.php/category/%E7%BE%8E%E5%9B%BE/page/2/",
           r"http://www.coserspark.com/index.php/category/%E7%BE%8E%E5%9B%BE/page/3/"]
    cj = http.cookiejar.CookieJar()
    openner = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    openner.addheaders = [('User-agent', 'Mozilla/5.0')]
    for u in urls:
        html = load_html(openner,u)
        decodeIndexPage(html,openner)