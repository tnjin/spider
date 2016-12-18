
import urllib.request
from bs4 import BeautifulSoup
import http.cookiejar

cj = http.cookiejar.CookieJar()
openner = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
res = openner.open(r"http://xiazai.zol.com.cn/detail/34/333261.shtml")
page = res.read()
html_str = page.decode("gbk")
res.close()
soup = BeautifulSoup(html_str, "html.parser")
print(html_str)
hx = soup.find("a", attrs={"id": "dxgs1"})
print('\n')
print(hx)

