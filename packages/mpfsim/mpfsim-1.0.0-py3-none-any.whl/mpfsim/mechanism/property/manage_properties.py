#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time:   2023/5/7 16:27
# File:   manage_properties.py
# Author: He Ma
# Email:  1692303843@qq.com

from itertools import product

import pandas as pd

from mechanism.property.black_oil import BlackOilProperty


# %%
class ManageProperties(BlackOilProperty):
    """物性管理器类"""

    def __init__(self, path_variable_info, *arg):
        # path_variable_info 用于加载的黑油模型变量信息管理文件
        # manager_config['variable_info']
        super().__init__()
        self.ans_df = None
        self.arg = arg
        self.property_info = pd.read_excel(path_variable_info)

    def update_series(self, update_dict={}):
        """
        更新 legal_vars 中的 部分参数
        Args:
            update_dict:

        Returns:

        """
        legal_vars = ['P', 'T', 'Pb', 'fw', 'Rp', 'rho_ro', 'rho_rg', 'rho_rw', 'method_dict_input']
        if len(update_dict.items()) == 0:
            print(legal_vars)
            return

        for k, v in update_dict.items():
            if k not in legal_vars:
                raise Exception('%s 不可更新' % legal_vars)
            exec('self.%s = v' % k)

        self.update()

    def series(self, P, T, Pb, fw, Rp, rho_ro, rho_rg, rho_rw=[1.0], method_dict_input={}):
        """
        矩阵更新，多参数的排列组合
        TODO 早日替换
        """
        self.method_dict_input = method_dict_input
        loop_val = [P, T, Pb, fw, Rp, rho_ro, rho_rg, rho_rw]  # method_dict_input = [{}]
        num_loop = len(list(product(*loop_val)))
        print('待计算排列组合数量:', num_loop)
        self.ans_df = []
        for i_val in product(*loop_val):
            P, T, Pb, fw, Rp, rho_ro, rho_rg, rho_rw = i_val
            self.P = P
            self.T = T
            self.Pb = Pb
            self.fw = fw
            self.Rp = Rp
            self.rho_ro = rho_ro
            self.rho_rg = rho_rg
            self.rho_rw = rho_rw
            # self.method_dict_input = method_dict_input

            self.update()

            ans = []
            for i_property in self.property_info['变量']:
                value = getattr(self, i_property)
                ans.append(value)
                # print(i_property, value)

            self.ans_df.append(ans)
        self.ans_df = pd.DataFrame(self.ans_df)

        # _temp = property_info[['含义', '标准单位']].T
        # self.ans_df = pd.concat([_temp, self.ans_df])
        self.ans_df.columns = self.property_info['变量']
        # print(type(self.ans_df))


# %%
if __name__ == '__main__':
    from core import manager_config

    variable_info = manager_config.work_dir + manager_config.variable_info
    # manager_p = ManageProperties(manager_config['variable_info'])
    manager_p = ManageProperties(variable_info)
