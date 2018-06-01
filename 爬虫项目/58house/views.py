# coding:utf8
import os
import datetime
from flask import Flask, render_template, redirect, flash, session, Response, url_for, request
from forms import  ArtForm,ArtEditForm
from models import House, field



app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678'
app.config['UP'] = os.path.join(os.path.dirname(__file__), "static/upload")

@app.route('/')
def index():
    return redirect('/art/list/1/')



# 发布文章
@app.route("/art/add/", methods=['GET', "POST"])
def art_add():
    form = ArtForm()
    if form.validate_on_submit():
        data = form.data
        print(data['category'],)
        if data['category'] == 1:
            category = '租房'
        if data['category'] == 2:
            category = '二手房'
        if data['category'] == 3:
            category = '商业地产'
        # 保存数据
        art = House(
            name= data['name'],
            category= category,
            number= data['number'],
            company= data['company'],
            address= data['address'],
            shop_address= data['shop_address'],
            created_time=datetime.datetime.now()
        )
        field.session.add(art)
        field.session.commit()
        flash(u"添加成功", 'ok')
    return render_template('art_add.html', title=u'添加', form=form)


# 编辑文章
@app.route("/art/edit/<int:id>/", methods=['GET', "POST"])
def art_edit(id):
    house = House.query.get_or_404(int(id))
    form = ArtEditForm()
    if house.category == '租房':
        category = 1
    if house.category == '二手房':
        category = 2
    if house.category == '商业地产':
        category = 3
    if request.method == 'GET':
        form.name.data = house.name
        form.category.data = category
        form.number.data = house.number
        form.company.data = house.company
        form.address.data = house.address
        form.shop_address.data = house.shop_address

    if form.validate_on_submit():
        data = form.data
        if data['category'] == 1:
            category = '租房'
        if data['category'] == 2:
            category = '二手房'
        if data['category'] == 3:
            category = '商业地产'
        house.name = data['name']
        house.category = category
        house.number = data['number']
        house.company = data['company']
        house.address = data['address']
        house.shop_address = data['shop_address']
        field.session.add(house)
        field.session.commit()
        flash(u"编辑成功", 'ok')
    return render_template('art_edit.html',form=form,title=u'编辑',art=house)


# 删除文章
@app.route("/art/del/<int:id>/", methods=['GET'])
def art_del(id):
    art = House.query.get_or_404(int(id))
    field.session.delete(art)
    field.session.commit()
    flash(u"删除成功", 'ok')
    return redirect('/art/list/1/')


# 文章列表
@app.route("/art/list/<int:page>/", methods=['GET'])
def art_list(page=None):
    if page is None:
        page = 1

    page_date = House.query.filter_by().order_by(House.created_time.desc()).paginate(page=page, per_page=20)
    return render_template('art_list.html', title=u'列表', page_date=page_date)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8080)
