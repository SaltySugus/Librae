import requests
from time import time

CheckerUrl="http://httpbin.org/get"
proxies={
               'http': "http://116.62.204.38:9999"
        }
Satrt_time = time()
resp = requests.get(CheckerUrl,proxies=proxies)
End_time = time()
Total_time = End_time - Satrt_time
print(Total_time)
print(resp.text)
# Match = '"origin": "(.*?)"'
# Match_Result = re.findall(Match, resp.text)
# print(Match_Result)
# print(Match_Result[0])