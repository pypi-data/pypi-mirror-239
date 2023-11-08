#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time:   2023/6/25 15:19
# File:   well_data_entry.py
# Author: He Ma
# Email:  1692303843@qq.com

import copy
import bisect
import numpy as np
import pandas as pd

from core.tool_class import Singleton
from core import manager_config
from mechanism.unit_conversion import unit_conversion as unit


# %% 数据对的线性插值与外推

def piecewise_linear_interp(x_list, y_list, is_step_func=False):
    """
    数据对左开右闭的线性插值与外推

    根据测深计算，离散数据对（测深-x）的垂深、环境温度、总传热系数U值、
    油管内径、管壁厚度、管壁粗糙度、套管内径、套管外径、套管导热系数、水泥环外径、水泥环导热系数、设备等
    Args:
        x_list: 测深列表
        y_list: 其他值列表
        is_step_func: 是否为阶梯函数 (油套管)

    Returns:

    """

    def wrapper(z):
        x_left, x_right = x_list[0], x_list[-1]

        if z < x_left:
            if not is_step_func:

                # 当插值点小于 x 范围下限时，对应于(y0, x0)和(y1, x1)的线性插值
                y0, y1 = y_list[0], y_list[1]
                x0, x1 = x_list[0], x_list[1]
                k = (y1 - y0) / (x1 - x0)
                b = y0 - k * x0
            else:
                k = 0
                b = y_list[0]

        elif z >= x_right:
            if not is_step_func:

                # 当插值点大于 x 范围上限时，对应于(y_n-1, x_n-1)和(y_n, x_n)的线性插值
                y0, y1 = y_list[-2], y_list[-1]
                x0, x1 = x_list[-2], x_list[-1]
                k = (y1 - y0) / (x1 - x0)
                b = y0 - k * x0
            else:
                k = 0
                b = y_list[-1]
        else:
            if not is_step_func:

                # 找到插值点对应的数据段
                idx = bisect.bisect_right(x_list, z) - 1
                x_left, x_right = x_list[idx], x_list[idx + 1]
                y_left, y_right = y_list[idx], y_list[idx + 1]

                # 计算数据段的斜率 k 和截距 b
                k = (y_right - y_left) / (x_right - x_left)
                b = y_left - k * x_left
            else:
                # 找到插值点对应的数据段
                idx = bisect.bisect_right(x_list, z) - 1
                k = 0
                b = y_list[idx + 1]

        # 在数据段上进行线性插值
        y_interp = k * z + b
        return y_interp

    return wrapper


def calculate_angle(MD_list, TVD_list):
    def angle_calculator(z_MD):
        # 井斜角 [0~180°] -> 管线与水平正方向的角度 [90~-90°] -> cos(井斜角) [1~-1]
        # 井斜角 + 管线与水平正方向的角度 = 90°
        for i in range(len(MD_list) - 1):
            if z_MD >= MD_list[i] and z_MD <= MD_list[i + 1]:
                dx = MD_list[i + 1] - MD_list[i]
                dy = TVD_list[i + 1] - TVD_list[i]

                angle = np.rad2deg(np.arccos(dy / dx))

                return angle
        return None

    return angle_calculator


class GetDataInterp:
    """
    根据变量测深z对各类参数进行插值或外推

    """

    def __init__(self, x_y_key_flag_list):
        """
        x列表、y列表、名称列表组成的三元组列表
        Args:
            x_y_key_list:
        """
        self.x_y_key_flag_list = x_y_key_flag_list

    def __call__(self, z):
        interp_results = dict()
        for x_vals, y_vals, key, flag_step_func in self.x_y_key_flag_list:
            if key == '井斜角':
                interp_func = calculate_angle(x_vals, y_vals)
            else:
                interp_func = piecewise_linear_interp(x_vals, y_vals, flag_step_func)

            interp_result = interp_func(z)
            interp_results[key] = interp_result
        return interp_results


# %%


class ParamsReader(Singleton):
    """
    用户Excel数据读取器
    """

    def __init__(self, Params_info='./assets/Params.xlsx'):

        params_dict = {
            'value': {},
            'unit': {},
        }  # 储存所有页的 DataFrame 结果
        with pd.ExcelFile(Params_info) as excel_file:
            all_sheets = excel_file.sheet_names  # 获取所有页的名称

            for sheet_name in all_sheets:
                # 第1行是列名，第2行是单位
                df = pd.read_excel(excel_file, sheet_name, header=0)

                # 判断 "注释" 列是否存在
                if '注释' in df.columns:
                    # 存在则删除
                    df = df.drop(columns=['注释'])
                df.dropna(how='all', inplace=True)

                _unit = df.iloc[0, :].fillna('-')
                df = df.iloc[1:]

                params_dict['value'][sheet_name] = df
                params_dict['unit'][sheet_name] = _unit

        self.params_dict = params_dict
        self._data_unit_conversion()
        self._well_structure()

    def _well_structure(self):
        """根据测深升序部分表单的数据"""

        # TODO 后两者的测深都不能超过井斜数据的测深
        for key, df in self.params_dict['value'].items():
            if key not in ['井斜数据', '地温梯度', '油套管结构', '井下设备']:
                continue
            # 根据测深升序排序
            try:
                df.sort_values('测深', inplace=True)
                df.reset_index(drop=True, inplace=True)
            except Exception as e:
                print(key, e)
                pass

            self.params_dict['value'][key] = df

        # 为测深数据增加0点和补心海拔
        df = self.params_dict['value']['井斜数据']

        # kb 补心海拔
        kb = df['补心海拔'][df['补心海拔'].notna()].values

        df = df[['测深', '垂深']].copy()
        if df['测深'].iloc[0] > 0:
            # 在DataFrame的第0行（也就是表头的下面）插入一行数据
            df.loc[-1] = [0, 0]
            # 重置索引
            df.index = df.index + 1
            df = df.sort_index()

        df['垂深'] += kb
        self.params_dict['value']['井斜数据'] = df

    def _data_unit_conversion(self):
        """
        将用户输入的单位转化为标准单位
        Returns:

        """

        def convert_unit(params_dict, sheet, columns, target_unit_func, target_unit):
            params_value = params_dict['value']
            params_unit = params_dict['unit']

            # unit_func = eval('unit.%s' % (target_unit_func))
            # getattr()函数来获取unit对象中名称为target_unit_func的属性或方法，
            # 并将其赋值给unit_func变量。getattr()函数接受一个默认参数，
            # 即在属性或方法不存在时返回的默认值（这里设为None）
            unit_func = getattr(unit, target_unit_func, None)
            # 检查unit_func是否为可调用的函数或方法，以确保获取到正确的属性或方法
            if not (unit_func is not None and callable(unit_func)):
                raise Exception("target_unit_func: %s not found" % target_unit_func)

            for column in columns:
                try:
                    data = params_value[sheet][column]
                    origin_unit = params_unit[sheet][column]
                    convert_data = unit_func(data, origin_unit, target_unit)
                    params_value[sheet][column] = convert_data
                    params_unit[sheet][column] = target_unit
                except Exception:
                    pass

        params_dict = copy.deepcopy(self.params_dict)

        convert_unit(params_dict, '井斜数据', ['测深', '垂深', '补心海拔'], 'unit_length', 'm')
        convert_unit(params_dict, '地温梯度', ['测深'], 'unit_length', 'm')
        convert_unit(params_dict, '地温梯度', ['环境温度'], 'unit_temperature', 'K')
        convert_unit(
            params_dict, '油套管结构',
            ['测深', '油管内径', '管壁厚度', '管壁粗糙度', '套管内径', '套管外径', '水泥环外径'],
            'unit_length', 'm'
        )
        convert_unit(params_dict, '井下设备', ['测深'], 'unit_length', 'm')

        convert_unit(params_dict, '组分模型输入参数', ['摩尔分数'], 'unit_percentage', 'decimals')

        self.params_dict = params_dict

    def get_z_data_interp(self):
        """
        根据测深z对各类参数进行插值或外推

        根据 测深 计算：
            '垂深', '环境温度', '总传热系数U值', '油管内径', '管壁厚度', '管壁粗糙度',
            '套管内径', '套管外径', '套管导热系数', '水泥环外径', '水泥环导热系数'

            '井斜角' # 管线与水平方向的角度

        Returns:
            插值和外推函数，输入z测深，得到字典，每个键为外推函数的插值结果

        """

        x_y_key_flag_list = []
        x = None
        params_value = self.params_dict['value']
        for key, df in params_value.items():
            if key not in ['井斜数据', '地温梯度', '油套管结构', '井下设备']:
                continue
            for column_name, col_data in df.items():
                if column_name == '测深':
                    x = col_data.values.tolist()

                else:
                    yi = col_data.values.tolist()
                    if x == []:
                        continue

                    # 油套管结构的数据是阶梯函数
                    flag_step_func = False if key != '油套管结构' else True
                    result = (x, yi, column_name, flag_step_func)
                    x_y_key_flag_list.append(result)

        column_name = '井斜角'
        x = params_value['井斜数据']['测深']
        yi = params_value['井斜数据']['垂深']
        result = (x, yi, column_name, None)
        x_y_key_flag_list.append(result)

        interp_func = GetDataInterp(x_y_key_flag_list)

        # test_z_vals = range(0, 22)
        # for z in test_z_vals:
        #     interp_y = interp_func(z)
        #     print(f'z = {z:.2f}, y = {interp_y}')

        return interp_func


if __name__ == '__main__':
    params_reader = ParamsReader(manager_config.Params_info)
    params_dict = params_reader.params_dict
    params_value = params_dict['value']

    # 根据测深对各类参数进行插值和外推
    interp_func = params_reader.get_z_data_interp()

    z = 1200  # 计算深度 (m)
    params_value_z = interp_func(z)  # 测深为z时的其他值
    print(params_value_z)
