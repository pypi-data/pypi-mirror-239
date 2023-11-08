#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/6/10 17:08
# @Author  : 马赫
# @Email   : 1692303843@qq.com
# @FileName: tool.py


import os, sys
import pickle
import subprocess
import time

import numpy as np
import pandas as pd

import yaml

import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams, ticker, cycler
import warnings

warnings.filterwarnings("ignore")


# %% 1. 通用模块


def read_excel(file_name, header_num=1, index_num=0):
    """
    读取数据文件，指定表头，行号

    Parameters
    ----------
    file_name : TYPE
        文件名.
    header_num : TYPE, optional 对pkl文件无影响
        DESCRIPTION. 无表头，或者整数表示前n行作为表头，默认首行
    index_num : TYPE, optional 对pkl文件无影响
        DESCRIPTION. 默认行号为索引，或者整数，表示第i列作为索引，默认行号

    Returns
    -------
    df : TYPE pd.DataFrame
        带有表头和行索引的二维矩阵.

    """
    # 表头（列名）设置
    if header_num == 0:
        header = None
    elif header_num == 1:
        header = 0
    else:  # header_num > 1
        header = [i for i in range(header_num)]

    if index_num == 0:
        index_col = None
    else:
        index_col = index_num - 1

    file_suffix = file_name.split('.')[-1]
    if file_suffix in ['xlsx', 'xls']:
        df = pd.read_excel(file_name, header=header, index_col=index_col)
    elif file_suffix == 'csv':
        # 可能会遇到utf-8无法打开的错误
        try:
            df = pd.read_csv(file_name, header=header, index_col=index_col)
        except Exception as e:
            # print(e, '\n')
            df = pd.read_csv(file_name, header=header,
                             index_col=index_col, encoding='gbk')

    elif file_suffix == 'txt':
        df = pd.read_table(file_name, header=header, index_col=index_col)
    elif file_suffix == 'pkl':
        df = pd.read_pickle(file_name)
    else:
        raise Exception('error file_suffix: %s' % file_suffix)

    # 对于多行和在一起作为表头的字符处理
    if isinstance(header, list):
        new_column_name_list = []
        for old_column_name_tuple in df.columns.tolist():
            new_column_name_list.append('_'.join(old_column_name_tuple))

        df.columns = new_column_name_list

    return df


def makedirs(path):
    """
    保证path这个文件或文件夹路径存在，如果没有则创建该路径
    path 可以为文件或文件夹
    通过是否有.xxx后缀判断是文件或文件夹
    如果是文件则去除文件名
    如果是文件夹则直接判断该文件夹是否存在并创建
    """

    if os.path.splitext(path)[1] != '':
        # 这个是文件
        path = os.path.split(path)[0]

    # 对于当前路径，则自动跳过创建文件夹
    if (path in ['', '.']) or os.path.isdir(path):
        return None
    else:
        os.makedirs(path)
        return path


def pickle_save(path, content):
    """
    保存变量
    """
    # 如果不存在该路径，则创建文件夹
    makedirs(path)
    with open(path, 'wb') as f:
        pickle.dump(content, f)


def pickle_load(path):
    """
    读取变量
    """
    with open(path, 'rb') as f:
        content = pickle.load(f)
    return content


def raw2stand(raw_data, mean, std):
    # data = (data - data.min()) / (data.max() - data.min())
    return (raw_data - mean) / (std + 1e-6)


def yaml_read(yaml_path):
    """
    yaml配置读取器，
    输入yaml文件路径
    返回变量与值的字典
    """
    try:
        with open(yaml_path) as f:
            _info_yaml = f.read()
    except UnicodeDecodeError:
        # print('捕获编码问题，尝试中文编码')
        with open(yaml_path, encoding='utf-8') as f:
            _info_yaml = f.read()
    except Exception as e:
        print('文件无法访问: ', yaml_path)
        raise e

    info_yaml = yaml.safe_load(_info_yaml)
    return info_yaml


# %% 目标函数执行用时的装饰器


def calculate_execution_time(func):
    """

    >>> @calculate_execution_time
    >>> def my_function():
    >>>     # 函数的代码逻辑
    >>>     pass
    >>> my_function()

    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print("函数执行时间: %s s" % execution_time)
        return result

    return wrapper


# %% 实时输出cmd命令的信息
def sh(command, is_show=True):
    """
    实时输出cmd命令的信息
    """
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    print(type(p))
    lines = []
    for line in iter(p.stdout.readline, b''):
        line = line.strip().decode("GB2312")
        if is_show:
            print(">>>", line)

        lines.append(line)
    return lines


# %% matlotlib 绘图相关函数

def plt_global(font_path="assets/tnw_simsun.ttf", font=14, color_list: list = None):
    """
    选择新罗马+宋体的组合字体，刻度线向内
    """
    # if color_list
    # 设置颜色循环列表
    if color_list is None:
        color_list = [
            'k', 'r', 'b', 'g',
            '#3B4992', '#008280', '#808180', '#EE0000', '#BB0021',
            '#1B1919', '#008B45', '#5F559B', '#631879', '#A20056'
        ]

    if font_path == "assets/tnw_simsun.ttf":
        core_file = os.path.abspath(__file__).replace('\\', '/')
        work_dir = os.path.dirname(os.path.dirname(core_file))
        font_path = '%s/%s' % (work_dir, font_path)

    # 字体加载
    font_manager.fontManager.addfont(font_path)
    prop = font_manager.FontProperties(fname=font_path)
    # print(prop.get_name())  # 显示当前使用字体的名称

    # 字体设置
    rcParams['font.family'] = 'sans-serif'  # 使用字体中的无衬线体
    rcParams['font.sans-serif'] = prop.get_name()  # 根据名称设置字体
    rcParams['font.size'] = font  # 设置字体大小
    rcParams['axes.unicode_minus'] = False  # 使坐标轴刻度标签正常显示正负号

    rcParams["axes.prop_cycle"] = cycler(color=color_list)

    # 设置刻度线向外还是向内
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'


def plt_ax(ax, xmax=0):
    # 设置x，y 的主刻度定位器
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(13.0))
    # ax.yaxis.set_major_locator(ticker.MultipleLocator(1.0))

    # 设置x，y 的次刻度定位器
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))

    # y轴以百分数形式表示，将xmax作为100%
    if xmax > 0:
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=xmax, decimals=2))

    # 设置次刻度格式器
    def minor_tick(x, pos):
        if not x % 1.0:
            return ""
        return "%.2f" % x

    # 启用后，次刻度将显示数值
    # ax.xaxis.set_minor_formatter(ticker.FuncFormatter(minor_tick))
    # ax.yaxis.set_minor_formatter(ticker.FuncFormatter(minor_tick))

    # 改变刻度和刻度标签的外观
    # axis: x y both
    # which:主刻度样式
    # length:主刻度长度
    # width:主刻度宽度
    # colors:主刻度线和主刻度标签的颜色
    ax.tick_params(axis='both', which="major", length=6, width=1.0, colors="black")
    ax.tick_params(which="minor", length=3, width=0.5, labelsize=10, labelcolor="black")

    # 设置上侧和右侧是否显示刻度线
    ax.tick_params(top='on', right='on', which='both')

    # 坐标轴-科学计数法
    # if plt_dict['is_sci_axis']:
    #     # axis='y', 'both'
    #     plt.ticklabel_format(axis=plt_dict['is_sci_axis'], style='sci', scilimits=(2, 4))


def plt_other(fig, _plt_dict):
    if _plt_dict['legend_list']:
        # plt.legend()的是给当前的图形对象添加图例
        # axes.legend()是给已经明确的axes子图对象添加图例， 在能明确操作的图形对象时建议直接使用Axes.legend()。
        # figure.legend()是对当前的figure对象添加图例，需要注意的是一个figure对象可能包括多个Axes的子对象，因此figure.legend()是给多个Axes添加共同的图例时使用的。
        plt.legend(
            _plt_dict['legend_list'],
            frameon=False,  # 关闭图例的边框实体
            # bbox_to_anchor = (0.5, -0.2),  # 图例的边框位置
            loc=_plt_dict['legend']['loc'],  # 'best', 'lower center'
            ncol=_plt_dict['legend']['ncol'],  # 分成最多n列显示图例  # 1, 4
            borderaxespad=_plt_dict['legend']['borderaxespad'],  # 坐标轴和图例边框之间的间距，单位为字体大小。 0, -2
        )

        fig.subplots_adjust(bottom=_plt_dict['legend']['subplots_adjust'])  # 0, 0.2

    if _plt_dict['xlabel']:
        plt.xlabel(_plt_dict['xlabel'])
    if _plt_dict['ylabel']:
        plt.ylabel(_plt_dict['ylabel'])
    if _plt_dict['title']:
        plt.title(_plt_dict['title'])

    if _plt_dict['is_grid']:
        plt.grid(linestyle=":", linewidth=0.5, color="#1B1919")

    if _plt_dict['is_save']:
        makedirs(_plt_dict['path_save'])
        plt.savefig(_plt_dict['path_save'])
    if _plt_dict['is_show']:
        plt.show()
    plt.close()


def draw_data_curve(*xy_pairs, plt_dict={}):
    """
    matplotlib库绘图函数
    Args:
        *xy_pairs: [x_data_list (optional), y_data_list]
            y_data_list: [y_data1, y_data2, ...]
                y_data1: list | numpy.array shape: (N, )
        plt_dict: 字典`_plt_dict`中的部分更新内容字典

    Examples:

    >>> plt_global(font_path="../assets/tnw_simsun.ttf")
    >>>
    >>> x = np.linspace(0.5, 13.5, 100)
    >>> y = np.sin(x)
    >>>
    >>> y_data_list = [y, y + 3]
    >>> x_data_list = [x, x]
    >>> plt_dict = {
    >>>     'legend_list': ['Orkiszewski方法', 'BB'],
    >>>     'xlabel': '总距离 (m)',
    >>>     'ylabel': '压力 (MPa)',
    >>>     'title': '总距离-压力曲线',
    >>>     'figsize': (5, 4),
    >>>     'dpi': 300,
    >>>     'is_save': 0,
    >>> }
    >>>
    >>> draw_data_curve(x_data_list, y_data_list, plt_dict=plt_dict)
    >>>
    """
    _plt_dict = {
        'legend_list': [],

        'xlabel': '',
        'ylabel': '',
        'title': '',
        'is_grid': 0,

        'figsize': (5, 4),
        'dpi': 300,
        'is_show': 1,
        'is_save': 0,
        'path_save': 'plt_save.jpg',  # '.eps'

        'legend': {
            'loc': 'lower center',  # 'best', 'lower center'
            'ncol': 4,  # 1, 4
            'borderaxespad': -5,  # 0, -5, -7
            'subplots_adjust': 0.2,  # 0, 0.2
        },
    }

    _plt_dict.update(plt_dict)

    if len(xy_pairs) == 1:
        y_data_list = xy_pairs[-1]
        x_data_list = []
        for _y_data in y_data_list:
            _x_data = np.arange(0, len(_y_data))
            x_data_list.append(_x_data)
    elif len(xy_pairs) == 2:
        y_data_list = xy_pairs[-1]
        x_data_list = xy_pairs[0]
    else:
        raise Exception("len(xy_pairs) 应该为1或者2，当前为%s" % len(xy_pairs))

    # ------------------- 画图 ----------------------------------
    fig = plt.figure(figsize=_plt_dict['figsize'], dpi=_plt_dict['dpi'])
    ax = fig.add_subplot(111)

    for i_line, (x_data, y_data) in enumerate(zip(x_data_list, y_data_list)):
        line = ax.plot(
            # 将N行曲线转化为N列曲线
            # np.array(x_data_list).T, np.array(y_data_list).T,
            x_data, y_data,
            # 折线类型, 折线宽度, 折线颜色
            linestyle='-', linewidth=1,  # color='#2f2fff'
            # 点的形状 s: 方形 None: 不添加点, 点的大小
            marker='s', markersize=4,
        )

    # 设置x,y轴的范围
    # ax.set_xlim(0,4)
    # ax.set_ylim(0,2)

    # 坐标轴设置
    plt_ax(ax)
    plt_other(fig, _plt_dict)


def draw_history(history, acc_key='mean_absolute_error', path='output/test_img.jpg'):
    """history中，必有的训练图片，以及可能存在的测试图片"""
    from core import mylog

    history_keys = list(history.history.keys())
    _text = 'history loss: %s' % history_keys
    mylog.logger.info(_text)
    mylog.logger.info('acc key: %s' % acc_key)
    mylog.logger.info('Generate picture')

    loss = history.history['loss']
    val_loss = history.history['val_loss']

    # epochs = range(1, len(loss) + 1)

    plt_dict = {
        'y_data_list': [
            loss,
            val_loss,
        ],
        'legend_list': [
            'Training loss',
            'Test loss',
        ],
        # 'custom_color_list': [],
        'custom_color_list': ['r', 'g'],
        'xlabel': 'Epochs',
        'ylabel': 'Loss',
        'is_save': 1,
        'save_path': '%s/Loss.jpg' % path,
    }
    # draw_sci(plt_dict)

    if acc_key in history_keys:
        acc = history.history[acc_key]
        val_acc = history.history['val_' + acc_key]

        acc_label = 'MAE'
        y_data_list = [
            acc,
            val_acc,
        ]
        legend_list = [
            'Training MAE',
            'Test MAE',
        ]
        if acc_key == 'acc':
            acc_label = 'Accuracy (%)'
            y_data_list = [y_data * 100 for y_data in y_data_list]
            legend_list = [
                'Training Acc',
                'Test Acc',
            ]

        plt_dict = {
            'y_data_list': y_data_list,
            'legend_list': legend_list,
            # 'custom_color_list': [],
            'custom_color_list': ['r', 'g'],
            'xlabel': 'Epochs',
            'ylabel': acc_label,
            'is_save': 1,
            'save_path': '%s/metrics.jpg' % path,
        }
        # draw_sci(plt_dict)


# %% 未完成部分
pass

# def func_print_file(path_file, func):
#     """将func函数内部的输出，临时重定向追加到指定文件"""
#     # TODO 这里经常会导致日志文件未完全关闭，锁定日志文件进程
#     with open(path_file, "a") as o:
#         with contextlib.redirect_stdout(o) as e:
#             obj = func()
#
#         e.close()
#     o.close()
#     return obj

# %% 测试


if __name__ == '__main__':
    import os

    print(os.getcwd())

    plt_global(font_path="../assets/tnw_simsun.ttf")

    x = np.linspace(0.5, 13.5, 100)
    y = np.sin(x)

    y_data_list = [y, y + 3]
    x_data_list = [x, x]
    plt_dict = {
        'legend_list': ['Orkiszewski方法', 'BB'],
        'xlabel': '总距离 (m)',
        'ylabel': '压力 (MPa)',
        'title': '总距离-压力曲线',
        'figsize': (5, 4),
        'dpi': 300,
        'is_save': 0,

    }
    draw_data_curve(x_data_list, y_data_list, plt_dict=plt_dict)
