
import urllib.request
from bs4 import BeautifulSoup

#抓取天涯鬼话中的我可能不是人类的楼主帖子


# open the url


def load_html(url):
    res = urllib.request.urlopen(url)
    page = res.read()
    html_str = page.decode("utf-8")
    res.close()
    # print(html)
    return html_str


def parse_html(txt):
    soup = BeautifulSoup(txt, "html.parser")
    # par = soup.select("div .bbs-content")
    content = soup.find_all("div", attrs={"class": "bbs-content"})
    # print(par)
    # for item in content:
      #  print(item.text)
    author = soup.find_all("div", attrs={"class": "atl-info"})
    # for alt in author:
       # print(alt.text)
    if len(author) == len(content):  #this is first page
        print("===============")
    else:  # not first page
        author.remove(author[0])
        # if soup.find("div", attrs={"class": "atl-con-bd"}):
    _print(author, content)


def _print(author, content):
    with open("C:\\Users\\Tjz\\Desktop\\teach\\tianya.txt", "a+") as f:
        for alt, con in zip(author, content):
            if "楼主" in alt.text:
                txt = con .text.strip()
                print(txt)
                print("++++++++++++++++++++++++++++++++++++++")
                f.write(txt)
                f.write("\n")
                f.write("++++++++++++++++++++++++++++++++++++++")
                f.write("\n")


if __name__ == '__main__':
    for i in range(1, 37):
        url = r"http://bbs.tianya.cn/post-16-1617041-%d.shtml" % i
        # print(url)
        html = load_html(url)
        parse_html(html)


