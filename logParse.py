import re
from datetime import datetime, timedelta


class Message(object):
    def __init__(self, time, log_type, username, s_ip, s_port, session_id):
        self.time = time
        self.log_type = log_type
        self.username = username
        self.s_ip = s_ip
        self.s_port = s_port
        self.session_id = session_id
        return

    def set_d_port(self, d_port):
        self.d_port = d_port
        return

    def get_dict(self):
        return {"time": self.time, "log_type": self.log_type, "username": self.username, "s_ip": self.s_ip,
                "s_port": self.s_port, "d_port": self.d_port}


# 将日志中以字符串表示的时间转换为datetime类型
def log2time(time_str):
    time_match = re.match(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}).(\d{3,8})([-+])(\d{2}):(\d{2})",
                          time_str)
    time_datetime = datetime(int(time_match.group(1)), int(time_match.group(2)), int(time_match.group(3)),
                             int(time_match.group(4)), int(time_match.group(5)), int(time_match.group(6)),
                             int(time_match.group(7)))
    time_offset = timedelta(0, 0, 0, 0, int(time_match.group(10)),
                            int(time_match.group(9)) * (-1 if time_match.group(8) == '-' else 1))
    time_offset_cn = timedelta(0, 0, 0, 0, 0, 8)
    time_datetime -= time_offset
    time_datetime += time_offset_cn
    return time_datetime


# 调用的主函数
# 参数1：文件路径，str类
# 参数2：传入上一次该函数返回的服务器端口号，str类，第一次调用时缺省
# 参数3：传入上一次该函数返回的最后更新时间，datetime类，第一次调用时缺省
#
# 返回值：
# [dict_list：由各项的dict组成的列表,
#  cur_d_port：当前会话服务器端端口,
#  cur_time：更新日志的时间]
#
# dict_list每一项的组成为：
# {"time"：时间,
#  "log_type"：日志类型，有四类，"correct.password"，"wrong.password"，"login"，"logout",
#  "username"：用户名,
#  "s_ip"：用户ip,
#  "s_port"：用户端口,
#  "d_port"：服务端端口}
# 时间是datetime类型，其它是str类型
def get_message_list(file_path, last_d_port='', last_time=datetime(2000, 1, 1)):
    cur_time = datetime.now()
    cur_d_port = last_d_port
    message_list = []
    dict_list = []
    with open(file_path) as file:
        lines = file.readlines()
        # for line in lines:
        #     print(line)
        for id, line in enumerate(lines):
            strlist = line.split()

            # 获得日志时间
            time = log2time(strlist[0])
            if time < last_time:
                continue
            if time > cur_time:
                break

            # 检查日志是否为ssh相关
            sshd_check = re.match(r"sshd\[(\d*)]", strlist[2])
            if not sshd_check:
                continue

            # 密码正确
            if strlist[3] == "Accepted":
                name = strlist[6]
                s_ip = strlist[8]
                s_port = strlist[10]
                message_list.append(
                    Message(time, "correct.password", name, s_ip, s_port, int(sshd_check.group(1))))

            # 密码错误
            elif strlist[3] == "Failed":
                name = strlist[6]
                s_ip = strlist[8]
                s_port = strlist[10]
                message_list.append(Message(time, "wrong.password", name, s_ip, s_port, int(sshd_check.group(1))))

            # 会话状态
            elif strlist[3] == "pam_unix(sshd:session):":

                # 开启会话
                if strlist[5] == "opened":
                    name = strlist[8].split('(')[0]
                    session_id = int(sshd_check.group(1))
                    for message in message_list:
                        if message.session_id == session_id:
                            message_list.append(
                                Message(time, "login", name, message.s_ip, message.s_port, session_id))
                            break

                # 关闭会话
                elif strlist[5] == "closed":
                    name = strlist[8]
                    session_id = int(sshd_check.group(1))
                    for message in message_list:
                        if message.session_id == session_id:
                            message_list.append(
                                Message(time, "logout", name, message.s_ip, message.s_port, session_id))
                            break

            # 服务器端口变化
            elif strlist[3] == "Server":
                if re.match(r"\d*\.", strlist[8]):
                    d_port = strlist[8].split('.')[0]
                    message_list.append(Message(time, "set.port", '', '', '', ''))
                    message_list[-1].set_d_port(d_port)

    for message in message_list:
        if message.log_type == "set.port":
            cur_d_port = message.d_port
        else:
            message.d_port = cur_d_port
            dict_list.append(message.get_dict())
    return [dict_list, cur_d_port, cur_time]


if __name__ == "__main__":
    data = get_message_list("./forensics.log")
    print(rf"cur_d_port: {data[1]}")
    print(rf"cur_time: {data[2]}")
    for d in data[0]:
        print(d)
