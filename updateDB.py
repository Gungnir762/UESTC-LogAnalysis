import argparse
import os
import socket
from datetime import datetime
import yaml
from flask import Flask
from IPy import IP
from exts import db
from modules import event
from logParse import get_message_list
from cronConfig import read_config

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)


# def get_global_ip():#获取公网ip
#     # return requests.get('http://myip.ipip.net', timeout=5).text
#     url = 'https://ip.cn/api/index?ip=&type=0'
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
#                       '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
#     response = requests.get(url, headers=headers)
#     return response.json()['ip']

def get_ip():  # 获取局域网ip，只能在unix系统下得到正确结果
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    return ip


def insert_data(data):
    event_data_list = data[0]
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
    parser = argparse.ArgumentParser(description='updateDB')
    parser.add_argument('--log_path', '-l', help='log_path，非必要参数，但是有默认值',
                        default="/home/zyr/test/UESTC-LogAnalysis/forensics.log")
    parser.add_argument('--program_path', '-p', help='program_path 程序所在路径 必要参数')

    log_path = parser.parse_args().log_path
    program_path = parser.parse_args().program_path

    path = os.path.abspath(os.path.join(program_path, r'./config/updateDBConfig.yaml'))
    # 读取配置文件
    config = read_config(path)
    last_update_time = datetime.strptime(config["last_update_time"], "%Y-%m-%d %H:%M:%S")
    last_d_port = config["last_d_port"]

    # 写入数据库
    data = get_message_list(log_path, last_d_port, last_update_time)
    with app.app_context():
        try:
            insert_data(data)
        except Exception as e:
            print(f"insert data error,{datetime.now()}")
            print(e)
    print(f"insert data successfully,{datetime.now()}")

    # 更新配置文件
    cur_d_port = data[1]
    cur_time = data[2].strftime("%Y-%m-%d %H:%M:%S")
    yaml_update = {"last_update_time": cur_time, "last_d_port": cur_d_port}
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_update, f, allow_unicode=False)

# python updateDB.py -p /home/zyr/test/UESTC-LogAnalysis
