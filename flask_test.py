from flask import request, jsonify
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


# result = {
#     "code": 200,
#     "msg": "",
#     "data": {}
# }


app = Flask(__name__)
CORS(app)#解决跨域
uri = 'mysql+pymysql://root:123456@127.0.0.1:3306/blog'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'blog_user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(100),nullable=False)


@app.route('/user_pass',methods=['GET','POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    with app.app_context():
        users = User.query.filter_by(username="{}".format(username))
        if users.count() == 0:
            return {
                "code": -1,
                "msg": "error",
                "data": {}
            }
        else:
            for user in users:
                # if user == []:
                # print(user.password)
                if password == user.password:
                    return {
                        "code": 0,
                        "msg": "ok",
                        "data": {}
                    }
                else:
                    print('-2')
                    return {
                        "code": -2,
                        "msg": "error",
                        "data": {}
                    }







if __name__ == '__main__':
    app.run()