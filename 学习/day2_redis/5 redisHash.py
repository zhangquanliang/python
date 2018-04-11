# -*- coding: utf-8 -*-
import redis
"""
Title = redisHash结构数据存储  name表名, key字段, value字段值
Date = 20180404
"""
"""使用StrictRedis连接池"""
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.StrictRedis(connection_pool=pool)

"""1.Hset 命令用于为哈希表中的字段赋值 。如果哈希表不存在，一个新的哈希表被创建并进行 HSET 操作。如果字段已经存在于哈希表中，旧值将被覆盖。
如果字段是哈希表中的一个新建字段，并且值设置成功，返回 1 。 如果哈希表中域字段已经存在且旧值已被新值覆盖，返回 0 。"""
# print(r.hset(name="name", key="key1", value="value"))  #返回的结果是 1

"""2.Hdel 命令用于删除哈希表 key 中的一个或多个指定字段，不存在的字段将被忽略。"""
# print(r.delete('name'))  # 删除成功后 返回的结果是 1, 失败0

"""3.Hexists命令用于查看哈希表的指定字段是否存在。哈希表含有给定字段，返回 True。如果哈希表不含有给定字段，或 key 不存在，返回False 。"""
# print(r.hset(name="1", key="1", value="1"))  # 返回的结果是 1
# print(r.hexists(name="1", key="1"))   # 返回的结果是 True

"""4.Hget 命令用于返回哈希表中指定字段的值。返回给定字段的值。如果给定的字段或 key 不存在时，返回 None 。"""
# print(r.hget("2","1"))   # 因为字段2不存在。所以返回的结果是 None

"""5.Hgetall 命令用于返回哈希表中，所有的字段和值。在返回值里，紧跟每个字段名(field name)之后是字段的值(value)，
所以返回值的长度是哈希表大小的两倍。"""
# print(r.hgetall('1'), r.hlen('1'))

"""6.Hincrby 命令用于为哈希表中的字段值加上指定增量值 增量也可以为负数，相当于对指定字段进行减法操作"""
# print(r.hincrby(name='1', key='1', amount=3)) hash表指必须为Int

"""7. Hincrbyfloat 命令用于为哈希表中的字段值加上指定浮点数增量值。 如果指定的字段不存在，那么在执行命令前，字段的值被初始化为 0 。"""
# print(r.hincrbyfloat(name='1', key='1', amount=11.20))

"""8.Hkeys 命令用于获取哈希表中的所有字段名。包含哈希表中所有字段的列表。 当 key 不存在时，返回一个空列表。"""
# print(r.hkeys(1))     # 返回的结果是 ['1', '2', '3']

"""9.Hlen 命令用于获取哈希表中字段的数量。哈希表中字段的数量。 当 key 不存在时，返回 0 。"""
# print(r.hlen(name='1'))

"""10.Hmset 命令用于同时将多个 field-value (字段-值)对设置到哈希表中。此命令会覆盖哈希表中已存在的字段。"""
# aa = {"a":"a","b":"b"}           # 返回的结果是 ['1']
# print(r.hmset("name",aa))            # 返回的结果是 True

"""11.Hmget 命令用于返回哈希表中，一个或多个给定字段的值。如果指定的字段不存在于哈希表，那么返回一个 nil 值"""
# print(r.hmget(name="1",keys="2"))   # 返回的结果是['2']

"""12.Hsetnx 命令用于为哈希表中不存在的的字段赋值 。"""
# print(r.hsetnx(name='231', key='12', value='1231'))

"""13.Hvals 命令返回哈希表所有字段的值。一个包含哈希表中所有值的表。 当 key 不存在时，返回一个空表。"""
# print(r.hvals('1'))