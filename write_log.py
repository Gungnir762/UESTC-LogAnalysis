from read_log import updateDB
import requests
from flask import Flask
from IPy import IP
from exts import db
from modules import event

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)


def get_ip():
    # return requests.get('http://myip.ipip.net', timeout=5).text
    url = 'https://ip.cn/api/index?ip=&type=0'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    return response.json()['ip']


def writeDB(data):
    event_data_list = data[0]
    cur_d_port = data[1]
    cur_time = data[2]
    d_ip = get_ip()  # "192.168.44.136"

    # print(d_ip)
    # for e_data in event_data_list:
    #     print(e_data)

    for e_data in event_data_list:
        e = event(e_data["log_type"], e_data["username"], IP(e_data["s_ip"]).int(), e_data["s_port"], IP(d_ip).int(),
                  e_data["d_port"], e_data["time"])
        print(e_data)
        print(e)
        # ip需要特殊转换
        db.session.add(e)
    db.session.commit()


if __name__ == "__main__":
    data = updateDB("./forensics.log")
    with app.app_context():
        writeDB(data)
