from flask import Flask, redirect, url_for, render_template
import config
app = Flask(__name__)

# 导入配置文件
app.config.from_object(config)


@app.route('/<is_login>/')
def index(is_login):
    if is_login == '1':
        # render_template喧染页面
        return render_template('index2.html', user='张三', age=18)
    else:
        return redirect(url_for('login'))


@app.route('/login/')
def login():
    return '这是登录页面'


@app.route('/question/<id>/')
def question(id):
    class Person(object):
        name = '张全'
        age = 21
    p = Person()
    if id == 1 or id == '1':
        context = {
            'uesr_name': '张全亮',
            'age': '22',
            'sex': '男',
            'person': p,
            'web': {
                'baidu': 'http://www.baidu.com',
                'goole': 'http://wwwbaidu.com'
            }
        }
        return render_template('index.html', **context)
    else:
        # redirect重定向 ,url_for获取到登陆页面地址
        return redirect(url_for('login'))


# Url传参, 以<>形式
@app.route('/test/<id>')
def test(id):
    return '这是第{}个test。'.format(id)


if __name__ == '__main__':
    app.run()
