import sqlalchemy
from flask import Flask, render_template, request
from exts import db

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object('config')

db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/by_date/')
def by_date():
    return render_template('by_date.html')


@app.route('/by_login_event/')
def by_login_event():
    return render_template('by_login_event.html')


@app.route('/by_user/')
def by_user():
    return render_template('by_user.html')


@app.route('/by_date_query/', methods=['POST'])
def by_date_query():
    date_begin = request.form["date_begin"]
    time_begin = request.form["time_begin"]
    date_end = request.form["date_end"]
    time_end = request.form["time_end"]
    # 提交的日期数据为月-日-年的写法
    sql_text = f"select event_id,type,username,inet_ntoa(s_ip),s_port,inet_ntoa(d_ip),d_port,time " \
               f"from event where time between " \
               f"STR_TO_DATE('{date_begin} {time_begin}','%m-%d-%Y %H:%i:%s') and " \
               f"STR_TO_DATE('{date_end} {time_end}','%m-%d-%Y %H:%i:%s')"
    print(sql_text)

    with db.engine.connect() as conn:
        results = conn.execute(sqlalchemy.text(sql_text))
        return render_template('by_date.html', results=results)


@app.route('/by_login_event_query/', methods=['POST'])
def by_login_event_query():
    # 需要修改
    event_type = request.form["event_type"]
    sql_text = rf"select event_id,type,username,inet_ntoa(s_ip),s_port,inet_ntoa(d_ip),d_port,time " \
               f"from event where type='{event_type}'"
    print(sql_text)
    with db.engine.connect() as conn:
        results = conn.execute(sqlalchemy.text(sql_text))
        return render_template('by_login_event.html', results=results)


@app.route('/by_user_query/', methods=['POST'])
def by_user_query():
    username = request.form["username"]
    sql_text = rf"select event_id,type,username,inet_ntoa(s_ip),s_port,inet_ntoa(d_ip),d_port,time " \
               f"from event where username='{username}'"
    print(sql_text)
    with db.engine.connect() as conn:
        results = conn.execute(sqlalchemy.text(sql_text))
        return render_template('by_user.html', results=results)


if __name__ == "__main__":
    app.run(debug=True)
