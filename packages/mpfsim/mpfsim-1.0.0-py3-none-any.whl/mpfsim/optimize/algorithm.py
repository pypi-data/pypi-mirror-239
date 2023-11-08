#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time:   2023/4/29 16:20
# File:   algorithm.py
# Author: He Ma
# Email:  1692303843@qq.com

import sympy
from core import mylog


# def fit_multipoint(func, x_list, y_list):
#     """
#     多点数据校正迭代器函数
#     f_calibrate = fit_multipoint(f, x, y)
#     y_calibrate = f_calibrate(x)  # x可为单个数据或列表
#     Args:
#         func: 校正函数
#         x_list: 校正的输入列表，长度为1时则为单点校正 len(x_list) >= func的参数个数
#         y_list: 校正的输出列表，len(x_list) == len(y_list)
#
#     Returns:
#         transform: 经过拟合的函数，使用时需要传入输入数据x, x可为单个数据或列表
#
#     """
#     popt, _pcov = curve_fit(func, x_list, y_list)
#     assert len(x_list) == len(y_list), \
#         '校正数据的输入输出需要相同长度, 输入:%s,输出:%s' % (len(x_list), len(y_list))
#     def transform(x):
#         y_calibrate = func(x, *popt)
#         return y_calibrate
#     return transform

def root_Newton(f, x0, symbol=sympy.Symbol('x'), epsilon=1e-6, max_iteration=100, verbose=0):
    x = symbol
    df = sympy.diff(f, x, 1)

    error = None
    x_list = [x0]
    for i in range(max_iteration):
        dy = df.subs(x, x0)
        if dy == 0:
            # print('极值点:', x0)
            break

        y_val = f.subs(x, x0)
        dy_val = df.subs(x, x0)
        x0 = x0 - float(y_val) / float(dy_val)
        x_list.append(x0)

        error = abs((x_list[-1] - x_list[-2]) / x_list[-1])
        if error < epsilon:
            if verbose > 0:
                mylog.logger.info('迭代%s次后，误差小于1e-6: %s ' % (i + 1, error))
            break
    else:
        mylog.logger.info('迭代%s次后，误差: %s, 未收敛结果: %s ' % (max_iteration, error, x_list[-1]))

        return None
    return x_list[-1]
