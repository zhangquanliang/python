# -*- coding: utf-8 -*-
import redis
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.StrictRedis(connection_pool=pool)

"""1.Zadd 命令用于将一个或多个成员元素及其分数值加入到有序集当中。"""
# print(r.zadd('1', '1231', 1))

"""2.Zcard 命令用于计算集合中元素的数量。"""
# print(r.zcard('1'))

"""3.Zcount 命令用于计算有序集合中指定分数区间的成员数量。分数值在 min 和 max 之间的成员的数量。"""
# print(r.zcount('1', '0', '1'))

"""4.Zincrby 命令对有序集合中指定成员的分数加上增量 increment"""
# print(r.zincrby('1', '张三', 1))

"""1.Zinterstore 命令计算给定的一个或多个有序集的交集，其中给定 key 的数量必须以 numkeys 参数指定，并将该交集(结果集)储存到 destination 。
默认情况下，结果集中某个成员的分数值是所有给定集下该成员分数值之和。"""
# print(r.zinterstore('炸公司', '1'))

"""6. Zlexcount 命令在计算有序集合中指定字典区间内成员数量。"""
# print(r.zlexcount(name='1', min='-', max='+'))

"""7.Zrange 返回有序集中，指定区间内的成员。"""
# print(r.zrange(name='1', start=1, end=3))

"""8. Zrangebylex 通过字典区间返回有序集合的成员。"""
# print(r.zrangebylex(name='1', min=1, max='1'))

"""9.Zrangebyscore 返回有序集合中指定分数区间的成员列表。有序集成员按分数值递增(从小到大)次序排列。"""
# print(r.zrangebyscore(name='1', min='-', max='+'))

"""10.Zrank 返回有序集中指定成员的排名。其中有序集成员按分数值递增(从小到大)顺序排列。"""
# print(r.zrank('1', '1'))

"""11. Zrem 命令用于移除有序集中的一个或多个成员，不存在的成员将被忽略。"""
# print(r.zrem('1', '1'))

"""12.Zremrangebylex 命令用于移除有序集合中给定的字典区间的所有成员。"""
# print(r.zremrangebylex('1', min='[a', max='[c'))

"""13. Zremrangebyrank 命令用于移除有序集中，指定排名(rank)区间内的所有成员。"""
# print(r.zremrangebyrank('1', min=1, max=3))

"""14.Zremrangebyscore 命令用于移除有序集中，指定分数（score）区间内的所有成员。"""
# print(r.zremrangebyscore('1', min=1, max='2'))

"""15.Zrevrange 命令返回有序集中，指定区间内的成员。"""
# print(r.zadd('1', 1, 'ada', 2, '21311'))
# print(r.zrevrange('1', start=0, end=2))

"""16.Zrevrangebyscore 返回有序集中指定分数区间内的所有的成员。有序集成员按分数值递减(从大到小)的次序排列。"""
# print(r.zremrangebyscore(name='1', min='1', max='3'))

"""17. Zrevrank 命令返回有序集中成员的排名。其中有序集成员按分数值递减(从大到小)排序。"""
# print(r.zrevrank('1', '11'))

"""18.Zscore 命令返回有序集中，成员的分数值。 如果成员元素不是有序集 key 的成员，或 key 不存在，返回 None 。"""
# print(r.zscore('1', '12'))

"""19.Zunionstore 命令计算给定的一个或多个有序集的并集，其中给定 key 的数量必须以 numkeys 参数指定，并将该并集(结果集)储存到 destination"""
# print(r.zunionstore('adada', '1'))

"""20.  Zscan 命令用于迭代有序集合中的元素（包括元素成员和元素分值）"""
# print(r.zscan('1'))