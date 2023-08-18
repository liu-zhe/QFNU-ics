# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO

week = {
    "星期一": "Mon", "星期二": "Tue", "星期三": "Wed", "星期四": "Thu", "星期五": "Fri", "星期六": "Sat", "星期七": "Sun"
}
session = requests.session()


class QFNUApi:
    RandCodeUrl = 'http://zhjw.qfnu.edu.cn/verifycode.servlet'
    loginUrl = 'http://zhjw.qfnu.edu.cn/Logon.do?method=logonLdap'
    dataStrUrl = 'http://zhjw.qfnu.edu.cn/Logon.do?method=logon&flag=sess'
    kbUrl = "http://zhjw.qfnu.edu.cn/jsxsd/framework/main_index_loadkb.jsp"

    kbWeek = -1
    kbText = ""
    num = 0

    def __init__(self, userAccount, userPassword):
        self.name = []
        self.info = []
        self.begin = []
        self.end = []
        self.location = []
        self.data = {
            'userAccount': userAccount,
            'userPassword':  userPassword,
            "RANDOMCODE": '',
            'encoded': ''
        }

        header = {
            "Content-Type": "text/html;charset=utf-8",
            "Vary": "Accept-Encoding"
        }
        response = session.get(
            url=self.dataStrUrl, headers=header, timeout=1000)
        self.cookies = session.cookies.get_dict()
        self.dataStr = response.text

    def display_random_code(self):
        response = session.get(
            self.RandCodeUrl, cookies=self.cookies)
        image = Image.open(BytesIO(response.content))
        image.show()
        self.data['RANDOMCODE'] = input("输入验证码内容：")

    def get_encoded(self):
        res = self.dataStr.split("#")
        code = res[0]
        sxh = res[1]
        data = self.data['userAccount'] + "%%%" + self.data['userPassword']
        length = 0
        for b in code:
            length += 1
        encoded = ""
        b = 0
        for a in range(length):
            if a < 20:
                encoded = encoded + data[a]
                for c in range(int(sxh[a])):
                    encoded = encoded + code[b]
                    b += 1
            else:
                encoded = encoded + data[a:]
                self.data['encoded'] = encoded
                return encoded
            a += 1
        self.data['encoded'] = encoded
        return encoded

    def login(self):
        print(self.data)
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;"
                      "q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Length": "135",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "zhjw.qfnu.edu.cn",
            "Origin": "http://zhjw.qfnu.edu.cn",
            "Proxy-Connection": "keep-alive",
            "Referer": "http://zhjw.qfnu.edu.cn/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/83.0.4103.116 Safari/537.36",
        }
        response = session.post(
            url=self.loginUrl, headers=header, data=self.data, cookies=self.cookies, timeout=1000)

        # print(response.text)
        return self.cookies

    def fetch(self, _date):
        self.name.clear()
        self.info.clear()
        self.location.clear()
        self.begin.clear()
        self.end.clear()
        date = _date.strftime("%Y-%m-%d")
        # 将日期字符串转换为datetime对象

        # 计算日期的周数
        _week = _date.isocalendar()[1]

        # 判断周数是否相等
        if _week != self.kbWeek:
            self.kbWeek = _week
            header = {
                "Host": "zhjw.qfnu.edu.cn",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50",
                "Origin": "http://zhjw.qfnu.edu.cn",
                "Referer": "http://zhjw.qfnu.edu.cn/jsxsd/framework/xsMain_new.jsp?t1=1"
            }
            res = session.post(
                self.kbUrl,
                headers=header,
                data={'rq': date, 'sjmsValue': '94786EE0ABE2D3B2E0531E64A8C09931'},
                cookies=self.cookies,
                timeout=3000
            )
            soup = BeautifulSoup(res.text, 'html.parser')
            # print(soup)
            data = soup.select("p")
            self.kbText = data
            self.num += 1
            print('POST #' + str(self.num))
        else:
            data = self.kbText

        for i in range(0, len(data), 1):
            htmlstr = str(data[i])
            htmlcontent = htmlstr[70:len(htmlstr)]
            content = htmlcontent.split("&lt;br/&gt;")
            # print(content)
            if (week[content[3].split(" ")[1]] == _date.strftime("%a")):
                self.name.append(content[2])
                self.info.append(content[0] + content[1])
                self.location.append(content[4])

                class_time = content[3].split(" ")[2].replace('[', '')
                class_time = class_time.replace(']节', '')
                self.begin.append(class_time.split("-")[0])
                self.end.append(class_time.split("-").pop())

            # content[len(content)-1] = content[len(content) -
            #                                   1].replace('</p>', '')
            # content[len(content)-1] = content[len(content) -
            #                                   1].replace('\">', ' ')
            # for i in range(0, len(content), 1):
            #     print(content[i])
