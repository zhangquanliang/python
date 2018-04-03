# -*- coding: utf-8 -*-

# abs() 函数返回数字的绝对值。  print("abs(-40) : ", abs(-40))
# dict() 函数用于创建一个字典。dict(关键字)  dict(元素的容器, **kwarg) dict(可迭代对象, **kwarg)
# help() 函数用于查看函数或模块用途的详细说明。
# min() 方法返回给定参数的最小值，参数可以为序列。  min(0, 100, -400))
# setattr 函数对应函数 getatt()，用于设置属性值，该属性必须存在。setattr(object, name, value)
# all() 函数用于判断给定的可迭代参数 iterable 中的所有元素是否不为 0、''、False 或者 iterable 为空，如果是返回 True，否则返回 False。
# dir() 函数不带参数时，返回当前范围内的变量、方法和定义的类型列表；带参数时，返回参数的属性、方法列表。 dir([object])
# hex() 函数用于将10进制整数转换成16进制，以字符串形式表示。 hex(x)  x代表10进制整数
# next() 返回迭代器的下一个项目  next(iterator[, default])
# slice() 函数实现切片对象，主要用在切片操作函数里的参数传递。 slice(stop), slice(start, stop[, step])
# any() 函数用于判断给定的可迭代参数 iterable 是否全部为空对象，如果都为空、0、false，则返回 False，如果不都为空、0、false，则返回 True。
# python divmod() 函数把除数和余数运算结果结合起来，返回一个包含商和余数的元组(a // b, a % b)。  divmod(a, b)
# id() 函数用于获取对象的内存地址。 id([object])
# sorted() 函数对所有可迭代的对象进行排序操作。 sorted(iterable, key=None, reverse=False)
# ascii() 函数类似 repr() 函数, 返回一个表示对象的字符串, 但是对于字符串中的非 ASCII 字符则返回通过 repr() 函数使用 \x, \u 或 \U 编码的字符。
# enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。
# Python3.x 中 input() 函数接受一个标准输入数据，返回为 string 类型。 python3 里 input() 默认接收到的是 str 类型。
# oct() 函数将一个整数转换成8进制字符串。
# bin() 返回一个整数 int 或者长整数 long int 的二进制表示
# eval() 函数用来执行一个字符串表达式，并返回表达式的值。 eval(expression[, globals[, locals]])
# open() 函数用于打开一个文件，创建一个 file 对象，相关的方法才可以调用它进行读写
# bool() 函数用于将给定参数转换为布尔类型，如果没有参数，返回 False。
# exec 执行储存在字符串或文件中的 Python 语句，相比于 eval，exec可以执行更复杂的 Python 代码。exec(object[, globals[, locals]])
# isinstance() 函数来判断一个对象是否是一个已知的类型，类似 type()。
# sum() 方法对系列进行求和计算。 sum(iterable[, start])
# bytearray() 方法返回一个新字节数组。这个数组里的元素是可变的，并且每个元素的值范围: 0 <= x < 256。 bytearray([source[, encoding[, errors]]])
# filter() 函数用于过滤序列，过滤掉不符合条件的元素 filter(function, iterable)
# issubclass() 方法用于判断参数 class 是否是类型参数 classinfo 的子类。
# pow() 方法返回 xy（x的y次方） 的值。  pow(x, y[, z])
# super() 函数是用于调用父类(超类)的一个方法。super(type[, object-or-type])
# bytes 函数返回一个新的 bytes 对象，该对象是一个 0 <= x < 256 区间内的整数不可变序列。它是 bytearray 的不可变版本。bytes([source[, encoding[, errors]]])
# iter() 函数用来生成迭代器。
# tuple 函数将列表转换为元组。。tuple( seq )
# callable() 函数用于检查一个对象是否是可调用的。如果返回True，object仍然可能调用失败；但如果返回False，调用对象ojbect绝对不会成功。
# format 函数可以接受不限个参数，位置可以不按顺序。 "{1} {0} {1}".format("hello", "world")  # 设置指定位置
# property() 函数的作用是在新式类中返回属性值。
# chr() 用一个范围在 range（256）内的（就是0～255）整数作参数，返回一个对应的字符。
# frozenset() 返回一个冻结的集合，冻结后集合不能再添加或删除任何元素
# list() 方法用于将元组转换为列表。
# vars() 函数返回对象object的属性和属性值的字典对象。 vars([object])
# getattr() 函数用于返回一个对象属性值。 getattr(object, name[, default])
# locals() 函数会以字典类型返回当前位置的全部局部变量locals()
# repr() 函数将对象转化为供解释器读取的形式 repr(object)
# zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。
# compile() 函数将一个字符串编译为字节代码。compile(source, filename, mode[, flags[, dont_inherit]])
# globals() 函数会以字典类型返回当前位置的全部全局变量。
# map() 会根据提供的函数对指定序列做映射。
# reversed 函数返回一个反转的迭代器。 reversed(seq)
# __import__() 函数用于动态加载类和函数 。如果一个模块经常变化就可以使用 __import__() 来动态载入。
# complex() 函数用于创建一个值为 real + imag * j 的复数或者转化一个字符串或数为复数。如果第一个参数为字符串，则不需要指定第二个参数。。
# hasattr() 函数用于判断对象是否包含对应的属性。
# max() 方法返回给定参数的最大值，参数可以为序列。
# round() 方法返回浮点数x的四舍五入值。
# delattr 函数用于删除属性。delattr(x, 'foobar') 相等于 del x.foobar。delattr(object, name)
# hash() 用于获取取一个对象（字符串或者数值等）的哈希值。
# memoryview() 函数返回给定参数的内存查看对象(Momory view)。
# set() 函数创建一个无序不重复元素集，可进行关系测试，删除重复数据，还可以计算交集、差集、并集等。