from flask import Flask, render_template

app = Flask(__name__)


# @app.route('/')
# def index():
#     user = {
#         'user_name': '张三',
#         'age': '19'
#     }
#     websize = ['www.baidu.com', 'www.google.com']
#     return render_template('index3.html', user=user, websize=websize)
@app.route('/')
def index():
    books = [
        {
            'name': '西游记',
            'author': '吴承恩',
            'price': '109'
        },
        {
            'name': '红楼梦',
            'author': '曹雪芹',
            'price': '200'
        },
        {
            'name': '三国演义',
            'author': '罗贯中',
            'price': '120'
        },
        {
            'name': '水浒传',
            'author': '施耐庵',
            'price': '130'
        },
    ]
    return render_template('index4.html', books=books)


if __name__ == '__main__':
    app.run(debug=True)
