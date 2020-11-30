import requests
import urllib.request
from fake_useragent import UserAgent
import json
import re
from flask import Flask,render_template

app = Flask(__name__)
json_list = []

@app.route('/')
def Hello_world():
    return "Hello World"


@app.route('/index')
def index_page():
    return render_template('index.html')


@app.route('/get_data')
def AjaxCrawler():
    Num = 3
    for num in range(Num):
        url1 = "http://ticket.lvmama.com/a-zhongguo3548/tf-P"+str(num)+"?keyword=%E4%B8%AD%E5%9B%BD&tabType=ticket#list"
        headers = {
            "User-Agent" : UserAgent().chrome
        }
        response = requests.get(url1,headers=headers)
        #print(response.text)
        RE_part = re.compile('<dd title="(.*?)">.*?</dd>',re.S)
        addr = re.findall(RE_part,response.text)
        for address in addr:
            url2 = 'http://api.map.baidu.com/geocoder/v2/?address=' + address + '&output=json&ak=ruEAsTrLeT1mDaWqkc9XFNuQ2GCzL8C7'
            json_data = requests.get(url2).json()
            json_geo = json_data['result']['location']
            json_list.append(json_geo)
        bjson_list = json.dumps(json_list)
        return bjson_list


if __name__ == "__main__":
    app.run(debug=1)