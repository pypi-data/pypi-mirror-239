#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time:   2023/4/27 14:28
# File:   black_oil_tools.py
# Author: He Ma
# Email:  1692303843@qq.com

import numpy as np
from scipy.optimize import curve_fit
import sympy
from mechanism.unit_conversion import unit_conversion as unit
from optimize import algorithm
from core.tool_expert import cached_function
from core.constants import lg, ln, exp


# %% Rs 溶解气油比
def _Rs_Lasater(P, T, rho_rg, rho_ro):
    """
    用Lasater公式计算溶解气油比Rs (m3/m3)
    建议用于API > 15º
    Args:
        P: 绝对压力 MPa
        T: 绝对温度T K
        rho_rg: 天然气的相对密度 无因次 小数
        rho_ro: 原油的相对密度 无因次 小数

    Returns:
        Rs: 溶解气油比 m3/m3
    """
    # 华氏温度
    theta = unit.unit_temperature(T, 'K', 'F')

    # 原油API重度
    D = unit.unit_API(rho_ro)

    # 地面脱气原油的有效分子量Mo g/mol
    if rho_ro <= 0.8251:
        Mo = 630 - 10 * D
    else:
        Mo = 73110 * D ** -1.562

    # 天然气的摩尔分数y
    _temp = P * rho_rg / (theta + 460)
    if _temp < 0.02269:
        yg = 0.359 * ln(_temp * 213.6 + 0.476)
    else:
        yg = (_temp * 17.546 - 0.236) ** 0.281

    # 天然气的溶解气油比Rs
    Rs = 24490.379 * rho_ro / Mo * (yg / (1 - yg))
    return Rs


def _Rs_Standing(P, T, rho_rg, rho_ro):
    """
    用Standing公式计算溶解气油比Rs (m3/m3)
    很有效适用于原油泡点压力及以下
    建议用于API < 15º
    Args:
        P: 绝对压力 MPa
        T: 绝对温度T K
        rho_rg: 天然气的相对密度 无因次 小数
        rho_ro: 原油的相对密度 无因次 小数

    Returns:
        Rs: 溶解气油比 m3/m3
    """
    # 华氏温度
    theta = unit.unit_temperature(T, 'K', 'F')

    # 原油API重度
    D = unit.unit_API(rho_ro)

    # 系数alpha
    alpha = 0.0125 * D - 0.00091 * theta

    # 天然气的溶解气油比Rs
    Rs = 2.277 * rho_rg * (P / 10 ** alpha) ** 1.204
    return Rs


def _Rs_Vazquez_Beggs(P, T, rho_rg, rho_ro, P_sep=0.791, T_sep=20 + 273.15):
    """
    用Vazquez&Beggs公式计算溶解气油比Rs (m3/m3)
    很有效适用于原油泡点压力及以下
    建议用于 16 < API < 58
    Args:
        P: 绝对压力 MPa
        T: 绝对温度 K
        rho_rg: 天然气的相对密度 无因次 小数
        rho_ro: 原油的相对密度 无因次 小数
        P_sep: 分离器操作压力（绝对） MPa
        T_sep: 分离器操作温度  K
    Returns:
        Rs: 溶解气油比 m3/m3
    """
    # 分离器操作温度下的华氏温度
    theta_sep = unit.unit_temperature(T_sep, 'K', 'F')

    # 原油API重度
    D = unit.unit_API(rho_ro)

    # 分离器基准压力(0.791MPa)下的气体相对密度rho_rg_sep
    rho_rg_sep = rho_rg * (1 + 5.912e-5 * D * theta_sep * lg(P_sep / 0.791))

    # 系数
    if rho_ro >= 0.8762:
        c1 = 0.0362
        c2 = 1.0937
        c3 = 25.724
    else:
        c1 = 0.0178
        c2 = 1.187
        c3 = 23.931

    # 天然气的溶解气油比Rs
    Rs = 0.1845 * c1 * rho_rg_sep * (145.03 * P) ** c2 * exp(c3 * D / (1.8 * T))
    return Rs


def _Rs_Glaso(P, T, rho_rg, rho_ro):
    """
    用Glaso公式计算溶解气油比Rs (m3/m3)
    适用范围: 不详
    Args:
        P: 绝对压力 MPa
        T: 绝对温度T K
        rho_rg: 天然气的相对密度 无因次 小数
        rho_ro: 原油的相对密度 无因次 小数
    Returns:
        Rs: 溶解气油比 m3/m3
    """
    # 分离器操作温度下的华氏温度
    theta = unit.unit_temperature(T, 'K', 'F')

    # 原油API重度
    D = unit.unit_API(rho_ro)

    # 天然气在原油中的溶解气油比P_star
    _temp = 2.8869 - (14.1811 - 3.3093 * lg(145.03 * P)) ** 0.5
    P_star = 10 ** (_temp)

    # 天然气的溶解气油比Rs
    Rs = rho_rg / 5.615 * ((D ** 0.989 / theta ** 0.172) * P_star) ** 1.2255
    return Rs


def _Rs_Marhoun(P, T, rho_rg, rho_ro):
    """
    用Marhoun公式计算溶解气油比Rs (m3/m3)
    适用范围: 不详
    Args:
        P: 绝对压力 MPa
        T: 绝对温度T K
        rho_rg: 天然气的相对密度 无因次 小数
        rho_ro: 原油的相对密度 无因次 小数
    Returns:
        Rs: 溶解气油比 m3/m3
    """
    a = 3598.5721
    b = 1.877840
    c = -3.1437
    d = -1.32657
    e = 1.398441

    # 天然气的溶解气油比Rs
    Rs = (a * rho_rg ** b * rho_ro ** c * T ** d * P) ** e
    return Rs


@cached_function
def f_Rs(P, T, Pb, rho_ro, rho_rg, method='Auto', P_sep=0.791, T_sep=20 + 273.15):
    """
    根据指定方法计算溶解气油比Rs (m3/m3)
    Lasater Standing Vazquez&Beggs Glaso Marhoun

    Args:
        Pb:
        P: 绝对压力 MPa
        T: 绝对温度T K
        rho_rg: 天然气的相对密度 无因次 小数
        rho_ro: 原油的相对密度 无因次 小数
        method: optional 选定计算方法 str None则自动根据根据API选择

        P_sep: optional 分离器操作压力（绝对） MPa
        T_sep: optional 分离器操作温度  K
    Returns:
        Rs: 溶解气油比 m3/m3
    """
    method_list = ['Auto', 'Lasater', 'Standing', 'Vazquez_Beggs', 'Glaso', 'Marhoun']
    if method == '-1':
        return method_list
    assert method in method_list, '该方法不存在'

    if P <= 0.1:
        # P = Pb
        Rs = 0
        return Rs
    if P > Pb:
        P = Pb

    # 原油API重度
    API = unit.unit_API(rho_ro)

    # 天然气的溶解气油比Rs
    if method == 'Auto':
        if API < 15:
            method = 'Standing'
        elif (16 < API < 58) and (P_sep is not None) and (T_sep is not None):
            method = 'Vazquez_Beggs'
        elif API > 15:
            method = 'Lasater'

    if method == 'Standing':
        Rs = _Rs_Standing(P, T, rho_rg, rho_ro)
    elif method == 'Vazquez_Beggs':
        Rs = _Rs_Vazquez_Beggs(P, T, rho_rg, rho_ro, P_sep, T_sep)
    elif method == 'Lasater':
        Rs = _Rs_Lasater(P, T, rho_rg, rho_ro)
    elif method == 'Glaso':
        Rs = _Rs_Glaso(P, T, rho_rg, rho_ro)
    elif method == 'Marhoun':
        Rs = _Rs_Marhoun(P, T, rho_rg, rho_ro)
    else:
        raise

    return Rs


# %% Bo 原油体积系数

def _Bob_Standing(Rs, T, rho_rg, rho_ro):
    """
    饱和原油体积系数 Bo (m3/m3)
        原油体积系数: 原油在地下的体积与其地面脱气后标准状况下体积的比值
    用Standing公式计算 饱和原油体积系数 , 含等于泡点压力的情况

    Args:
        Rs: 天然气在原油中的溶解气油比 m3/m3
        T: 绝对温度T K
        rho_rg: 天然气的相对密度 无因次 小数
        rho_ro: 原油的相对密度 无因次 小数

    Returns:
        Bob: 饱和原油体积系数 m3/m3
    """

    # 华氏温度
    theta = unit.unit_temperature(T, 'K', 'F')
    Bob = 0.9759 + 0.00012 * (5.615 * Rs * (rho_rg / rho_ro) ** 0.5 + 1.25 * theta) ** 1.2
    return Bob


def _Bob_Vasquez_Beggs(Rs, T, rho_rg, rho_ro, P_sep=0.791, T_sep=20 + 273.15):
    """
    饱和原油体积系数 Bo (m3/m3)
        原油体积系数: 原油在地下的体积与其地面脱气后标准状况下体积的比值
    用Vasquez_Beggs公式计算 饱和原油体积系数 , 含等于泡点压力的情况

    Args:
        Rs: 天然气在原油中的溶解气油比 m3/m3
        T: 绝对温度T K
        rho_rg: 天然气的相对密度 无因次 小数
        rho_ro: 原油的相对密度 无因次 小数
        P_sep: 分离器操作压力（绝对） MPa
        T_sep: 分离器操作温度  K
    Returns:
        Bob: 饱和原油体积系数 m3/m3
    """

    D = unit.unit_API(rho_ro)
    theta = unit.unit_temperature(T, 'K', 'F')
    theta_sep = unit.unit_temperature(T_sep, 'K', 'F')

    # 计算在分离器基准压力（0.791MPa）下的气体相对密度
    rho_rg_sep = rho_rg * (1 + 5.912e-5 * D * theta_sep * lg(P_sep / 0.791))

    # 系数
    if rho_ro >= 0.8762:
        c1 = 2.626e-3
        c2 = 1.751e-5
        c3 = -1.071e-7
    else:
        c1 = 2.626e-3
        c2 = 1.100e-5
        c3 = 7.507e-7

    Bob = 1 + c1 * Rs + (theta - 60) * (D / rho_rg_sep) * (c2 + c3 * Rs)
    return Bob


def _Bob_Glaso(Rs, T, rho_rg, rho_ro):
    """
    饱和原油体积系数 Bo (m3/m3)
        原油体积系数: 原油在地下的体积与其地面脱气后标准状况下体积的比值
    用Glaso公式计算 饱和原油体积系数 , 含等于泡点压力的情况

    Args:
        Rs: 天然气在原油中的溶解气油比 m3/m3
        T: 绝对温度 K
        rho_rg: 天然气的相对密度 无因次 小数
        rho_ro: 原油的相对密度 无因次 小数

    Returns:
        Bo: 饱和原油体积系数 m3/m3
    """

    theta = unit.unit_temperature(T, 'K', 'F')

    Bob_star = 5.615 * Rs * (rho_rg / rho_ro) ** 0.526 + 0.968 * theta
    A = -6.58511 + 2.91329 * lg(Bob_star) - 0.27683 * (lg(Bob_star)) ** 2

    Bob = 1 + 10 ** A
    return Bob


def _Bob_Marhoun(Rs, T, rho_rg, rho_ro):
    """
    饱和原油体积系数 Bo (m3/m3)
        原油体积系数: 原油在地下的体积与其地面脱气后标准状况下体积的比值
    用Marhoun公式计算 饱和原油体积系数 , 含等于泡点压力的情况

    Args:
        Rs: 天然气在原油中的溶解气油比 m3/m3
        T: 绝对温度 K
        rho_rg: 天然气的相对密度 无因次 小数
        rho_ro: 原油的相对密度 无因次 小数

    Returns:
        Bob: 饱和原油体积系数 m3/m3
    """
    a = 0.742390
    b = 0.323294
    c = -1.202040
    F = (5.615 * Rs) ** a * rho_rg ** b * rho_ro ** c

    Bob = 0.497069 + 1.5533334 * 1e-3 * T + 1.82594 * 1e-3 * F + 3.18099 * 1e-6 * F ** 2
    return Bob


def _Bob_Ahmed(Rs, P, T, rho_rg, rho_ro):
    """
    饱和原油体积系数 Bo (m3/m3)
    用Ahmed公式计算 饱和原油体积系数 , 含等于泡点压力的情况

    Returns:
        Bob: 饱和原油体积系数 m3/m3
    """

    theta = unit.unit_temperature(T, 'K', 'F')
    D = unit.unit_API(rho_ro)
    a1 = -4.5243937 * 1e-4
    a2 = 3.9063637 * 1e-6
    a3 = -5.5542509
    a4 = -5.7603220 * 1e-6
    a5 = -3.9528992 * 1e-9
    a6 = 16.289473
    a7 = 3.8718887 * 1e-4
    a8 = 7.070368 * 1e-8
    a9 = -1.4358395
    a10 = -0.128693
    a11 = 0.023484894
    a12 = 0.015966573
    a13 = 0.021946351

    F = a10 + (5.615 * Rs) ** a11 * D ** a12 / rho_rg ** a13
    Bob = F + a1 * theta + a2 * theta ** 2 + a3 * theta ** -1 + \
          a4 * (145.03 * P) + a5 * (145.03 * P) ** 2 + a6 * (145.03 * P) ** -1 + \
          a7 * (5.615 * Rs) + a8 * (5.615 * Rs) ** 2 + a9 * (5.615 * Rs) ** -1

    return Bob


@cached_function
def f_Bob(Rs, P, T, rho_rg, rho_ro, method='Standing', P_sep=0.791, T_sep=20 + 273.15):
    """
    根据指定方法计算 饱和原油体积系数 Bo (m3/m3), 含等于泡点压力的情况
        原油体积系数: 原油在地下的体积与其地面脱气后标准状况下体积的比值

    常用: Standing Vazquez&Beggs
    其他: Glaso Marhoun Ahmed

    Args:
        T: 绝对温度T K
        rho_rg: 天然气的相对密度 无因次 小数
        rho_ro: 原油的相对密度 无因次 小数
        method: optional 选定计算方法 str 默认Standing方法
        P_sep: optional 分离器操作压力  MPa
        T_sep: optional 分离器操作温度  K
    Returns:
        Bob: 饱和原油体积系数 m3/m3
    """
    method_list = ['Standing', 'Vazquez_Beggs', 'Glaso', 'Marhoun', 'Ahmed']
    if method == '-1':
        return method_list
    assert method in method_list, '该方法不存在'

    if method == 'Standing':
        Boi = _Bob_Standing(Rs, T, rho_rg, rho_ro)
    elif method == 'Vazquez_Beggs':
        Boi = _Bob_Vasquez_Beggs(Rs, T, rho_rg, rho_ro, P_sep, T_sep)
    elif method == 'Glaso':
        Boi = _Bob_Glaso(Rs, T, rho_rg, rho_ro)
    elif method == 'Marhoun':
        Boi = _Bob_Marhoun(Rs, T, rho_rg, rho_ro)
    elif method == 'Ahmed':
        Boi = _Bob_Ahmed(Rs, P, T, rho_rg, rho_ro)
    else:
        raise

    return Boi


def _Bo_Vasquez_Beggs(Bob, Rs, Pb, P, T, rho_rg, rho_ro, P_sep=0.791, T_sep=20 + 273.15):
    """
    不饱和原油体积系数 Bo (m3/m3)
        原油体积系数: 原油在地下的体积与其地面脱气后标准状况下体积的比值
    用Vasquez_Beggs公式计算 饱和原油体积系数 , 含等于泡点压力的情况

    Args:
        Bob: 饱和原油体积系数 m3/m3
        T: 绝对温度 K
        rho_rg: 天然气的相对密度 无因次 小数
        rho_ro: 原油的相对密度 无因次 小数
        P_sep: 分离器操作压力（绝对） MPa
        T_sep: 分离器操作温度  K
    Returns:
        Bo: 不饱和原油体积系数 m3/m3
    """

    D = unit.unit_API(rho_ro)
    theta = unit.unit_temperature(T, 'K', 'F')
    theta_sep = unit.unit_temperature(T_sep, 'K', 'F')

    rho_rg_sep = rho_rg * (1 + 5.912e-5 * D * theta_sep * lg(P_sep / 0.791))

    _temp = -1433 + 28.075 * Rs + 17.2 * theta - 1180 * rho_rg_sep + 12.61 * D
    A = 10 ** -5 * (_temp)

    Bo = Bob * exp(-A * ln(P / Pb))

    return Bo


def _Bo_Ahmed(Bob, Rs, Pb, P):
    """
    不饱和原油体积系数 Bo (m3/m3)
    用Ahmed公式计算 饱和原油体积系数 , 含等于泡点压力的情况

    """

    B = -(665.5392437 + 2.117285066 * Rs) ** -1
    a = -0.026791878

    Bo = Bob * exp(B * (exp(a * P) - exp(a * Pb)))

    return Bo


@cached_function
def f_Bo(P, T, Pb, Rs, rho_ro, rho_rg, method_dict=None, P_sep=0.791, T_sep=20 + 273.15):
    """
    根据指定方法计算 原油体积系数 Bo (m3/m3)
        原油体积系数: 原油在地下的体积与其地面脱气后标准状况下体积的比值

    常用: Standing Vazquez&Beggs
    其他: Glaso Marhoun Ahmed

    Args:
        Rs: 溶解气油比 m3/m3
        Pb: 泡点压力  MPa
        P: 压力  MPa
        T: 温度  K
        rho_rg: 天然气的相对密度 无因次 小数
        rho_ro: 原油的相对密度 无因次 小数
        method_dict: optional 选定计算方法 str

        P_sep: optional 分离器操作压力  MPa
        T_sep: optional 分离器操作温度  K

    Returns:
        Bo: 原油体积系数 m3/m3
    """

    # 'Vazquez_Beggs', method_Bob = 'Standing'
    if method_dict is None:
        method_dict = {
            '饱和原油体积系数': 'Standing',
            '不饱和原油体积系数': 'Vazquez_Beggs',
        }

    Bob = f_Bob(Rs, P, T, rho_rg, rho_ro, method_dict['饱和原油体积系数'], P_sep, T_sep)

    if P <= Pb:
        Bo = Bob
    else:
        if method_dict['不饱和原油体积系数'] == 'Vazquez_Beggs':
            Bo = _Bo_Vasquez_Beggs(Bob, Rs, Pb, P, T, rho_rg, rho_ro, P_sep, T_sep)
        elif method_dict['不饱和原油体积系数'] == 'Ahmed':
            Bo = _Bo_Ahmed(Bob, Rs, Pb, P)

    return Bo


# %% rhoo 原油密度
def _rhoo_saturated_Standing(T, Rs, rho_ro, rho_rg):
    """
    Standing 方法计算 饱和原油密度
    rhoo_unsaturated 方法原理:
        ρ_ob = 1000kg/cm3(水密度)γ_o + 1.205 Rs γ_g / 1
        ρ_ob = 水密度 * 油比重 + 空气密度 * 气体比重 / 校正系数(温度、气、液比重)
    """
    theta = unit.unit_temperature(T, 'K', 'F')

    _temp = 0.972 + 0.000147 * (5.615 * Rs * (rho_rg / rho_ro) ** 0.5 + 1.25 * theta) ** 1.175
    rhoo_b = (1000 * rho_ro + 1.205 * Rs * rho_rg) / (_temp)

    return rhoo_b


def _rhoo_unsaturated_Vazquez_Beggs(P, T, rhoo_b, Pb, Rs, rho_ro, rho_rg, P_sep=0.791, T_sep=20 + 273.15):
    """
    Vazquez_Beggs 方法计算 不饱和原油密度
    不饱和原油密度 方法原理:
        rho_o = rho_ob e^(C0(P-Pb))

    """
    theta = unit.unit_temperature(T, 'K', 'F')
    theta_sep = unit.unit_temperature(T_sep, 'K', 'F')
    D = unit.unit_API(rho_ro)

    # 分离器基准压力(0.791MPa)下的气体相对密度rho_rg_sep
    rho_rg_sep = rho_rg * (1 + 5.912e-5 * D * theta_sep * lg(P_sep / 0.791))

    A = 10 ** -5 * (-1433 + 28.075 * Rs + 17.2 * theta - 1180 * rho_rg_sep + 12.61 * D)
    rhoo = rhoo_b * exp(A * ln(P / Pb))
    return rhoo


@cached_function
def f_rhoo(P, T, Pb, Rs, rho_ro, rho_rg, method_dict=None, P_sep=0.791, T_sep=20 + 273.15):
    """
    原油密度 rhoo (kg/m3)
    不饱和
    Args:
        P: 压力 MPa
        T: 温度 K
        Pb: 泡点压力 MPa
        Rs: 溶解气油比 m3/m3
        rho_ro: 原油的相对密度 无因次 小数
        rho_rg: 天然气的相对密度 无因次 小数
        method_dict: dict
        P_sep: 分离器操作压力（绝对） MPa
        T_sep: 分离器操作温度  K

        # rhoo_b: 饱和原油密度 kg/m3
        # rhoo: 不饱和原油密度 kg/m3

    Returns:
        rhoo: 不饱和原油密度 kg/m3
    """

    if method_dict is None:
        method_dict = {
            '饱和原油密度计算方法': 'Standing',
            '不饱和原油密度计算方法': 'Vazquez_Beggs',
        }

    if method_dict['饱和原油密度计算方法'] == 'Standing':
        rhoo_b = _rhoo_saturated_Standing(T, Rs, rho_ro, rho_rg)

    if P > Pb:
        if method_dict['不饱和原油密度计算方法'] == 'Vazquez_Beggs':
            rhoo = _rhoo_unsaturated_Vazquez_Beggs(P, T, rhoo_b, Pb, Rs, rho_ro, rho_rg, P_sep, T_sep)
    else:
        rhoo = rhoo_b

    return rhoo


# %% muo 原油粘度

def _muo_degassed_Beggs_Robinson(T, rho_ro):
    """
    脱气原油粘度 Beggs and Robinson方法
    适用条件
        P（压力）：50~5250psia；
        T（温度）：70~295℉；
        gAPI（API重度）：16~58°API；
        Rsb（泡点压力下的溶解气）：20~2070scf/STB。

    Returns:
        muo_d
    """
    D = unit.unit_API(rho_ro)
    theta = unit.unit_temperature(T, 'K', 'F')

    z = 3.0324 - 0.02023 * D
    y = 10 ** z
    x = y * theta ** -1.163
    muo_d = 10 ** x - 1
    return muo_d


def _muo_degassed_Beggs_Glaso(T, rho_ro):
    """
    脱气原油粘度 Glaso方法
    适用条件
        P（压力）：50~5250psia；
        T（温度）：70~295℉；
        gAPI（API重度）：16~58°API；
        Rsb（泡点压力下的溶解气）：20~2070scf/STB。

    Returns:
        muo_d
    """
    D = unit.unit_API(rho_ro)
    theta = unit.unit_temperature(T, 'K', 'F')

    a = 10.313 * lg(theta) - 36.447
    muo_d = 3.141e10 * theta ** -3.44 * (lg(D)) ** a
    return muo_d


def _muo_saturated_Beggs_Robinson(muo_d, Rs):
    """
    饱和原油粘度 Beggs and Robinson方法 （设为默认值）
    适用条件：
        P=0.97~38.9 MPa
        T=22.2~146.1°C
        rho_ro=0.80~0.97
        Rs==24~1900
    """

    a = 10.715 * (5.615 * Rs + 100) ** -0.515
    b = 5.44 * (5.615 * Rs + 150) ** -0.338
    muo_b = a * (muo_d) ** b
    return muo_b


def _muo_unsaturated_Vazquez_Beggs(P, Pb, muo_b):
    """
    不饱和原油粘度 Vazquez and Beggs方法 （设为默认值）
    适用条件：
        P=0.97~65.6 MPa
        muo=0.117~148 mPa•s
        rho_ro=0.74~0.96
        rho_rg=0.511~1.351
        Rs=9.3~2198 m3/m3
    """
    a = -5.66 * 1e-3 * P - 5
    m = 956.4 * P ** 1.187 * 10 ** a

    muo = muo_b * (P / Pb) ** m
    return muo


def _muo_degassed_calibration(
        mode='单点', method='Beggs_Robinson', muo_d_prime_50C=None, rho_ro=None, T_list=[], muo_d_list=[]
):
    """
    用多点粘度校正方法计算脱气原油粘度

    Args:
        mode: str '单点' or '多点'
        '单点'
            muo_d_prime_50C: # 单点校正 50°C下实测脱气原油粘度
            rho_ro: 原油的相对密度 无因次

        '多点'
            T_list: 多点校正 输入两组或两组以上的不同温度下的脱气原油粘度值 len >=2
            muo_d_list: 多点校正 输入两组或两组以上的不同温度下的脱气原油粘度值 len >=2

    Returns:

    """

    def single_point(muo_d_prime_50C, muo_d_50C, rho_ro):
        def f_calibrate(T_calibrate):
            C1 = muo_d_prime_50C / muo_d_50C
            gamma_API = unit.unit_API(rho_ro)
            y = 10 ** (3.0321 - 0.02023 * gamma_API)
            x = y * (32 + 1.8 * T_calibrate) ** -1.163
            muo_d_calibrate = C1 * (10 ** x - 1)
            return muo_d_calibrate

        return f_calibrate

    def multi_point(x_list, y_list):
        assert len(x_list) == len(y_list), \
            '校正数据的输入输出需要相同长度, 输入:%s,输出:%s' % (len(x_list), len(y_list))

        def func(T, A, B):
            muo_d_calibrate = A * exp(B * T)
            return muo_d_calibrate

        popt, _pcov = curve_fit(func, x_list, y_list)

        def f_calibrate(T_calibrate):
            muo_d_calibrate = func(T_calibrate, *popt)
            return muo_d_calibrate

        return f_calibrate

    if mode == '单点':
        # 50°C下计算的脱气原油粘度
        muo_d_50C = _muo_degassed_Beggs_Robinson(T=50, rho_ro=rho_ro, method=method)
        f_muo_d_calibrate = single_point(muo_d_prime_50C, muo_d_50C, rho_ro)
    else:
        f_muo_d_calibrate = multi_point(T_list, muo_d_list)

    return f_muo_d_calibrate


def _f_muo_degassed(T, rho_ro, method='Beggs_Robinson'):
    """
    脱气原油粘度，其定义为在常压和系统（油藏）温度条件下的原油粘度
    Returns:
        muo_d 脱气原油粘度
    """
    method_list = ['Beggs_Robinson', 'Glaso']
    if method == '-1':
        return method_list
    assert method in method_list, '该方法不存在'

    if method == 'Beggs_Robinson':
        muo_d = _muo_degassed_Beggs_Robinson(T, rho_ro)
    elif method == 'Glaso':
        muo_d = _muo_degassed_Beggs_Glaso(T, rho_ro)

    return muo_d


def _f_muo_saturated(muo_d, Rs, method='Beggs_Robinson'):
    """
    饱和原油粘度，在泡点压力和油藏温度下的原油粘度

    """
    method_list = ['Beggs_Robinson']
    if method == '-1':
        return method_list
    assert method in method_list, '该方法不存在'

    if method == 'Beggs_Robinson':
        muo_b = _muo_saturated_Beggs_Robinson(muo_d, Rs)
    return muo_b


def _f_muo_unsaturated(P, Pb, muo_b, method='Vazquez_Beggs'):
    """
    不（非）饱和原油粘度，压力高于泡点压力和储层温度时的原油粘度

    """
    method_list = ['Vazquez_Beggs']
    if method == '-1':
        return method_list
    assert method in method_list, '该方法不存在'

    if method == 'Vazquez_Beggs':
        muo_d = _muo_unsaturated_Vazquez_Beggs(P, Pb, muo_b)
    return muo_d


@cached_function
def f_muo(P, T, Pb, Rs, rho_ro,
          method_dict=None,
          calibrate_dict=None,
          ):
    """
    原油粘度 mPa•s
    """

    if calibrate_dict is None:
        calibrate_dict = {
            'is_calibrate': False,
            'mode': '单点',
            '单点': {
                'method': 'Beggs_Robinson',
                'muo_d_prime_50C': None,
                'rho_ro': None,
            },
            '多点': {
                'T_list': [],
                'muo_d_list': [],
            },
        }

    if method_dict is None:
        method_dict = {
            '脱气原油粘度计算方法': 'Beggs_Robinson',
            '饱和原油粘度计算方法': 'Beggs_Robinson',
            '不饱和原油粘度计算方法': 'Vazquez_Beggs',
        }

    muo_d = _f_muo_degassed(T, rho_ro, method_dict['脱气原油粘度计算方法'])

    if calibrate_dict['is_calibrate']:
        f_muo_d_calibrate = _muo_degassed_calibration(mode=calibrate_dict['mode'],
                                                      method=calibrate_dict['单点']['method'],
                                                      muo_d_prime_50C=calibrate_dict['单点']['muo_d_prime_50C'],
                                                      rho_ro=calibrate_dict['单点']['rho_ro'],
                                                      T_list=calibrate_dict['多点']['T_list'],
                                                      muo_d_list=calibrate_dict['多点']['muo_d_list'])
        muo_d = f_muo_d_calibrate(T)

    muo_b = _f_muo_saturated(muo_d, Rs, method_dict['饱和原油粘度计算方法'])

    if P > Pb:
        muo = _f_muo_unsaturated(P, Pb, muo_b, method_dict['不饱和原油粘度计算方法'])
    else:
        muo = muo_b

    return muo


# %% rhow 水相密度
@cached_function
def f_rhow(rho_rw):
    """
    水相的密度
    """
    rhow = rho_rw * 1000
    return rhow


# %% muw 水相粘度


def _muw_Bill_Beggs(T):
    """
    Bill_Beggs 方法计算 油田 水的粘度 (mPa•s)
    """
    # 华氏温度
    theta = unit.unit_temperature(T, 'K', 'F')
    muw = exp(1.003 - 1.479 * 1e-2 * theta + 1.982 * 1e-5 * theta ** 2)

    return muw


@cached_function
def f_muw(T):
    """
    水相粘度 (mPa•s)
    """
    muw = _muw_Bill_Beggs(T)
    return muw


# %% rhol 液相密度
@cached_function
def f_rhol(rhoo, rhow, fw):
    """
    油水混合物密度 (kg/m3)
    体积含水率方法

    """

    rhol = fw * rhow + (1 - fw) * rhoo
    return rhol


# %% mul 液相粘度
@cached_function
def f_mul(muo, muw, fw, f0=0.45):
    """
    油水混合物粘度 (mPa•s)
    计算复杂
        采用近似法
    f0: fw影响mul突变的阈值
    其他方法采用了 水的体积含量Vw 此处不知道如何获取 不知道Vw 与 fw 的关系(%)
    """

    # 含水低于设定值时，认为混合物粘度等于油粘度
    # 含水高于设定值时，认为混合物粘度等于水粘度。
    if fw >= f0:
        mul = muw
    else:
        mul = muo
    return mul


# %% rhog 天然气密度
@cached_function
def f_rhog(P, T, rho_rg, Z):
    """
    rhog 天然气的密度 (kg/m3)

    rhoa: 标况空气密度 1.29Kg/m3
    rhoa * T_sc / P_sc = 1.29Kg/m3 * 273K * 0.101MPa = 3484.4
    """

    rhog = 3484.4 * rho_rg * P / (Z * T)

    return rhog


# %% mug 天然气的粘度

def _mug_Lee_Gonzalez_Eakin(T, Mg, rhog):
    """
    Lee_Gonzalez_Eakin 方法计算 天然气的粘度 (mPa•s)

    Mg 天然气的平均分子质量 (g/mol)
    rhog 天然气的密度 (kg/m3)
    # 这个可能有问题 指数太大了 rhog 在大气压时0.6, 30MPa则上百 不推荐使用
    """

    K = (9.4 + 0.02 * Mg) * 1.8 * T ** 1.5 / (209 + 19 * Mg + 1.8 * T)
    x = 3.5 + 986 / (1.8 * T) + 0.01 * Mg
    y = 2.4 - 0.2 * x

    mug = 1e-4 * K * exp(x * (1000 * rhog) ** y)

    return mug


def _mug_Dempsey(P, T, Ppc, Tpc, rho_rg):
    """
    Dempsey 方法计算 天然气的粘度 (mPa•s)

    Ppc 天然气的拟临界压力 (MPa)
    Tpc 天然气的拟临界温度 (K)

    rho_rg 天然气的相对密度 (无因次-小数)

    中间变量:
    Ppr: 拟对比力 (MPa)
    Tpr: 拟对比温度 (K)
    """
    # 拟对比压力
    Ppr = P / Ppc
    # 拟对比温度
    Tpr = T / Tpc

    # 计算在 0.101 MPa 和给定温度下的天然气的粘度

    mug_1 = (1.709 * 1e-5 - 2.062 * 1e-6 * rho_rg) * (1.8 * T - 460) + \
            8.188 * 1e-3 - 6.15 * 1e-3 * lg(rho_rg)

    a0 = -2.46211820
    a1 = 2.97054714
    a2 = -2.86264054 * 1e-1
    a3 = 8.05420522 * 1e-3
    a4 = 2.80860949
    a5 = -3.49803305
    a6 = 3.60373020 * 1e-1
    a7 = -1.044324 * 1e-2
    a8 = -7.93385684 * 1e-1
    a9 = 1.39643306
    a10 = -1.49144925 * 1e-1
    a11 = 4.41015512 * 1e-3
    a12 = 8.3938178 * 1e-2
    a13 = -1.86408848 * 1e-1
    a14 = 2.03367881 * 1e-2
    a15 = -6.09579263 * 1e-4

    # _temp: ln(mug / mu1 * Tpr)
    _temp = a0 + a1 * Ppr + a2 * Ppr ** 2 + a3 * Ppr ** 3 + Tpr * (
            a4 + a5 * Ppr + a6 * Ppr ** 2 + a7 * Ppr ** 3) + Tpr ** 2 * (
                    a8 + a9 * Ppr + a10 * Ppr ** 2 + a11 * Ppr ** 3) + Tpr ** 3 * (
                    a12 + a13 * Ppr + a14 * Ppr ** 2 + a15 * Ppr ** 3)

    mug = mug_1 * exp(_temp) / Tpr

    return mug


@cached_function
def f_mug(P, T, Ppc, Tpc, rho_rg):
    """
    天然气的粘度 (mPa•s)

    Ppc 天然气的拟临界压力 (MPa)
    Tpc 天然气的拟临界温度 (K)

    rho_rg 天然气的相对密度 (无因次-小数)

    中间变量:
    Ppr: 拟对比力 (MPa)
    Tpr: 拟对比温度 (K)
    """

    mug = _mug_Dempsey(P, T, Ppc, Tpc, rho_rg)
    return mug


# %% sigmao 原油-天然气的表面张力

@cached_function
def f_sigmao(P, T, rho_ro):
    """
    计算 σ_o 原油-天然气的表面张力 mN/m
    Args:
        P: 压力 MPa
        T: 温度 K
        rho_ro: 原油的相对密度 无因次 小数

    Returns:
        sigmao: 原油-天然气的表面张力 mN/m

    """
    if P < 0:
        raise Exception(f'！异常压力负数 {P}')
    D = unit.unit_API(rho_ro)
    theta = unit.unit_temperature(T, 'K', 'F')
    sigmao = (42.4 - 0.047 * theta - 0.267 * D) * exp(-0.101521 * P)

    return sigmao


# %% sigmaw 气-水表表面张力

def _f_sigmaw_Lee_Gonzalez_Eakin(P, T):
    """
    气-水表面张力 σ_w 是指作用在气-水界面单位表面积上的表面能 (mN/m)
    T 温度 (K)  这里输入K，使用时将转为摄氏度

    """
    T_degree = unit.unit_temperature(T, 'K', 'C')

    # 计算温度为23.33 摄氏度时水的表面张力
    sigmaw_23point33 = 76 * exp(-0.0362575 * P)
    # 计算温度为137.78 摄氏度时水的表面张力
    sigmaw_137point78 = 52.5 - 0.87018 * P
    # 3.2计算温度为T摄氏度时水的表面张力, T的单位是K, 文档中这么写的
    sigmaw = (137.78 - T_degree) * 1.8 / 206 * (sigmaw_23point33 - sigmaw_137point78) + sigmaw_137point78

    return sigmaw


@cached_function
def f_sigmaw(P, T):
    """
    气-水表面张力 σ_w 是指作用在气-水界面单位表面积上的表面能 (mN/m)
    T 温度 (K)  这里输入K，使用时将转为摄氏度
    """
    sigmaw = _f_sigmaw_Lee_Gonzalez_Eakin(P, T)
    return sigmaw


# %% sigmal 液相的表面张力

@cached_function
def f_sigmal(sigmao, sigmaw, fw):
    """
    油水混合液表面张力 (mN/m)
    """
    sigmal = (1 - fw) * sigmao + fw * sigmaw
    return sigmal


# %% Mg 天然气的平均分子量

@cached_function
def f_Mg(rho_rg):
    """
    Mg 天然气的平均分子量 (无因次)
    """
    Mg = 28.96 * rho_rg
    return Mg


# %% Ppc_Tpc 天然气的拟临界参数

@cached_function
def f_pseudo_critical_gas(rho_rg, is_condensate=False):
    """
    Ppc 天然气的拟临界压力 (MPa)
    Tpc 天然气的拟临界温度 (K)

    pc: pseudo_critical

    由于天然气为多组分气体，工程上采用拟临界参数的概念，主要是指拟临界参数 Tpc 和拟临界压力 Ppc ,
    常用于天然气的偏差系数的计算，已知条件不同，其计算的方法不同。

    P: 气体的绝对压力 MPa
    is_condensate: 是否为凝析气
    """

    # 干气
    if not is_condensate:
        Ppc = 4.67 + 0.10 * rho_rg - 0.26 * rho_rg ** 2
        Tpc = 93.3 + 180.6 * rho_rg - 6.9 * rho_rg ** 2

    # 凝析气干气
    else:
        Ppc = 4.67 - 0.36 * rho_rg - 0.08 * rho_rg ** 2
        Tpc = 103.9 + 183.3 * rho_rg - 39.7 * rho_rg ** 2

    return Ppc, Tpc


@cached_function
def f_pseudo_critical_gas_calibration(Ppc, Tpc, yH2S, yCO2, B):
    """
    FIXME 这个关系式有问题，B=64.065，则B ** 4过小，校正的PT均异常

    Wichert_Aziz 方法
    天然气中 H2S 和 CO2 含量较高，使用standing-Katz的 Z=f(Ppr, Tpr) 图或表,
    在使用干气和凝析气计算临界参数时， 应对 Ppc Tpc 进行非烃校正

    Ppc_prime: 计算校正后的拟临界压力 (小数)
    Tpc_prime: 计算校正后的拟临界温度 (小数)

    Ppc 天然气的拟临界压力 (MPa)
    Tpc 天然气的拟临界温度 (K)
    yH2S: 天然气中 H2S 的摩尔分数 (小数)
    yCO2: 天然气中 CO2 的摩尔分数 (小数)
    B: 天然气中 H2S 的摩尔数 (小数)
    """

    # 拟临界温度校正系数ε
    A = yH2S + yCO2

    epsilon = (120 * (A ** 0.9 - A ** 1.6) + 15 * (B ** 0.5 - B ** 4)) / 1.8
    Tpc_prime = Tpc - epsilon
    Ppc_prime = Ppc * Tpc / (Tpc + B * (1 - B) * epsilon)

    return Ppc_prime, Tpc_prime


# %% Z 天然气的偏差系数

def _Z_Cranmer(P, T, Ppc, Tpc, Z):
    """
    Cranmer 方法计算 天然气的偏差系数、压缩因子 (m3/m3)
    该方法适合于压力 P < 35MPa 的情况
    牛顿迭代法 计算
    偏差系数的定义 Z = Va / Vi
        Va 实际气体的体积 (m3)
        Vi 在同一状态下等质量理想气体体积 (m3)


    Ppc 天然气的拟临界压力 (MPa)
    Tpc 天然气的拟临界温度 (K)
    Z 天然气的拟临界参数 (m3/m3)

    中间变量:
    Ppr: 拟对比力 (MPa)
    Tpr: 拟对比温度 (K)
    rhopr: 拟对比密度 (kg/m3)

    """

    Ppr = P / Ppc
    Tpr = T / Tpc
    rhopr = 0.27 * Ppr / (Z * Tpr)

    a = 0.31506 - 1.04677 / Tpr - 0.5783 / Tpr ** 3
    b = 0.5353 - 0.6123 / Tpr
    c = 0.6815

    Z = 1 + a * rhopr + b * rhopr ** 2 + c * rhopr ** 2 / Tpr ** 3

    return Z


@cached_function
def f_Z(P, T, Ppc, Tpc, Z_init):
    """
    天然气的偏差系数、压缩因子 (m3/m3)
    牛顿迭代法 计算
    偏差系数的定义 Z = Va / Vi
        Va 实际气体的体积 (m3)
        Vi 在同一状态下等质量理想气体体积 (m3)

    Ppc 天然气的拟临界压力 (MPa)
    Tpc 天然气的拟临界温度 (K)
    Z_init 天然气的拟临界参数 迭代前的猜测值 (m3/m3)

    调用函数的中间变量:
        Ppr: 拟对比力 (MPa)
        Tpr: 拟对比温度 (K)
        rhopr: 拟对比密度 (kg/m3)

    """

    Z_Symbol = sympy.Symbol('Z')
    f = _Z_Cranmer(P, T, Ppc, Tpc, Z_Symbol) - Z_Symbol
    # print(f)
    x0 = Z_init
    x_root = algorithm.root_Newton(f, x0, symbol=Z_Symbol)
    # print('所求方程式的根为:', x_root)
    Z_new = round(x_root, 3)
    return Z_new


# %% Co 不饱和原油的等温压缩系数

@cached_function
def f_Co(T, Rsb, rho_ro, rho_rg, P_sep=0.791, T_sep=20 + 273.15):
    """

    计算 Co 不饱和原油的等温压缩系数 MPa^-1

    Args:
        T:
        Rsb: 在泡点压力时天然气在原油中的溶解气油比 m3/m3
        rho_ro:
        rho_rg:
        P_sep:
        T_sep:

    Returns:

    """

    D = unit.unit_API(rho_ro)
    theta = unit.unit_temperature(T, 'K', 'F')
    theta_sep = unit.unit_temperature(T_sep, 'K', 'F')

    rho_rg_sep = rho_rg * (1 + 5.912e-5 * D * theta_sep * lg(P_sep / 0.791))

    Co = -1433 + 28.075 * Rsb + 17.2 * theta - 1180 * rho_rg_sep + 12.61 * D

    return Co


# %% Cg 天然气的等温压缩系数

@cached_function
def f_Cg(P, T, Ppc, Tpc):
    """
    天然气的等温压缩系数 (1/MPa)
    Gopal
    """

    MATRIX_ABCD = np.array([
        [1.6643, -2.2114, -0.3647, 1.4385],
        [0.5222, -0.8511, -0.03647, 1.0490],
        [0.1391, -0.2988, 0.0007, 0.9969],
        [0.0295, -0.0825, 0.0009, 0.9967],
        [-1.3570, 1.4942, 4.6315, -4.7009],
        [0.1711, -0.3232, 0.5869, 0.1229],
        [0.0984, -0.2053, 0.0621, 0.8580],
        [0.0211, -0.0527, 0.0127, 0.9549],
        [-0.3278, 0.4752, 1.8223, -1.9036],
        [-0.2521, 0.3871, 1.6087, -1.6635],
        [-0.0284, 0.0625, 0.4714, -0.0011],
        [0.0041, 0.0039, 0.0607, 0.7927],
        [0.711, 3.66, -1.637, 2.071]
    ])

    Ppr = P / Ppc
    Tpr = T / Tpc

    if Ppr <= 1.2:  # 0.2-1.2
        i = 0
    elif Ppr <= 2.8:
        i = 1
    elif Ppr <= 5.4:
        i = 2
    else:  # 5.4-15.0
        i = 3

    if i == 3:
        A, B, C, D = MATRIX_ABCD[-1, :]
    else:
        if Tpr <= 1.2:  # 1.05-1.2
            A, B, C, D = MATRIX_ABCD[4 * i + 0, :]
        elif Tpr <= 1.4:
            A, B, C, D = MATRIX_ABCD[4 * i + 1, :]
        elif Tpr <= 2:
            A, B, C, D = MATRIX_ABCD[4 * i + 2, :]
        else:  # 5.4-15.0
            A, B, C, D = MATRIX_ABCD[4 * i + 3, :]

    _temp1 = A * Tpr + B
    _temp2 = Ppr * (A * Tpr + B) + C * Tpr + D
    _temp = _temp1 / _temp2
    Cg = 1 / Ppc * (1 / Ppr - _temp)

    # 保证Cg为正数
    Cg = max(Cg, 0)

    return Cg


# %% Cpo Cpg Cpw Cpo_wax 油气水比热 校正的原油比热
@cached_function
def f_Cpo(T=None, rhoo_15=None):
    """
    原油的比热 (KJ/(kg•K))

    1 kcal/(kg•C) = 4.1868 KJ/(kg•K) = 4.1868 KJ/(kg•C)
    克莱格公式
    适用条件: 0<=T<=400 °C 720<=rhoo<=920 kg/m3

    Args:
        T: 温度 (K)
        rhoo_15: 15摄氏度时原油的密度 (kg/m3)

    Returns:
        Cpo: 原油的比热 (KJ/(kg•K))
    """
    if T is None:
        Cpo = unit.unit_C_specific_heat(0.47, u_in='kcal/(kg•C)', u_to='KJ/(kg•K)')
    else:
        T_degree = unit.unit_temperature(T, 'K', 'C')

        # rhoo_15 / 1000 计算相对密度
        Cpo = 1 / (rhoo_15 / 1000) ** 0.5 * (0.403 + 0.00081 * T_degree)  # kcal/(kg•C)
        Cpo = unit.unit_C_specific_heat(Cpo, 'kcal/(kg•C)', 'KJ/(kg•K)')

    return Cpo


@cached_function
def f_Cpw(T):
    """
    水的比热 (KJ/(kg•K))
    Args:
        T: 温度 (K)

    Returns:
        Cpw: 水的比热 (KJ/(kg•K))
    """
    # (J/(kg•K))
    Cpw = 0.0143 * T ** 2 - 9.1549 * T + 5643.8
    Cpw = unit.unit_C_specific_heat(Cpw, u_in='J/(kg•K)', u_to='KJ/(kg•K)')

    return Cpw


@cached_function
def f_Cpg(T=None):
    """
    气体的比热 (KJ/(kg•K))

    适用条件: 273 < T < 1500 K
    由于天然气的组分以CH4和C2H6为主，各油田变化不大，而且随温度变化很小，
    因此可以在更大的范围内取做常数 0.5 kcal/(kg•C)

    Args:
        T: 温度 (K)

    Returns:
        Cpg: 气体的比热 (KJ/(kg•K))
    """
    if T is None:
        Cpg = unit.unit_C_specific_heat(0.5, u_in='kcal/(kg•C)', u_to='KJ/(kg•K)')
    else:
        Cpg = 1243 + 3.14 * T + 7.931 * 1e-4 * T ** 2 - 6.881 * 1e-7 * T ** 3  # (KJ/(kg•K))
        Cpg = unit.unit_C_specific_heat(Cpg, u_in='J/(kg•K)', u_to='KJ/(kg•K)')

    return Cpg


@cached_function
def f_Cpo_wax(T):
    """
    含蜡原油经验公式估算
    1 kcal/(kg•C) = 4.1868 KJ/(kg•K) = 4.1868 KJ/(kg•C)

    TODO 文档方法不详细

    Args:
        T: 温度 (K)

    Returns:
        Cpg: 气体的比热 (KJ/(kg•K))

    """
    T = unit.unit_temperature(T, 'K', 'C')

    # kcal/(kg•C)
    if 0 <= T <= 20:
        m = 0.0156
        B = 0.416  # kcal/kg
        Cpo_wax = 1 - B * exp(-m * T)
    # elif 20 < T <= 47.5:
    #     # 此处不详细
    else:
        Cpo_wax = 0.505

    Cpo_wax = unit.unit_C_specific_heat(Cpo_wax, 'kcal/(kg•C)', 'KJ/(kg•K)')

    return Cpo_wax

# %% 函数向量化

# f_Rs = np.vectorize(f_Rs)
# f_Rs = np.vectorize(f_Rs)
# f_Bo = np.vectorize(f_Bo)
# f_rhoo = np.vectorize(f_rhoo)
# f_rhow = np.vectorize(f_rhow)
# f_rhol = np.vectorize(f_rhol)
# f_rhog = np.vectorize(f_rhog)
# f_muo = np.vectorize(f_muo)
# f_muw = np.vectorize(f_muw)
# f_mul = np.vectorize(f_mul)
# f_mug = np.vectorize(f_mug)
# f_sigmao = np.vectorize(f_sigmao)
# f_sigmaw = np.vectorize(f_sigmaw)
# f_sigmal = np.vectorize(f_sigmal)
# f_Mg = np.vectorize(f_Mg)
# f_pseudo_critical_gas = np.vectorize(f_pseudo_critical_gas)
# f_pseudo_critical_gas_calibration = np.vectorize(f_pseudo_critical_gas_calibration)
# f_Z = np.vectorize(f_Z)
# f_Co = np.vectorize(f_Co)
# f_Cg = np.vectorize(f_Cg)
# f_rhoo = np.vectorize(f_rhoo)
# f_Cpo = np.vectorize(f_Cpo)
# f_Cpo_wax = np.vectorize(f_Cpo_wax)
# f_Cpw = np.vectorize(f_Cpw)
# f_Cpg = np.vectorize(f_Cpg)
