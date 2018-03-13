# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return '12312313'


if __name__ == '__main__':
    app.run(debug=True)  # debug=True的作用是每次修改代码之后，不需要每次都重启服务器