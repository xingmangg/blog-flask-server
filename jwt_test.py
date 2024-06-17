from datetime import timedelta
from flask import (Flask, request, jsonify)
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, create_refresh_token, get_jwt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

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
    avatar_img = db.Column(db.String(100), nullable=False)


@app.route("/login", methods=["POST"],endpoint='blog_user')   #登录
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    with app.app_context():
        try:
            users = User.query.filter(User.username == username).first()
            if password == users.password:
                access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=TOKEN_TIME))
                refresh_token = create_refresh_token(identity=username,expires_delta=timedelta(minutes=REFTER_TOKEN_REF_CODE))
                return {"code": SUCCESS_CODE, "msg": "登录成功",
                        "data": {"token": access_token,
                                 "refresh_token": refresh_token,
                                 }
                        }
            else:
                return {"code": LOGIN_PASSWORD_ERROR_CODE, "msg": "密码错误", "data": {}}
        except Exception as e:
            return {"code": LOGIN_USER_ERROR_CODE, "msg": "error", "data": {}}



@app.route("/user_info", methods=["POST"],endpoint='user_info')  #获取用户信息
def obt_img():
    data = request.get_json()
    username = data['User_name']
    users = User.query.filter_by(username="{}".format(username))
    for user in users:
        return {"img_url":user.avatar_img,"mailbox":user.mailbox,"level":user.level,"username":user.username}


invalid_tokens = set()
@app.route('/logout', methods=['GET'],endpoint='blog_user_dc')  #登出
@jwt_required()
def logout():
    jwt_token = get_jwt()["jti"]
    invalid_tokens.add(jwt_token)
    return {"code": SUCCESS_CODE, "msg": "ok", "data": {}}


@app.route("/regis", methods=["POST"],endpoint='blog_user_reg')  #注册
def regis():
    data = request.get_json()
    username = data['username']
    password = data['password']
    mailbox = data['mailbox']
    level = '3'
    avatar_img = '/src/assets/img/default_user.jpg'
    newUser = User()
    newUser.username = username
    newUser.password = password
    newUser.mailbox = mailbox
    newUser.level = level
    newUser.avatar_img = avatar_img
    db.session.add(newUser)
    db.session.commit()
    access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=TOKEN_TIME))
    refresh_token = create_refresh_token(identity=username, expires_delta=timedelta(minutes=REFTER_TOKEN_REF_CODE))
    return {"code": SUCCESS_CODE, "msg": "注册成功",
            "data": {"token": access_token,
                     "refresh_token": refresh_token,
                    }
            }



@app.route("/refresh", methods=["POST"],endpoint='blog_user_ref')  #刷新token
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

@app.route("/user_renew", methods=["POST"],endpoint='user_renew')  #修改用户数据
def obt_img():
    data = request.get_json()
    try:
        user = User.query.filter_by(username=data['old_username']).one()
        if user.password == data['password']:
                user.username = data['username']

                user.mailbox = data['mailbox']
                user.password = data['newpassword']
                db.session.commit()
                extra_claims = {"level": user.level}
                new_token = create_access_token(identity=user.username, expires_delta=timedelta(minutes=TOKEN_TIME),additional_claims=extra_claims)
                new_refresh_token = create_refresh_token(identity=user.username,expires_delta=timedelta(minutes=REFTER_TOKEN_REF_CODE),additional_claims=extra_claims)
                return {"code": SUCCESS_CODE, "msg": "修改成功",
                        "token": new_token,
                        "refresh_token": new_refresh_token
                }

        else:
            return '密码错误'
    except IntegrityError:
        db.session.rollback()  # 回滚事务，确保数据库状态不变
        return {"msg":'账号或邮箱重复'}

@app.route("/user_newimg", methods=["POST"],endpoint='user_newimg')  #修改用户数据
def obt_img():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    user.avatar_img = '/src/assets/img/'+data['new_img']
    db.session.commit()
    return {"code": SUCCESS_CODE, "msg": "修改成功"}




#---------------------------------------------------------------------------------------------------------------------------

class Gg(db.Model):
    __tablename__ = 'blog_gg'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    the_me = db.Column(db.String(100), nullable=False)
    txt_html = db.Column(db.Text, nullable=False)
    txt = db.Column(db.Text, nullable=False)
    avatar_img = db.Column(db.Text, nullable=False)

@app.route("/gg_pubart", methods=["POST"],endpoint='blog_gg')
def regis():
    data = request.get_json()
    username = data['username']
    the_me = data['the_me']
    txt_html = data['txt_html']
    txt = data['txt']
    avatar_img =  data['avatar_img']

    newGg = Gg()
    newGg.username = username
    newGg.the_me = the_me
    newGg.txt_html = txt_html
    newGg.txt = txt
    newGg.avatar_img = avatar_img
    db.session.add(newGg)
    db.session.commit()
    return {"code": SUCCESS_CODE, "msg": "发表成功"}

@app.route('/gg_articles', methods=['GET'],endpoint='gg_articles')
def get_articles():
    articles = Gg.query.all()
    articles_list = []
    for article in articles:
        article_dict = {
            'id': article.id,
            'username': article.username,
            'the_me': article.the_me,
            'txt': article.txt,
            'avatar_img':article.avatar_img,

        }
        articles_list.append(article_dict)
    return jsonify(articles_list)

@app.route('/gg_artde', methods=['POST'],endpoint='gg_artde')
def get_articles():
    data = request.get_json()
    id = data['ID']
    articles = Gg.query.filter_by(id="{}".format(id))
    articles_list = []
    for article in articles:
        article_dict = {
            'id':article.id,
            'username': article.username,
            'the_me': article.the_me,
            'txt': article.txt,
            'txt_html':article.txt_html,
            'avatar_img':article.avatar_img,
        }
        articles_list.append(article_dict)
    return jsonify(articles_list)

@app.route('/gg_len', methods=['GET'],endpoint='gg_len')
def get_articles():
    articles_count = db.session.query(Gg).count()
    return str(articles_count)

@app.route('/gg_delete', methods=['POST'],endpoint='gg_delete')
def get_articles():
    data = request.get_json()
    art_id = data['ID']
    article = Gg.query.filter_by(id=art_id).first()  # 或者使用 .one() 如果你确定查询结果只有一个对象
    print(article)
    if article:
        db.session.delete(article)
        db.session.commit()
        return ("文章已删除")
    else:
        return ("文章不存在")




#---------------------------------------------------------------------------------------------------------------------------


class Cg(db.Model):
    __tablename__ = 'blog_cg'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    the_me = db.Column(db.String(100), nullable=False)
    txt_html = db.Column(db.Text, nullable=False)
    txt = db.Column(db.Text, nullable=False)
    avatar_img = db.Column(db.String(100), nullable=False)
    visible = db.Column(db.String(10), nullable=False)

@app.route("/cg_pubart", methods=["POST"],endpoint='blog_cg')
def regis():
    data = request.get_json()
    print(data)
    username = data['username']
    the_me = data['the_me']
    txt_html = data['txt_html']
    txt = data['txt']
    avatar_img =  data['avatar_img']
    if data['level'] == '1':
        visible = 'true'
    else:
        visible = 'false'


    newCg = Cg()
    newCg.username = username
    newCg.the_me = the_me
    newCg.txt_html = txt_html
    newCg.txt = txt
    newCg.avatar_img = avatar_img
    newCg.visible = visible
    db.session.add(newCg)
    db.session.commit()
    return {"code": SUCCESS_CODE, "msg": "发表成功"}

@app.route('/cg_articles', methods=['GET'],endpoint='cg_articles')
def get_articles():
    articles = Cg.query.all()
    articles_list = []
    for article in articles:
        article_dict = {
            'id': article.id,
            'username': article.username,
            'the_me': article.the_me,
            'txt': article.txt,
            'avatar_img':article.avatar_img,
            'visible':article.visible,

        }
        articles_list.append(article_dict)
    return jsonify(articles_list)

@app.route('/cg_artde', methods=['POST'],endpoint='cg_artde')
def get_articles():
    data = request.get_json()
    id = data['ID']
    articles = Cg.query.filter_by(id="{}".format(id))
    articles_list = []
    for article in articles:
        article_dict = {
            'id':article.id,
            'username': article.username,
            'the_me': article.the_me,
            'txt': article.txt,
            'txt_html':article.txt_html,
            'avatar_img':article.avatar_img,
        }
        articles_list.append(article_dict)
    return jsonify(articles_list)

@app.route('/cg_len', methods=['GET'],endpoint='cg_len')
def get_articles():
    articles_count = db.session.query(Cg).filter(Cg.visible == 'true').count()
    una_articles_count = db.session.query(Cg).filter(Cg.visible == 'false').count()
    return {'art':articles_count,'una':una_articles_count}

@app.route('/cg_delete', methods=['POST'],endpoint='cg_delete')
def get_articles():
    data = request.get_json()
    art_id = data['ID']
    article = Cg.query.filter_by(id=art_id).first()
    if article:
        db.session.delete(article)
        db.session.commit()
        return ("文章已删除")
    else:
        return ("文章不存在")

@app.route("/cg_artpass", methods=["POST"],endpoint='cg_artpass')  #修改用户数据
def obt_img():
    data = request.get_json()
    art_id = data['ID']
    article = Cg.query.filter_by(id=art_id).first()
    article.visible = 'true'
    db.session.commit()
    return {"code": SUCCESS_CODE, "msg": "修改成功"}


#---------------------------------------------------------------------------------------------------------------------------


class Zy(db.Model):
    __tablename__ = 'blog_zy'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    the_me = db.Column(db.String(100), nullable=False)
    txt_html = db.Column(db.Text, nullable=False)
    txt = db.Column(db.Text, nullable=False)
    avatar_img = db.Column(db.String(100), nullable=False)
    visible = db.Column(db.String(10), nullable=False)

@app.route("/zy_pubart", methods=["POST"],endpoint='blog_zy')
def regis():
    data = request.get_json()
    print(data)
    username = data['username']
    the_me = data['the_me']
    txt_html = data['txt_html']
    txt = data['txt']
    avatar_img =  data['avatar_img']
    if data['level'] == '1':
        visible = 'true'
    else:
        visible = 'false'


    newZy = Zy()
    newZy.username = username
    newZy.the_me = the_me
    newZy.txt_html = txt_html
    newZy.txt = txt
    newZy.avatar_img = avatar_img
    newZy.visible = visible
    db.session.add(newZy)
    db.session.commit()
    return {"code": SUCCESS_CODE, "msg": "发表成功"}

@app.route('/zy_artde', methods=['POST'],endpoint='zy_artde')
def get_articles():
    data = request.get_json()
    id = data['ID']
    articles = Zy.query.filter_by(id="{}".format(id))
    articles_list = []
    for article in articles:
        article_dict = {
            'id':article.id,
            'username': article.username,
            'the_me': article.the_me,
            'txt': article.txt,
            'txt_html':article.txt_html,
            'avatar_img':article.avatar_img,
        }
        articles_list.append(article_dict)
    return jsonify(articles_list)

@app.route('/zy_len', methods=['GET'],endpoint='zy_len')
def get_articles():
    articles_count = db.session.query(Zy).filter(Zy.visible == 'true').count()
    una_articles_count = db.session.query(Zy).filter(Zy.visible == 'false').count()
    return {'art':articles_count,'una':una_articles_count}


@app.route('/zy_articles', methods=['GET'],endpoint='zy_articles')
def get_articles():
    articles = Zy.query.all()
    articles_list = []
    for article in articles:
        article_dict = {
            'id': article.id,
            'username': article.username,
            'the_me': article.the_me,
            'txt': article.txt,
            'avatar_img':article.avatar_img,
            'visible':article.visible,

        }
        articles_list.append(article_dict)
    return jsonify(articles_list)

@app.route('/zy_delete', methods=['POST'],endpoint='zy_delete')
def get_articles():
    data = request.get_json()
    art_id = data['ID']
    article = Zy.query.filter_by(id=art_id).first()
    if article:
        db.session.delete(article)
        db.session.commit()
        return ("文章已删除")
    else:
        return ("文章不存在")

@app.route("/zy_artpass", methods=["POST"],endpoint='zy_artpass')  #修改用户数据
def obt_img():
    data = request.get_json()
    art_id = data['ID']
    article = Zy.query.filter_by(id=art_id).first()
    article.visible = 'true'
    db.session.commit()
    return {"code": SUCCESS_CODE, "msg": "修改成功"}

#---------------------------------------------------------------------------------------------------------------------------


class Jh(db.Model):
    __tablename__ = 'blog_jh'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    the_me = db.Column(db.String(100), nullable=False)
    txt_html = db.Column(db.Text, nullable=False)
    txt = db.Column(db.Text, nullable=False)
    avatar_img = db.Column(db.String(100), nullable=False)
    visible = db.Column(db.String(10), nullable=False)


@app.route("/jh_pubart", methods=["POST"], endpoint='blog_jh')
def regis():
    data = request.get_json()
    username = data['username']
    the_me = data['the_me']
    txt_html = data['txt_html']
    txt = data['txt']
    avatar_img = data['avatar_img']
    if data['level'] == '1':
        visible = 'true'
    else:
        visible = 'false'

    newJh = Jh()
    newJh.username = username
    newJh.the_me = the_me
    newJh.txt_html = txt_html
    newJh.txt = txt
    newJh.avatar_img = avatar_img
    newJh.visible = visible
    db.session.add(newJh)
    db.session.commit()
    return {"code": SUCCESS_CODE, "msg": "发表成功"}

@app.route('/jh_len', methods=['GET'],endpoint='jh_len')
def get_articles():
    articles_count = db.session.query(Jh).filter(Jh.visible == 'true').count()
    una_articles_count = db.session.query(Jh).filter(Jh.visible == 'false').count()
    return {'art':articles_count,'una':una_articles_count}

@app.route('/jh_articles', methods=['GET'],endpoint='jh_articles')
def get_articles():
    articles = Jh.query.all()
    articles_list = []
    for article in articles:
        article_dict = {
            'id': article.id,
            'username': article.username,
            'the_me': article.the_me,
            'txt': article.txt,
            'avatar_img':article.avatar_img,
            'visible':article.visible,

        }
        articles_list.append(article_dict)
    return jsonify(articles_list)

@app.route('/jh_delete', methods=['POST'],endpoint='jh_delete')
def get_articles():
    data = request.get_json()
    art_id = data['ID']
    article = Jh.query.filter_by(id=art_id).first()
    if article:
        db.session.delete(article)
        db.session.commit()
        return ("文章已删除")
    else:
        return ("文章不存在")

@app.route('/jh_artde', methods=['POST'],endpoint='jh_artde')
def get_articles():
    data = request.get_json()
    id = data['ID']
    articles = Jh.query.filter_by(id="{}".format(id))
    articles_list = []
    for article in articles:
        article_dict = {
            'id':article.id,
            'username': article.username,
            'the_me': article.the_me,
            'txt': article.txt,
            'txt_html':article.txt_html,
            'avatar_img':article.avatar_img,
        }
        articles_list.append(article_dict)
    return jsonify(articles_list)

@app.route("/jh_artpass", methods=["POST"],endpoint='jh_artpass')  #修改用户数据
def obt_img():
    data = request.get_json()
    art_id = data['ID']
    article = Jh.query.filter_by(id=art_id).first()
    article.visible = 'true'
    db.session.commit()
    return {"code": SUCCESS_CODE, "msg": "修改成功"}

if __name__ == "__main__":
    app.run(debug=True)
