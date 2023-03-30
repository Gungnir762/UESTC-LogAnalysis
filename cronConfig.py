from crontab import CronTab
import subprocess
import yaml
import argparse
import os


def read_config(path):
    with open(path, 'r', encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test for argparse')
    parser.add_argument('--program_path', '-p', help='program_path 程序所在路径 必要参数')
    parser.add_argument('--log_path', '-l', help='log_path，非必要参数，但是有默认值',
                        default="/home/zyr/test/UESTC-LogAnalysis/forensics.log")

    program_path = parser.parse_args().program_path
    log_path = parser.parse_args().log_path
    # print(program_path)
    # print(log_path)

    path = os.path.abspath(os.path.join(program_path, r'./config/cronConfig.yaml'))
    config = read_config(path)
    user = config['user']
    cron_interval = config['cron_interval']

    # print(config)
    # print(type(config))

    with CronTab(user=user) as cron:
        # 测试用
        # job = cron.new(command=rf'echo "hello world,`date`" >> {program_path}cron.log')
        job = cron.new(
            command=rf'python3 {program_path}/updateDB.py -p {program_path} -l {log_path} >> '
                    rf'{program_path}/cron.log 2>&1 </dev/null &')
        job.minute.every(cron_interval)
        print("restarting cron service")
    subprocess.call("sudo service cron restart", shell=True)
    print('cron.write() was just executed')

# python cronConfig.py -p /home/zyr/test/UESTC-LogAnalysis
