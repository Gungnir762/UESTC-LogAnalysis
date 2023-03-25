from crontab import CronTab
import subprocess

if __name__ == '__main__':
    user = 'zyr'
    program_path = '/home/zyr/test/'
    with CronTab(user=user) as cron:
        # 测试用
        # job = cron.new(command=rf'echo "hello world,`date`" >> {program_path}cron.log')
        job = cron.new(command=rf'python3 {program_path}updateDB.py >> {program_path}cron.log')
        job.minute.every(1)
        print("restarting cron service")
    subprocess.call("sudo service cron restart", shell=True)
    print('cron.write() was just executed')
