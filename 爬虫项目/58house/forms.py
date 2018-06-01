# cofing:utf8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,IntegerField
from wtforms.validators import DataRequired
from models import House



"""
发布文章表单
1.标题
2.分类
3.封面
4.内容
5.发布文章按钮
"""


class ArtForm(FlaskForm):
    name = StringField(
        label=u"名称",
        validators=[
            DataRequired(u"名称不能为空！")
        ],
        description=u"名称",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入名称!"
        }
    )

    category = SelectField(
        label=u"分类",
        validators=[
            DataRequired(u"分类不能为空！")
        ],
        description=u"分类",
        choices=[(1, u"租房"), (2, u"二手房"), (3, u"商业地产")],
        default=1,
        coerce=int,
        render_kw={
            "class": "form-control",
        }
    )

    number = IntegerField(
        label=u"号码",
        validators=[
            DataRequired(u"号码不能为空！")
        ],
        description=u"号码",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入号码!"
        }
    )

    company = StringField(
        label=u"公司",
        validators=[
            DataRequired(u"公司不能为空！")
        ],
        description=u"公司",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入公司!"
        }
    )

    address = StringField(
        label=u"所属城市",
        validators=[
            DataRequired(u"所属城市不能为空！")
        ],
        description=u"所属城市",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入所属城市!"
        }
    )

    shop_address = StringField(
        label=u"详细地址",
        validators=[
            DataRequired(u"详细地址不能为空！")
        ],
        description=u"详细地址",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入详细地址!"
        }
    )

    submit = SubmitField(
        u"添加",
        render_kw={
            "class": "btn btn-primary",
        }
    )



"""
文章编辑表单
1.标题
2.分类
3.封面
4.内容
5.发布文章按钮
"""


class ArtEditForm(FlaskForm):
    id = IntegerField(
        label=u'编号',
        validators=[
            DataRequired(u'编号不能为空！')
        ]
    )
    name = StringField(
        label=u"名称",
        validators=[
            DataRequired(u"名称不能为空！")
        ],
        description=u"名称",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入名称!"
        }
    )

    category = SelectField(
        label=u"分类",
        validators=[
            DataRequired(u"分类不能为空！")
        ],
        description=u"分类",
        choices=[(1, u"租房"), (2, u"二手房"), (3, u"商业地产")],
        default=3,
        coerce=int,
        render_kw={
            "class": "form-control",
        }
    )

    number = IntegerField(
        label=u"号码",
        validators=[
            DataRequired(u"号码不能为空！")
        ],
        description=u"号码",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入号码!"
        }
    )

    company = StringField(
        label=u"公司",
        validators=[
            DataRequired(u"公司不能为空！")
        ],
        description=u"公司",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入公司!"
        }
    )

    address = StringField(
        label=u"所属城市",
        validators=[
            DataRequired(u"所属城市不能为空！")
        ],
        description=u"所属城市",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入所属城市!"
        }
    )

    shop_address = StringField(
        label=u"详细地址",
        validators=[
            DataRequired(u"详细地址不能为空！")
        ],
        description=u"详细地址",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入详细地址!"
        }
    )
    submit = SubmitField(
        u"编辑文章",
        render_kw={
            "class": "btn btn-primary",
        }
    )
