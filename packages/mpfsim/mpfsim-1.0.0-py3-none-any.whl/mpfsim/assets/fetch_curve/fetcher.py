#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time:   2023/4/22 14:24
# File:   fetcher.py
# Author: He Ma
# Email:  1692303843@qq.com

from core.fetch_tools import *

fetcher = CurveFetcher()

# %%
# C1-Nb曲线
curve_name = "C1-Nb.csv"
# 读取数据

fetcher.init(curve_name, base_path='fetch_curve/origin_project',
             path_db='assets/MPF.db', table_name='chart_digitization')
# 选择曲线列名
curve_xy_list = [['x1', 'px1'], ['x2', 'px2']]
fetcher.fit(curve_xy_list)
# 应用
x_origin = fetcher.x_origin
fetcher.f(x_origin)
# 验证数据

fetcher.draw_verify(x_origin)

# %%
# C2-NRe'曲线
curve_name = "C2-NRe'.csv"
# 读取数据

fetcher.init(curve_name, base_path='fetch_curve/origin_project',
             path_db='assets/MPF.db', table_name='chart_digitization_test')
# 选择曲线列名
curve_xy_list = [['x1', 'px1'], ['x2', 'px2'], ['x2', 'px2'], ['x3', 'px3'], ['x4', 'px4'], ['x5', 'px5']]
fetcher.fit(curve_xy_list, degree=2)
# %%
# 应用
x_origin = fetcher.x_origin
fetcher.f(x_origin)
# 验证数据

fetcher.draw_verify(x_origin)

# %%
# 显示整个数据表
print(fetcher.select_all())

# 关闭连接
fetcher.close()
