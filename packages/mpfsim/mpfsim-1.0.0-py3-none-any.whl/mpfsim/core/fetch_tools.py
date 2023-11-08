#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time:   2023/4/23 22:01
# File:   fetch_tools.py
# Author: He Ma
# Email:  1692303843@qq.com

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from core.tool_sql import *


def str2var(text):
    """
    主要用于将字符串转化为字典
    :param text: str 有str(var)形成的, text = str(var)
    :return: var, Python变量，一般为字典
    """
    array = np.array
    var = eval(text)
    return var


class _CurveFetcherGet:
    """曲线信息加载类"""

    def __init__(self, curve_name, base_path='assets/fetch_curve/origin_project'):
        # curve_name = 'C1 - Nb.csv'
        self.line_list = None
        self.x_origin = None
        self.y_origin = None
        self.coeff_list = None
        self.data = None
        self.x = None
        self.y = None
        self.section_list = []

        self.curve_name = curve_name
        self.base_path = base_path
        self.curve_path = '%s/%s' % (self.base_path, self.curve_name)

    def fit(self, curve_xy_list, degree=4):
        data = pd.read_csv(self.curve_path)

        line_list = []
        coeff_list = []
        for curve_xy in curve_xy_list:
            # 选择每组xy曲线
            # curve_xy = ['x1', 'px1']
            curve_data_xy = data[curve_xy].dropna(how='all')
            _x = curve_data_xy.iloc[:, 0]
            _y = curve_data_xy.iloc[:, 1]

            # 对每条线进行拟合
            # coeff: np.arraay, shape: [degree,]
            coeff = np.polyfit(_x, _y, degree)

            coeff_list.append(coeff)
            line_list.append(curve_data_xy)

        # 将n条线的散点堆叠为一组散点列表
        section_list = [line.iloc[0, 0] for line in line_list[1:]]
        self.x_origin = np.hstack([line.iloc[:, 0] for line in line_list])
        self.y_origin = np.hstack([line.iloc[:, 1] for line in line_list])

        self.line_list = line_list
        self.coeff_list = coeff_list
        self.section_list = section_list

    def f(self, x_array):
        """
        拟合曲线的函数,
        加载分段点位置self.section_list，加载系数列表self.coeff_list
        并应用于x_array，实现`y=f(x)`
        :param x_array: 一维数组，y=f(x)的输入
        :return:
        """
        # len(self.section_list) == len(self.coeff_list) - 1
        cond_list = [x_array <= section for section in self.section_list]
        cond_list.append(x_array > self.section_list[-1])
        choice_list = [np.poly1d(coeff)(x_array) for coeff in self.coeff_list]
        y_fit = np.select(cond_list, choice_list)

        return y_fit

    def draw_verify(self, x_fit):
        # 用户画图验证

        # x_fit = np.linspace(0, 50, 100)
        y_fit = self.f(x_fit)
        plt.figure(figsize=(10, 6), dpi=500)
        plt.plot(self.x_origin, self.y_origin)
        plt.plot(x_fit, y_fit)
        plt.show()


class _CurveFetcherSQL(SQLReader):
    def __init__(self, path_db='./test.db', table_name='chart_digitization', table_columns=None):
        # self.sql_reader = None
        if table_columns is None:
            table_columns = ['name', 'value']
        self.path_db = path_db
        self.table_name = table_name
        # _CurveFetcherSQL和SQLReader类内部同时有self.table_columns，注意避免冲突或覆盖
        self.table_columns = table_columns

    def sql_connect(self):
        SQLReader.__init__(self, self.path_db, self.table_name, self.table_columns)

        # self.sql_reader = SQLReader(path_db=self.path_db, table_name=self.table_name)
        status = self.create_table(self.table_name, self.table_columns)
        return status

    def sql_write(self, params_list):
        """
        将曲线参数保存到数据库
        :param sql_reader: sqlite3 sql_tools.SQLReader
        :return: status True or other
        """

        status = self.insert_data(params_list)
        return status

    def sql_load(self, curve_name):
        sql_text_curve = "SELECT * FROM %s WHERE name=='%s'" % (self.table_name, curve_name)
        self.cur.execute(sql_text_curve)
        sql_value = self.cur.fetchall()

        sql_value_dict = str2var(sql_value[0][1])
        return sql_value_dict


class CurveFetcher(_CurveFetcherGet, _CurveFetcherSQL):
    def __init__(self):
        pass

    def init(
            self, curve_name, base_path='fetch_curve/origin_project',
            path_db='./test.db', table_name='chart_digitization', table_columns=None
    ):
        _CurveFetcherGet.__init__(self, curve_name, base_path)
        _CurveFetcherSQL.__init__(self, path_db, table_name, table_columns)

        self.sql_connect()

    def fit(self, curve_xy_list, degree=4):
        super().fit(curve_xy_list, degree)

        value_dict = {
            'self.coeff_list': self.coeff_list,
            'self.section_list': self.section_list,
        }
        params_list = [
            [self.curve_name, str(value_dict)],
        ]

        # 新增n行数据params_list, 此处n=1
        self.sql_write(params_list)

    def f(self, x_array):
        """
        读取数据库
        :param x_array:
        :return:
        """
        sql_value_dict = self.sql_load(self.curve_name)
        self.coeff_list = sql_value_dict['self.coeff_list']
        self.section_list = sql_value_dict['self.section_list']

        # 基类y=f(x)派生
        y_fit = super(CurveFetcher, self).f(x_array)
        return y_fit
