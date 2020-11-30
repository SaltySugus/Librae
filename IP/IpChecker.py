import socket
import requests
import re
from fake_useragent import UserAgent
from multiprocessing import Pool

HttpFile = "HTTP_IP.txt"
HttpsFile = "HTTPS_IP.txt"

MyName = socket.getfqdn(socket.gethostname())
MyAddr = socket.gethostbyname(MyName)

def Delete_ip(Str,filename):
    iterance = True
    with open(filename, "r", encoding="utf-8") as f1:
        lines = f1.readlines()
        #print(lines)
    with open(filename, "w", encoding="utf-8") as f1:
        for line in lines:
            if Str in line and iterance == True:
                iterance = False
                continue
            f1.write(line)


CheckerUrl="http://httpbin.org/get"
headers={
    "User-Agent": UserAgent().random
}
def Get_IpData(fileName):
    with open(fileName, "r", encoding="utf-8") as f:
        Data = f.read()
    Match = "(.*?)\n"
    Match_Rsult = re.findall(Match,Data)
    return Match_Rsult

def Checker(data,Num,filename):
    for num in range(Num,len(data),4):
        Data = data[num]
        proxies={
               'http': "http://"+Data
        }
        try:
            resp = requests.get(CheckerUrl,proxies=proxies,timeout=3)
        except:
            print("This ip is unuseable....")
            Delete_ip(Data, filename)
            continue
        Match = '"origin": "(.*?)"'
        Match_Result = re.findall(Match, resp.text)
        if Match_Result == []:
            Delete_ip(Data,filename)
            continue
        print(Match_Result[0])

if __name__ == "__main__":
    print("本机ip：", MyAddr)
    getData1 = Get_IpData(HttpFile)
    #Checker(getData)
    pool1 = Pool(4)
    for i in range(4):
        pool1.apply_async(Checker,args=(getData1,i, HttpFile))
    pool1.close()
    pool1.join()
    print("------Http ip is done,now is the Https-----")
    getData2 = Get_IpData(HttpsFile)
    # Checker(getData)
    pool2 = Pool(4)
    for i in range(4):
        pool2.apply_async(Checker, args=(getData2, i, HttpsFile))
    pool2.close()
    pool2.join()