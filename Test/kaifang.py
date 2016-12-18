import urllib.request
from bs4 import BeautifulSoup
import threading
import  time
#抓取传说中两千万的开放数据

def decode_person(content):
    soup = BeautifulSoup(content, "html.parser")
    table = soup.select("td")
    person = dict()
    for i in range(0, len(table), 2):
        if(table[i+1].text == '' ):
            continue
        person[table[i].text] = table[i+1].text
    return person



def load_html(url):
    res = urllib.request.urlopen(url)
    page = res.read()
    html_str = page.decode("gbk")
    res.close()
    # print(html)
    return html_str


def grab(start, end):
    url = r"http://www.kfzlk.com/show.asp?id=%d"
    file_name = "E:\\private\\kaifang_%d_%d.txt" % (start, end)
    log_name = "E:\\private\\kaifang_log_%d_%d.txt" % (start, end)
    with open(file_name, "a+") as f:
        for i in range(start, end):
            temp_url = url % i
            if i % 100 == 0:
                print(temp_url)
            try:
                _str = load_html(temp_url)
                per = decode_person(_str)
                per["id"] = i
                if i % 100 == 0:
                    print(per)
                f.write(str(per))
                f.write("\n")
            except Exception as ex:
                with open(log_name, "a+") as log:
                    log.write(temp_url)
                    log.write("\n")
                    print(ex)
        f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

if __name__ == '__main__':
    for i in range(0, 10):
        s = i * 2000000
        e = s + 2000000
        t1 = threading.Thread(target=grab, args=(s, e))
        t1.start()

