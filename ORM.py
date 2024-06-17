from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
uri = 'mysql+pymysql://root:123456@127.0.0.1:3306/blog'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'blog_user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    mailbox = db.Column(db.String(100),nullable=False)

with app.app_context():
    # print("======查询全部：")
    # users = User.query.all()
    # for user in users:
    #     print(user.id)
    #     print(user.username)
    #     print(user.password)

    # print("======按条件查询：")
    # users = User.query.filter_by(username="xiaoming")
    # for user in users:
    #     print(user.username)
    #     print(user.id)
    #     print(user.password)

    print("======新增数据：")
    newUser = User()
    newUser.username = "xiaoli3"
    newUser.password = "1112"
    newUser.mailbox = "1234456@qq.com"
    db.session.add(newUser)
    db.session.commit()

