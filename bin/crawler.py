import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

url = "https://zhuanye.911cha.com/list_6_"
url_final = "https://zhuanye.911cha.com/list_6_200.html"


def crawled_url(url):
    """
    爬去一个网页，返回单词列表
    :param url:
    :return:
    """

    try:
        # 下载网页
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent,}
        r = requests.get(url,headers=headers)

        # 解析网页
        result = []
        soup = BeautifulSoup(r.text,features="html.parser")
        for a in soup.body.table.select("a"):
            if a.string == "详细»":
                continue
            result.append(a.string)
        # 4.返回
        return result
    except:
        return None

def save_list(my_list,filepath):
    with open(filepath,encoding="utf8",mode="w") as fw:
        for line in my_list:
            fw.write(line+"\n")

def crawl_all():
    urls = [url+str(i)+".html" for i in range(1,201)]
    result =[]
    error_url = []
    for url_my in tqdm(urls):
        result_tmep = crawled_url(url_my)
        if result_tmep is None:
            error_url.append(url_my)
        else:
            result.extend(result_tmep)

    save_list(result,"../data/crawled.csv")
    save_list(error_url,"../data/error_url.txt")
if __name__ == "__main__":
    crawl_all()