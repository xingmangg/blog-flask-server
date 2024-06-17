from datetime import timedelta

from flask import (Flask, jsonify, request)
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, create_refresh_token, \
    get_jwt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

SUCCESS_CODE = 0  # 成功
ERROR_CODE = -1  # 错误
LOGIN_USER_ERROR_CODE = -2  # 用户不存在
LOGIN_PASSWORD_ERROR_CODE = -3  # 密码错误
LOGIN_TOKEN_REF_CODE = -5  # 密码错误

TOKEN_TIME = 1.
REFTER_TOKEN_REF_CODE = 2

app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = "hykesou"
uri = 'mysql+pymysql://root:123456@127.0.0.1:3306/blog'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)
jwt_Man = JWTManager(app)


class User(db.Model):
    __tablename__ = 'blog_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    mailbox = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(100), nullable=False)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    with app.app_context():
        try:
            users = User.query.filter(User.username == username).first()
            if password == users.password:
                extra_claims = {"level": users.level}
                access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=TOKEN_TIME),additional_claims=extra_claims)
                refresh_token = create_refresh_token(identity=username,expires_delta=timedelta(minutes=REFTER_TOKEN_REF_CODE),additional_claims=extra_claims)
                return {"code": SUCCESS_CODE, "msg": "登录成功",
                        "data": {"token": access_token,
                                 "refresh_token": refresh_token,
                                 }  
                        }
            else:
                return {"code": LOGIN_PASSWORD_ERROR_CODE, "msg": "密码错误", "data": {}}
        except Exception as e:
            return {"code": LOGIN_USER_ERROR_CODE, "msg": "error", "data": {}}


invalid_tokens = set()


@app.route('/logout', methods=['get'])  #登出
@jwt_required()
def logout():
    jwt_token = get_jwt()["jti"]
    invalid_tokens.add(jwt_token)
    return {"code": SUCCESS_CODE, "msg": "ok", "data": {}}


@app.route("/regis", methods=["POST"])  #注册
def regis():
    data = request.get_json()
    username = data['username']
    password = data['password']
    mailbox = data['mailbox']
    level = '3'

    newUser = User()
    newUser.username = username
    newUser.password = password
    newUser.mailbox = mailbox
    newUser.level = level
    db.session.add(newUser)
    db.session.commit()
    extra_claims = {"level":level}
    access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=TOKEN_TIME),
                                       additional_claims=extra_claims)
    refresh_token = create_refresh_token(identity=username, expires_delta=timedelta(minutes=REFTER_TOKEN_REF_CODE),
                                         additional_claims=extra_claims)


    return {"code": SUCCESS_CODE, "msg": "注册成功",
            "data": {"token": access_token,
                     "refresh_token": refresh_token,
                    }
            }


@app.route("/protected")
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    print(current_user)
    return jsonify(logged_in_as=current_user), 200


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    new_token = create_access_token(identity=identity, expires_delta=timedelta(minutes=TOKEN_TIME))
    new_refresh_token = create_refresh_token(identity=identity, expires_delta=timedelta(minutes=REFTER_TOKEN_REF_CODE))
    return {
        "code": SUCCESS_CODE,
        "msg": "刷新成功",
        "data": {
            "new_token": new_token,
            "new_refresh_token": new_refresh_token
        }
    }


if __name__ == "__main__":
    app.run(debug=True)
