#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time:   2023/4/27 14:34
# File:   unit_conversion.py
# Author: He Ma
# Email:  1692303843@qq.com
# func: 单位转换
import numpy


# from mechanism.unit_conversion import unit_conversion as unit


# %% 基本单位换算


# def _unit_angle(angle, u_in='deg', u_to='rad'):
#     # numpy.deg2rad()
#     # numpy.rad2deg()
#     # * pi / 180
#     """温度转换"""
#     u_list = ['deg', 'rad']
#     assert u_in in u_list, 'u_in: %s 不是标准单位 %s' % (u_in, u_list)
#     assert u_to in u_list, 'u_to: %s 不是标准单位 %s' % (u_to, u_list)
#     angle_stand = None
#     angle_u_to = None
#     # 从输入任意转为标准K
#     if u_in == 'deg':
#         angle_stand = angle
#     elif u_in == 'rad':
#         angle_stand = angle * 180 / 3.1415
#
#     # 从标准K转为任意输出
#     if u_to == 'deg':
#         # 温度华氏度
#         angle_u_to = angle_stand
#     elif u_to == 'rad':
#         # 温度华氏度
#         angle_u_to = angle_stand * 3.1415 / 180
#
#     return angle_u_to


def unit_percentage(decimals, u_in='%', u_to='decimals'):
    """长度转换"""
    u_list = ['decimals', '%']
    assert u_in in u_list, 'u_in: %s 不是标准单位 %s' % (u_in, u_list)
    assert u_to in u_list, 'u_to: %s 不是标准单位 %s' % (u_to, u_list)
    decimals_stand = None
    decimals_u_to = None
    # 从输入任意转为标准
    if u_in == 'decimals':
        decimals_stand = decimals
    elif u_in == '%':
        decimals_stand = decimals / 100

    # 从标准转为任意输出
    if u_to == 'decimals':
        decimals_u_to = decimals_stand
    elif u_to == '%':
        decimals_u_to = decimals_stand * 100

    return decimals_u_to


def unit_length(length, u_in='in', u_to='m'):
    """长度转换"""
    u_list = ['m', 'km', 'cm', 'mm', 'in', 'mile', 'ft']
    assert u_in in u_list, 'u_in: %s 不是标准单位 %s' % (u_in, u_list)
    assert u_to in u_list, 'u_to: %s 不是标准单位 %s' % (u_to, u_list)
    length_stand = None
    length_u_to = None
    # 从输入任意转为标准
    if u_in == 'm':
        length_stand = length
    elif u_in == 'km':
        length_stand = length / 0.001
    elif u_in == 'cm':
        length_stand = length / 100
    elif u_in == 'mm':
        length_stand = length / 1000
    elif u_in == 'in':
        length_stand = length / 39.3700787
    elif u_in == 'mile':
        length_stand = length / 0.0006214
    elif u_in == 'ft':
        length_stand = length / 3.2808399

    # 从标准转为任意输出
    if u_to == 'm':
        length_u_to = length_stand
    elif u_to == 'km':
        length_u_to = length_stand * 0.001
    elif u_to == 'cm':
        length_u_to = length_stand * 100
    elif u_to == 'mm':
        length_u_to = length_stand * 1000
    elif u_to == 'in':
        length_u_to = length_stand * 39.3700787
    elif u_to == 'mile':
        length_u_to = length_stand * 0.0006214
    elif u_to == 'ft':
        length_u_to = length_stand * 3.2808399

    return length_u_to


def unit_temperature(T, u_in='C', u_to='K'):
    """温度转换"""
    u_list = ['K', 'C', 'F', 'R']
    assert u_in in u_list, 'u_in: %s 不是标准单位 %s' % (u_in, u_list)
    assert u_to in u_list, 'u_to: %s 不是标准单位 %s' % (u_to, u_list)
    T_stand = None
    T_u_to = None
    # 从输入任意转为标准K
    if u_in == 'K':
        T_stand = T
    elif u_in == 'C':
        T_stand = T + 273.15
    elif u_in == 'F':
        T_stand = (T + 459.67) / 1.8
    elif u_in == 'R':
        T_stand = T / 1.8

    # 从标准K转为任意输出
    if u_to == 'K':
        T_u_to = T_stand
    elif u_to == 'C':
        T_u_to = T_stand - 273.15
    elif u_to == 'F':
        T_u_to = T_stand * 1.8 - 459.67
    elif u_to == 'R':
        T_u_to = T_stand * 1.8

    return T_u_to


def unit_pressure(P, u_in='MPa', u_to='Pa'):
    """
    压力转换

    """
    u_list = ['Pa', 'MPa', 'KPa', 'atm', 'bar', 'psi', 'mmH2O']
    assert u_in in u_list, 'u_in: %s 不是标准单位 %s' % (u_in, u_list)
    assert u_to in u_list, 'u_to: %s 不是标准单位 %s' % (u_to, u_list)
    P_stand = None
    P_u_to = None
    # 从输入任意转为标准
    if u_in == 'Pa':
        P_stand = P
    elif u_in == 'MPa':
        P_stand = P * 1e6
    elif u_in == 'KPa':
        P_stand = P * 1e3
    elif u_in == 'atm':
        P_stand = P * 101325
    elif u_in == 'bar':
        P_stand = P * 100000
    elif u_in == 'psi':
        P_stand = P * 6894.757
    elif u_in == 'mmH2O':
        P_stand = P * 9.8066136

    # 从标准转为任意输出
    if u_to == 'Pa':
        P_u_to = P_stand
    elif u_to == 'MPa':
        P_u_to = P_stand / 1e6
    elif u_to == 'KPa':
        P_u_to = P_stand / 1e3
    elif u_to == 'atm':
        P_u_to = P_stand / 101325
    elif u_to == 'bar':
        P_u_to = P_stand / 100000
    elif u_to == 'psi':
        P_u_to = P_stand / 6894.757
    elif u_to == 'mmH2O':
        P_u_to = P_stand / 9.8066136

    return P_u_to


def unit_API(API, u_in='gamma_non_dim', u_to='Degree'):
    """
    原油API重度
    Degree: API(°)
    gamma_non_dim: 相对密度 油在60°F的比重 无因次 γ: gamma
    """
    u_list = ['Degree', 'gamma_non_dim']
    assert u_in in u_list, 'u_in: %s 不是标准单位 %s' % (u_in, u_list)
    assert u_to in u_list, 'u_to: %s 不是标准单位 %s' % (u_to, u_list)
    API_stand = None
    API_u_to = None
    # 从输入任意转为标准
    if u_in == 'Degree':
        API_stand = API
    elif u_in == 'gamma_non_dim':
        API_stand = (141.5 / API) - 131.5

    # 从标准转为任意输出
    if u_to == 'Degree':
        API_u_to = API_stand
    elif u_to == 'gamma_non_dim':
        API_u_to = 141.5 / (API_stand + 131.5)

    return API_u_to


def unit_mu(mu, u_in='mPa•s', u_to='Pa•s'):
    """
    动力粘度单位换算
    """
    u_list = ['Pa•s', 'mPa•s', 'cp']
    assert u_in in u_list, 'u_in: %s 不是标准单位 %s' % (u_in, u_list)
    assert u_to in u_list, 'u_to: %s 不是标准单位 %s' % (u_to, u_list)
    mu_stand = None
    mu_u_to = None
    # 从输入任意转为标准
    if u_in == 'Pa•s':
        mu_stand = mu
    elif u_in == 'mPa•s':
        mu_stand = mu / 1000
    elif u_in == 'cp':
        mu_stand = mu / 1000

    # 从标准转为任意输出
    if u_to == 'Pa•s':
        mu_u_to = mu_stand
    elif u_to == 'mPa•s':
        mu_u_to = mu_stand * 1000
    elif u_to == 'cp':
        mu_u_to = mu_stand * 1000

    return mu_u_to


def unit_C_specific_heat(C, u_in='kcal/(kg•C)', u_to='KJ/(kg•K)'):
    """
    原油API重度
    Degree: API(°)
    gamma_non_dim: 相对密度 油在60°F的比重 无因次 γ: gamma

    1 kcal/(kg•C) = 4.1868 KJ/(kg•K) = 4.1868 KJ/(kg•C) = 4186.8 J/(kg•C)


    """
    u_list = ['kcal/(kg•C)', 'KJ/(kg•C)', 'KJ/(kg•K)', 'J/(kg•C)', 'J/(kg•K)']
    assert u_in in u_list, 'u_in: %s 不是标准单位 %s' % (u_in, u_list)
    assert u_to in u_list, 'u_to: %s 不是标准单位 %s' % (u_to, u_list)
    C_stand = None
    C_u_to = None
    # 从输入任意转为标准
    if u_in == 'kcal/(kg•C)':
        C_stand = C
    elif (u_in == 'KJ/(kg•C)') or (u_in == 'KJ/(kg•K)'):
        C_stand = C / 4.1868
    elif (u_in == 'J/(kg•C)') or (u_in == 'J/(kg•K)'):
        C_stand = C / 4.1868 / 1000

    # 从标准转为任意输出
    if u_to == 'kcal/(kg•C)':
        C_u_to = C_stand
    elif (u_to == 'KJ/(kg•C)') or (u_to == 'KJ/(kg•K)'):
        C_u_to = C_stand * 4.1868
    elif (u_to == 'J/(kg•C)') or (u_to == 'J/(kg•K)'):
        C_u_to = C_stand * 4.1868 * 1000

    return C_u_to


# %% 复合单位换算

def unit_q_volume_rate(q, u_in='m3/s', u_to='m3/d'):
    """
    体积流量转换

    """
    u_list = ['m3/s', 'm3/d']
    assert u_in in u_list, 'u_in: %s 不是标准单位 %s' % (u_in, u_list)
    assert u_to in u_list, 'u_to: %s 不是标准单位 %s' % (u_to, u_list)
    q_stand = None
    q_u_to = None
    # 从输入任意转为标准
    if u_in == 'm3/s':
        q_stand = q
    elif u_in == 'm3/d':
        q_stand = q / 86400

    # 从标准转为任意输出
    if u_to == 'm3/s':
        q_u_to = q_stand
    elif u_to == 'm3/d':
        q_u_to = q_stand * 86400

    return q_u_to


def unit_sigma(sigma, u_in='mN/m', u_to='N/m'):
    """
    气液的表面张力

    """
    u_list = ['N/m', 'mN/m']
    assert u_in in u_list, 'u_in: %s 不是标准单位 %s' % (u_in, u_list)
    assert u_to in u_list, 'u_to: %s 不是标准单位 %s' % (u_to, u_list)
    sigma_stand = None
    sigma_u_to = None
    # 从输入任意转为标准
    if u_in == 'N/m':
        sigma_stand = sigma
    elif u_in == 'mN/m':
        sigma_stand = sigma / 1000

    # 从标准转为任意输出
    if u_to == 'N/m':
        sigma_u_to = sigma_stand
    elif u_to == 'mN/m':
        sigma_u_to = sigma_stand * 1000

    return sigma_u_to


def unit_Cp(Cp, u_in='KJ/(kg•K)', u_to='J/(kg•K)'):
    """
    油气水的比热

    """
    u_list = ['KJ/(kg•K)', 'KJ/(kg•C)', 'kcal/(kg•K)', 'kcal/(kg•C)', 'J/(kg•K)', 'J/(kg•C)']
    assert u_in in u_list, 'u_in: %s 不是标准单位 %s' % (u_in, u_list)
    assert u_to in u_list, 'u_to: %s 不是标准单位 %s' % (u_to, u_list)
    Cp_stand = None
    Cp_u_to = None
    # 从输入任意转为标准
    if u_in in ['KJ/(kg•K)', 'KJ/(kg•C)']:
        Cp_stand = Cp
    elif u_in in ['kcal/(kg•K)', 'kcal/(kg•C)']:
        Cp_stand = Cp * 4.1868
    elif u_in in ['J/(kg•K)', 'J/(kg•C)']:
        Cp_stand = Cp / 1000

    # 从标准转为任意输出
    if u_to in ['KJ/(kg•K)', 'KJ/(kg•C)']:
        Cp_u_to = Cp_stand
    elif u_to in ['kcal/(kg•K)', 'kcal/(kg•C)']:
        Cp_u_to = Cp_stand / 4.1868
    elif u_to in ['J/(kg•K)', 'J/(kg•C)']:
        Cp_u_to = Cp_stand * 1000

    return Cp_u_to


def unit_B(B, u_in='scf/STB', u_to='m3/m3'):
    """
    体积系数

    """
    u_list = ['m3/m3', 'scf/STB']
    assert u_in in u_list, 'u_in: %s 不是标准单位 %s' % (u_in, u_list)
    assert u_to in u_list, 'u_to: %s 不是标准单位 %s' % (u_to, u_list)
    B_stand = None
    B_u_to = None
    # 从输入任意转为标准
    if u_in == 'm3/m3':
        B_stand = B
    elif u_in == 'scf/STB':
        B_stand = B * 0.178

    # 从标准转为任意输出
    if u_to == 'm3/m3':
        B_u_to = B_stand
    elif u_to == 'scf/STB':
        B_u_to = B_stand / 0.178

    return B_u_to


# %% 条件换算

def cond_q_volume_rate(q1, P1, T1, Z1, P2=0.101, T2=15 + 273.15, Z2=1):
    """
    体积流量的状态转换函数，从一种状态(PTZ)转换到另一个状态(PTZ)下的体积流量
    相当于 q2 = q1 * B; B = (Z2 * T2 / P2) / (Z1 * T1 / P1)
    Args:
        q1: 状态1的体积流量 (m3/d) 或 其他量纲

        P1: 状态1的压力 (MPa) 或 其他量纲
        T1: 状态1的温度 (K)
        Z1: 状态1的天然气压缩系数 (-)

    Returns:
        q2: 状态2的体积流量 (m3/d) 或 与q1量纲相同

    """
    q2 = q1 * (Z2 * T2 / P2) / (Z1 * T1 / P1)

    return q2


# %%
if __name__ == '__main__':
    T = 0.8984
    T_u_to = unit_temperature(T)
    print(T_u_to)
