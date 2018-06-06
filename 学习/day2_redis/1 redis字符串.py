# -*- coding: utf-8 -*-
import redis
"""
Title = redis字符串操作
Date = 20180404
"""

r = redis.Redis(host='127.0.0.1', port=6379,  decode_responses=True)    # 默认输出字节。修改为Str

# TODO StrictRedis 连接池
# pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
# r = redis.StrictRedis(connection_pool=pool)

# TODO SET GET设值
"""1.SET 命令用于设置给定 key 的值。如果 key 已经存储其他值， SET 就覆写旧值，且无视类型。"""
# print(r.set('123', '[123,dffd]'))  # 插入成功后返回True, 否则False

"""2.Get 命令用于获取指定 key 的值。如果 key 不存在，返回 None 。如果key 储存的值不是字符串类型，返回一个错误。"""
# print(r.get('123'))  # 返回的结果是[123,dffd]

"""3.Setrange 命令用指定的字符串覆盖给定 key 所储存的字符串值，覆盖的位置从偏移量 offset 开始。"""
# print(r.set('11', 'hello world'))  # 返回的结果是    True
# print(r.setrange('11', 6, "redis"))    # 返回的结果是    11

"""4.Getrange 命令用于获取存储在指定 key 中字符串的子字符串。字符串的截取范围由 start 和 end 两个偏移量决定(包括 start 和 end 在内)。"""
# print(r.set('getrange','wo shi hao ren '))
# print(r.getrange('getrange', 2, 4))   # 返回的结果是" sh"

"""1.Setbit 命令用于对 key 所储存的字符串值，设置或清除指定偏移量上的位(bit)。"""
# print(r.get('getrange'))  # 返回的结果是    hello word
# print(r.setbit('getrange', 1, 10086))  # 返回的结果是    1

"""6.Getbit 命令用于对 key 所储存的字符串值，获取指定偏移量上的位(bit)字符串值指定偏移量上的位(bit)。当偏移量 getrange 比字符串值的长度大，或者 key 不存在时，返回 0。"""
# print(r.getbit('getrange', 10086))

# TODO 多key设值
"""7.Setnx（SET if Not eXists） 命令在指定的 key 不存在时，为 key 设置指定的值。设置成功，返回True。 设置失败，返回False。"""
# print(r.setnx('getrange', 11223))

"""8.Getset 命令用于设置指定 key 的值，并返回 key 旧的值，当 key 存在但不是字符串类型时，返回一个错误。"""
# print(r.getset('123', '123')) # 返回的结果是[123,dffd]
# print(r.get('123')) # 返回的结果是123

"""9.Mset 命令用于同时设置一个或多个 key-value 对。"""
# print(r.mset(name1="1", name2='2'))  #  返回的结果是   True)
# print(r.mset({'name3':'3', 'name4':'4'}))
# print(r.mget('name1', 'name2', 'name3', 'name4'))

"""10.Msetnx 命令用于所有给定 key 都不存在时，同时设置一个或多个 key-value 对。
 当所有 key 都成功设置，返回True 。 如果所有给定 key 都设置失败(至少有一个 key 已经存在)，那么返回False 。"""
# print(r.msetnx(name5="1", name6='6'))     #返回的结果是  True
# print(r.msetnx(name5="55", name7='7'))    #返回的结果是   False

# TODO 返回数据
"""11.Mget 命令返回所有(一个或多个)给定 key 的值。 如果给定的 key 里面，有某个 key 不存在，那么这个 key 返回特殊值 None"""
# print(r.set('1', '1'))   # 返回的结果是    True
# print(r.set('11', '11'))  # 返回的结果是   True
# print(r.mget('1', '11', '222222'))  # 因为键222222不存在，返回的结果是   ['1', '11', None]

# TODO 字符长度
"""12.Strlen 命令用于获取指定 key 所储存的字符串值的长度。当 key 储存的不是字符串值时，返回一个错误。"""
# print(r.strlen('11'))  # 返回11

# TODO 过期时间
"""13.Setex 命令为指定的 key 设置值及其过期时间。如果 key 已经存在， SETEX 命令将会替换旧的值。"""
# print(r.setex('getrange', 1223, 2))

"""14.Psetex 命令以毫秒为单位设置 key 的生存时间。主意：SETEX 命令那样，以秒为单位。"""
# print(r.psetex('name2', 2, '123'))

# TODO 数据增减值
"""15.Incr 命令将 key 中储存的数字值增一 key 不存在，那么 key 的值会先被初始化为 0 """
# print(r.set('1', 12))
# print(r.incr('1'))  # 返回增1后的指

"""16.Redis Incrby 命令将 key 中储存的数字加上指定的增量值。 key 不存在，那么 key 的值会先被初始化为 0 """
# print(r.set('1', 12))
# print(r.incrby('21', 18))  # 返回增1后的指

"""17.Redis Incrbyfloat 命令为 key 中所储存的值加上指定的浮点数增量值 key 不存在，那么 INCRBYFLOAT 会先将 key 的值设为 0"""
# print(r.incrbyfloat('1', 12.12))

"""18.Redis Decr 命令将 key 中储存的数字值减一  key 不存在，那么 key 的值会先被初始化为 0"""
# print(r.decr('1', 1))

"""19.Redis Append 命令用于为指定的 key 追加值。key 已经存在并且是一个字符串， APPEND 命令将 value 追加到 key 原来的值的末尾。
如果 key 不存在， APPEND 就简单地将给定 key 设为 value ，就像执行 SET key value 一样。"""