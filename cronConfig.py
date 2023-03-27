from crontab import CronTab
import subprocess
import yaml


def read_config(path):
    with open(path, 'r', encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


if __name__ == '__main__':
    config = read_config(r'home/kali/test/config/cronConfig.yaml')
    user = config['user']
    program_path = config['program_path']
    cron_interval = config['cron_interval']
    # print(config)
    # print(type(config))

    with CronTab(user=user) as cron:
        # 测试用
        # job = cron.new(command=rf'echo "hello world,`date`" >> {program_path}cron.log')
        job = cron.new(command=rf'python3 {program_path}updateDB.py >> {program_path}cron.log')
        job.minute.every(cron_interval)
        print("restarting cron service")
    subprocess.call("sudo service cron restart", shell=True)
    print('cron.write() was just executed')
