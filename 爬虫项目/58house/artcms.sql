/*
用户表
1.编号
2.账号
3.密码
4.注册时间
 */

CREATE TABLE if NOT EXISTS user (
  id INT unsigned NOT NULL auto_increment KEY comment '主键ID',
  name VARCHAR(20) NOT NULL comment '账号',
  pwd VARCHAR(100) NOT NULL comment '密码',
  addtime datetime NOT NULL comment '注册时间'
)engine=InnoDB DEFAULT charset=utf8 comment '会员';


/*
文章表
1.编号
2.标题
3.分类
4.作者
1.封面
6.内容
7.发布时间
 */
CREATE TABLE if NOT EXISTS art (
  id INT unsigned NOT NULL auto_increment KEY comment '主键ID',
  title VARCHAR(100) NOT NULL comment '标题',
  cate tinyint unsigned NOT NULL cmment '分类',
  user_id int unsigned NOT NULL comment '作者',
  loge VARCHAR(100) NOT NULL comment '封面',
  cintent mediumtext NOT NULL comment '文章',
  addtime datetime NOT NULL comment '发布时间'
)engine=InnoDB DEFAULT charset=utf8 comment '文章';