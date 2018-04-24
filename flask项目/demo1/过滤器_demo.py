from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    # img_path = 'https://pic.qiushibaike.com/system/avtnew/873/8737794/medium/20180417163505.JPEG'
    commounts = [
        {
            'user': '张三',
            'context': 'xxx'
        },
        {
            'user': '李四',
            'context': 'xxx'
        },
        {
            'user': '王二',
            'context': 'xxx'
        }
    ]
    return render_template('index5.html', commounts=commounts)


if __name__ == '__main__':
    app.run(debug=True)
