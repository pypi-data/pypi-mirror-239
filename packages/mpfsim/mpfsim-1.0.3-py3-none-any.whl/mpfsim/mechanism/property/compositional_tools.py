#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time:   2023/7/24 15:04
# File:   compositional_tools.py
# Author: He Ma
# Email:  1692303843@qq.com
import numpy as np
import sympy
from core.constants import exp

from optimize.algorithm import root_Newton

from core import mylog, manager_config
from core.tool import draw_data_curve
from core.tool_expert import cached_function
from mechanism.unit_conversion import unit_conversion as unit
from mechanism.data_control.well_data_entry import ParamsReader

params_reader = ParamsReader(manager_config.Params_info)
params_dict = params_reader.params_dict
params_value = params_dict['value']

param_composition = params_value['组分模型输入参数']
mol_weight = sum(param_composition['摩尔分数'] * param_composition['摩尔数'])


# %% Pr、Tr、Ppr、Tpr 对比压力、对比温度、拟对比压力、拟对比温度

def f_Pr(P, Pc):
    """对比压力 reduced pressure"""
    Pr = P / Pc
    return Pr


def f_Tr(T, Tc):
    """对比温度 reduced temperature """
    Tr = T / Tc
    return Tr


def f_Ppr(P, Ppc):
    """拟对比压力 pseudo-reduced pressure"""
    Ppr = P / Ppc
    return Ppr


def f_Tpr(T, Tpc):
    """拟对比温度 pseudo-reduced temperature """
    Tpr = T / Tpc
    return Tpr


# %% Ppc、Tpc 拟临界压力温度的混合规则

def f_Ppc_Tpc_weight(yi_list, Pci_list, Tci_list):
    """
    拟临界压力、温度的混合规则 Kay方法
    低分子量气体混合物
    比重小于0.75的同源气体混合物

    英制单位
    Args:
        yi_list: 各组分摩尔分数列表 (1)
        Pci_list: 各组分临界压力列表 (psia)
        Tci_list: 各组分临界温度列表 (R)

    Returns:
        Ppc: 拟临界压力 (psia)
        Tpc: 拟临界温度 (R)
    """

    yi = np.array(yi_list)
    Pci = np.array(Pci_list)
    Tci = np.array(Tci_list)

    Ppc = sum(yi * Pci)
    Tpc = sum(yi * Tci)

    return Ppc, Tpc


def f_Ppc_Tpc_SBV(yi_list, Pci_list, Tci_list):
    """
    拟临界压力、温度的混合规则 SBV方法 (Stewart, Burkhart, and Voo)
    高分子量气体混合物

    英制单位
    Args:
        yi_list: 各组分摩尔分数列表 (1)
        Pci_list: 各组分临界压力列表 (psia)
        Tci_list: 各组分临界温度列表 (R)

    Returns:
        Ppc: 拟临界压力 (psia)
        Tpc: 拟临界温度 (R)
    """

    yi = np.array(yi_list)
    Pci = np.array(Pci_list)
    Tci = np.array(Tci_list)

    J = 1 / 3 * sum(yi * Tci / Pci) + 2 / 3 * (yi * (Tci / Pci) ** 0.5) ** 2
    K = sum(yi * Tci / Pci ** 0.5)

    Tpc = K ** 2 / J
    Ppc = Tpc / J

    return Ppc, Tpc


def f_Ppc_Tpc_SSBV(yi_list, Pci_list, Tci_list, n_C7_plus=0):
    """
    拟临界压力、温度的混合规则 SSBV方法 (Sutton修正的SBV)
    高浓度的C7+组分(高达14.27 mole%)

    英制单位
    Args:
        yi_list: 各组分摩尔分数列表 (1)
        Pci_list: 各组分临界压力列表 (psia)
        Tci_list: 各组分临界温度列表 (R)
        n_C7_plus: 将组分按照升序排列后，C7+组分的个数，用于取最后n个元素进行计算

    Returns:
        Ppc: 拟临界压力 (psia)
        Tpc: 拟临界温度 (R)
    """

    yi = np.array(yi_list)
    Pci = np.array(Pci_list)
    Tci = np.array(Tci_list)

    J = 1 / 3 * sum(yi * Tci / Pci) + 2 / 3 * (yi * (Tci / Pci) ** 0.5) ** 2
    K = sum(yi * Tci / Pci ** 0.5)

    if n_C7_plus > 0:
        yi = yi[-n_C7_plus:]
        Pci = Pci[-n_C7_plus:]
        Tci = Tci[-n_C7_plus:]

        # 对于C7+
        Fj = 1 / 3 * (yi * Tci / Pci) + 2 / 3 * (yi ** 2 * Tci / Pci)
        epsilon_j = 0.6081 * Fj + 1.1325 * Fj ** 2 - 14.004 * Fj * yi + 64.434 * Fj * yi ** 2
        epsilon_k = Tci / Pci ** 0.5 * (0.3129 * yi - 4.8156 * yi ** 2 + 27.3751 * yi ** 3)

        J = J - epsilon_j
        K = K - epsilon_k

    Tpc = K ** 2 / J
    Ppc = Tpc / J

    return Ppc, Tpc


def _Ppc_Tpc_correct_H2S_CO2(Ppc, Tpc, yi_CO2, yi_H2S):
    """
    CO2、H2S组分修正方法 Wichert and Aziz

    英制单位
    Args:
        Ppc: 拟临界压力 (psia)
        Tpc: 拟临界温度 (R)
        yi_CO2: CO2组分摩尔分数 (1)
        yi_H2S: H2S组分摩尔分数 (1)

    Returns:
        Ppc_star: 修正后的拟临界压力 (psia)
        Tpc_star: 修正后的拟临界温度 (R)
    """

    # ξ: xi
    xi = 120 * ((yi_CO2 + yi_H2S) ** 0.9 - (yi_CO2 + yi_H2S) ** 1.6) + 15 * (yi_H2S ** 0.5 - yi_H2S ** 4)
    Tpc_star = Tpc - xi
    Ppc_star = (Ppc - Tpc_star) / (Tpc + yi_H2S * (1 - yi_H2S) * xi)

    return Ppc_star, Tpc_star


# %% Z_DAK 偏差因子

@cached_function
def _Z_DAK(Z, Ppr, Tpr):
    """
    The DAK correlation is applicable over the following ranges
    of reduced pressure and temperature:
    0.2 ≤ Ppr < 30, 1.0 < Tpr ≤ 3.0 and Ppr < 1.0; 0.7 < Tpr ≤ 1.0.
    The correlation gives poor results for Tpr = 1.0 and Ppr > 1.0.

    """

    A1 = 0.3265
    A2 = -1.0700
    A3 = -0.5339
    A4 = 0.01569
    A5 = -0.05165
    A6 = 0.5475
    A7 = -0.7361
    A8 = 0.1844
    A9 = 0.1056
    A10 = 0.6134
    A11 = 0.7210

    rhor = 0.27 * Ppr / (Z * Tpr)

    c1 = A1 + A2 / Tpr + A3 / Tpr ** 3 + A4 / Tpr ** 4 + A5 / Tpr ** 5
    c2 = A6 + A7 / Tpr + A8 / Tpr ** 2
    c3 = A9 * (A7 / Tpr + A8 / Tpr ** 2)
    # sympy.exp 用于迭代计算
    c4 = A10 * (1 + A11 * rhor ** 2) * (rhor ** 2 / Tpr ** 3) * sympy.exp(-A11 * rhor ** 2)

    Z_new = 1 + c1 * rhor + c2 * rhor ** 2 - c3 * rhor ** 5 + c4

    return Z_new


@cached_function
def f_Z_DAK(Ppr, Tpr, Z_init=1):
    """
    DAK相关式计算组分模型的偏差因子Z
    (Dranchuk and Abou-Kassem)

    Parameters
    ----------
    Ppr : 拟对比压力 (-) Ppr = P / Ppc pseudo-critical pressure
    Tpr : 拟对比温度 (-) Tpr = T / Tpc pseudo-critical temperature
    Z_init : 偏差因子Z迭代初始值 (-)

    Returns
    -------
    Z : 偏差因子

    """
    Z_Symbol = sympy.Symbol('Z')
    f = _Z_DAK(Z_Symbol, Ppr, Tpr) - Z_Symbol
    Z = root_Newton(f, Z_init, symbol=Z_Symbol)
    if Z is None:
        Z = -1

    return Z


def _test_f_Z_DAK():
    T_list = np.arange(1.05, 3.001, 0.05)

    # 区间 [0, 16], [14, 30]
    # P_list = np.arange(0, 16.001, 1)
    P_list = np.arange(14, 30.001, 1)

    line_list = []
    for i, Tpr in enumerate(T_list):
        line = []
        mylog.logger.debug('%s/%s' % (i, len(T_list)))

        for j, Ppr in enumerate(P_list):
            Z = f_Z_DAK(Ppr, Tpr)
            line.append(Z)

            # print('%s, %s: 所求方程式的根为: %s' % (i, j, x_root))
        line_list.append(line)
        # break

    plt_dict = {
        'legend_list': list(np.round(T_list, 2)),
        'xlabel': '拟对比压力 Pr',
        'ylabel': '压缩因子 Z',
        'title': '天然气压缩因子图版$P_{Pr}-T_{Tr}-Z$',
        'figsize': (5, 6),
        'dpi': 300,
        'is_save': 0,
        'legend': {
            'loc': 'lower center',  # 'best', 'lower center'
            'ncol': 5,  # 1, 4
            'borderaxespad': -15,  # 0, -5, -7
            'subplots_adjust': 0.4,  # 0, 0.2
        },
    }
    draw_data_curve(np.tile(P_list, (len(line_list), 1)), line_list, plt_dict=plt_dict)


# %% Bg 气体地层体积系数

def f_Bg(P1, T1, Z1, P2=14.65, T2=60, Z2=1):
    """
    气体地层体积系数 (-) FVF (Formation Volume Factor)

    Args:
        P1: 状态1的压力 (psia)
        T1: 状态1的温度 (°F)
        Z1: 状态1的天然气压缩系数 (-)

    Returns:
        Bg: 气体地层体积系数 (-)

    Equations:
        R (reservoir) 油藏条件
        SC (standard temperature) 标况条件 (60 °F, 14.65 psia) (15 °C, 0.1 MPa)
        Bg = V_R / V_SC
        V_R = Z_R * n * R * T_R / P_R
        V_SC = Z_SC * n * R * T_SC / P_SC

    """
    Bg = (Z1 * T1 / P1) / (Z2 * T2 / P2)

    return Bg


# %% rhog 气体密度

def f_rhog(P, T, Z, gamma_g):
    """
    气体密度

    Args:
        P: 压力 (MPa)
        T: 温度 (K)
        Z: 天然气压缩系数 (-)
        gamma_g: 天然气比重γg (-)

    Returns:
        rhog: 气体密度 (kg/m3)

    Equations:
        rhog = m / V
        V = ZnRT / P
        Mg = m / n
        rhog = Mg*P/(ZRT)
        gamma_g = Mg / 28.9586
        rhog = 28.9586 * gamma_g * P / (ZRT)

    """
    R = 8.314  # 克拉伯龙常数 J/(mol•K)
    P = unit.unit_pressure(P, 'MPa', 'Pa')
    rhog = 28.9586 * gamma_g * P / (Z * R * T)

    return rhog


# %% mug 气体粘度


def _f_mug_Lee(T, Mg, rhog):
    """
    TODO 英制单位
    气体粘度 Lee相关式
    适用范围:
        rhog(g/cm3):<0.77
        N2(mol%):[0.55, 4.8]
        CO2(mol%):[0.9, 3.2]

    Args:
        T:温度 (R)
        Mg:摩尔质量 (lbm/lb-mole)
        rhog:气体密度 (g/cm3)

    Returns:
        mug: 粘度 (cp)

    """

    K = (9.379 + 0.01607 * Mg) * T ** 1.5 / (209.2 + 19.26 * Mg + T)
    X = 3.448 + 986.4 / T + 0.01009 * Mg
    Y = 2.447 - 0.2224 * X
    mug = 1e-4 * K * exp(X * rhog ** Y)

    return mug


def _f_mug_Sutton(T, Mg, rhog, Ppc, Tpc, Tpr):
    """

    TODO 英制单位
    气体粘度 Sutton 相关式
    粘度 centipoise (cp)

    在Lee相关式基础上 拓展 气体比重gamma_g>1.861

    适用范围:
        gamma_g(g/cm3):(1.861, ]  # 气体比重
        rhog(g/cm3):[0.554, 1.861]
        P(psia):[14.74, 20305]
        T(R):[-45.7, 1112]
        mug(cp):[0.008, 0.435]

        N2(mol%):[0, 5.2]
        CO2(mol%):[0, 8.9]
        H2S(mol%):[0, 1.7]
        C7+(mol%):[0, 24.3]

    Args:
        T:温度 (R)
        Mg:摩尔质量 (lbm/lb-mole)
        rhog:气体密度 (g/cm3)
        Ppc: 拟临界压力 (psia)
        Tpc: 拟临界温度 (R)
        Tpr: 拟对比温度 (-)

    Returns:
        mug: 粘度 (cp)

    Args:
        T:
        Mg:
        rhog:

    Returns:

    """

    X = 3.47 + 1588 / T + 0.0009 * Mg
    Y = 1.66378 - 0.04679 * X

    _A = 0.807 * Tpr ** 0.618
    _B = 0.357 * exp(-0.449 * Tpr)
    _C = 0.34 * exp(-4.05 * Tpr)
    _D = 0.018

    mug_SC_product_Xi = 1e-4 * (_A - _B + _C + _D)
    # ξ粘度归一化参数
    Xi = 0.949 * (Tpc / (Mg ** 3 * Ppc ** 4)) ** (1 / 6)
    # 低压气体粘度
    mug_SC = mug_SC_product_Xi / Xi
    mug = mug_SC * exp(X * rhog ** Y)

    return mug


def f_mug(T, Mg, rhog, Ppc, Tpc, Tpr, gamma_g=1):
    """气体粘度"""
    if gamma_g <= 1.861:
        _f_mug_Lee(T, Mg, rhog)
    else:
        _f_mug_Sutton(T, Mg, rhog, Ppc, Tpc, Tpr)


# %% Cg 气体等温压缩系数
def f_Cg():
    """气体粘度"""
    # TODO 2023年8月5日19:56:57
    if gamma_g <= 1.861:
        _f_mug_Lee(T, Mg, rhog)
    else:
        _f_mug_Sutton(T, Mg, rhog, Ppc, Tpc, Tpr)
