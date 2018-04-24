from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

class User(db.Model):
    __table_name__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Text, nullable=False)

db.create_all()
@app.route('/')
def index():
    """增加"""
    # user1 = User(user_name='张三', age=20)
    # db.session.add(user1)
    # db.session.commit()

    """查询"""
    # result = User.query.filter(User.age == 20).all()    # 查的一个first  User.age == 20查询条件，可不加
    # for user in result:
    #     print(user.user_name)
    #     print(user.age)

    """修改"""
    # result = User.query.filter(User.age == 20).all()  # 查的一个first  User.age == 20查询条件，可不加
    # for user in result:
    #     user.user_name = '李四'
    #     user.age = '18'
    # db.session.commit()

    """删除"""
    result = User.query.filter(User.age == 18).first()
    db.session.delete(result)
    db.session.commit()
    return '主页面'


if __name__ == '__main__':
    app.run(debug=True)
