import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
import os
import datetime
import logging
import requests

from openai import OpenAI

with open("apiley.txt", "r") as f:
    openai_key = f.readline()
# openai_key = "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"
openai_client = OpenAI(api_key=openai_key)

def sendMail(sender, receivers, mail_content):
    # nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    heading = "<p> In some random days, you will receive some random verses! </p>"

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(heading + "\n" + mail_content, "html", "utf-8")
    message["Subject"] = Header("L'amour de tes Rose", "utf-8")
    message["From"] = str("boshi_an@126.com")  # 发送者
    message["To"] = str("Little Fox")  # 接收者

    smtpObj = smtplib.SMTP_SSL("smtp.126.com:465")
    # smtpObj.connect("ssl://smtp.126.com", port=465)
    try:
        # 126的密码需要自己去126的设置里面查找
        smtpObj.login("boshi_an@126.com", "VSOOPELQMTGHEZYX")
    except:
        print("smtp login error")

    smtpObj.sendmail("boshi_an@126.com", receivers, message.as_string())
    smtpObj.quit()


def get_weather():
    # api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}
    api_url = "https://pro.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": 59.9311,
        "lon": 30.3609,
        "appid": "363d4519a3f7c8004129ba4cbdde0312",
    }
    response = requests.get(api_url, params=params)
    data = response.json()
    today = data["list"][0]
    temp = today["main"]["temp"]
    weather = today["weather"][0]["description"]
    return {"temp": temp, "weather": weather}


def get_poem(root):
    # walk the directory
    res = []
    for dir_path, dir_names, file_names in os.walk(root):
        res.extend(file_names)
    # print(res)
    date_str = str(datetime.datetime.today()).split()[0]
    year = int(date_str[0:4])
    month = int(date_str[5:7])
    day = int(date_str[8:10])
    # id = (year * 13 + month * 17 + day * 131) % len(res)
    id = random.randint(0, len(res) - 1)
    if month == 1 and day == 25:
        return (
            '<p align="center">'
            + "Happy birth day! Love my little fox so much! 🥹"
            + "</p>"
        )
    elif day == 1:
        return '<p align="center">' + "Love my little fox so much! 🥺" + "</p>"
    elif year == 2023 and month == 11 and day >= 7 and day <= 21:
        return '<p align="center">' + "Enjoy the trip with your Роза!" + "</p>"
    else:
        file_name = res[id]
        with open(os.path.join(root, file_name)) as f:
            s = f.readlines()
        res = ""
        for line in s:
            res += '<p align="center">' + line + "</p>"
        return res


def get_content(poem, weather):
    # ret = "<p>Today is a lovely day! The temperature is <b>{}°C</b> and the weather is <b>{}</b>.<p>\n".format(
    #     int(round(weather["temp"]-273.15)), weather["weather"]
    # )
    # ret += poem
    gpt_reply = openai_client.chat.completions.create(
    messages=[
            {
                "role": "user",
                "content": "Can you help me create a bed time story for my child? The story should include 2 characters: Little Fox and Little Parrot. Just provide the story without additional words.",
            }
        ],
        model="gpt-4-1106-preview",
    )
    print(gpt_reply)
    ret = "No more verses!"
    return ret


if __name__ == "__main__":
    logging.basicConfig(
        filename="/root/EmailSender/app.log",
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    poem = get_poem("/root/EmailSender/Poems")
    weather = get_weather()
    mail_content = get_content(poem, weather)
    # mail_content = "今天的天气不错，lucky!"
    receivers = ["st122919@student.spbu.ru"]
    # receivers = ["boshi_an@stu.pku.edu.cn"]
    sender = "boshi_an@126.com"
    sendMail(sender, receivers, mail_content)
    logging.warning("Email sent: " + mail_content)
