# coding:utf8
import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:254613@localhost:3306/58house"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

field = SQLAlchemy(app)


# 用户表
class House(field.Model):
    __tablename__ = '58house'

    id = field.Column(field.Integer, primary_key=True)  # 编号
    name = field.Column(field.String(20), nullable=False)  # 名称
    number= field.Column(field.String(100), nullable=False)  # 号码
    company= field.Column(field.String(100), nullable=False)  # 公司
    address= field.Column(field.String(100), nullable=False)  # 地址
    created_time = field.Column(field.DateTime, nullable=False)  # 创建时间
    category = field.Column(field.Integer, nullable=False)  # 分类
    shop_address= field.Column(field.String(100), nullable=False)  # 详细地址


    def __repr__(self):
        return "<User %r>" % self.name




if __name__ == '__main__':
    field.create_all()
