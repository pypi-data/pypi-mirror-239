#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/6/22 0:04
# @Author  : 马赫
# @Email   : 1692303843@qq.com
# @FileName: temperature_tools.py

import numpy as np
from core.constants import lg, ln, pi
from core import mylog


def comprehensive_heat_transfer_coefficient(
        z, zD,
        r_ti, r_to, r_ci_1, r_ci_j, r_co_j, r_cem_o_j,
        lambda_t, lambda_c_j, lambda_cem_j, lambda_f,
        h_o, h_c, h_r,

):
    """
    综合传热系数计算模块

    •: Alt + 数字键盘0149

    导热系数 λ: lambda (W/(m•K))

    Q = dT / R = dT * λ * S / L
    R = L / λ • S

    Q: 热量 (W) 1 W = 1 J/s
    dT: 温差 (K) K ~ C
    R: 热阻 (K/W)
    L: 厚度 (m)
    λ: 导热系数 (W/(m•K)) == (W/(m•C))
    S: 面积 (m2)


    传热系数 U: (W/(m2•K))

    U = λ / L = 1 / R

    Abbreviation:
        t: tubing 油管, c: casing 套管, cem: cement 水泥环, f: fluid 流体

        o: outside 外侧, i: inside 内侧

        lambda: λ 导热系数, h: heat 传热系数

        h_c: convective 对流传热系数, h_r: radiant 辐射传热系数

    Args:
        z: 计算深度 (m) 200
        zD: 动液面深度 (m) 1200

        r_ti: 油管内表面半径 (m) 0.15
        r_to: 油管外表面半径 (m) 0.1625
        r_ci_1: 第1层套管的套管内半径 (m) 0.225
        r_ci_j: 第j层套管的套管内半径 (m) 0.225
        r_co_j: 第j层套管的套管外半径 (m) 0.425
        r_cem_o_j: 第j层套管的水泥环外半径(cement) (m) 0.475

        lambda_t: 油管的导热系数 (W/(m•K)) 10
        lambda_c_j: 第j层套管所在套管的导热系数 (W/(m•K)) 10
        lambda_cem_j: 第j层套管所在水泥环的导热系数 (W/(m•K)) 10
        lambda_f: 环空流体的导热系数 (W/(m•K)) 10

        h_o: TODO ??? 油管内壁液膜的对流传热系数 (W/(m2•K)) 700
        h_c: 油套环空的对流传热系数 (W/(m2•K)) 700
        h_r: 油套环空的辐射传热系数 (W/(m2•K)) 700


    Returns:
        U: 综合传热系数 (W/(m2•K))

    """
    # R1 套管、水泥环的总导热系数 (K/W)
    R1 = 1 / (2 * pi) * (ln(r_co_j / r_ci_j) / lambda_c_j + ln(r_cem_o_j / r_co_j) / lambda_cem_j)

    # R2 环空中流体的导热热阻、或环空中空气的对流和辐射热阻 (K/W)
    # R2 环空存在流体的流体的导热热阻，或者环空为空气的自然对流和辐射换热热阻 (K/W)
    # 计算深度在动液面以下是流体导热,动液面以上为空气导热
    if z > zD:
        # 环境（环空）为流体情况下热传导过程的热阻 (K/W)
        R2 = 1 / (2 * pi * lambda_f) * ln(r_ci_1 / r_to)
    else:
        # 环境（环空）为空气情况下热对流`h_c`和热辐射`h_r`过程的热阻 (K/W)
        R2 = 1 / (2 * pi * (h_c + h_r) * r_to)

    # R3 油管内流与油管壁间的对流换热热阻 + 油管内外壁之间的导热热阻 (K/W)
    R3 = 1 / (2 * pi * h_o * r_ti) + 1 / (2 * pi * lambda_t) * ln(r_to / r_ti)

    # 井筒指定位置H处的总热阻 (K/W)
    R = R1 + R2 + R3
    # 计算井筒指定深度H处的综合传热系数 (W/(m2•C))
    U = 1 / R
    return U
