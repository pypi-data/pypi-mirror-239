#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/6/2 15:02
# @Author  : 马赫
# @Email   : 1692303843@qq.com
# @FileName: constants.py

import os
import numpy as np

from core.tool_class import Singleton

# 全局不可变参数
g = 9.8  # 重力加速度 (m/s^2)

lg = np.log10
ln = np.log
exp = np.exp
pi = np.pi

# # 获取当前文件的路径
# current_path = os.path.abspath(__file__)
#
# # 获取当前文件所在的目录路径
# # directory_path = '../mpfsim'
# directory_path = os.path.dirname(os.path.dirname(current_path))
#
# # 全局信息字典
# BASE_DICT = {
#     'BASE_PATH': directory_path,
#     'path': {
#         'database': './assets/MPF.db',
#         'database_test': './assets/test.db',
#
#         'variable_info': './assets/variable_info.xlsx',
#         'Params_info': './assets/Params.xlsx',
#
#         'font_path': './assets/tnw_simsun.ttf',
#     },
#     # 标准状况
#     'sc': {
#         'P': 0.101,  # 标况压力 (MPa)
#         'T': 15 + 273.15,  # 标况温度 (K)
#         'Z': 1,  # 标况天然气压缩系数 (-)
#     },
# }


# class DefaultInfo(Singleton):
#     def __init__(self, **BASE_DICT):
#         super().__init__()
#
#         self.BASE_PATH = None
#         self.path = None
#
#         self.__dict__.update(**BASE_DICT)
#
#         self.path_update()
#
#     def path_update(self):
#         """文件路径拼接"""
#         for key, value in self.path.items():
#             setattr(self, key, os.path.join(self.BASE_PATH, value))
#
#
# if __name__ == '__main__':
#     # 全局公用变量
#     default_info = DefaultInfo(**BASE_DICT)
