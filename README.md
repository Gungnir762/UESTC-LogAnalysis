采用flask框架，使用mysql作为数据库，实现了一个简单的unix日志分析系统。
# 使用说明
## 1.安装依赖
```pip install -r requirements.txt```
## 2.配置数据库连接
在```config.py```中配置数据库连接信息
## 3.配置计划任务
在```cronConfig.py```中配置```user```和```program_path```的值以用于定期更新数据库，更新日志写在```program_path```下的```cron.log```中
## 4.配置日志文件路径
```updateDB.py```中的```log_path```变量用于指定日志文件的路径
## 5.运行
```python cronConfig.py```日志数据库会每分钟更新一次。
若要手动更新数据库，运行```python updateDB.py```
## 6.启动web服务
```python app.py```
## 7.访问
浏览器访问```http://localhost:5000/```
选择功能即可