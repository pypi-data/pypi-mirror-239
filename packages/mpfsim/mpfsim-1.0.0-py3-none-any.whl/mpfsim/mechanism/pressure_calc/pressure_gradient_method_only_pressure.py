#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time:   2023/4/26 19:50
# File:   pressure_gradient_method.py
# Author: He Ma
# Email:  1692303843@qq.com

from mechanism.pressure_calc.pressure_tools import *
from core.constants import lg, ln, pi
from core import mylog


def pressure_gradient_Orkiszewski(P_avg, g, D, Delta, rhol, rhog, mul, mug, sigmal, fw, Gt, ql, qg):
    """
    垂直管道中的多相管流压降梯度
    所有单位均为国际单位制

    奥氏方法可能受到流型变化导致的微元段内平均密度的突变引起的压力梯度的突变

    1967年奥氏将前人的压力梯度计算方法分为三类，每类中选出具有代表性的方法，共5个，
    以148口井的数据对它们进行了检验和对比，然后，在不同的流动形态下则其优者，
    并加上他自己的研究结果，综合处的一种新结果，组成如下表示

    Args:
        P_avg: 当前管段平均压力 (Pa)
        g: 重力加速度 (m/s^2)
        D: 管道直径 (m)
        Delta:  Δ管壁相对粗糙度 (-) 0.00182
        rhol: 液相密度 (kg/m^3)
        rhog: 气相密度 (kg/m^3)
        mul: 液体粘度 (Pa·s) 1e-5
        mug: 气体粘度 (Pa·s) 1e-2
        sigmal: 液体表面张力 (N/m)  # 如果是油水混合物则取体积加权平均值
        fw: 含水率 (-) 0.7  # 影响段塞流连续液相是油或是水
        Gt: 流体总质量流量 (kg/s) 1.4769
        ql: 液体体积流量 (m^3/s)
        qg: 气体体积流量 (m^3/s)

    Returns:
        DPt: 压力梯度项

    """

    # ------------------ 1. 计算参数 ------------------
    Ap = pi * (D / 2) ** 2  # 管道流动截面积 (m^2)

    # 计算总流量
    qt = ql + qg

    # PT条件下的各相表观速度 (m/s)
    vt = qt / Ap
    vsl = ql / Ap
    vsg = qg / Ap

    # vg_non_dim 无因次气体流速
    vg_non_dim = qg / Ap * (rhol / (g * sigmal)) ** (1 / 4)

    # ------------------ 2. 计算判别式 ------------------

    # L 不同流型的界限 float 小数
    LB = max(1.071 - 0.727 * vt ** 2 / D, 0.13)  # 泡流界限
    LS = 50 + 36 * vg_non_dim * ql / qg  # 段塞流界限
    LM = 75 + 84 * (vg_non_dim * ql / qg) ** 0.75  # 雾流界限

    # criterion_L 不同流型的界限判别式 bool
    criterion_LB = qg / qt < LB  # 泡流判别式
    criterion_LS = (qg / qt > LB) and (vg_non_dim < LS)  # 段塞流判别式
    criterion_LS_M = (vg_non_dim > LS) and (vg_non_dim < LM)  # 过渡流判别式
    criterion_LM = vg_non_dim > LM  # 雾流判别式

    # !!! 流型的判定有顺序关系
    flow_pattern_id_dict = {
        0: '泡流',
        1: '段塞流',
        2: '过渡流',
        3: '雾流',
    }
    if criterion_LB:
        flow_pattern_id = 0
    elif criterion_LS:
        flow_pattern_id = 1
    elif criterion_LS_M:
        flow_pattern_id = 2
    elif criterion_LM:
        flow_pattern_id = 3

    else:
        raise Exception('未知流型，仅支持', flow_pattern_id_dict.values())
    mylog.logger.debug(f"{flow_pattern_id_dict[flow_pattern_id]}")

    # ------------------ 3. 计算不同流型下的重力梯度、摩擦力梯度 ------------------

    # 根据不同流型计算压力梯度项
    if flow_pattern_id == 0:  # '泡流'
        DP_g, tauf = orkiszewski_gradient_bubble(g, D, Ap, Delta, rhol, rhog, mul, ql, qg, qt, vsl)
    elif flow_pattern_id == 1:  # '段塞流'
        DP_g, tauf = orkiszewski_gradient_slug(g, D, Ap, Delta, rhol, mul, fw, Gt, ql, qt, vt)
    elif flow_pattern_id == 3:  # '雾流'
        DP_g, tauf = orkiszewski_gradient_mist(g, D, rhol, rhog, mul, mug, sigmal, ql, qg, vsg)
    elif flow_pattern_id == 2:  # '过渡流'
        _DP_g_slug, _tauf_slug = orkiszewski_gradient_slug(g, D, Ap, Delta, rhol, mul, fw, Gt, ql, qt, vt)
        _DP_g_mist, _tauf_mist = orkiszewski_gradient_mist(g, D, rhol, rhog, mul, mug, sigmal, ql, qg, vsg)
        DP_g, tauf = orkiszewski_gradient_transition(g, LM, LS, _DP_g_slug, _tauf_slug, _DP_g_mist, _tauf_mist,
                                                     vg_non_dim)
    else:
        raise Exception('未知流型，仅支持', flow_pattern_id_dict.values())
    mylog.logger.debug(f"{flow_pattern_id_dict[flow_pattern_id]}")

    DPt = (DP_g + tauf) / (1 - Gt * qg / (Ap ** 2 * P_avg))

    info = {
        'DP_g': DP_g,
        'tauf': tauf,
        'flow_pattern_id': flow_pattern_id,
    }

    return DPt, info


def pressure_gradient_Hagedorn_Brown(P_avg, g, D, Delta, rhol, rhog, mul, mug, sigmal, fw, Gt, ql, qg):
    """
    Hagedorn_Brown的参数难以确定
    """
    pressure_gradient_Orkiszewski(P_avg, g, D, Delta, rhol, rhog, mul, mug, sigmal, fw, Gt, ql, qg)


def pressure_gradient_Beggs_Brill(P_avg, g, D, rhol, rhog, mul, mug, sigmal, ql, qg, theta):
    """
    倾斜管道中的多相管流压降梯度
    所有单位均为国际单位制

    梯度组成:
        - 重力梯度 rho * g sin(theta)
        - 摩擦 气液混合物机械能损失梯度 rho * dE / dZ

    Args:
        P_avg: 当前管段平均压力 (Pa)
        g: 重力加速度 (m/s^2)
        D: 管道直径 (m)
        rhol: 液相密度 (kg/m^3)
        rhog: 气相密度 (kg/m^3)
        mul: 液体粘度 (Pa·s) 1e-5
        mug: 气体粘度 (Pa·s) 1e-2
        sigmal: 液体表面张力 (N/m)  # 如果是油水混合物则取体积加权平均值
        ql: 液体体积流量 (m^3/s)
        qg: 气体体积流量 (m^3/s)
        # 0: 水平向右; pi/2: 垂直向上; -pi/2 垂直乡下; pi: 水平向左
        # 其他角度关于y轴对称
        theta: 管线与水平方向的夹角 (rad) [-pi/2, pi/2]

    Returns:
        DPt: 压力梯度项

    """

    # ------------------ 1. 计算参数 ------------------

    if (theta > pi / 2) or (theta < -pi / 2):
        raise f'theta 区间: [-pi / 2, pi / 2], 当前 {theta}'

    Ap = pi * (D / 2) ** 2  # 管道流动截面积 (m^2)

    # 计算总流量
    qt = ql + qg

    # PT条件下的各相表观速度 (m/s)
    vt = qt / Ap
    vsl = ql / Ap
    vsg = qg / Ap

    # 体积持液率 (-)  # 无滑脱持液率
    El = ql / qt

    # 液相速度准数 (-)
    Nvl = vsl * (rhol / (g * sigmal)) ** 0.25

    # 弗鲁德数 (-)
    NFr = vt ** 2 / (g * D)

    # ------------------ 2. 计算判别式 ------------------

    # L 不同流型的界限 (-)
    L1 = 316 * El ** 0.302  # 分离流
    L2 = 92.52e-5 * El ** -2.4684  # 间歇流
    L3 = 0.1 * El ** -1.4516  # 分散流
    L4 = 0.5 * El ** -6.733  # 过渡流

    # 分离流: 分层流 波状流 环状流
    # 间歇流: 团状流 段塞流
    # 分散流: 泡流 雾流
    criterion_separated = (El < 0.01 and NFr < L1) or (El >= 0.01 and NFr < L2)  # 分离流判别式
    criterion_transitional = El >= 0.01 and L2 < NFr <= L3  # 过渡流判别式
    criterion_intermittent = (0.01 <= El < 0.4 and L3 < NFr < L1) or (El >= 0.4 and L3 < NFr < L4)  # 间歇流判别式
    criterion_dispersed = (El < 0.4 and NFr >= L1) or (El >= 0.4 and NFr > L4)  # 分散流判别式

    flow_pattern_id_dict = {
        # 流型的判定有顺序关系
        0: '分离流',
        1: '过渡流',
        2: '间歇流',
        3: '分散流',
    }

    if criterion_separated:
        flow_pattern_id = 0
    elif criterion_transitional:
        flow_pattern_id = 1
    elif criterion_intermittent:
        flow_pattern_id = 2
    elif criterion_dispersed:
        flow_pattern_id = 3
    else:
        raise Exception('未知流型，仅支持', flow_pattern_id_dict.values())
    mylog.logger.debug(f"{flow_pattern_id_dict[flow_pattern_id]}")

    # ------------------ 3. 计算不同流型下的重力梯度 ------------------

    if flow_pattern_id == '过渡流':
        _Hl_theta_separated = beggs_brill_pattern_Hl_theta(El, Nvl, NFr, theta, '分离流')
        _Hl_theta_intermittent = beggs_brill_pattern_Hl_theta(El, Nvl, NFr, theta, '间歇流')

        # 检查 L3 - NFr 是否相近 或位于[0, 1]
        A = (L3 - NFr) / (L3 - L2)
        B = 1 - A
        Hl_theta = A * _Hl_theta_separated + B * _Hl_theta_intermittent
    else:
        Hl_theta = beggs_brill_pattern_Hl_theta(El, Nvl, NFr, theta, flow_pattern_id_dict[flow_pattern_id])

    if not 0 < Hl_theta < 1:
        Hl_theta = max(Hl_theta, 1)

    # 混合物实际密度
    rhom = rhol * Hl_theta + rhog * (1 - Hl_theta)
    DP_g = rhom * g * np.sin(theta)

    # ------------------ 4. 计算不同流型下的摩擦力梯度 ------------------
    # 比持液率
    y = El / Hl_theta ** 2
    # y = 1.0924623599684424
    # 系数s
    if 1 < y < 1.2:
        S = ln(2.2 * y - 1.2)
    else:
        _temp = -0.0523 + 3.18 * ln(y) - 0.8725 * ln(y) ** 2 + 0.01853 * ln(y) ** 4
        S = ln(y) / _temp

    # 两相流动的雷诺数 NRe‘
    NRe_prime = D * vt * (rhol * El + rhog * (1 - El)) / (mul * El + mug * (1 - El))

    # 无滑脱气液两相流阻力系数 λ'
    _temp = NRe_prime / (4.5332 * lg(NRe_prime) - 3.8125)
    lambda_prime_coeff = (2 * lg(_temp)) ** -2

    # 气液两相流阻力系数 λ
    f = lambda_prime_coeff * np.e ** S

    # tauf 摩擦梯度损失项 τ: tau
    tauf = f * rhom * vt ** 2 / (2 * D)

    DPt = (DP_g + tauf) / (1 - rhom * vt * vsg / P_avg)

    info = {
        'DP_g': DP_g,
        'tauf': tauf,
        'flow_pattern_id': flow_pattern_id,
    }

    return DPt, info


def pressure_gradient_Kaya(g, D, Delta, rhol, rhog, mul, mug, sigmal, ql, qg, theta):
    """
    倾斜管道中的多相管流压降梯度
    所有单位均为国际单位制

    计算倾斜管道中任意位置的多相管流压降梯度，本方法属于机理模型方法。
    Kaya将流型划分为泡状流、分散泡流、段塞流、冲击流和环状流等五种流型。
    对于某一种流动状况，首先划分其所属的流型，然后根据相应流型下的模型计算压降梯度。
    Kaya在Barnea和Taitel等人的模型基础上，着力研究了环状流的过渡准则。

    梯度组成:
        - 重力梯度 rho * g sin(theta)
        - 摩擦 气液混合物机械能损失梯度 rho * dE / dZ

    Args:
        g: 重力加速度 (m/s^2)
        D: 管道直径 (m)
        Delta:  Δ管壁相对粗糙度 (-) 0.00182
        rhol: 液相密度 (kg/m^3)
        rhog: 气相密度 (kg/m^3)
        mul: 液体粘度 (Pa·s) 1e-5
        mug: 气体粘度 (Pa·s) 1e-2
        sigmal: 液体表面张力 (N/m)  # 如果是油水混合物则取体积加权平均值
        ql: 液体体积流量 (m^3/s)
        qg: 气体体积流量 (m^3/s)
        # 0: 水平向右; pi/2: 垂直向上; -pi/2 垂直乡下; pi: 水平向左
        # 其他角度关于y轴对称
        theta: 管线与水平方向的夹角 (rad) [-pi/2, pi/2]

    Returns:
        DPt: 压力梯度项

    """

    # ------------------ 1. 计算参数 ------------------

    if (theta > pi / 2) or (theta < -pi / 2):
        raise f'theta 区间: [-pi / 2, pi / 2], 当前 {theta}'

    Ap = pi * (D / 2) ** 2  # 管道流动截面积 (m^2)

    # 计算总流量
    qt = ql + qg

    # PT条件下的各相表观速度 (m/s)
    vt = qt / Ap
    vsl = ql / Ap
    vsg = qg / Ap

    # 体积持液率 (-)  # 无滑脱持液率
    El = ql / qt

    # ------------------ 2. 计算判别式 ------------------

    flow_pattern_id_dict = {
        # 流型的判定有顺序关系
        0: '泡流',
        1: '分散泡流',
        2: '段塞流',
        3: '环状流',
        4: '冲击流',
    }

    # 泡流
    _flow_pattern, return_info = kaya_criterion_B(g, D, theta, rhol, rhog, sigmal, vsl, vsg)
    if not _flow_pattern:
        # 分散泡流
        _flow_pattern, return_info = kaya_criterion_DB(g, D, theta, rhol, rhog, sigmal, vsl, vsg, mul, mug, vt, El,
                                                       Delta)
    if not _flow_pattern:
        # 段塞流
        _flow_pattern, return_info = kaya_criterion_S(g, D, theta, rhol, rhog, vsl, vsg)
    if not _flow_pattern:
        # 环状流, 段塞流, 冲击流
        _flow_pattern, return_info = kaya_criterion_A(g, D, theta, rhol, rhog, sigmal, vsl, vsg, mul, mug, Delta)
    if not _flow_pattern:
        raise Exception('未知流型，仅支持', flow_pattern_id_dict.values())
    mylog.logger.debug(f"{flow_pattern_id_dict[_flow_pattern]}")

    # 根据流型名称查询流型ID
    flow_pattern_id = {v: k for k, v in flow_pattern_id_dict.items()}[_flow_pattern]

    # 根据不同流型计算压力梯度项
    if flow_pattern_id == 0:  # '泡流':
        DP_g, tauf = kaya_gradient_B(g, D, theta, rhol, rhog, sigmal, vsg, mul, mug, vt, Delta)
    elif flow_pattern_id == 1:  # '分散泡流':
        DP_g, tauf = kaya_gradient_DB(g, D, theta, rhol, rhog, vsl, vsg, mul, mug, vt, Delta)
    elif flow_pattern_id == 2:  # '段塞流':
        DP_g, tauf = kaya_gradient_S(g, D, theta, rhol, rhog, sigmal, vsl, vsg, mul, mug, vt, Delta)
    elif flow_pattern_id == 3:  # '环状流':
        DP_g, tauf = kaya_gradient_A(g, D, theta, return_info)
    elif flow_pattern_id == 4:  # '冲击流':
        DP_g, tauf = kaya_gradient_I(g, D, theta, rhol, rhog, sigmal, vsl, vsg, mul, mug, vt, Delta)
    else:
        raise

    info = {
        'DP_g': DP_g,
        'tauf': tauf,
        'flow_pattern_id': flow_pattern_id
    }
    DPt = DP_g + tauf

    return DPt, info


def pressure_gradient_Lockhart_Martinelli(D, Delta, rhol, rhog, mul, mug, ql, qg):
    """
    水平管道中的多相管流压降梯度
    所有单位均为国际单位制

    本方法属于经验方法，1949年由Lockhart和Martinelli在实验室内研究完成，适用于小管径和低气液流量。

    Args:
        D: 管道直径 (m)
        Delta:  Δ管壁相对粗糙度 (-) 0.00182
        rhol: 液相密度 (kg/m^3)
        rhog: 气相密度 (kg/m^3)
        mul: 液体粘度 (Pa·s) 1e-5
        mug: 气体粘度 (Pa·s) 1e-2
        ql: 液体体积流量 (m^3/s)
        qg: 气体体积流量 (m^3/s)

    Returns:
        DPt: 压力梯度项

    """

    # ------------------ 1. 计算参数 ------------------

    Ap = pi * (D / 2) ** 2  # 管道流动截面积 (m^2)

    # 计算总流量
    # qt = ql + qg

    # PT条件下的各相表观速度 (m/s)
    # vt = qt / Ap
    vsl = ql / Ap
    vsg = qg / Ap

    # 液相雷诺数
    NRe_l = D * vsl * rhol / mul
    # 气相雷诺数
    NRe_g = D * vsg * rhog / mug

    # ------------------ 2. 计算判别式 ------------------

    flow_pattern_id_dict = {
        # 流型的判定有顺序关系
        0: 'LL',
        1: 'LT',
        2: 'TL',
        3: 'TT',
    }

    # *注：为了保证计算机处理时的连续性，此处对于流态指标进行了修改

    if NRe_l <= 1000 and NRe_g <= 1000:
        flow_pattern_id = 0
    elif NRe_l <= 1000 and NRe_g > 1000:
        flow_pattern_id = 1
    elif NRe_l > 1000 and NRe_g <= 1000:
        flow_pattern_id = 2
    elif NRe_l > 1000 and NRe_g > 1000:
        flow_pattern_id = 3
    else:
        raise Exception('未知流型，仅支持', flow_pattern_id_dict.values())
    mylog.logger.debug(f"{flow_pattern_id_dict[flow_pattern_id]}")

    # 计算单相液流、气流的压降
    f_liquid = friction_moody(NRe_l, Delta)
    f_gas = friction_moody(NRe_g, Delta)
    DP_liquid = f_liquid * rhol * vsl ** 2 / (2 * D)
    DP_gas = f_gas * rhog * vsg ** 2 / (2 * D)

    # 计算Lockhart-Matinelli参数
    X = (DP_liquid / DP_gas) ** 0.5

    # 根据不同流型计算压力梯度项
    if flow_pattern_id == 0:  # 'LL':
        C = 20
    elif flow_pattern_id == 1:  # 'LT':
        C = 12
    elif flow_pattern_id == 2:  # 'TL':
        C = 10
    elif flow_pattern_id == 3:  # 'TT':
        C = 5
    else:
        raise

    # phi_l2: Φl²
    phi_l2 = 1 + C / X + 1 / X ** 2

    DPt = phi_l2 * DP_liquid

    info = {}

    return DPt, info


def pressure_gradient_Dukler(P_avg, P_up, P_down, D, rhol, rhog, mul, mug, ql, qg):
    """
    水平管道中的多相管流压降梯度
    所有单位均为国际单位制

    Dukler第一方法

    本方法由美国休斯敦大学的Dukler在1964年发表。
    Dukler建立了具有2629个试验数据组成的验证数据库，
    并利用相似原理建立了水平气液两相管流压降的新方法。

    梯度组成:
        - 重力梯度 rho * g sin(theta)
        - 摩擦 气液混合物机械能损失梯度 rho * dE / dZ
        - 加速度 动能损失梯 rho * v * dv / dZ

    Args:
        P_avg: 当前管段平均压力 (Pa)
        P_up: 当前管段上游压力 (Pa)
        P_down: 当前管段下游压力 (Pa)
        g: 重力加速度 (m/s^2)
        D: 管道直径 (m)
        Delta:  Δ管壁相对粗糙度 (-) 0.00182
        rhol: 液相密度 (kg/m^3)
        rhog: 气相密度 (kg/m^3)
        mul: 液体粘度 (Pa·s) 1e-5
        mug: 气体粘度 (Pa·s) 1e-2
        sigmal: 液体表面张力 (N/m)  # 如果是油水混合物则取体积加权平均值
        ql: 液体体积流量 (m^3/s)
        qg: 气体体积流量 (m^3/s)
        # 0: 水平向右; pi/2: 垂直向上; -pi/2 垂直乡下; pi: 水平向左
        # 其他角度关于y轴对称

    Returns:
        DPt: 压力梯度项

    """

    Ap = pi * (D / 2) ** 2  # 管道流动截面积 (m^2)

    # 计算总流量
    qt = ql + qg

    # PT条件下的各相表观速度 (m/s)
    vt = qt / Ap
    # vsl = ql / Ap
    # vsg = qg / Ap

    # 体积持液率 (-)  # 无滑脱持液率
    El = ql / qt

    rhom = rhol * El + rhog * (1 - El)
    mum = mul * El + mug * (1 - El)

    # 混合物的雷诺数
    NRem = rhom * vt * D / mum

    # 气液混合物的无滑脱沿程阻力系数
    f = 0.0056 + 0.5 / NRem ** 0.32
    # 摩阻压降梯度
    tauf = f * rhom * vt ** 2 / (2 * D)

    # 加速度动能损失梯
    alpha = qt * qg * rhom * P_avg / (Ap ** 2 * P_up * P_down)

    # 总压降梯度
    DPt = tauf / (1 - alpha)

    info = {}

    return DPt, info


def pressure_gradient_single_phase(g, D, Delta, rhol, mul, ql, theta):
    """
    单相管流压降梯度
    所有单位均为国际单位制

    根据Moody图法（将来添加Panhandal方法、Hanzen-Wallims方法等方法）
    计算单相牛顿流体的压力损失梯度，由重位压降梯度和摩阻压降梯度两部分组成。
    计算时首先判断流态，然后调用摩阻系数计算公式计算当前流态的摩阻系数，
    最后求出重位导致的压降。当流道为非圆形流道时，应校正为圆形流道。以下提出的倾角表示与竖直线所成的角度。
    计算出总压降梯度后，乘以管段的长度，即可求出当前管道的压降。

    梯度组成:
        - 重力梯度 rho * g sin(theta)
        - 摩擦 气液混合物机械能损失梯度 rho * dE / dZ

    Args:
        g: 重力加速度 (m/s^2)
        D: 管道直径 (m)
        Delta:  Δ管壁相对粗糙度 (-) 0.00182
        rhol: 液相密度 (kg/m^3)
        mul: 液体粘度 (Pa·s) 1e-5
        ql: 液体体积流量 (m^3/s)
        # 0: 水平向右; pi/2: 垂直向上; -pi/2 垂直乡下; pi: 水平向左
        # 其他角度关于y轴对称
        theta: 管线与水平方向的夹角 (rad) [-pi/2, pi/2]

    Returns:
        DPt: 压力梯度项

    """

    # ------------------ 1. 计算参数 ------------------

    if (theta > pi / 2) or (theta < -pi / 2):
        raise f'theta 区间: [-pi / 2, pi / 2], 当前 {theta}'

    Ap = pi * (D / 2) ** 2  # 管道流动截面积 (m^2)

    # PT条件下的各相表观速度 (m/s)
    vsl = ql / Ap

    # 混合物的雷诺数
    NRe = rhol * vsl * D / mul

    f = friction_moody(NRe, Delta)

    # 摩阻压降梯度
    tauf = f * rhol * vsl ** 2 / (2 * D)
    # 重力压降梯度
    DP_g = rhol * g * np.sin(theta)

    DPt = DP_g + tauf

    info = {}

    return DPt, info


def pressure_gradient(
        P_segment, P_up, P_down, g, D, Delta,
        rhol, rhog, mul, mug, sigmal, fw, Gt,
        ql_segment, qg_segment,
        theta=90, method_pressure='Beggs_Brill'
):
    """
    根据用户选择的多相管流计算模型求解压力梯度DPt
    """

    # 根据当前段气量多少确定是否按照多相管流进行计算
    # 流体可能倒流即qg << 0
    # if abs(qg_segment) <= 1e-10:  # q_iter m^3/s 数量级很小
    # 气体流量为零调用多相管流二级模块中的单相管流计算模块计算压力梯度DPt
    if abs(qg_segment) <= 1e-9:  # m^3/s 数量级很小
        method_pressure = 'single_phase'

    # 计算多相管流的压降梯度
    if method_pressure == 'Orkiszewski':
        DPt, info = pressure_gradient_Orkiszewski(
            P_segment, g, D, Delta,
            rhol, rhog, mul, mug, sigmal,
            fw, Gt, ql_segment, qg_segment
        )

    elif method_pressure == 'Beggs_Brill':
        DPt, info = pressure_gradient_Beggs_Brill(
            P_segment, g, D,
            rhol, rhog, mul, mug, sigmal,
            ql_segment, qg_segment, theta
        )

    elif method_pressure == 'Kaya':
        DPt, info = pressure_gradient_Kaya(
            g, D, Delta,
            rhol, rhog, mul, mug, sigmal,
            ql_segment, qg_segment, theta
        )

    elif method_pressure == 'Lockhart_Martinelli':
        DPt, info = pressure_gradient_Lockhart_Martinelli(
            D, Delta, rhol, rhog, mul, mug, ql_segment, qg_segment
        )

    elif method_pressure == 'Dukler':
        DPt, info = pressure_gradient_Dukler(
            P_segment, P_up, P_down, D, rhol, rhog, mul, mug,
            ql_segment, qg_segment
        )


    elif method_pressure == 'single_phase':
        DPt, info = pressure_gradient_single_phase(g, D, Delta, rhol, mul, ql_segment, theta)
    else:
        raise

    return DPt, info
