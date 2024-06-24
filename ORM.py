from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null

app = Flask(__name__)
uri = 'mysql+pymysql://root:123456@127.0.0.1:3306/blog'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)

class Cg(db.Model):
    __tablename__ = 'blog_cg'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plate = db.Column(db.String(10), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    the_me = db.Column(db.String(100), nullable=False)
    txt_html = db.Column(db.Text, nullable=False)
    txt = db.Column(db.Text, nullable=False)
    avatar_img = db.Column(db.String(100), nullable=False)
    visible = db.Column(db.String(10), nullable=False)

class Gg(db.Model):
    __tablename__ = 'blog_gg'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plate = db.Column(db.String(10), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    the_me = db.Column(db.String(100), nullable=False)
    txt_html = db.Column(db.Text, nullable=False)
    txt = db.Column(db.Text, nullable=False)
    avatar_img = db.Column(db.Text, nullable=False)

class Zy(db.Model):
    __tablename__ = 'blog_zy'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plate = db.Column(db.String(10), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    the_me = db.Column(db.String(100), nullable=False)
    txt_html = db.Column(db.Text, nullable=False)
    txt = db.Column(db.Text, nullable=False)
    avatar_img = db.Column(db.String(100), nullable=False)
    visible = db.Column(db.String(10), nullable=False)

class Jh(db.Model):
    __tablename__ = 'blog_jh'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plate = db.Column(db.String(10), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    the_me = db.Column(db.String(100), nullable=False)
    txt_html = db.Column(db.Text, nullable=False)
    txt = db.Column(db.Text, nullable=False)
    avatar_img = db.Column(db.String(100), nullable=False)
    visible = db.Column(db.String(10), nullable=False)
def get_posts_by_username(username):
    with app.app_context():
        query_cg = db.session.query(Cg.plate.label('plate'),Cg.id.label('id'),Cg.username.label('username'),
                                    Cg.the_me.label('the_me'),Cg.txt.label('txt'),Cg.avatar_img.label('avatar_img'),
                                    Cg.visible.label('visible')).filter(Cg.username.ilike(f'%{username}%'))

        query_gg = db.session.query(Gg.plate.label('plate'),Gg.id.label('id'),Gg.username.label('username'),
                                    Gg.the_me.label('the_me'),Gg.txt.label('txt'),Gg.avatar_img.label('avatar_img'),
                                    null().label('visible')).filter(Gg.username.ilike(f'%{username}%'))

        query_jh = db.session.query(Jh.plate.label('plate'),Jh.id.label('id'),Jh.username.label('username'),
                                    Jh.the_me.label('the_me'),Jh.txt.label('txt'),Jh.avatar_img.label('avatar_img'),
                                    Jh.visible.label('visible')).filter(Jh.username.ilike(f'%{username}%'))


        query_zy = db.session.query(Zy.plate.label('plate'),Zy.id.label('id'),Zy.username.label('username'),
                                    Zy.the_me.label('the_me'),Zy.txt.label('txt'),Zy.avatar_img.label('avatar_img'),
                                    Zy.visible.label('visible')).filter(Zy.username.ilike(f'%{username}%'))


        combined_query = query_cg.union(query_gg, query_jh, query_zy)

        # 将结果转换为期望的格式
        posts = [{"plate": post.plate, "id": post.id, "username": post.username, "the_me": post.the_me,
                  "txt": post.txt,"avatar_img": post.avatar_img,"visible": post.visible,}
                 for post in combined_query]

        return posts






if __name__ == '__main__':
    username_to_search = 'adm'
    posts = get_posts_by_username(username_to_search)
    print(posts)


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

    # print("======新增数据：")
    # newUser = User()
    # newUser.username = "xiaoli3"
    # newUser.password = "1112"
    # newUser.mailbox = "1234456@qq.com"
    # db.session.add(newUser)
    # db.session.commit()


    # articles_count = db.session.query(Cg).filter(Cg.visible == 'true').count()
    # print(articles_count)
