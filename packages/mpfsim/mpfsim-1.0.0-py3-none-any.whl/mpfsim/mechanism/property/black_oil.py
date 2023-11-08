#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/6/22 22:23
# @Author  : 马赫
# @Email   : 1692303843@qq.com
# @FileName: black_oil.py

from mechanism.property.black_oil_tools import *
from mechanism.unit_conversion import unit_conversion as unit
from core.tool_expert import StateParam


# %% 黑油模型各类参数管理类


class BlackOilProperty:
    """黑油模型各类参数管理类"""

    def __init__(self, *arg):
        self.arg = arg

        # ====================== 输入参数 ======================

        self.P = 30  # 绝对压力 (MPa)
        self.T = 20 + 273  # 绝对温度 (K)
        self.Pb = 10  # 泡点压力 (MPa)

        self.fw = 0.1  # 含水率 (无因次-%) （体积含水率）
        self.Rp = 600  # 生产油气比 (m3/m3) # TODO 暂未用到

        self.rho_ro = 0.9  # 原油的相对密度 (无因次-小数)
        self.rho_rg = 0.6  # 天然气的相对密度 (无因次-小数)
        self.rho_rw = 1.0  # 水相相对密度 (无因次-小数)

        # 相关式方法可用字典 不可修改
        self.__method_support_list = {
            'Rs': ['Auto', 'Lasater', 'Standing', 'Vazquez_Beggs', 'Glaso', 'Marhoun'],
            'Bo': {
                '饱和原油体积系数': ['Standing', 'Vazquez_Beggs', 'Glaso', 'Marhoun', 'Ahmed'],
                '不饱和原油体积系数': ['Vazquez_Beggs', 'Ahmed'],
            },
            'rhoo': {
                '饱和原油密度计算方法': ['Standing'],
                '不饱和原油密度计算方法': ['Vazquez_Beggs'],
            },
            'muo': {
                '脱气原油粘度计算方法': ['Beggs_Robinson'],
                '饱和原油粘度计算方法': ['Beggs_Robinson'],
                '不饱和原油粘度计算方法': ['Vazquez_Beggs'],
            },
        }
        # 默认相关式方法字典 不可修改
        self.__default_method_dict = {
            'Rs': 'Auto',
            'Bo': {
                '饱和原油体积系数': 'Standing',
                '不饱和原油体积系数': 'Vazquez_Beggs',
            },
            'rhoo': {
                '饱和原油密度计算方法': 'Standing',
                '不饱和原油密度计算方法': 'Vazquez_Beggs',
            },
            'muo': {
                '脱气原油粘度计算方法': 'Beggs_Robinson',
                '饱和原油粘度计算方法': 'Beggs_Robinson',
                '不饱和原油粘度计算方法': 'Vazquez_Beggs',
            },
        }

        # 用户输入所采用的方法的部分信息
        self.method_dict_input = {}
        self.method_dict = {}

        # ====================== 可选的其他参数 ======================

        self.P_sep = 0.791  # 分离器操作压力 (MPa)
        self.T_sep = 20 + 273.15  # 分离器操作温度 (K)

        # 相关式校正方法信息录入字典
        self.calibrate_dicts = {
            'muo': {
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
            },
        }

        self.is_condensate = False  # 是否为凝析气
        self.is_wax = False  # 是否含蜡
        # self.yH2S = 0.5  # 天然气中 H2S 的摩尔分数 (小数)
        # self.yCO2 = 0.5  # 天然气中 H2S 的摩尔分数 (小数)
        # self.B = 64.065  # 天然气中 H2S 的摩尔数 (小数)

        # ====================== 初始化参数 ======================

        self.Rs = 145.77  # 溶解气油比 (m3/m3)
        self.Rsb = 29.83  # 在泡点压力时天然气在原油中的溶解气油比 (m3/m3)

        self.Bo = 1.27  # 原油体积系数 Bo (m3/m3)  # TODO 暂未用到

        self.rhoo = 788.14  # 原油密度 (kg/m3)
        self.rhow = 1000.00  # 水相密度 (kg/m3)
        self.rhol = 809.11  # 天然气密度 (kg/m3)
        self.rhog = 253.19  # 水相密度 (kg/m3)

        self.muo = 9.20  # 原油粘度 (mPa·s)
        self.muw = 1.2  # 水相粘度 (mPa·s)
        self.mul = 9.20  # 液相粘度 (mPa·s)
        self.mug = 0.04  # 天然气粘度 (mPa·s)

        self.sigmao = 1.54  # σ_o 原油-天然气的表面张力 (mN/m)
        self.sigmaw = 0.6  # σ_w 气-水表面张力 (mN/m)
        self.sigmal = 0.7  # σ_l 油水混合液表面张力 (mN/m)

        self.Mg = 17.37  # 天然气的平均分子量 (无因次) TODO 暂未用到

        self.Ppc = 4.64  # 天然气的拟临界压力 (MPa)
        self.Tpc = 199.18  # 天然气的拟临界温度 (K)

        self.Z = 0.887  # 天然气的偏差系数 (无因次)  # 迭代计算 0.85

        self.Co = 185.86  # 不饱和原油的等温压缩系数 (1/MPa)
        self.Cg = 0.025  # 天然气的等温压缩系数 (1/MPa)

        self.Cpo = 1.97  # 原油的比热 (KJ/(kg·K))
        self.Cpw = 4.20  # 水的比热 (KJ/(kg·K))
        self.Cpg = 111  # 气体的比热 (KJ/(kg·K))
        self.Cpo_wax = 2.114  # 含蜡原油经验公式估算 (J/(kg·K))

        self.update()

    def update(self):
        """

        输入参数
        self.X -> P, T, Pb, fw, Rp, rho_ro, rho_rg, rho_rw=[1.0], method_dict_input={}
        TODO 向量化更新

        """
        self.update_method_dict()

        self.Rs = f_Rs(self.P, self.T, self.Pb, self.rho_ro, self.rho_rg, self.method_dict['Rs'], self.P_sep,
                       self.T_sep)
        self.Rsb = f_Rs(self.Pb, self.T, self.Pb, self.rho_ro, self.rho_rg, self.method_dict['Rs'], self.P_sep,
                        self.T_sep)

        self.Bo = f_Bo(self.P, self.T, self.Pb, self.Rs, self.rho_ro, self.rho_rg,
                       self.method_dict['Bo'], self.P_sep, self.T_sep
                       )

        self.rhoo = f_rhoo(self.P, self.T, self.Pb, self.Rs, self.rho_ro, self.rho_rg,
                           self.method_dict['rhoo'], self.P_sep, self.T_sep
                           )
        self.rhow = f_rhow(self.rho_rw)
        self.rhol = f_rhol(self.rhoo, self.rhow, self.fw)
        self.rhog = f_rhog(self.P, self.T, self.rho_rg, self.Z)

        self.muo = f_muo(self.P, self.T, self.Pb, self.Rs, self.rho_ro, self.method_dict['muo'],
                         self.calibrate_dicts['muo'])
        self.muw = f_muw(self.T)
        self.mul = f_mul(self.muo, self.muw, self.fw)
        self.mug = f_mug(self.P, self.T, self.Ppc, self.Tpc, self.rho_rg)

        self.sigmao = f_sigmao(self.P, self.T, self.rho_ro)
        self.sigmaw = f_sigmaw(self.P, self.T)
        self.sigmal = f_sigmal(self.sigmao, self.sigmaw, self.fw)

        self.Mg = f_Mg(self.rho_rg)

        self.Ppc, self.Tpc = f_pseudo_critical_gas(self.rho_rg, self.is_condensate)
        # self.Ppc_prime, self.Tpc_prime = f_pseudo_critical_gas_calibration(self.Ppc, self.Tpc, self.yH2S, self.yCO2,
        self.Z = f_Z(self.P, self.T, self.Ppc, self.Tpc, Z_init=self.Z)  # 迭代计算

        # 等温压缩系数计算
        self.Co = f_Co(self.T, self.Rsb, self.rho_ro, self.rho_rg, self.P_sep, self.T_sep)
        self.Cg = f_Cg(self.P, self.T, self.Ppc, self.Tpc)

        self._T_degree15 = 15  # 15°C时原油的密度
        self._rhoo_15 = f_rhoo(self.P, unit.unit_temperature(self._T_degree15), self.Pb, self.Rs, self.rho_ro,
                               self.rho_rg)

        # 比热计算
        self.Cpo = f_Cpo(self.T, self._rhoo_15)
        if self.is_wax:
            # 含蜡校正
            self.Cpo_wax = f_Cpo_wax(self.T)
            self.Cpo = self.Cpo_wax
        self.Cpw = f_Cpw(self.T)
        self.Cpg = f_Cpg(self.T)

    def get_method_support_list(self):
        return self.__method_support_list

    def update_method_dict(self):
        self.method_dict = self.__default_method_dict
        self.method_dict.update(self.method_dict_input)

    def _other(self):
        # P_list = np.arange(0.1, 40, 1.023076914)
        # T = 273.15 + 20
        #
        # mug_list = []
        # for P in P_list:
        #     mug = f_mug(P, T, blackoilproperty.Ppc, blackoilproperty.Tpc, blackoilproperty.rho_rg)
        #     mug_list.append(mug)
        pass


# %%
if __name__ == '__main__':
    blackoilproperty = BlackOilProperty()

    blackoilproperty.P = 30
    blackoilproperty.T = unit.unit_temperature(20)
    blackoilproperty.update()
