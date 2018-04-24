from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

# 用户模型，即表
class Users(db.Model):
    __table_name__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(255), nullable=False)

# 文章模型，即表
class Article(db.Model):
    __table_name__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    context = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))   # 外键引用，映射users表中的id
    author = db.relationship('Users', backref=db.backref('articles'))  # Users是模型名
db.create_all()

@app.route('/')
def index():
    """外键约束，插入数据"""
    # article1 = Article(title='标题', context='文章', author_id='1')
    # db.session.add(article1)
    # db.session.commit()

    """需要找到title为'标题'的用户"""
    # article1 = Article.query.filter(Article.title == '标题').first()
    # author_id = article1.author_id
    # result = Users.query.filter(Users.id==author_id).first()
    # print(result.user_name)

    # article1 = Article(title='1123', context='2131')
    # article1.author = Users.query.filter(Users.id == 1).first()
    # db.session.add(article1)
    # db.session.commit()

    """需要找到title为'aaa'的用户"""
    # article = Article.query.filter(Article.title == 'aaa').first()
    # a = article.author.user_name
    # print(a)

    """需要找到zs这个用户所有的文章"""
    user = Users.query.filter(Users.id == '1').first()
    result = user.articles
    for res in result:
        print('-' * 10)
        print(res.title)
    return '这是主页面'


if __name__ == '__main__':
    app.run(debug=True)