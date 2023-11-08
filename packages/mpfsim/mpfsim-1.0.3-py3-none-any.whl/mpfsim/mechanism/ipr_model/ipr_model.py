#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time:   2023/5/12 23:20
# File:   ipr_model.py
# Author: He Ma
# Email:  1692303843@qq.com

from core.constants import ln, pi
import numpy as np
import matplotlib.pyplot as plt
from mechanism.unit_conversion import unit_conversion as unit

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


# %% 直井流入动态模块

def _basic_Vogel(Pwf_test, Pb):
    # Pr_avg, Pb
    _temp = 1 - 0.2 * (Pwf_test / Pb) - 0.8 * (Pwf_test / Pb) ** 2
    return _temp


def _IPR_vertical_1pahse_well_PI(qo_test, Pwf_test, Pwf, Pr_avg, Pb):
    """

    垂直井筒 两相渗流 流入动态
    Args:
        qo_test: 测试点产液量 (m3/d)
        Pwf_test: 测试点油藏压力 (MPa)

        - 单个测试点
            Pr_avg: 油藏平均压力 (MPa)
        # - 两个测试点
        #     qo_test2: 测试点产液量2 (m3/d)
        #     Pwf_test2: 测试点油藏压力2 (MPa)

    Returns:

    """

    J = qo_test / (Pr_avg - Pwf_test)
    qb = J * (Pr_avg - Pb)

    qo_max = qb + J * Pb / 1.8

    qo = J * (Pr_avg - Pwf)

    return qo


def _IPR_vertical_2phase_Vogel(qo_test, Pwf_test, Pwf, Pr_avg, qo_test2=None, Pwf_test2=None):
    """

    垂直井筒 两相渗流 流入动态
    Args:
        qo_test: 测试点产液量 (m3/d)
        Pr_avg: 油藏压力 (MPa)

    - 单个测试点
        Pr_avg: 油藏平均压力 (MPa)
    - 两个测试点
        qo_test2: 测试点产液量2 (m3/d)
        Pwf_test2: 测试点油藏压力2 (MPa)

    Returns:

    """

    if Pr_avg is None:
        if (qo_test2 is None) or (Pwf_test2 is None):
            raise Exception('如果没有Pr_avg, 则qo_test2 and Pwf_test2 必须提供')

        # 0. 若没有油藏平均压力Pr_avg, 但已知两种油井工作制度的产量和对应流压，计算油藏平均压力
        A = qo_test / qo_test2 - 1
        B = 0.2 * (qo_test / qo_test2 * Pwf_test2 - Pwf_test)
        C = 0.8 * (qo_test / qo_test2 * Pwf_test2 ** 2 - Pwf_test ** 2)
        Pr_avg = (B + np.sqrt(B ** 2 + 4 * A * C)) / (2 * A)

    # print(qo_test, Pwf_test, Pr_avg)

    _temp = _basic_Vogel(Pwf_test, Pr_avg)
    qo_max = qo_test / _temp

    # print('绝对无阻流量: ', qo_max)
    _temp = _basic_Vogel(Pwf, Pr_avg)
    qo = _temp * qo_max
    return qo


def _IPR_vertical_2phase_Standing(qo_test, Pwf_test, Pwf, Pr_avg, FE, ):
    """

    垂直井油气两相渗流时的流入动态－Vogel方法修正－Standing方法
    不完善井Vogel方程的修正－Standing方法，无因次流入动态曲线
    FE = 0.5 ~ 1.5
    """

    # 理想完善井的井底流压
    Pwf_test_FE1 = Pr_avg - (Pr_avg - Pwf_test) * FE

    _temp = _basic_Vogel(Pwf_test_FE1, Pr_avg)
    qo_max_FE1 = qo_test / _temp

    _temp = _basic_Vogel(Pwf, Pr_avg)
    qo = _temp * qo_max_FE1

    return qo


def _IPR_vertical_2phase_Harrison(qo_test, Pwf_test, Pwf, Pr_avg, FE):
    """
    已弃用
    垂直井油气两相渗流时的流入动态－不完善井Vogel方法
    修正－Harrison方法Harrison提供了FE=1~2.5的无因次IPR曲线，扩大了Standing曲线的范围

    """
    # 理想完善井的井底流压
    FE1 = 1
    Pwf_test_FE1 = Pr_avg - (Pr_avg - Pwf_test) * FE1

    qo_max_FE1 = qo_test / (1 - 0.2 * (Pwf_test_FE1 / Pr_avg) - 0.8 * (Pwf_test_FE1 / Pr_avg) ** 2)

    Pwf_FE = Pr_avg - (Pr_avg - Pwf_test) * FE1

    qo = (1 - 0.2 * (Pwf_FE / Pr_avg) - 0.8 * (Pwf / Pr_avg) ** 2) * qo_max_FE1

    return qo


def _IPR_vertical_2pahse_well_PI_Vogel(qo_test, Pwf_test, Pwf, Pr_avg, Pb):
    """
    垂直井单相、两相共存时的流入动态
    当油藏压力 高于饱和压力 ，而流动压力 低于饱和压力 时，油藏中将同时存在单相和两相流动

    Args:
        qo_test: 测试点产液量 (m3/d)
        Pwf_test: 测试点油藏压力 (MPa)
        Pr_avg: 油藏平均压力 (MPa)

    Returns:

    """

    if Pwf_test >= Pb:
        J = qo_test / (Pr_avg - Pwf_test)
    else:
        _temp = _basic_Vogel(Pwf_test, Pb)
        J = qo_test / (Pr_avg - Pb + Pb / 1.8 * _temp)

    qb = J * (Pr_avg - Pb)
    qc = J * Pb / 1.8

    qo_max = qb + qc
    print('垂直井单相、两相共存时的流入动态 qo_max', qo_max)

    _temp = _basic_Vogel(Pwf, Pb)
    qo = qb + qc * _temp

    qo_saturate = J * (Pr_avg - Pwf)

    qo[Pwf > Pb] = qo_saturate[Pwf > Pb]

    return qo


def _IPR_vertical_3pahse_Petrobras(qt_test, Pwf_test, Pwf, Pr_avg, Pb, fw):
    """
    垂直井油气水三相流入动态-Petrobras方法
    Petrobras提出了一种计算三相流动IPR曲线的方法
    综合了IPR曲线的实质是按含水率取纯油IPR曲线的加权平均值

    Args:
        qo_test: 测试点产液量 (m3/d)
        Pwf_test: 测试点油藏压力 (MPa)
        Pr_avg: 油藏平均压力 (MPa)

    Returns:

    """

    if Pwf_test >= Pb:
        J = qt_test / (Pr_avg - Pwf_test)
    else:
        _temp = _basic_Vogel(Pwf_test, Pb)
        _temp2 = (Pr_avg - Pb + Pb / 1.8 * _temp)
        J = qt_test / ((1 - fw) * _temp2 + fw * (Pr_avg - Pwf_test))

    qb = J * (Pr_avg - Pb)
    qc = J * Pb / 1.8
    qo_max = qb + qc

    _temp = _basic_Vogel(Pwf, Pb)
    qo = qb + qc * _temp
    qw = J * (Pr_avg - Pwf)
    qt = qo * (1 - fw) + qw * fw

    qt_saturate = J * (Pr_avg - Pwf)

    qt[Pwf > Pb] = qt_saturate[Pwf > Pb]

    return qt


def f_IPR_vertical(qo_test, Pwf_test, Pwf, Pr_avg, Pb, fw, FE=1):
    """
    直井流入动态模块

    Args:
        fw: 含水率 小数-%
        qo_test: 测试点的产液量 (m3/d)
        Pwf_test: 测试点的井底流压 (MPa)
        Pwf: 计算的压力列表 np.array (MPa)
        Pr_avg: 油藏平均压力 (MPa)
        Pb: 泡点压力 (MPa)
        FE: 流动效率 无因次 (-)

    Returns:
        qo: 产液量列表 np.array (m3/d)
    """
    if fw > 1e-4:
        qo = _IPR_vertical_3pahse_Petrobras(qo_test, Pwf_test, Pwf, Pr_avg, Pb, fw)
    elif abs(FE - 1) > 0.01:
        qo = _IPR_vertical_2phase_Standing(qo_test, Pwf_test, Pwf, Pr_avg, FE)
    else:
        qo = _IPR_vertical_2pahse_well_PI_Vogel(qo_test, Pwf_test, Pwf, Pr_avg, Pb)
    return qo


# %% 定向井流入动态计算模块


def _IPR_directional_Cheng(qo_test, Pwf_test, Pwf, Pr_avg, theta):
    """
    定向井IPR曲线也可视为沃格尔型的曲线，随着井斜角的不断增大，
    斜井和直井的产能比逐渐增加，斜井的IPR曲线大都逐渐向右偏离直井的沃格尔曲线。
    随之，Cheng用回归的方法得到了不同井斜角下的斜井IPR曲线方程。
    Args:
        qo_test: 测试点产液量 (m3/d)
        Pwf_test: 测试点油藏压力 (MPa)

        theta: 井斜角 (°)

    Returns:
        qo: 产液量列表 np.array (m3/d)
    """

    A = -0.0001 * theta + 1.0004
    B = -0.0044 * theta + 0.2379
    C = 0.0042 * theta + 0.7628

    qo_max = qo_test / (A - B * (Pwf_test / Pr_avg) - C * (Pwf_test / Pr_avg) ** 2)
    qo = qo_max * (A - B * (Pwf / Pr_avg) - C * (Pwf / Pr_avg) ** 2)

    return qo


def f_IPR_directional(qo_test, Pwf_test, Pwf, Pr_avg, theta):
    """
    定向井IPR曲线也可视为沃格尔型的曲线，随着井斜角的不断增大，
    斜井和直井的产能比逐渐增加，斜井的IPR曲线大都逐渐向右偏离直井的沃格尔曲线。
    随之，Cheng用回归的方法得到了不同井斜角下的斜井IPR曲线方程。
    Args:
        qo_test: 测试点产液量 (m3/d)
        Pwf_test: 测试点油藏压力 (MPa)

        Pwf: 计算的压力列表 np.array (MPa)
        Pr_avg: 油藏平均压力 (MPa)

        theta: 井斜角 (°)

    Returns:
        qo: 产液量列表 np.array (m3/d)
    """

    qo = _IPR_directional_Cheng(qo_test, Pwf_test, Pwf, Pr_avg, theta)
    return qo


# %% 水平井流入动态计算模块


def f_IPR_horizontal(Pwf, Pr_avg, Pb, h, Lw, Kh, Kv, muo, Bo, rw, reh, method='Joshi'):
    """
    水平井流入动态计算模块 默认 Joshi
    Args:
        Pwf: 计算的压力列表 np.array (MPa)
        Pr_avg: 油藏平均压力 (MPa) 20.684
        Pb: 泡点压力 (MPa) 2
        h: 油层厚度 (m) 18.29
        Kh: 水平方向渗透率 (mD) 100
        Kv: 垂直方向渗透率 (mD) 100
        Lw: 水平段长度 (m) 600
        muo: 原油粘度 (mPa·s) 2.6
        Bo: 原油体积系数 (-) 1.20
        rw: 井筒半径 (m) 0.0915
        reh: 泄油半径 (m) 300
        method: str 'Joshi'

    Returns:
        qo: 产液量列表 np.array (m3/d)
    """
    _temp = 1 / 4 + (2 * reh / Lw) ** 4
    alpha = 1 / 2 * Lw * (1 / 2 + _temp ** 0.5) ** 0.5
    beta = np.sqrt(Kh / Kv)

    A = 0.543 * Kh * h / (muo * Bo)

    # x = 2 * alpha / Lw

    # Joshi 和 Renard 方法其实相同，大软件理论文档中，关于水平井稳态产能公式全部有误
    B1 = None  # 外部渗流阻力R1的系数
    if method == 'Giger':
        B1 = ln((1 + (1 + (Lw / (2 * reh)) ** 2) ** 0.5) / (Lw / (2 * reh)))
    elif method == 'Borisov':
        B1 = ln(4 * reh / Lw)
    elif method == 'Joshi':
        B1 = ln((alpha + (alpha ** 2 - (Lw / 2) ** 2) ** 0.5) / (Lw / 2))
    elif method == 'Renard':
        B1 = ln(2 * alpha / Lw + ((2 * alpha / Lw) ** 2 - 1) ** 0.5)

    B2 = beta * (h / Lw) * ln(beta * h / (2 * pi * rw))  # 内部渗流阻力R2的系数
    # Joshi认为第二项没有Pi，且与Pipesim的结果更符合，但从其他公式的规律看应该有Pi
    # if method == 'Joshi':
    #     B2 = (h / Lw) * ln(h / (2  * rw))  # 内部渗流阻力R2的系数

    J = A / (B1 + B2)  # 外部+内部的渗流阻力

    # 原始版本
    # qo_max = J * Pr_avg
    # print(method, qo_max)
    # qo_sc = qo_max * (1 - Pwf / Pr_avg)

    # 加入Vogel泡点压力变为两项的版本（参考 PIPESIM 结果特点构建的）
    qb = J * (Pr_avg - Pb)
    qc = J * Pb / 1.8
    qo_max = qb + qc
    # print(method, qo_max)

    _temp = _basic_Vogel(Pwf, Pb)
    qo = qb + qc * _temp

    qo_saturate = J * (Pr_avg - Pwf)

    qo[Pwf > Pb] = qo_saturate[Pwf > Pb]

    return qo


# %% 气井流入动态计算模块

def _IPR_gas_ss(Pwf, Pe, h, rw, re, s, K, T, mu, Z):
    """
    稳定状态流动气井产能公式 Steady State (ss)
    本函数在假定气井符合稳定达西流动条件下对气井产能进行求解、预测
    Args:
        Pwf: 计算的压力列表 np.array (MPa)
        Pe: 油藏平均压力 (MPa)
        h: 油层厚度 (m)
        rw: 井筒半径 (m)
        re: 泄油半径 (m)
        s: 表皮系数 (-)
        K: 渗透率 (mD)
        T: 地层温度 (K)
        mu: 气体粘度 (mPa·s)
        Z: 气体压缩因子 (-)

    Returns:
        qsc: 产液量列表 np.array (m3/d)
    """

    qsc = 774.6 * K * h * (Pe ** 2 - Pwf ** 2) / ((ln(re / rw) + s) * T * mu * Z)

    return qsc


def _IPR_gas_nonDarcy(Pwf, Pe, h, rw, re, s, K, T, mu, Z, gamma_g):
    """
    有问题
    稳定状态流动气井产能公式 nonDarcy
    本函数在假定气井符合稳定达西流动条件下对气井产能进行求解、预测
    Args:
        Pwf: 计算的压力列表 np.array (MPa)
        Pe: 油藏平均压力 (MPa)
        h: 油层厚度 (m)
        rw: 井筒半径 (m)
        re: 泄油半径 (m)
        s: 表皮系数 (-)
        K: 渗透率 (mD)
        T: 地层温度 (K)
        mu: 气体粘度 (mPa·s)
        Z: 气体压缩因子 (-)
        gamma_g: 天然气相对密度 (-)

    Returns:
        qsc: 产液量列表 np.array (m3/d)
    """

    M = ln(re / rw) + s
    l = 1.291e-3 * T * mu * Z / (K * h)
    beta = 7.644e10 / K ** 1.5

    D = 1 / l * 2.828 * 1e-21 * beta * gamma_g * Z * T / (rw * h ** 2)

    # TODO 讲道理 `_temp`是qsc的一元二次方程，求根公式中的 Delta 所以应该是-4，
    #  但这回导致 l * M > Delta， 进而导致产量为负数，而改为正数后即可
    #  理论文档中的+号可能也是此原因，理由不详
    _temp = l ** 2 * M ** 2 + 4 * l * D * (Pe ** 2 - Pwf ** 2)
    A = -l * M + _temp ** 0.5
    qsc = A / (2 * l * D)

    return qsc


def _IPR_gas_pss(Pwf, Pe, h, rw, re, s, K, T, mu, Z, gamma_g):
    """
    标况气体产量
    拟稳定状态流动气井产能公式 Pseudo Steady State (ss)
    本函数在假定气井符合稳定达西流动条件下对气井产能进行求解、预测
    Args:
        Pwf: 计算的压力列表 np.array (MPa)
        Pe: 油藏平均压力 (MPa)
        h: 油层厚度 (m)
        rw: 井筒半径 (m)
        re: 泄油半径 (m)
        s: 表皮系数 (-)
        K: 渗透率 (mD)
        T: 地层温度 (K)
        mu: 气体粘度 (mPa·s)
        Z: 气体压缩因子 (-)
        gamma_g: 天然气相对密度 (-)

    Returns:
        qsc: 产液量列表 np.array (m3/d)
    """

    M = ln(0.472 * re / rw) + s
    l = 1.291e-3 * T * mu * Z / (K * h)
    beta = 7.644e10 / K ** 1.5
    N = 2.828e-21 * beta * gamma_g * Z * T ** rw * h ** 2

    # TODO 这里可能是 +4
    _temp = l ** 2 * M ** 2 + 4 * N * (Pe ** 2 - Pwf ** 2)
    A = -l * M + _temp ** 0.5
    qsc = A / (2 * N)

    return qsc


def f_IPR_gas(Pwf, Pr_avg, h, rw, re, s, K, T, muo, Z, gamma_g, method='pss'):
    """
    气井产能公式 默认 拟稳定状态流动 方法 Pseudo Steady State (ss)
    本函数在假定气井符合稳定达西流动条件下对气井产能进行求解、预测
        Args:
        Pwf: 计算的压力列表 np.array (MPa)
        Pe: 油藏平均压力 (MPa)
        h: 油层厚度 (m)
        rw: 井筒半径 (m)
        re: 泄油半径 (m)
        s: 表皮系数 (-)
        K: 渗透率 (mD)
        T: 地层温度 (K)
        mu: 气体粘度 (mPa·s)
        Z: 气体压缩因子 (-)
        gamma_g: 天然气相对密度 (-) 0.76

    Returns:
        qsc: 产液量列表 np.array (m3/d)
    """

    if method == 'ss':
        qsc = _IPR_gas_ss(Pwf, Pr_avg, h, rw, re, s, K, T, muo, Z)
    elif method == 'nonDarcy':
        qsc = _IPR_gas_nonDarcy(Pwf, Pr_avg, h, rw, re, s, K, T, muo, Z, gamma_g)
    elif method == 'pss':
        qsc = _IPR_gas_pss(Pwf, Pr_avg, h, rw, re, s, K, T, muo, Z, gamma_g)
    else:
        raise Exception('method not found')

    return qsc


# %% 不同井型IPR测试
def _test_IPR_vertical():
    Pr_avg = 22  # 地层压力 MPa
    Pb = 10  # 泡点压力 MPa

    qo_test = 20  # 测试点产量 sm3/d
    Pwf_test = 15  # 测试点压力 MPa

    FE = 1 - 0.2  # 流动效率 井的理想生产压差与实际生产压差的比 0.5~1.5
    fw = 0.5  # 含水率 0.1 小数-%
    Pwf = np.linspace(0, Pr_avg, num=100)

    qo = f_IPR_vertical(qo_test, Pwf_test, Pwf, Pr_avg, Pb, fw, FE=1)

    plt.figure()
    plt.plot(qo, Pwf)
    plt.xlabel('产量 sm3/d')
    plt.ylabel('井底压力 MPa')
    plt.xlim(0)
    plt.ylim(0)
    # plt.legend()
    plt.grid()
    plt.tight_layout()

    plt.show()


def _test_IPR_directional():
    theta = 40  # 井斜角 (°)
    Pr_avg = 22  # 地层压力 MPa
    Pb = 10  # 泡点压力 MPa

    qo_test = 20  # 测试点产量 sm3/d
    Pwf_test = 15  # 测试点压力 MPa

    FE = 1 - 0.2  # 流动效率 井的理想生产压差与实际生产压差的比 0.5~1.5
    fw = 0.5  # 含水率 0.1 小数-%
    Pwf = np.linspace(0, Pr_avg, num=100)

    qo = f_IPR_directional(qo_test, Pwf_test, Pwf, Pr_avg, theta)

    plt.figure()
    plt.plot(qo, Pwf)
    plt.xlabel('产量 sm3/d')
    plt.ylabel('井底压力 MPa')
    plt.xlim(0)
    plt.ylim(0)
    # plt.legend()
    plt.grid()
    plt.tight_layout()

    plt.show()


def _test_IPR_horizonal():
    Pr_avg = 20.684  # 地层压力 MPa
    Pb = 2  # 泡点压力 MPa
    h = 18.29  # 油层厚度
    Kh = 100  # 水平方向渗透率 (mD)
    Kv = 100  # 垂直方向渗透率 (mD)
    Lw = 609.76  # 水平段长度 (m)
    muo = 2.6  # 原油粘度 (mPa·s)
    Bo = 1.20  # 原油体积系数 (-)
    reh = 300
    rw = 0.0915  # 井筒半径 (m)

    Pwf = np.linspace(0, Pr_avg, num=100)
    # Pwf = Pr_avg - 3.447

    qo = f_IPR_horizontal(Pwf, Pr_avg, Pb, h, Lw, Kh, Kv, muo, Bo, rw, reh, method='Joshi')

    plt.figure()
    plt.plot(qo, Pwf)
    plt.xlabel('产量 sm3/d')
    plt.ylabel('井底压力 MPa')
    plt.xlim(0)
    plt.ylim(0)
    # plt.legend()
    plt.grid()
    plt.tight_layout()

    plt.show()


def _test_IPR_gas():
    Pr_avg = 20.684  # 地层压力 MPa
    T = unit.unit_temperature(40)  # 地层压力 K
    Pb = 2  # 泡点压力 MPa
    h = 18.29  # 油层厚度
    K = 100  # 渗透率 (mD)
    Lw = 609.76  # 水平段长度 (m)
    muo = 2.6  # 原油粘度 (mPa·s)
    Bo = 1.20  # 原油体积系数 (-)
    re = 300
    rw = 0.0915  # 井筒半径 (m)
    s = 0  # 表皮系数 (-)
    Z = 0.996  # 天然气压缩系数 (-)
    gamma_g = 0.76  # 天然气相对密度 (-)
    Pwf = np.linspace(0, Pr_avg, num=100)

    # qo0 = _IPR_gas_ss(Pwf, Pr_avg, h, rw, re, s, K, T, muo, Z)
    # qo1 = _IPR_gas_nonDarcy(Pwf, Pr_avg, h, rw, re, s, K, T, muo, Z, gamma_g)
    # qo2 = _IPR_gas_pss(Pwf, Pr_avg, h, rw, re, s, K, T, muo, Z, gamma_g)

    qsc0 = f_IPR_gas(Pwf, Pr_avg, h, rw, re, s, K, T, muo, Z, gamma_g, method='ss')
    qsc1 = f_IPR_gas(Pwf, Pr_avg, h, rw, re, s, K, T, muo, Z, gamma_g, method='nonDarcy')
    qsc2 = f_IPR_gas(Pwf, Pr_avg, h, rw, re, s, K, T, muo, Z, gamma_g, method='pss')

    plt.figure()
    plt.plot(qsc0, Pwf, label='ss')
    plt.plot(qsc1, Pwf, label='nonDarcy')
    plt.plot(qsc2, Pwf, label='pss')
    plt.xlabel('产量 sm3/d')
    plt.ylabel('井底压力 MPa')
    # plt.xlim(0)
    # plt.ylim(0)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


# %%

if __name__ == '__main__':
    _test_IPR_directional()
    _test_IPR_gas()
