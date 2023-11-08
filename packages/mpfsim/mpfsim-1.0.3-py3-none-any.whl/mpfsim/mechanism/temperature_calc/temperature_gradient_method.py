#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/6/21 14:10
# @Author  : 马赫
# @Email   : 1692303843@qq.com
# @FileName: temperature_gradient_method.py


import numpy as np
from core import mylog, manager_config

from mechanism.temperature_calc.temperature_tools import comprehensive_heat_transfer_coefficient
from mechanism.property.black_oil_tools import f_Cpo, f_Cpw, f_Cpg
from mechanism.unit_conversion import unit_conversion as unit
from mechanism.data_control.well_data_entry import ParamsReader

from mechanism.property.manage_properties import ManageProperties


def temperature_calc(z, zD, zL, interp_func, _rhoo_15, Go, Gg, Gw, _epsilon=1):
    """
    温度迭代函数

    Args:
        z: 计算测深 (m) 200
        zD: 动液面测深 (m) 1200
        zL: 井筒的井底测量测深 (m) 2000
        interp_func: 生成器对象 函数字典 根据测深对各类参数进行插值和外推 params_value_z = interp_func(z)
        _rhoo_15: 15 °C时原油的密度 (kg/m3) 800
        Go: 油质量流量 (kg/s) 0.8
        Gg: 气质量流量 (kg/s) 0.4
        Gw: 水质量流量 (kg/s) 0.7
        _epsilon: 温度迭代允许误差 (K)

    Returns:
        T_z: 测深为z位置处的流体温度 (C)
    """

    l = zL - z  # 井底至地层某一深度的垂直距离 (m)
    params_value_z = interp_func(z)  # 测深为z时的其他值
    T_e = params_value_z['环境温度']  # 测深为z时的环境温度 (C)

    T_z_hypo = T_e  # 假设测深z处的井筒温度，与地层温度相等 (W/(m2•C))

    # m = 0.03  # 地温梯度 (C/m)  [0.03 ~ 0.035]
    m = T_e - interp_func(z - 1)['环境温度']

    r_ti = params_value_z['油管内径']  # 油管内表面半径 (m)
    r_to = r_ti + params_value_z['管壁厚度']  # 油管外表面半径 (m)

    r_ci_1 = interp_func(zL)['套管内径']  # 第1层套管的套管内半径 (m) [15 in]
    r_ci_j = params_value_z['套管内径']  # 第j层套管的套管内半径 (m) [15 in]
    r_co_j = params_value_z['套管外径']  # 第j层套管的套管外半径 (m) [17 in]
    r_cem_o_j = params_value_z['水泥环外径']  # 第j层套管的水泥环外半径(cement) (m) [35 in]

    # r_ti = unit.unit_length(r_ti, 'in', 'm')
    # r_to = unit.unit_length(r_to, 'in', 'm')
    #
    # r_ci_1 = unit.unit_length(r_ci_1, 'in', 'm')
    # r_ci_j = unit.unit_length(r_ci_j, 'in', 'm')
    # r_co_j = unit.unit_length(r_co_j, 'in', 'm')
    # r_cem_o_j = unit.unit_length(r_cem_o_j, 'in', 'm')

    k_an = params_value_z['套管导热系数']  # 环空液体或气体的导热系数 (W/(m•K))
    k_cem = params_value_z['水泥环导热系数']  # 水泥环导热系数 (J/(s•m•C))
    lambda_f = k_an  # 环空流体的导热系数 (W/(m•K))
    lambda_t = k_an  # 油管的导热系数 (W/(m•K))
    lambda_c_j = k_an  # 第j层套管所在套管的导热系数 (W/(m•K)) [10]
    lambda_cem_j = k_cem  # 第j层套管所在水泥环的导热系数 (W/(m•K)) [10]

    h_o = 700  # TODO ??? 油管内壁液膜的对流传热系数 (W/(m2•K))
    h_c = 700  # 油套环空的对流传热系数 (W/(m2•K))
    h_r = 700  # 油套环空的辐射传热系数 (W/(m2•K))

    # 综合传热系数 (W/(m2•C))
    # k_l (W/(m•C))  从油管中的流体至地层间单位管长的传热系数，需要从单位面积转为单位管长
    k_l = comprehensive_heat_transfer_coefficient(
        z, zD,
        r_ti, r_to, r_ci_1, r_ci_j, r_co_j, r_cem_o_j,
        lambda_t, lambda_c_j, lambda_cem_j, lambda_f,
        h_o, h_c, h_r,
    )

    for i_iter in range(100):  # 避免无法收敛
        # mylog.logger.debug(T_z_hypo)
        _T_z_hypo = unit.unit_temperature(T_z_hypo, 'C', 'K')
        # (J/(kg•C))
        Cpo = unit.unit_Cp(f_Cpo(_T_z_hypo, _rhoo_15), 'KJ/(kg•K)', 'J/(kg•K)')  # 油定压比热
        Cpg = unit.unit_Cp(f_Cpg(_T_z_hypo), 'KJ/(kg•K)', 'J/(kg•K)')  # 气定压比热
        Cpw = unit.unit_Cp(f_Cpw(_T_z_hypo), 'KJ/(kg•K)', 'J/(kg•K)')  # 水定压比热

        # 水当量 (W/C)
        W = Go * Cpo + Gg * Cpg + Gw * Cpw

        # 油井温度分布
        # T_d 产液井底温度 (C)
        # T_z = W * m / k_l * (1 - np.exp(-k_l / W * l)) + (T_d - m * l)
        # T_z = W * m / k_l * (1 - np.exp(-k_l / W * l)) + T_e
        T_fluid = W * m / k_l * (1 - np.exp(-k_l / W * l))
        T_z = T_fluid + T_e

        flag_convergence = abs(T_z - T_z_hypo) / T_z <= _epsilon

        # _text = '%s段, %s轮, Temperature: last %.3f, new %.3f C, delta %.4f C' % (
        #     l_i, i_iter, T_z_hypo, T_z, T_z - T_z_hypo
        # )
        # mylog.logger.debug(_text)
        T_z_hypo = T_z

        if flag_convergence:
            # mylog.logger.debug('第%s段 经过%s轮收敛' % ((l_i + 1), i_iter))

            # _text = f'T_fluid: {T_fluid}, W: {W}, Cpo: {Cpo}, m: {m}, k_l: {k_l}, coeff: {(np.exp(-k_l / W * l))},'
            # mylog.logger.debug(_text)
            break



    else:
        mylog.logger.error('无法收敛')

    return T_z


if __name__ == '__main__':

    params_reader = ParamsReader(manager_config.Params_info)
    params_dict = params_reader.params_dict
    params_value = params_dict['value']
    # 根据测深对各类参数进行插值和外推
    interp_func = params_reader.get_z_data_interp()

    # %% 待使用变量
    pass
    # k_e = 1  # 地层导热系数 (J/(s•m•C))
    # alpha = 1  # 地温梯度 (C/m)
    #
    # w = 1  # 气体质量流量 (kg/s)
    # T_gs = 20  # 年平均地表温度 (C)
    # r_h = 1  # 井眼半径 (m)
    # alpha1 = 1  # 地层热扩散系数 (m2/s)
    # t = 1  # 生产时间 (s)
    # theta = 0  # ??? 与垂直方向的井斜角 (°)
    #
    # P_wh = 1  # 井口压力 (Pa)
    # T_wh = 1  # 井口注气温度 (C)
    #
    # epsilon_to = 1  # 油管外表面的辐射传热系数 (W/(m•C))
    # epsilon_ci = 1  # 套管内表面的辐射传热系数 (W/(m•C))
    # sigma = 5.673e-8  # Stefan-Boltzman常数 (W/(m2•K4))
    # g = 9.8  # 重力加速度 (m/s2)
    # L = 1  # 油管长度 (m)
    # rho = 1  # 油管密度 (kg/m3)
    # C = 11 * 1e-6  # 油管柱线膨胀系数 (1/C)
    # P_e0 = 1  # 井口油管外压 (Pa)
    # rhog = 1  # 气体密度 (kg/m3)
    # r = 1  # r_ti与r_to间的任意半径 (m)
    # c_pan = 1  # 环空液体或气体在平均温度下的热容量 (KJ/(KJ•K))
    # F_gl = 1  # 气液比 (m3/m3)
    # API = 1  # 原油API度 (°)
    # U_to_temp = 1  # 假定的井筒总传热系数 (W/(m•C))
    # f_t = 1  # 瞬态传热函数 (-)
    # T_h = 1  # 水泥环的壁温 (C)
    # T_ci = 1  # 套管温度 (C)
    # T_an = 1  # 环空流体的平均温度 (C)
    # beta = 1  # 平均温度下的体积膨胀系数 (1/C)
    # Grashof = 1  # 格拉晓夫数 (-)
    # C_pan = 1  # 环空流体的定压比热 (KJ/(kg•C))
    # Prandtl = 1  # 普朗特数 (-)
    # U_to = 1  # 计算得到的井筒总的传热系数 (W/(m•C))
    # C_p = 1  # 井筒流体的定压比热 (KJ/(kg•C))
    # phi = 1  # 焦耳-汤姆森系数 (-)
    pass

    # %% 测试用例

    # 临时物性管理器
    # Pb = unit.unit_pressure(15)  # 泡点压力 (Pa)
    Pb = unit.unit_pressure(20)  # 泡点压力 (Pa)
    rho_ro = 0.876  # 原油相对密度 (-)
    rho_rg = 0.6  # 天然气的相对密度 (-)
    rho_rw = 1  # 水的相对密度 (-)
    method_dict_input = {}  # 黑油模型用户输入所采用的方法的部分信息 (-)

    update_dict = {
        'P': unit.unit_pressure(2, 'MPa', 'MPa'),
        'T': 293,
        'Pb': unit.unit_pressure(Pb, 'Pa', 'MPa'),
        'fw': 0.1,
        'Rp': 150,  # TODO 暂未用到
        'rho_ro': rho_ro,
        'rho_rg': rho_rg,
        'rho_rw': rho_rw,
        'method_dict_input': method_dict_input,
    }

    manager_p = ManageProperties(manager_config.variable_info)
    manager_p.update_series(update_dict)

    # %% 常规油井井筒温度分布

    # 油气水质量流量 (kg/s)
    Go = 1.1
    Gg = 0.2
    Gw = 0.9

    _T_degree15 = 15  # 15 摄氏度时原油的密度
    _rhoo_15 = manager_p._rhoo_15

    _epsilon = 1  # ε收敛误差(K)

    # %% 段内温度迭代

    l_i = 1  # 第i段

    z = 200  # 计算测深 (m)
    zD = 1200  # 动液面测深 (m)
    zL = params_value['井斜数据']['测深'].values[-1]  # 井筒的井底测量测深 (m)
    T_z = temperature_calc(z, zD, zL, interp_func, _rhoo_15, Go, Gg, Gw, _epsilon=1)
    print(T_z)

    # %% 沿程温度剖面

    for z in range(2000, 0, -500):
        T_z = temperature_calc(z, zD, zL, interp_func, _rhoo_15, Go, Gg, Gw, _epsilon=1)
        print(T_z)
