import requests
import ics
import qfnu_api
import browser_cookie3
import requests
import datetime as dt
from time import sleep


cal = ics.Calendar()

class_time_begin = {
    "01": "08:00:00",
    "02": "09:00:00",
    "03": "10:10:00",
    "04": "11:10:00",
    "05": "14:00:00",
    "06": "15:00:00",
    "07": "16:00:00",
    "08": "17:00:00",
    "09": "19:00:00",
    "10": "20:00:00",
    "11": "21:00:00"
}

class_time_end = {
    "01": "08:50:00",
    "02": "09:50:00",
    "03": "11:00:00",
    "04": "12:00:00",
    "05": "14:50:00",
    "06": "15:50:00",
    "07": "16:50:00",
    "08": "17:50:00",
    "09": "19:50:00",
    "10": "20:50:00",
    "11": "21:50:00",
    "12": "21:50:00"  # 哪个脑瘫犯的错误，12节课
}

summer_class_time_begin = {
    "01": "08:00:00",
    "02": "09:00:00",
    "03": "10:10:00",
    "04": "11:10:00",
    "05": "14:30:00",
    "06": "15:30:00",
    "07": "16:30:00",
    "08": "17:30:00",
    "09": "19:00:00",
    "10": "20:00:00",
    "11": "21:00:00"
}

summer_class_time_end = {
    "01": "08:50:00",
    "02": "09:50:00",
    "03": "11:00:00",
    "04": "12:00:00",
    "05": "15:20:00",
    "06": "16:20:00",
    "07": "17:20:00",
    "08": "18:20:00",
    "09": "19:50:00",
    "10": "20:50:00",
    "11": "21:50:00",
    "12": "21:50:00"  # 哪个脑瘫犯的错误，12节课
}

duration_per_class = 45


sjmsValue = input("打开浏览器登录曲阜师范大学教务系统\n请输入您的sjmsValue（不输入则使用默认）：")
print(sjmsValue)

cookie = browser_cookie3.load('202.194.188.38')
cookies = requests.utils.dict_from_cookiejar(cookie)
api = qfnu_api.QFNUApi(cookies)

print("Sending POST request and generating ics...")

now_date = dt.datetime.now()
for i in range(1, 366, 1):
    # print(now_date.strftime("%a"));
    if (sjmsValue == "\n"):
        api.fetch(now_date)
    else:
        api.fetch(now_date, sjmsValue)

    vis = []
    for j in range(0, len(api.name)):
        if (api.name[j] not in vis):
            e = ics.Event()
            e.name = api.name[j]
            e.location = api.location[j]
            e.description = api.info[j]

            # 夏季作息时间特判
            if (now_date > dt.datetime(dt.datetime.now().year, 5, 1) and now_date < dt.datetime(dt.datetime.now().year, 10, 1)):
                date_time = dt.datetime.strptime(now_date.strftime("%Y-%m-%d") +
                                                 " " + summer_class_time_begin[api.begin[j]], '%Y-%m-%d %H:%M:%S')
                e.begin = str(date_time - dt.timedelta(hours=8))
                date_time = dt.datetime.strptime(now_date.strftime("%Y-%m-%d") +
                                                 " " + summer_class_time_end[api.end[j]], '%Y-%m-%d %H:%M:%S')
                e.end = str(date_time - dt.timedelta(hours=8))  # 时区转换
            else:
                date_time = dt.datetime.strptime(now_date.strftime("%Y-%m-%d") +
                                                 " " + class_time_begin[api.begin[j]], '%Y-%m-%d %H:%M:%S')
                e.begin = str(date_time - dt.timedelta(hours=8))
                date_time = dt.datetime.strptime(now_date.strftime("%Y-%m-%d") +
                                                 " " + class_time_end[api.end[j]], '%Y-%m-%d %H:%M:%S')
                e.end = str(date_time - dt.timedelta(hours=8))  # 时区转换

            cal.events.add(e)
            vis.append(api.name[j])
    now_date = now_date + dt.timedelta(days=1)

with open('output.ics', 'wb') as f:
    raw = cal.serialize()
    f.write(raw.encode('utf8'))

qwq = input("Done..")
