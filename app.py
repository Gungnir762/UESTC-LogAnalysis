import sqlalchemy
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates', static_folder='static')

HOSTNAME = "localhost"
PORT = 3306
USERNAME = "zyr"
PASSWORD = "123456"
DATABASE = "forensicsdb"

app.config[
    'SQLALCHEMY_DATABASE_URI'] = rf"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

db = SQLAlchemy()
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/histories/')
def histories():
    return render_template('histories.html')
    # return "histories"


@app.route('/login_failed/')
def login_failed():
    return render_template('login_failed.html')


@app.route('/root_login/')
def root_login():
    return render_template('root_login.html')


@app.route('/histories_query/', methods=['POST', 'GET'])
def histories_query():
    date_begin = request.form["date_begin"]
    time_begin = request.form["time_begin"]
    date_end = request.form["date_end"]
    time_end = request.form["time_end"]
    sql_text = f"select event_id,type,username,inet_ntoa(s_ip),s_port,inet_ntoa(d_ip),d_port,time " \
               f"from event where time between " \
               f"STR_TO_DATE('{date_begin} {time_begin}','%m-%d-%Y %H:%i:%s') and " \
               f"STR_TO_DATE('{date_end} {time_end}','%m-%d-%Y %H:%i:%s')"
    print(sql_text)

    with db.engine.connect() as conn:
        results = conn.execute(sqlalchemy.text(sql_text))
        return render_template('histories.html', results=results)
    # with app.app_context():
    #     with db.engine.connect() as conn:
    #         rs = conn.execute(sqlalchemy.text(sql_text))
    #         print(rs)
    #         # return render_template('histories.html', data_dict=rs)


if __name__ == "__main__":
    app.run(debug=True)
