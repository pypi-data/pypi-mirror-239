#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/6/22 21:47
# @Author  : 马赫
# @Email   : 1692303843@qq.com
# @FileName: tool_expert.py

import functools
import hashlib
import numpy as np


# %% 函数的结果缓存
# import functools
# import hashlib
# import numpy as np


def hash_function(*args, **kwargs):
    """哈希算法"""
    key = hashlib.sha256()

    for arg in args:
        if isinstance(arg, np.ndarray):
            arg_data = arg.tobytes()
            key.update(arg_data)
        else:
            key.update(str(arg).encode())

    for kwarg in kwargs.values():
        if isinstance(kwarg, np.ndarray):
            kwarg_data = kwarg.tobytes()
            key.update(kwarg_data)
        else:
            key.update(str(kwarg).encode())

    return key.digest()


def cached_function(func):
    """
    基于哈希算法的任意数据缓存装饰器
    函数在输入不变的情况下，结果进行缓存

    @cached_function
    def calculate_sum(a, b):
        print("执行函数计算")
        return a + b

    # 第一次调用，需要进行函数计算
    output = calculate_sum(1, 2)
    print("函数计算结果:", output)

    # 再次使用相同的输入参数调用，不需要进行函数计算，直接返回上一次的结果
    output = calculate_sum(1, 2)
    print("函数计算结果:", output)

    """
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = hash_function(*args, **kwargs)

        if key in cache:
            # print("从缓存中获取结果")
            return cache[key]

        result = func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper


def _test_cached_function():
    """函数在输入不变的情况下，结果进行缓存"""

    # 示例用法
    @cached_function
    def calculate_sum(a, b):
        print("执行函数计算")
        return a + b

    # 第一次调用，需要进行函数计算
    output = calculate_sum(1, 2)
    print("函数计算结果:", output)

    # 再次使用相同的输入参数调用，不需要进行函数计算，直接返回上一次的结果
    output = calculate_sum(1, 2)
    print("函数计算结果:", output)

    # 改变输入参数，需要重新进行函数计算
    output = calculate_sum(3, 4)
    print("函数计算结果:", output)

    # Numpy数组作为输入参数
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    output = calculate_sum(a, b)
    print("函数计算结果:", output)

    # 再次使用相同的Numpy数组作为输入参数调用，不需要进行函数计算，直接返回上一次的结果
    output = calculate_sum(a, b)
    print("函数计算结果:", output)


# %% 状态参数定义与更新管理类
class StateParam:
    """
    TODO 这是干嘛的？？？
    状态参数定义与更新管理类
    """

    def __init__(self, properties=[], default_properties=None, functions=[], dependent_properties=[], *args):
        """

        Args:
            properties: list len: n 状态参数的名称列表 ['a', 'b', 'c', 'd', 'e']
            default_properties: list len: n 与properties对应的状态参数的默认值 [1, 2, 3, 4, 5]
            functions: list len: m < n 状态更新函数列表 [some_function1, some_function2, some_function3]
            dependent_properties: list len: m 状态更新函数的输入输出对列表
                # 第i个元素为两个元素组成的列表
                    # 两个元素中第一个为输入数据列表，第二个为输出数据列表
                [
                    [['a', 'b'], ['c']],
                    [['c'], ['d']],
                    [['b'], ['e']],
                ]

        Examples:
        --------
        def some_function1(x, y):
            print('计算1')
            return x + y


        def some_function2(x):
            print('计算2')
            return x * 10

        # 状态参数的名称列表
        properties = ['a', 'b', 'c', 'd', 'e']
        # 状态参数的缺省值列表
        default_properties = None
        # 状态参数更新公式列表
        functions = [some_function1, some_function2, some_function2]
        # 状态参数更新公式的输入输出对列表
        dependent_properties = [
            [['a', 'b'], ['c']],
            [['c'], ['d']],
            [['b'], ['e']],
        ]
        # 示例用法
        state_param = StateParam(properties, default_properties, functions, dependent_properties)

        print('--> 1')
        # 打印属性值
        state_param.print_properties()

        print('--> 2')
        # 设置初始属性值
        state_param.a = 4
        # 更新依赖的属性
        state_param.update_dependent_properties()
        # 打印属性值
        state_param.print_properties()

        print('--> 3')
        # 设置初始属性值
        state_param.b = 14

        # 更新依赖的属性
        state_param.update_dependent_properties()
        # 打印属性值
        state_param.print_properties()

        print('--> 4')

        # 更新依赖的属性
        state_param.update_dependent_properties()
        # 打印属性值
        state_param.print_properties()

        """

        self.properties = properties
        self.functions = functions
        self.dependent_properties = dependent_properties
        self.args = args
        assert len(self.functions) == len(self.dependent_properties), '函数-参数对，长度应当一致'

        if default_properties is None:
            default_properties = [-1] * len(properties)
        for j in range(len(self.properties)):
            setattr(self, properties[j], default_properties[j])

        self.old_property_values = dict()
        self.update_dependent_properties()

    def update_dependent_properties(self):
        for i in range(len(self.functions)):
            function = self.functions[i]
            dependent_properties_input, dependent_properties_output = self.dependent_properties[i]

            # 检查依赖的属性是否有变化
            property_changed = False
            for prop in dependent_properties_input:
                if getattr(self, prop) != self.old_property_values.get(prop):
                    property_changed = True
                    print('Update: %s' % prop)
                    break

            # 根据函数和依赖的属性进行更新
            if property_changed:
                new_values = function(*[getattr(self, prop) for prop in dependent_properties_input])

                # 更新对应的属性值
                if len(dependent_properties_output) == 1:
                    new_values = [new_values]
                for j in range(len(dependent_properties_output)):
                    setattr(self, dependent_properties_output[j], new_values[j])

        # 更新旧属性值
        self.update_old_property_values()

    def update_old_property_values(self):
        self.old_property_values = {prop: getattr(self, prop) for prop in self.properties}

    def print_properties(self):
        for prop in self.properties:
            value = getattr(self, prop, None)
            print('%s: %s' % (prop, value))


def _test_state_param():
    def some_function1(x, y):
        print('计算1')
        return x + y

    def some_function2(x):
        print('计算2')
        return x * 10

    # 状态参数的名称列表
    properties = ['a', 'b', 'c', 'd', 'e']
    # 状态参数的缺省值列表
    default_properties = None
    # 状态参数更新公式列表
    functions = [some_function1, some_function2, some_function2]
    # 状态参数更新公式的输入输出对列表
    dependent_properties = [
        [['a', 'b'], ['c']],
        [['c'], ['d']],
        [['b'], ['e']],
    ]
    # 示例用法
    state_param = StateParam(properties, default_properties, functions, dependent_properties)

    print('--> 1')
    # 打印属性值
    state_param.print_properties()

    print('--> 2')
    # 设置初始属性值
    state_param.a = 4
    # 更新依赖的属性
    state_param.update_dependent_properties()
    # 打印属性值
    state_param.print_properties()

    print('--> 3')
    # 设置初始属性值
    state_param.b = 14

    # 更新依赖的属性
    state_param.update_dependent_properties()
    # 打印属性值
    state_param.print_properties()

    print('--> 4')

    # 更新依赖的属性
    state_param.update_dependent_properties()
    # 打印属性值
    state_param.print_properties()
