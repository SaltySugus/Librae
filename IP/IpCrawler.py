from pyquery import PyQuery as pq
import requests
from fake_useragent import UserAgent
from multiprocessing import Pool

headers = {
        "User-Agent": UserAgent().random
    }

#从ip代理网站获取ip信息
def HTTP_and_HTTPS_crawler(url):
    response = requests.get(url,headers=headers)
    doc = pq(response.text)
    trs = doc('#ip_list tr')
    for num in  range(1,len(trs)):
        ip = trs.eq(num).find('td').eq(1).text()
        port = trs.eq(num).find('td').eq(2).text()
        type = trs.eq(num).find('td').eq(5).text()
        if type == "HTTP":
            Data_SaveFile(ip, port, "HTTP_IP.txt")
        elif type == "HTTPS":
            Data_SaveFile(ip, port, "HTTPS_IP.txt")

#保存获取到的ip信息
def Data_SaveFile(ip,port,fileName):
    with open(fileName, "a", encoding="utf-8") as f:
        f.write(ip + ':' + port+'\n')


def main(Offest):
    url = "http://www.xicidaili.com/nn/"+str(Offest)
    HTTP_and_HTTPS_crawler(url)


#进程池来多线程爬取网站
if __name__ == "__main__":
    num = int(input("输入爬取页数"))
    pool = Pool()
    pool.map(main,[i for i in range(num)])
    pool.close()
    pool.join()
    print(" Crawler running success !....")