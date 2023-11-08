#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time:   2023/4/25 16:18
# File:   pressure_tools.py
# Author: He Ma
# Email:  1692303843@qq.com

import numpy as np
from core.constants import lg, ln, pi
from core import mylog

from mechanism.unit_conversion import unit_conversion as unit


# %% moody图版

def friction_moody(NRe, Delta, return_branch=False):
    """
    根据给定的雷诺数NRe和管道的相对粗糙度DeltaΔ=ε/D
    按照工程流体力学中的Moody图方法计算范宁摩阻系数
    Args:
        NRe: 雷诺数，无单位 NRe = D * vsl * rhol / mul
                参考取值 NRe = 125.2, 取值范围: 0~约1e8
        Delta: Delta = 2 * epsilon / D  # Delta: Δ管壁相对粗糙度
                参考取值 Delta = 0.0018, 取值范围: 约1e-6~约5e-2

                D = 0.05  # 管道直径, m
                epsilon = 4.57 * 1e-5  # epsilon: ε 管壁绝对粗糙度, m
        return_branch: bool 是否显示分支
    Returns:
        f: 摩擦阻力系数, 无量纲, 参考取值0.04
    """

    if NRe <= 2000:  # 层流
        f = 64 / NRe
        flag_id = 0

    elif NRe <= 59.7 / (Delta ** (8 / 7)):
        f = 0.3164 / NRe ** 0.25
        flag_id = 1

    elif NRe <= (665 - 765 * lg(Delta) / lg(10)) / Delta:
        _f = 1.8 * lg(6.8 / NRe + (Delta / 7.4) ** 1.11) / lg(10)
        f = (1 / _f) ** 2
        flag_id = 2
    else:
        _f = 2 * lg(Delta / 7.4) / lg(10)
        f = (1 / _f) ** 2
        flag_id = 3
    if return_branch:
        mylog.logger.debug('moody摩阻系数的雷诺数分支: %s' % flag_id)
        return f, flag_id
    return f


# %% Orkiszewski
def orkiszewski_vs_slug(g, D, rhol, mul, NRe_prime):
    """
    试算法 迭代计算段塞流的滑脱速度
    Args:
        g:重力加速度9.8 m/s^2
        D:管径 0.05 m
        rhol:液体密度850 kg/m^3
        mul:液体粘度0.1 Pa·s
        NRe_prime:雷诺数 7515.65

    Returns:
        vs:段塞流的滑脱速度
    """

    vs_pseudo = 0.1
    vs = vs_pseudo
    _i = 0
    while True:
        # 泡流雷诺数Nb
        Nb = D * vs * rhol / mul

        # vs: 段塞流滑脱速度, m/s, Griffith和Wallis提出公式
        if Nb <= 3000:
            vs = (0.546 + 8.74 * 1e-6 * NRe_prime) * (g * D) ** 0.5
        elif Nb >= 8000:
            vs = (0.35 + 8.74 * 1e-6 * NRe_prime) * (g * D) ** 0.5
        else:
            _vsi = (0.251 + 8.74 * 1e-6 * NRe_prime) * (g * D) ** 0.5
            vs = (1 / 2) * (_vsi + (_vsi ** 2 + 11.17 * 1e3 * mul / (rhol * D ** 0.5)) ** 0.5)

        # print(Nb, NRe_prime, vs, vs_pseudo)
        if abs(vs_pseudo - vs) < 1e-2:
            break
        vs_pseudo = vs

        _i += 1
        if _i > 5:
            raise Exception('迭代%s次后仍未收敛，需核验' % _i)

    return vs


def orkiszewski_gradient_bubble(g, D, Ap, Delta, rhol, rhog, mul, ql, qg, qt, vsl):
    """
    泡流压力梯度项
    Args:
        g: 重力加速度9.8 m/s^2
        D: 管道直径0.0019, m
        Ap: 管道流动截面积 Ap = pi * (D / 2) ** 2, m^2
        Delta: 2 * epsilon / D  # Delta: Δ管壁相对粗糙度
                epsilon = 4.57 * 1e-5  # epsilon: ε 管壁绝对粗糙度, m
        rhol: 液体密度, kg/m^3 850
             p_avg, T_avg条件下的液体密度，
            如果是油水混合物则取体积加权平均值
        rhog: 气体密度, kg/m^3 0.7
        mul: 液体粘度0.01 Pa·s, mu: μ
            p_avg, T_avg条件下的液体粘度，
            如果是油水混合物未乳化情况下可采用体积加权平均值
        ql: 液体积流量, m^3/s 150 / 86400
        qg: 气体体积流量, m^3/s 150 / 86400
        qt: qt = qg + ql  # 总体积流量, m^3/s


        vsl: 液相的表观速度 vsl = ql / Ap



    Returns:
        DP_g: 重力损失梯度项, DP_g在使用中将根据dh进行积分∫
        tauf: 摩擦梯度损失项f, τ tau
        泡流 动能损失梯度项忽略不计
    """

    vs = 0.224  # 泡流滑脱速度实验确定, Griffith实验结果0.224, m/s

    # 1. 计算截面含气率
    # Hg 气相存容比（截面含气率），计算管段中气相体积与管段容积的比, 根据滑脱速度`vs`计算
    _temp = (1 + qt / (vs * Ap)) ** 2 - 4 * qg / (vs * Ap)
    Hg = 0.5 * (1 + qt / (vs * Ap) - (_temp) ** 0.5)
    # Hl 液相存容比（持液率），计算管段中液相体积与管段容积的比
    Hl = 1 - Hg
    # 2. 平均混合物密度
    # rhom: 平均混合物密度 p_avg, T_avg条件下的平均混合物密度, kg/m^3
    rhom = Hl * rhol + Hg * rhog

    # 3. 计算重力损失梯度
    # dp_g = rhom * g * dh, 此时DP_g在使用中将根据dh进行积分∫
    DP_g = rhom * g

    # 4. 计算摩阻系数
    # 4.1 计算液相雷诺数
    # NRe: 雷诺数，无单位
    # !!! 这里粘度单位是`Pa·s`
    NRe = D * vsl * rhol / mul

    # 4.2 计算摩阻系数f
    # f: 摩擦阻力系数, 小数, 根据NRe和ε/D epsilon 查图版得到
    f = friction_moody(NRe, Delta)
    # print(f)

    # 5. 计算液相真实流速
    # vlh 液相真实流速, m/s
    vlh = ql / (Ap * (1 - Hg))

    # tauf 摩擦梯度损失项 τ: tau
    tauf = f * rhol * vlh ** 2 / (2 * D)

    return DP_g, tauf


def orkiszewski_gradient_slug(g, D, Ap, Delta, rhol, mul, fw, Gt, ql, qt, vt):
    """
    段塞流压力梯度项

    Args:
        g: 重力加速度9.8 m/s^2
        D: 管道直径0.0019, m
        Ap: 管道流动截面积 Ap = pi * (D / 2) ** 2, m^2
        Delta: 2 * epsilon / D  # Delta: Δ管壁相对粗糙度
                epsilon = 4.57 * 1e-5  # epsilon: ε 管壁绝对粗糙度, m
        rhol: 液体密度, kg/m^3 850
             p_avg, T_avg条件下的液体密度，
            如果是油水混合物则取体积加权平均值
        mul: 液体粘度0.01 Pa·s, mu: μ
            p_avg, T_avg条件下的液体粘度，
            如果是油水混合物未乳化情况下可采用体积加权平均值
        fw: 含水率 小数，取值范围0~1, 参考值0.7

        Gt: 流体总质量流量 kg/s 参考值1.4769 Gt = rhol * ql + rhog * qg
        ql: 液体积流量, m^3/s 150 / 86400
        qt: qt = qg + ql  # 总体积流量, m^3/s 参考值0.0034
        vt: 混合物流速, m/s vt = qt / Ap 参考值1.768 p_avg, T_avg条件下

    Returns:
        DP_g: 重力损失梯度项, DP_g在使用中将根据dh进行积分∫
        tauf: 摩擦梯度损失项f, τ tau
    """
    # 1. 计算平均密度
    # 1.1 计算雷诺数
    # The prime symbol ( ′ ), double prime symbol ( ″ ), and triple prime symbol ( ''' ), etc.,
    # are used to designate several different units and for various other purposes in mathematics,
    # the sciences, linguistics and music.
    # 雷诺数 `NRe'` `'`: prime
    NRe_prime = D * vt * rhol / mul

    # 1.2 迭代滑脱速度
    vs = orkiszewski_vs_slug(g, D, rhol, mul, NRe_prime)

    # 1.3 计算液体分布系数, delta: δ
    # 段塞流连续相为液相，此时含水率高则为液相中的水相，否则为油相
    if fw > 0.5:
        if vt <= 3.048:
            delta = 0.00252 * lg(1e3 * mul) / D ** 1.38 \
                    - 0.782 + 0.232 * lg(vt) - 0.428 * lg(D)
        else:
            delta = 0.0174 * lg(1e3 * mul) / D ** 0.799 \
                    - 1.352 - 0.162 * lg(vt) - 0.888 * lg(D)
    else:
        if vt <= 3.048:
            delta = 0.00236 * lg(1e3 * mul + 1) / D ** 1.415 \
                    - 0.140 + 0.167 * lg(vt) - 0.113 * lg(D)
        else:
            X = (lg(vt) + 0.516) * \
                (0.0016 * lg(1e3 * mul + 1) / D ** 1.571 + 0.722 + 0.63 * lg(D))
            delta = 0.00537 * lg(1e3 * mul + 1) / D ** 1.371 \
                    + 0.455 + 0.569 * lg(D) - X

    # 混合物平均密度 ρm_avg
    rhom_avg = (Gt + rhol * vs * Ap) / (qt + vs * Ap) + delta * rhol

    # 1.4 校正液体分布系数, delta: δ
    if vt <= 3.048:
        delta_correction = max(delta, -0.2132 * vt)
    else:
        delta_correction = max(delta, (-vs * Ap) / (qt + vs * Ap) * (1 - rhom_avg / rhol))

    delta = delta_correction

    # 2. 重力梯度项
    DP_g = rhom_avg * g

    f = friction_moody(NRe_prime, Delta)

    # 3. 摩擦梯度项
    tauf = f * rhol * vt ** 2 / (2 * D) * ((ql + vs * Ap) / (qt + vs * Ap) + delta)

    return DP_g, tauf


def orkiszewski_gradient_mist(g, D, rhol, rhog, mul, mug, sigma, ql, qg, vsg):
    """
    雾流压力梯度项

    Args:
        g: 重力加速度9.8 m/s^2
        D: 管道直径0.0019, m
        rhol: 液体密度, kg/m^3 850
             p_avg, T_avg条件下的液体密度，
            如果是油水混合物则取体积加权平均值
        rhog: 气体密度, kg/m^3 0.7
             p_avg, T_avg条件下的气体密度，
            如果是油水混合物则取体积加权平均值
        mul: 液体粘度0.01 Pa·s, mu: μ
            p_avg, T_avg条件下的液体粘度，
            如果是油水混合物未乳化情况下可采用体积加权平均值
        mug: 气体粘度1e-5 Pa·s, mu: μ 气体粘度 1e-2~1e-3 mPa·s
        sigma: 液体表面张力N/m,  sigma = 1.83 * 1e-2 p_avg, T_avg条件下的液体表面张力, 如果是油水混合物则取体积加权平均值
        ql: 液体积流量, m^3/s 150 / 86400
        qg: 气体体积流量, m^3/s 150 / 86400
        vsg: 气相的表观速度, m/s 0.884 vsg = qg / Ap

    Returns:
        DP_g: 重力损失梯度项, DP_g在使用中将根据dh进行积分∫
        tauf: 摩擦梯度损失项f, τ tau
        雾流 动能损失梯度项 本应计算，但书中未提及
    """
    # 1. 计算含气率
    # 雾流的气液滑脱速度≈0，故
    Hg = qg / (ql + qg)

    # 2. 计算混合物平均密度 ρm_avg
    rhom_avg = rhol * (1 - Hg) + rhog * Hg

    # 3. 计算重力损失梯度项
    DP_g = rhom_avg * g

    # 4. 计算摩阻系数
    # 4.1 气相雷诺数
    NReg = D * vsg * rhog / mug
    # 4.2 液膜壁厚准数Nw
    Nw = rhog * (vsg * mul / sigma) * (vsg * mul / sigma) / rhol
    # 液膜相对粗糙度Delta Δ 0.001~0.5: Δ = ε / D
    if Nw <= 0.005:
        Delta = 34 * sigma / (rhog * vsg ** 2 * D)
    else:
        Delta = 174.8 * sigma * Nw ** 0.302 / (rhog * vsg ** 2 * D)

    f = friction_moody(NReg, Delta)

    # 雾流的连续相为气相
    tauf = f * rhog * vsg ** 2 / (2 * D)
    # 4. 摩擦梯度项

    return DP_g, tauf


def orkiszewski_gradient_transition(g, LM, LS, DP_g_slug, tauf_slug, DP_g_mist, tauf_mist, vg_non_dim):
    """
    过渡流压力梯度项
    Args:
        g: 重力加速度9.8 m/s^2
        LM: 雾流界限 449.44 LM = 75 + 84 * (vg_non_dim * ql / qg) ** 0.75
        LS: 段塞流界限 314.11 LS = 50 + 36 * vg_non_dim * ql / qg
        DP_g_slug: 段塞流重力损失梯度项 Pa/m, 4893.12
        tauf_slug: 段塞流摩擦梯度损失项f Pa/m, 950.47
        DP_g_mist: 雾流重力损失梯度项 Pa/m, 4168.43
        tauf_mist: 雾流流摩擦梯度损失项f Pa/m, 5.75
        vg_non_dim: 无因次气体流速, m/s 7.33
            vg_non_dim = qg / Ap * (rhol / (g * sigma)) ** (1 / 4)

    Returns:
        DP_g: 重力损失梯度项, DP_g在使用中将根据dh进行积分∫
        tauf: 摩擦梯度损失项f, τ tau
    """
    # 段塞流平均密度
    rhom_avg_slug = DP_g_slug / g
    # 雾流平均密度
    rhom_avg_mist = DP_g_mist / g

    # 过渡流混合物平均密度
    rhom_avg = (LM - vg_non_dim) / (LM - LS) * rhom_avg_slug + \
               (vg_non_dim - LS) / (LM - LS) * rhom_avg_mist

    # 计算重力损失梯度项
    DP_g = rhom_avg * g

    # 过渡流混合物平均摩擦梯度项

    tauf = (LM - vg_non_dim) / (LM - LS) * tauf_slug + \
           (vg_non_dim - LS) / (LM - LS) * tauf_mist

    return DP_g, tauf


# %% Beggs_Brill

def beggs_brill_pattern_Hl_theta(El, Nvl, NFr, theta, flow_pattern):
    MATRIX_abc = np.array([
        [0.98, 0.4846, 0.0868],
        [0.845, 0.5351, 0.0173],
        [1.065, 0.5929, 0.0609],
    ])
    MATRIX_defg = np.array([
        [0.011, -3.768, 3.539, -1.614],  # 分离流-上坡
        [2.96, 0.305, -0.4473, 0.0978],  # 间歇流-上坡
        # 分散流: C=0, phi=1, Hl(theta)与theta无关
        [4.7, -0.3692, 0.1244, -0.5056],  # 各种流型-下坡
    ])

    def coeff_C(dd, ee, ff, gg):
        C = (1 - El) * ln(dd * El ** ee * Nvl ** ff * NFr ** gg)
        return C

    # aa, bb, cc 不区分坡度
    # dd, ee, ff, gg 在上下坡的计算系数不同
    if flow_pattern == '分离流':
        aa, bb, cc = MATRIX_abc[0, :]
        dd, ee, ff, gg = MATRIX_defg[0, :]
        C = coeff_C(dd, ee, ff, gg)

    elif flow_pattern == '间歇流':
        aa, bb, cc = MATRIX_abc[1, :]
        dd, ee, ff, gg = MATRIX_defg[1, :]
        C = coeff_C(dd, ee, ff, gg)

    elif flow_pattern == '分散流':
        aa, bb, cc = MATRIX_abc[2, :]
        # dd, ee, ff, gg = 0,0,0,0
        C = 0
    else:
        # TODO 需要补充过渡流计算过程
        raise Exception('过渡流应该根据平均值计算 %s ' % flow_pattern)

    # dd, ee, ff, gg 下坡计算系数
    if theta < 0:
        dd, ee, ff, gg = MATRIX_defg[0, :]
        C = coeff_C(dd, ee, ff, gg)

    # 有滑脱持液率 (-)  # 倾角theta=0情况下，水平流动的持液率
    Hl_0 = aa * El ** bb / NFr ** cc
    # 有滑脱持液率 >= 无滑脱持液率
    Hl_0 = max(Hl_0, El)

    # 倾斜校正系数
    # 当theta=pi/2 即90°时，C的系数退化为0.3
    phi = 1 + C * (np.sin(1.8 * theta) - 1 / 3 * np.sin(1.8 * theta) ** 3)

    # 倾角为theta的气液两相流的持液率
    Hl_theta = Hl_0 * phi
    return Hl_theta


# %% Kaya

def kaya_criterion_B(g, D, theta, rhol, rhog, sigmal, vsl, vsg):
    # 1. 泡流边界
    # 泡状流能够出现的最小直径
    #   实验证明，泡状流只出现在相对较粗的管道之中。出现泡状流的最小直径为
    D_min = 19.01 * (sigmal * (rhol - rhog) / (g * rhol ** 2))

    # 泡状流能够出现的最小管道倾角
    #   与水平方向的夹角小于此倾角时，由于气泡之间发生聚并，
    #   不能出现泡状流，出现泡状流的最小管道倾角按如下步骤计算：
    # 气泡在静止液柱中的上升速度
    v_bs = 1.53 * (g * sigmal * (rhol - rhog) / rhol ** 2) ** 0.25
    # 将theta取值为0~90度，以0.1度为步长按照下式计算各个角度下f_theta的值，
    # 将计算结果排序，其中最接近于0的f对应的倾角theta即为最小管道倾角
    # _range_theta = unit.unit_angle(np.arange(0, 90, 0.1), u_in='deg', u_to='rad')
    _range_theta = np.deg2rad(np.arange(0, 90, 0.1))
    f_theta = np.cos(_range_theta) / np.sin(_range_theta) ** 2 - 0.75 * np.cos(pi / 4) * v_bs ** 2 * (0.968 / D) / g
    theta_min = abs(f_theta).argmin()
    theta

    # 计算泡状流和段塞流之间的边界
    # 计算气相表观速度界限
    vsg_limit = 0.333 * vsl + 0.3825 * (g * sigmal * (rhol - rhog) / rhol ** 2) ** 0.25 * np.sin(theta) ** 0.5

    # 泡流判别式
    criterion_B = (D > D_min) and (theta > theta_min) and (vsg > vsg_limit)

    if not criterion_B:
        return False, ()

    return '泡流', ()


def kaya_criterion_DB(g, D, theta, rhol, rhog, sigmal, vsl, vsg, mul, mug, vt, El, Delta):
    # 2. 分散泡流边界
    # 2.1 计算稳定气泡的最大直径
    # 计算混合流体的平均密度、粘度
    rhom = rhol * El + rhog * (1 - El)
    mum = mul * El + mug * (1 - El)
    # 计算混合流体的雷诺数
    NRem = rhom * vt * D / mum
    # 摩擦阻力系数
    f = friction_moody(NRem, Delta)
    _temp = 4.15 * (vsg / vt) ** 0.5 + 0.725
    d_max = _temp * (sigmal / rhol) ** 0.6 * (2 * f * rhom * vt ** 2 / D) ** -0.4

    # 2.2 计算气泡破裂临界直径
    # 临界 Critical
    d_CD = 2 * (0.4 * sigmal / (g * (rhol - rhog))) ** 0.5

    # 2.3 计算气泡向上运移临界直径
    #   如果稳定气泡的最大直径大于气泡运移临界直径，
    #   则可以导致气泡在倾斜管道的顶部聚并，从而导致分散泡流向泡状流转变
    d_CB = 3 * rhol * f * vt ** 2 / (8 * g * (rhol - rhog) * np.cos(theta))

    # 分散泡流判别式
    criterion_DB = (El <= 0.48 and vsg < 1.083 * vsl) or (El > 0.48 and d_max <= d_CD and d_max <= d_CB)

    if not criterion_DB:
        return False, ()

    return '分散泡流', ()


def kaya_criterion_S(g, D, theta, rhol, rhog, vsl, vsg):
    # 3. 段塞流边界
    # 3.1 计算Taylor泡的上升速度
    v0 = (0.35 * np.sin(theta) + 0.54 * np.cos(theta)) * (g * (rhol - rhog) * D / rhol) ** 0.5
    # 3.2 计算段塞流向冲击流的转换边界
    #   根据漂移模型，考虑到段塞流向冲击流流型转换时的Taylor泡区的空隙率一般为0.78（Owen等人的实验结果），
    #   得到段塞流向冲击流的转换边界：
    v_SC_slug = 12.19 * (1.2 * vsl + v0)

    # 段塞流判别式
    criterion_S = vsg < v_SC_slug

    if not criterion_S:
        return False, ()

    return '段塞流', ()


def kaya_criterion_A(g, D, theta, rhol, rhog, sigmal, vsl, vsg, mul, mug, Delta):
    # 4. 环状流边界
    # 4.1 计算液体携带率
    _temp = -0.125 * (10000 * vsg * mug * (rhog / rhol) ** 0.5 / sigmal) - 1.5
    fe = 1 - np.exp(_temp)
    # 4.2 计算气芯物性参数
    #   计算气芯的无滑脱持液率
    lambda_LC = 1 - fe * vsl / (vsg + fe * vsl)
    #   计算气芯的表观速度
    v_SC = vsg + fe * vsl
    #   计算气芯的流体密度
    rho_C = rhol * lambda_LC + rhog * (1 - lambda_LC)
    #   计算气芯的流体粘度
    mu_C = mul * lambda_LC + mug * (1 - lambda_LC)

    # 4.3 计算 液相、气芯、液膜的摩阻系数
    #   计算液相摩阻系数
    NRe_SL = rhol * vsl * D / mul
    f_SL = friction_moody(NRe_SL, Delta)
    #   计算气芯摩阻系数
    NRe_SC = rho_C * v_SC * D / mu_C
    f_SC = friction_moody(NRe_SC, Delta)
    #   计算液膜摩阻系数
    NRe_F = rhol * vsl * (1 - fe) * D / mul
    f_F = friction_moody(NRe_F, Delta)

    # 4.4 计算Lockhart-Martinelli参数
    _temp_SL = f_F * f_SL * rhol * vsl ** 2 / (2 * D)
    _temp_SC = f_SL * f_SC * rho_C * v_SC ** 2 / (2 * D)
    Xm = ((1 - fe) ** 2 * _temp_SL / _temp_SC) ** 0.5
    Ym = (g * np.sin(theta) * (rhog / rhol)) / (f_SL * rho_C * v_SC ** 2 / (2 * D))

    # 4.5 计算气液界面摩阻系数Z 最小无因次液膜厚度delta
    if fe <= 0.9:
        # 气液界面摩阻系数Z
        Z = 1 + 24 * (rhol / rhog) ** (1 / 3)
        _range_delta = np.arange(0, 1, 0.01)
        # 最小无因次液膜厚度delta
        delta = _range_delta
        _temp_b = 4 * delta * (1 - delta)
        _temp_a = _temp_b * (1 - _temp_b) ** 2.5
        f_delta = Ym - Z / (_temp_a) + Xm ** 2 / (_temp_b) ** 3
        delta_min = abs(f_delta).argmin()
    else:
        _epsilon = 1e-3
        # 迭代计算
        # 气液界面摩阻系数Z
        Z_star = 1
        for i in range(1000):  # 最大迭代次数
            # 最小无因次液膜厚度delta
            delta = (Z_star - 1) / 300
            _temp_b = 4 * delta * (1 - delta)
            Z = (Ym - Xm ** 2 / _temp_b ** 3) * (_temp_b * ((1 - _temp_b) ** 2.5))
            if abs((Z_star) - Z / Z_star) <= _epsilon:
                Z = Z_star
                break
            Z_star = Z
        else:
            raise Exception('达到最大迭代次数时仍未收敛 %s' % (Z_star))

    # 4.6 计算截面含液率
    H_LF = 4 * delta * (1 - delta)

    # 环状流判别式
    criterion_A = False  # 环状流
    criterion_S = False  # 段塞流
    criterion_I = False  # 冲击流
    if H_LF < 0.22:
        if Ym < (2 - 1.5 * H_LF) * Xm ** 2 / (H_LF ** 3 * (1 - 1.5 * H_LF)):
            criterion_A = True
        else:
            criterion_I = True
    else:
        # if H_LF + lambda_LC * A_C / Ap <= 0.12:
        # TODO 假定(1-H_LF)=A_C / Ap
        if H_LF + lambda_LC * (1 - H_LF) <= 0.12:
            criterion_A = True
        else:
            criterion_S = True

    if criterion_A:
        flow_pattern = '环状流'
    elif criterion_S:
        flow_pattern = '段塞流'
    elif criterion_I:
        flow_pattern = '冲击流'
    else:
        mylog.logger.warning('kaya模型: 未识别到任何流型')
        raise Exception('kaya模型: 未识别到任何流型')

    return_info = f_SC, rho_C, v_SC, Z, delta,
    return flow_pattern, return_info


def kaya_gradient_B(g, D, theta, rhol, rhog, sigmal, vsg, mul, mug, vt, Delta):
    v_bs = 1.53 * (g * sigmal * (rhol - rhog) / rhol ** 2) ** 0.25

    _range_Hl = np.arange(0, 1, 0.01)
    f_Hl = v_bs * (_range_Hl * np.sin(theta)) ** 0.5 - vsg / (1 - _range_Hl) + 1.2 * vt
    # 泡流持液率
    Hl = abs(f_Hl).argmin()

    rhom = rhol * Hl + rhog * (1 - Hl)
    mum = mul * Hl + mug * (1 - Hl)
    NRem = rhom * vt * D / mum
    f = friction_moody(NRem, Delta)

    DP_g = rhom * g * np.sin(theta)
    # tauf 摩擦梯度损失项 τ: tau
    tauf = f * rhom * vt ** 2 / (2 * D)
    return DP_g, tauf


def kaya_gradient_DB(g, D, theta, rhol, rhog, vsl, vsg, mul, mug, vt, Delta):
    # 持液率
    Hl = vsl / (vsl + vsg)

    rhom = rhol * Hl + rhog * (1 - Hl)
    mum = mul * Hl + mug * (1 - Hl)
    NRem = rhom * vt * D / mum
    f = friction_moody(NRem, Delta)

    DP_g = rhom * g * np.sin(theta)
    # tauf 摩擦梯度损失项 τ: tau
    tauf = f * rhom * vt ** 2 / (2 * D)
    return DP_g, tauf


def kaya_gradient_S(g, D, theta, rhol, rhog, sigmal, vsl, vsg, mul, mug, vt, Delta):
    # 漂移速度
    v0 = (0.35 * np.sin(theta) + 0.54 * np.cos(theta)) * (g * (rhol - rhog) * D / rhol) ** 0.5
    # 计算Taylor泡速度
    v_TB = 1.08 * vt + v0
    # 计算液塞区的空隙率H_GLS 和持液率H_LLS
    _temp = (g * sigmal * (rhol - rhog) / rhol ** 2) ** 0.25
    H_GLS = vsg / (1.208 * vt + 1.414 * _temp * np.sin(theta) ** 0.5)
    H_LLS = 1 - H_GLS

    # 计算液塞区气体流速
    v_GLS = 1.08 * vt + 1.414 * _temp * np.sin(theta) ** 0.5
    # 计算液塞区液体流速
    v_LLS = (vt - v_GLS * H_GLS) / (1 - H_GLS)

    # 计算Taylor泡区的液膜速度和截面空隙率
    # 迭代计算
    H_LTB = 1
    H_GTB = 1 - H_LTB
    for i in range(1000):
        v_LTB_star = -9.916 * (g * D * (1 - H_LTB ** 0.5))
        H_LTB_star = (v_TB - v_LLS) * (1 - H_GLS) / (v_TB - v_LTB_star)
        if (H_LTB_star - H_LTB) < 1e-3:
            H_LTB = (H_LTB + H_LTB_star) / 2
            break
        H_LTB = H_LTB_star
    else:
        mylog.logger.warning('kaya模型的Taylor泡区计算未收敛')
        raise

    # 计算液塞长度与整个段塞单元之比
    ratio_LLS_LSU = 1 + (vsl - v_LLS * H_LLS) / (v_TB * (H_LLS - H_LTB))

    # 段塞区液体粘度
    rho_LS = rhol * (1 - H_GLS) + rhog * H_GLS
    mu_LS = mul * (1 - H_GLS) + mug * H_GLS

    # 计算混合流体的雷诺数
    NRem = rho_LS * vt * D / mu_LS
    # 摩擦阻力系数
    f = friction_moody(NRem, Delta)

    DP_g = rho_LS * g * np.sin(theta) * ratio_LLS_LSU
    # tauf 摩擦梯度损失项 τ: tau
    tauf = f * rho_LS * vt ** 2 / (2 * D) * ratio_LLS_LSU
    return DP_g, tauf


def kaya_gradient_I(g, D, theta, rhol, rhog, sigmal, vsl, vsg, mul, mug, vt, El, Delta):
    # 漂移速度
    v0 = (0.35 * np.sin(theta) + 0.54 * np.cos(theta)) * (g * (rhol - rhog) * D / rhol) ** 0.5
    # 计算Taylor泡速度
    # 与段塞流不同，冲击流vt的分布系数取值为1.0
    v_TB = vt + v0
    # 计算液塞区的空隙率H_GLS 和持液率H_LLS
    _temp = (g * sigmal * (rhol - rhog) / rhol ** 2) ** 0.25
    H_GLS = vsg / (1.126 * vt + 1.414 * _temp * np.sin(theta) ** 0.5)
    H_LLS = 1 - H_GLS

    # 计算液塞区气体流速
    v_GLS = vt + 1.414 * _temp * np.sin(theta) ** 0.5
    # 计算液塞区液体流速
    v_LLS = (vt - v_GLS * H_GLS) / (1 - H_GLS)

    # 计算Taylor泡区的液膜速度和截面空隙率
    # 迭代计算
    H_LTB = 1
    H_GTB = 1 - H_LTB
    for i in range(1000):
        v_LTB_star = -9.916 * (g * D * (1 - H_LTB ** 0.5))
        H_LTB_star = (v_TB - v_LLS) * (1 - H_GLS) / (v_TB - v_LTB_star)
        if (H_LTB_star - H_LTB) < 1e-3:
            H_LTB = (H_LTB + H_LTB_star) / 2
            break
        H_LTB = H_LTB_star
    else:
        mylog.logger.warning('kaya模型的Taylor泡区计算未收敛')
        raise

    # 计算液塞长度与整个段塞单元之比
    ratio_LLS_LSU = 1 + (vsl - v_LLS * H_LLS) / (v_TB * (H_LLS - H_LTB))

    # 段塞区液体粘度
    rho_LS = rhol * (1 - H_GLS) + rhog * H_GLS
    mu_LS = mul * (1 - H_GLS) + mug * H_GLS

    # 计算混合流体的雷诺数
    NRem = rho_LS * vt * D / mu_LS
    # 摩擦阻力系数
    f = friction_moody(NRem, Delta)

    DP_g = rho_LS * g * np.sin(theta) * ratio_LLS_LSU
    # tauf 摩擦梯度损失项 τ: tau
    tauf = f * rho_LS * vt ** 2 / (2 * D) * ratio_LLS_LSU
    return DP_g, tauf


def kaya_gradient_A(g, D, theta, return_info):
    f_SC, rho_C, v_SC, Z, delta = return_info

    DP_g = rho_C * g * np.sin(theta)
    # 计算气芯表观摩阻压降
    tau_SC = f_SC * rho_C * v_SC ** 2 / (2 * D) * Z / (1 - 2 * delta) ** 5
    return DP_g, tau_SC
