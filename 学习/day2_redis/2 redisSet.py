# -*- coding: utf-8 -*-
import redis
"""
Title = redisSet结构数据存储
Date = 20180408
"""
r = redis.Redis(host='127.0.0.1', port=6379)
"""1. Sadd 命令将一个或多个成员元素加入到集合中，已经存在于集合的成员元素将被忽略。"""
# print(r.sadd('1', '123', '1213123',123,'掌声'))

"""2.Scard 命令返回集合中元素的数量。集合的数量。 当集合 key 不存在时，返回 0 。"""
# print(r.scard('1'))

"""3.Sdiff 命令返回给定集合之间的差集。不存在的集合 key 将视为空集。"""
# print(r.sdiff('1', '123'))

"""4.Sdiffstore 命令将给定集合之间的差集存储在指定的集合中。如果指定的集合 key 已存在，则会被覆盖。"""
# print(r.sdiffstore('1', '12', '12213'))

"""1.Sinter 命令返回给定所有给定集合的交集。 不存在的集合 key 被视为空集。 当给定集合当中有一个空集时，结果也为空集(根据集合运算定律)。"""
# print(r.sinter('1'))

"""6.Sinterstore 命令将给定集合之间的交集存储在指定的集合中。如果指定的集合已经存在，则将其覆盖。"""
# print(r.sinterstore('a', '1'))

"""7.Sismember 命令判断成员元素是否是集合的成员。"""
# print(r.sismember('1', '张三'))

"""8.Smembers 命令返回集合中的所有的成员。 不存在的集合 key 被视为空集合。"""
# print(r.smembers('1'))

"""9.Smove 命令将指定成员 member 元素从 source 集合移动到 destination 集合。"""
# print(r.smove('1', 'adawda', '1213'))

"""10. Spop 命令用于移除并返回集合中的一个随机元素。"""
# print(r.spop('1'))

"""11.Srandmember 命令用于返回集合中的一个随机元素。"""
# print(r.srandmember('1'))

"""12. Srem 命令用于移除集合中的一个或多个成员元素，不存在的成员元素会被忽略。"""
# print(r.srem('1', '1213'))

"""13.Sunion 命令返回给定集合的并集。不存在的集合 key 被视为空集。"""
# print(r.sunion('1', 'awdaw'))

"""14.Sunionstore 命令将给定集合的并集存储在指定的集合 destination 中。"""
# print(r.sunionstore('a', '1213'))

"""15.Sscan 命令用于迭代集合键中的元素。"""
# print(r.sscan('1'))