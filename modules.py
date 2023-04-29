from exts import db


# 以下为数据库模型
class event(db.Model):
    __tablename__ = "event"
    # 字段名及类型
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(24), nullable=False)
    username = db.Column(db.String(24), nullable=False)
    s_ip = db.Column(db.Integer, nullable=False)
    s_port = db.Column(db.Integer, nullable=False)
    d_ip = db.Column(db.Integer, nullable=False)
    d_port = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    def __init__(self, type, username, s_ip, s_port, d_ip, d_port, time):
        self.type = type
        self.username = username
        self.s_ip = s_ip
        self.s_port = s_port
        self.d_ip = d_ip
        self.d_port = d_port
        self.time = time

    # 返回函数
    def __repr__(self):
        return '<Event %r>' % self.time
