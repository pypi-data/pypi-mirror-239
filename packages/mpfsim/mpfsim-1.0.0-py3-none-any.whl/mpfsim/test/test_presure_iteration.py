#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/6/2 14:57
# @Author  : 马赫
# @Email   : 1692303843@qq.com
# @FileName: presure_iteration.py

import copy
import os

import numpy as np

from mechanism.data_control.well_data_entry import ParamsReader
from mechanism.property.manage_properties import ManageProperties
from mechanism.pressure_calc.pressure_gradient_method import *
from mechanism.temperature_calc.temperature_gradient_method import temperature_calc
from mechanism.unit_conversion import unit_conversion as unit

from core.constants import g
from core.tool import *

# 对象
from core import mylog, manager_config, tracker

# %% 管理器初始化

os.chdir(manager_config.work_dir)  # FIXME 开发用的目录切换

# 日志管理器: 记录等级设置
mylog.setting('console', verbose=1)
mylog.logger.debug(f'============ {manager_config.work_dir}')

# 变量跟踪管理器: 清空全部信息
tracker.clear_values()

# 变量文件相对路径
variable_info = manager_config.variable_info
# 标准状况
sc_dict = manager_config.sc


def multiphase_flow_iteration(
        D, Delta, angle,
        ql_sc, P_up, zD, zL, interp_func,
        lt, fw, Rp, manager_property,
        method_pressure='Beggs_Brill',
        sc_P=0.101 * 1e6, sc_T=0 + 273.15, sc_Z=1,
        delta_l=100, delta_P_hypo=1e6, is_fit=False, _epsilon=1,
):
    """
    多相管流沿程温压迭代计算
    Args:
        # ------------------------ 随管道节点变化的参数 ------------------------

        D: 管道直径 (m) 0.05
        Delta: Δ管壁相对粗糙度 (-) 0.0018
        angle: 全局井斜角 (deg) [0~180°] if angle == None: angle根据参数文件自动计算

        # ------------------------ 温度迭代参数 ------------------------
        zD: 动液面测深 (m) 1200
        zL: 井筒的井底测深 (m) 2000
        interp_func: 插值和外推函数 (-) 输入z测深，得到字典，每个键为外推函数的插值结果

        # ------------------------ 重要参数 ------------------------
        ql_sc: 标况的液体体积流量 (sm^3/s) 0.0011
        P_up: 管段上游压力 (Pa) 30000000
        lt: 管线总长 (m) 3000
        fw:  标况的含水率 (-) 0.7  # 影响段塞流连续液相是油或是水
        Rp: 生产气油比 (m^3/m^3) 30

        # ------------------------ 物性模型参数 ------------------------
        manager_property: ManageProperties(BlackOilProperty)  # 需要提前更新好所有关键参数

            Pb = unit.unit_pressure(15)  # 泡点压力 (Pa)
            rho_ro = 0.876  # 原油相对密度 (-)
            rho_rg = 0.6  # 天然气的相对密度 (-)
            rho_rw = 1  # 水的相对密度 (-)
            method_dict_input = {}  # 黑油模型用户输入所采用的方法的部分信息 (-)

            update_dict = {
                'P': unit.unit_pressure(P_up, 'Pa', 'MPa'),
                'T': T_up,
                'Pb': unit.unit_pressure(Pb, 'Pa', 'MPa'),
                'fw': fw,
                'Rp': Rp,  # TODO 暂未用到
                'rho_ro': rho_ro,
                'rho_rg': rho_rg,
                'rho_rw': rho_rw,
                'method_dict_input': method_dict_input,
            }
            manager_property = ManageProperties(variable_info)
            manager_property.update_series(update_dict)


        # ------------------------ 计算相关式 ------------------------
        method_pressure: str 'Orkiszewski', 'Hagedorn_Brown' 垂直管流
        method_pressure: str 'Beggs_Brill', 'Kaya' 倾斜管流
        method_pressure: str 'Lockhart_Martinelli', 'Dukler' 水平管流
        method_pressure: str 'single_phase' 单相任意角度管流

        # ------------------------ 基本不变参数 ------------------------
        sc_P: 标况压力 (MPa) 0.101*1e6
        sc_T: 标况温度 (K) 0 + 273.15
        sc_Z: 标况天然气气体压缩因子 (-) 1

        delta_l: 迭代管线步长 (m) 50~100
        delta_P_hypo: 一段管段内假设的压力降落 (Pa) 1e6 # 每千米垂直10MPa
        is_fit: 是否由拟合公式计算 False
        _epsilon: ε收敛误差 (Pa) 1

    Returns:
        l_list: 管线计算节点沿程分布
        P_list: 压力沿程分布
        T_list: 温度沿程分布
        info_list: 其他字典信息
    """

    # ------------------------ 初始化 ------------------------
    # if method_dict is None:
    #     method_dict = {
    #         'pressure_gradient': ['Orkiszewski', 'Beggs_Brill']
    #     }

    # 稳态流的管线中各个位置处的折算到标况后的体积流量应该处处相等

    qo_sc = (1 - fw) * ql_sc  # 标况的油相体积流量 (sm^3/s)

    rhol = manager_property.rhol
    rhog = manager_property.rhog
    Rs = manager_property.Rs
    qg_sc = qo_sc * (Rp - Rs)

    _rhoo_15 = manager_property._rhoo_15

    # 稳态流动认为每个迭代计算区间内的产量折算到标况下是相等的
    # 即管线沿程的质量流量相等
    # 混合物总质量流量 (kg/s) 1.4769

    # 计算油、气、水、混合物总质量流量 (kg/s)
    # 温度迭代所需参数
    Go = rhol * ql_sc * (1 - fw)
    Gw = rhol * ql_sc * fw
    Gg = rhog * qg_sc

    # Gt = rhol * ql_sc + rhog * qg_sc
    Gt = Go + Gw + Gg

    # 管线沿程设置计算节点 [头, 中途, ..., 尾]
    # 计算总分段数 四舍五入
    N = round(lt / delta_l) + 1

    # 动态节点长度
    N = max(N, 10)  # 当N不足10个节点的时候，最少将其9等分，形成10个节点，其中9个计算节点
    N = min(N, 100)  # 总节点数上限

    # len(l_list) == N + 1 将起点和终点都记录在沿程列表中
    l_list = np.linspace(0, lt, N)
    # 给最后一个截面赋坐标
    dl_list = np.diff(l_list)

    # 管段上游（井底）温度 (K)
    T_up = unit.unit_temperature(interp_func(zL)['环境温度'], 'C', 'K')

    # 各计算节点位置处的 压力、压力梯度、温度 记录列表
    P_list = [P_up]
    T_list = [T_up]
    # ------------------------ 是否选择拟合分支 ------------------------

    # 判断是否由拟合公式计算
    if is_fit:
        # TODO 若由拟合公式计算，则转到○13
        pass
    else:
        # TODO 否则计算每一段流道的平均压力：
        pass

    # ------------------------ 迭代过程 ------------------------

    tracker.add_value('l_%s' % method_pressure, 0)
    tracker.add_value('P_%s' % method_pressure, P_up)
    tracker.add_value('T_%s' % method_pressure, T_up)

    tracker.add_value('l_list', l_list)

    # 计算第`i_segment`段的数据
    for i_segment, l in enumerate(l_list[1:], start=1):
        print(i_segment)
        mylog.logger.debug('开始计算第%s/%s段' % ((i_segment + 1), len(dl_list)))
        dl = l_list[i_segment] - l_list[i_segment - 1]
        # 当前段内的计算测深 (m)
        # l_list 从0开始 z从最长距离开始
        z = zL - l_list[i_segment]

        # ------------------------ 随管道节点变化的参数 ------------------------
        params_value_z = interp_func(z)  # 测深为z时的其他值

        # 井斜角 [0~180°] -> 管线与水平正方向的角度 [90~-90°] -> cos(井斜角) [1~-1]
        # 井斜角 + 管线与水平正方向的角度 = 90°
        # 井斜角

        if angle is None:
            angle = params_value_z['井斜角']

        # 管线与水平正方向的弧度值
        theta = np.deg2rad(90 - angle)

        # TODO 这里段数序号最大的情况大于总段数了
        mylog.logger.debug('开始计算第%s/%s段' % ((i_segment + 1), len(dl_list)))

        # 1 根据假设增量计算的下游压力为:
        P_down = P_up - delta_P_hypo
        T_down = None
        for i_iter in range(100):  # 避免无法收敛
            # 2 计算该段的平均压力
            P_segment = (P_up + P_down) / 2
            if P_segment < 0:
                # P_down = None
                break

            # 3 计算该段的平均温度
            # 调用温度场计算函数计算第`i_segment`段的流体温度T_down
            # _rhoo_15 15°C时原油的密度 受压力等参数的影响
            # TODO 可能是这里缓存函数模式？
            manager_property.update()
            _rhoo_15 = manager_property._rhoo_15

            # 温度计算
            _T = temperature_calc(z, zD, zL, interp_func, _rhoo_15, Go, Gg, Gw)
            T_down = unit.unit_temperature(_T, 'C', 'K')
            T_segment = (T_up + T_down) / 2

            # 4 计算该段的平均物性参数
            update_dict = {
                # 物性管理器中压力MPa单位，临时改变单位
                'P': unit.unit_pressure(P_segment, 'Pa', 'MPa'),
                'T': T_segment,
            }
            manager_property.update_series(update_dict)

            rhog = manager_property.rhog
            rhol = manager_property.rhol
            mul = manager_property.mul
            mug = manager_property.mug
            sigmal = manager_property.sigmal
            Bo = manager_property.Bo
            Z = manager_property.Z
            Rs = manager_property.Rs

            # 物性模型的内置公式单位与多相管流模型的内置公式单位 不统一
            # 此次临时从物性转为多相管流
            mul = unit.unit_mu(mul, u_in='mPa•s', u_to='Pa•s')
            mug = unit.unit_mu(mug, u_in='mPa•s', u_to='Pa•s')
            sigmal = unit.unit_sigma(sigmal, u_in='mN/m', u_to='N/m')

            # 5 计算PT条件的液相流量
            ql_segment = qo_sc * Bo / (1 - fw)

            # 6 计算PT条件的气体流量
            qg_sc = qo_sc * (Rp - Rs)
            qg_sc = max(qg_sc, 0)
            # 正常情况 Rp 应该大于 Rs
            # mylog.logger.warning(f'Rp {Rp} < Rs {Rs}')

            qg_segment = unit.cond_q_volume_rate(
                qg_sc, sc_P, sc_T, sc_Z,
                P_segment, T_segment, Z
            )

            # 根据用户选择的多相管流计算模型求解压力梯度DPt
            DPt, info = pressure_gradient(
                P_segment, P_up, P_down, g, D, Delta,
                rhol, rhog, mul, mug, sigmal, fw, Gt,
                ql_segment, qg_segment,
                theta, method_pressure
            )
            # 10 当前管段总压降为：
            DP = DPt * dl

            # 11 计算该管段的下游压力
            P_down_new = P_up - DP
            # if np.isnan(P_down_new):
            #     raise

            flag_convergence = abs(P_down_new - P_down) <= _epsilon

            # _text = '%s段, %s轮, Pressure: last %.3f, new %.3f MPa, delta %.4f KPA' % (
            #     i_segment, i_iter, P_down / 1e6, P_down_new / 1e6, (P_down - P_down_new) / 1e3
            # )
            # mylog.logger.debug(_text)

            # 一次更新到位可能导致陷入震荡
            # P_down = P_down_new
            loss = (P_down - P_down_new)
            lr = max(min(-0.05 * i_iter + 1, 1), 0.6)

            P_down = P_down - loss * lr

            if flag_convergence:
                mylog.logger.debug('第%s段 经过%s轮收敛' % ((i_segment + 1), i_iter))
                break
        else:
            mylog.logger.error('无法收敛')

        # 下游压力 < 0, 无法举升，退出多相管流计算，温度场计算同步停止
        if P_down < 0:
            # P_down = None
            break

        P_up = P_down
        T_up = T_down
        P_list.append(P_down)
        T_list.append(T_down)

        mylog.logger.debug('iter -> P: %.3f, rhol: %.3f' % (P_down / 1e6, rhol))

        tracker.add_value('l_%s' % method_pressure, l)
        tracker.add_value('P_%s' % method_pressure, P_down)
        tracker.add_value('T_%s' % method_pressure, T_down)

    # ------------------------ 拟合过程 ------------------------

    # TODO ○13 由拟合公式进行计算
    # （1）将全部流道分段，以管道入口压力做为第一段入口压力。
    # （2）假设当前段的出口压力，计算当前段的平均压力和平均温度：

    return


# %% 参数

def mpf(method_list, angle=None):
    # method_list = ['Orkiszewski', 'Beggs_Brill', 'Kaya']

    # ------------------------ 温度迭代加载类 ------------------------
    params_reader = ParamsReader(manager_config.Params_info)
    params_dict = params_reader.params_dict
    params_value = params_dict['value']
    # 根据测深对各类参数进行插值和外推
    interp_func = params_reader.get_z_data_interp()

    # ------------------------ 温度迭代参数 ------------------------
    zD = 1200  # 动液面深度 (m)
    zL = params_value['井斜数据']['测深'].values[-1]  # 井筒的井底测量深度 (m)
    # 管段上游（井底）温度 (K)
    T_up = unit.unit_temperature(interp_func(zL)['环境温度'], 'C', 'K')

    # ------------------------ 随管道节点变化的参数 ------------------------
    # D = 0.05  # 管道直径 (m)
    D = 0.05  # 管道直径 (m)
    epsilon = 4.57 * 1e-5  # epsilon: ε 管壁绝对粗糙度 (m)
    Delta = 2 * epsilon / D  # Delta: Δ管壁相对粗糙度 (-)
    # theta = unit.unit_angle(80, u_in='deg', u_to='rad')  # 管线与水平方向的夹角 (rad) [-pi/2, pi/2]

    # ------------------------ 重要参数 ------------------------
    # ql_sc = unit.unit_q_volume_rate(50, 'm3/d', 'm3/s')  # 标况的液体体积流量 (sm^3/s)
    ql_sc = unit.unit_q_volume_rate(30, 'm3/d', 'm3/s')  # 标况的液体体积流量 (sm^3/s)
    # P_up = unit.unit_pressure(40, 'MPa', 'Pa')  # 管段上游压力 (Pa)
    P_up = unit.unit_pressure(70, 'MPa', 'Pa')  # 管段上游压力 (Pa)
    # lt = 2010  # 管线总长 (m) 3000
    lt = 5016  # 管线总长 (m) 3000
    fw = 0.9  # 标况的含水率 (-) 0.7  # 影响段塞流连续液相是油或是水
    # Rp = 100  # 生产气油比 (m^3/m^3)
    Rp = 10000 / 30  # 生产气油比 (m^3/m^3)

    # ------------------------ 物性模型参数 ------------------------

    # Pb = unit.unit_pressure(15)  # 泡点压力 (Pa)
    Pb = unit.unit_pressure(20, 'MPa', 'Pa')  # 泡点压力 (Pa)
    # rho_ro = 0.876  # 原油相对密度 (-)
    rho_ro = 0.85  # 原油相对密度 (-)
    rho_rg = 0.6  # 天然气的相对密度 (-)
    rho_rw = 1  # 水的相对密度 (-)
    method_dict_input = {}  # 黑油模型用户输入所采用的方法的部分信息 (-)

    update_dict = {
        'P': unit.unit_pressure(P_up, 'Pa', 'MPa'),
        'T': T_up,
        'Pb': unit.unit_pressure(Pb, 'Pa', 'MPa'),
        'fw': fw,
        'Rp': Rp,  # TODO 暂未用到
        'rho_ro': rho_ro,
        'rho_rg': rho_rg,
        'rho_rw': rho_rw,
        'method_dict_input': method_dict_input,
    }
    manager_p = ManageProperties(variable_info)
    manager_p.update_series(update_dict)

    # ------------------------ 基本不变参数 ------------------------
    # sc_dict = {
    #     'P': 0.101,  # 标况压力 (MPa)
    #     'T': 0 + 273.15,  # 标况温度 (K)
    #     'Z': 1,  # 标况天然气压缩系数 (-)
    # }
    sc_P = unit.unit_pressure(sc_dict['P'], 'MPa', 'Pa')
    sc_T = sc_dict['T']
    sc_Z = sc_dict['Z']

    # ------------------------ 多相流计算迭代参数 ------------------------
    delta_l = 100  # 迭代管线步长 (m) 50~100
    delta_P_hypo = 1e5  # 一段管段内假设的压力降落 (Pa)  # 每千米垂直10MPa
    is_fit = False  # 是否由拟合公式计算

    # method_list = ['Orkiszewski', 'Beggs_Brill', 'Kaya']
    # method_list = ['Kaya']

    # 变量跟踪管理器: 清空全部信息
    tracker.clear_values()
    for method in method_list:
        multiphase_flow_iteration(
            D, Delta, angle,
            ql_sc, P_up, zD, zL, interp_func,
            lt, fw, Rp, copy.deepcopy(manager_p),
            method_pressure=method, sc_P=sc_P, sc_T=sc_T,
            sc_Z=sc_Z, delta_l=delta_l, delta_P_hypo=delta_P_hypo,
            is_fit=is_fit
        )


# %%
import time

t1 = time.time()

angle = 0  # 井斜角 (deg) [0~180°]

method_list = ['Orkiszewski']  # 垂直
method_list = ['Beggs_Brill', 'Kaya']  # 倾斜
# method_list = ['Lockhart_Martinelli', 'Dukler']  # 水平
method_list = ['Beggs_Brill', ]
mpf(method_list, angle)

time_consume = time.time() - t1
mylog.logger.info('多相管流计算耗时: %.3fs' % time_consume)

# %% 总距离-压力曲线

x_data_list = []
y_data_list = []
for method in method_list:
    draw_var = 'l_%s' % method
    x_data = tracker.get_values(draw_var)

    draw_var = 'P_%s' % method
    y_data = tracker.get_values(draw_var)
    y_data = unit.unit_pressure(y_data, 'Pa', 'MPa')

    x_data_list.append(x_data)
    y_data_list.append(y_data)

plt_dict = {
    'legend_list': method_list,
    'xlabel': '总距离 (m)',
    'ylabel': '压力 (MPa)',
    'title': '总距离-压力曲线-%s°' % angle,
}

draw_data_curve(x_data_list, y_data_list, plt_dict=plt_dict)

# %% 总距离-压力增量曲线

x_data_list = []
y_data_list = []
for method in method_list:
    draw_var = 'l_%s' % method
    x_data = tracker.get_values(draw_var)

    draw_var = 'P_%s' % method
    y_data = tracker.get_values(draw_var)
    y_data = unit.unit_pressure(y_data, 'Pa', 'MPa')

    x_data_list.append(x_data[:-1])
    y_data_list.append(np.diff(y_data))

plt_dict = {
    'legend_list': method_list,
    'xlabel': '总距离 (m)',
    'ylabel': '压力 (MPa)',
    'title': '总距离-压力增量曲线-%s°' % angle,
}

draw_data_curve(x_data_list, y_data_list, plt_dict=plt_dict)

# %% 总距离-温度曲线

x_data_list = []
y_data_list = []
for method in method_list:
    draw_var = 'l_%s' % method
    x_data = tracker.get_values(draw_var)

    draw_var = 'T_%s' % method
    y_data = tracker.get_values(draw_var)
    y_data = unit.unit_temperature(y_data, 'K', 'C')

    x_data_list.append(x_data)
    y_data_list.append(y_data)

plt_dict = {
    'legend_list': method_list,
    'xlabel': '总距离 (m)',
    'ylabel': '温度 (C)',
    'title': '总距离-温度曲线-%s°' % angle,
}

draw_data_curve(x_data_list, y_data_list, plt_dict=plt_dict)

# %% 总距离-温度增量曲线

x_data_list = []
y_data_list = []
for method in method_list:
    draw_var = 'l_%s' % method
    x_data = tracker.get_values(draw_var)

    draw_var = 'T_%s' % method
    y_data = tracker.get_values(draw_var)
    y_data = unit.unit_temperature(y_data, 'K', 'C')

    x_data_list.append(x_data[:-1])
    y_data_list.append(np.diff(y_data))

plt_dict = {
    'legend_list': method_list,
    'xlabel': '总距离 (m)',
    'ylabel': '温度 (C)',
    'title': '总距离-温度增量曲线-%s°' % angle,
}

draw_data_curve(x_data_list, y_data_list, plt_dict=plt_dict)
