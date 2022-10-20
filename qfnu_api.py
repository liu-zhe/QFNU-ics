from bs4 import BeautifulSoup
import requests
from time import sleep

week = {
    "星期一": "Mon", "星期二": "Tue", "星期三": "Wed", "星期四": "Thu", "星期五": "Fri", "星期六": "Sat", "星期七": "Sun"
}


class QFNUApi:
    def __init__(this, cookies):
        this.name = []
        this.info = []
        this.begin = []
        this.end = []
        this.location = []
        this.url = "http://202.194.188.38/jsxsd/framework/main_index_loadkb.jsp"
        this.headers = {
            "Host": "202.194.188.38",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50",
            "Origin": "http://202.194.188.38",
            "Referer": "http://202.194.188.38/jsxsd/framework/xsMain_new.jsp?t1=1"
        }
        this.cookies = cookies

    def fetch(this, _date, sjmsValue='94786EE0ABE2D3B2E0531E64A8C09931'):
        this.name.clear()
        this.info.clear()
        this.location.clear()
        this.begin.clear()
        this.end.clear()
        date = _date.strftime("%Y-%m-%d")
        res = requests.post(
            this.url,
            headers=this.headers,
            data={'rq': date, 'sjmsValue': sjmsValue},
            cookies=this.cookies
        )
        soup = BeautifulSoup(res.text, 'html.parser')
        data = soup.select("p")
        for i in range(0, len(data), 1):
            htmlstr = str(data[i])
            htmlcontent = htmlstr[70:len(htmlstr)]
            content = htmlcontent.split("&lt;br/&gt;")

            if (week[content[3].split(" ")[1]] == _date.strftime("%a")):
                this.name.append(content[2])
                this.info.append(content[0] + content[1])
                this.location.append(content[4])

                class_time = content[3].split(" ")[2].replace('[', '')
                class_time = class_time.replace(']节', '')
                this.begin.append(class_time.split("-")[0])
                this.end.append(class_time.split("-").pop())

            # content[len(content)-1] = content[len(content)-1].replace('</p>', '')
            # content[len(content)-1] = content[len(content)-1].replace('\">', ' ')
            # for i in range(0, len(content), 1):
            #     print(content[i])
