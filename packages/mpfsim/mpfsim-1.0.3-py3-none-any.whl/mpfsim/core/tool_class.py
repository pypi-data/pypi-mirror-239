#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time:   2023/9/10 17:05
# File:   tool_class.py
# Author: He Ma
# Email:  1692303843@qq.com

from core.tool import *
import logging


# 单例模式 主要用于构建全局字典信息

class Singleton:
    """
    单例模式 主要用于构建全局字典信息
    """
    # 类属性
    __obj = None
    # 是否经历过全局初始化
    __has_been_inited = False

    def __new__(cls, *args, **kwargs):
        if cls.__obj == None:
            cls.__obj = object.__new__(cls)
        return cls.__obj

    def __init__(self, **kwargs):
        if Singleton.__has_been_inited:
            # 单例模式 如果曾经创建过该类，则直接返回第一次的类对象
            return

        self.__dict__.update(kwargs)


class MyLog(Singleton):
    """
    单例模式的日志管理器
    """

    def __init__(self, **kwargs):

        """

        # 1. DEBUG 打印一些调试信息，级别最低
        # 2. INFO 打印一些正常的操作信息
        # 3. WARNING 打印警告信息
        # 4. ERROR 打印一些错误信息
        # 5. CRITICAL 打印一些致命的错误信息，等级最高

        Examples
        --------

        log_filename = 'logs/log.txt'
        # 0. 初始化
        mylog = MyLog()

        # ['', None, 'console', 'file', 'both']
        # 1. 控制台和文件同时输出
        mylog.setting('both', 'log.txt', 'a')
        # 2. 控制台和文件只输出文件
        mylog.setting('file', log_filename)
        # 3. 控制台和文件只输出控制台
        mylog.setting('console')
        #  4. 文件和控制台都不输出
        mylog.setting('')

        mylog.logger.debug('log')
        for i in range(10):
            # mylog.logger.debug("a-%s" % i)

        # 5. 关闭文件占用
        mylog.close()

        # 6. 日志过滤
        # 停止此命令后所有日志
        logging.disable(logging.DEBUG)
        # 恢复此命令后所有日志
        logging.disable(0)

        """
        super().__init__(**kwargs)
        self.mode = None
        self.log_file = None
        self.logger = None
        self.formatter = None

    # 这会导致debug信息所在的代码行改变至该函数内部
    # def __call__(self, *info):
    #     info = [str(i) for i in info]
    #     text_all = ', '.join(info)
    #     self.logger.debug(text_all)

    def setting(self, log_to='console', log_file='log.txt', mode='a', verbose=2):
        """

        Args:
            log_to: 日志输出到: 控制台  console 文件 file | | 同时 both
                ['', None, 'console', 'file', 'both']
            log_file: 文件保存路径
            mode: 追加 a, a+ 覆盖 w, w+
            verbose: 日志输出等级 0, 1, 2

        Returns:

        """

        # mode: 追加 a+ 覆盖 w, w+
        self.mode = '%s+' % mode[0]

        # 设置日志和时间格式
        if verbose == 2:
            formatter = "[%(asctime)s] %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s"
        elif verbose == 1:
            formatter = "%(filename)s [line:%(lineno)d]: %(message)s"
        # elif verbose == 0:
        else:
            formatter = "%(message)s"

        self.formatter = logging.Formatter(formatter)

        self.log_file = log_file

        self.logger = logging.getLogger('logger')

        # 设置日志的默认级别
        self.logger.setLevel(logging.DEBUG)

        if log_to in ['file', 'both']:
            # 确保存在该路径
            makedirs(self.log_file)

        # 关闭文件占用
        self.close()
        # 清除先前已有的handlers
        self._clear_handlers()

        # log_to = ['', None, 'console', 'file', 'both']
        if log_to in ['', None]:
            pass
        elif log_to == 'file':
            # 将日志输出到文件
            self.logger.addHandler(self._get_file_handler(self.log_file))
        elif log_to == 'console':
            # 将日志输出到控制台
            self.logger.addHandler(self._get_console_handler())
        elif log_to == 'both':
            self.logger.addHandler(self._get_file_handler(self.log_file))
            self.logger.addHandler(self._get_console_handler())
        else:
            raise Exception('MyLog occured wrong param, log_to:  %s' % log_to)

    def close(self):
        """结束进程占用"""
        logging.shutdown()

    def _clear_handlers(self):
        self.logger.handlers = []

    # 输出到文件handler的函数定义
    def _get_file_handler(self, filename):
        filehandler = logging.FileHandler(filename, mode=self.mode, encoding="utf-8")
        filehandler.setFormatter(self.formatter)
        return filehandler

    # 输出到控制台handler的函数定义
    def _get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler


# 变量跟踪管理器
class VariableTracker(Singleton):
    """
    单例模式的变量跟踪管理器

    Examples
    --------

    # tracker = VariableTracker()  # 单例模式
    tracker.clear_values()  # 全部变量清空，初始化

    tracker.clear_values('my_variable')  # 清空 my_variable 的值

    tracker.my_variable = 10  # 创建变量 my_variable 并设置值为 10
    tracker.my_variable = 20  # 将 my_variable 的值追加为 [10, 20]
    values = tracker('my_variable')  # 获取 my_variable 的值为 [10, 20]
    print(values)
    last_value = tracker.get_last_value('my_variable')  # 获取 my_variable 的最后一个值为 20
    tracker.plot_history('my_variable')

    tracker.clear_values('my_variable2')  # 清空 my_variable 的值
    tracker.my_variable2 = 30  # 创建变量 my_variable 并设置值为 10
    tracker.my_variable2 = 44  # 将 my_variable 的值追加为 [10, 20]
    values = tracker('my_variable2')  # 获取 my_variable 的值为 [10, 20]
    print(values)
    last_value = tracker.get_last_value('my_variable2')  # 获取 my_variable 的最后一个值为 20

    tracker.plot_history('my_variable2')

    tracker.plot_history('my_variable', 'my_variable2')

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.variables = None
        self.__dict__['variables'] = {}

    # def __setattr__(self, name, value):
    #     if name in self.variables:
    #         self.add_value(name, value)
    #     else:
    #         self._add_variable(name)
    #         self.add_value(name, value)

    def __call__(self, name):
        return self.get_values(name)

    def _add_variable(self, name):
        self.variables[name] = []

    def add_value(self, name, value):
        if name not in self.variables:
            # raise ValueError("Variable '{}' is not being tracked.".format(name))
            self._add_variable(name)
        self.variables[name].append(value)

    def get_values(self, name):

        if name not in self.variables:
            raise ValueError("Variable '{}' is not being tracked.".format(name))

        data = np.array(self.variables[name])

        return data

    def get_last_value(self, name):
        if name not in self.variables:
            raise ValueError("Variable '{}' is not being tracked.".format(name))
        if self.variables[name]:
            return self.variables[name][-1]
        else:
            return None

    def clear_values(self, *names):
        if not names:
            self.__dict__['variables'] = {}
        else:
            for name in names:
                if name in self.variables:
                    self.variables.pop(name)
                else:
                    print(ValueError("Variable '{}' is not being tracked.".format(name)))

    @property
    def key(self):
        key = list(self.variables.keys())
        return key

    def plot_history(self, *names, y_data_list=None):
        if not names:
            names = self.key

        if not y_data_list:
            y_data_list = [self.variables[name] for name in names]

        plt_dict = {
            'legend_list': names,
            'xlabel': 'Time',
            'ylabel': '%s' 'Value' if len(names) != 1 else names[0],
            'title': 'History',
        }

        draw_data_curve(y_data_list, plt_dict=plt_dict)


# 参数管理器

def combine_path(dictionary, keys, prefix=''):
    """
    用于GlobalConfig类
    将字典的多个键重新组合

    """
    path = '/'.join([dictionary[key] for key in keys if key in dictionary])
    last_key = keys[-1]

    if last_key in dictionary:
        dictionary[last_key] = os.path.abspath(prefix + path).replace('\\', '/')


class GlobalConfig(Singleton):
    shared_attributes = {}

    def __init__(self, relative_path_config='configs/config.yaml', **kwargs):
        super().__init__()

        self.dir_combination_key_list = None
        self.origin_config = None
        self.config = None

        self.shared_attributes = [
            "shared_attributes", "kwargs", "relative_path_config",
            "core_file", "work_dir", "path_yaml",
        ]

        self.kwargs = kwargs
        self.relative_path_config = relative_path_config

        self.core_file = os.path.abspath(__file__).replace('\\', '/')
        self.work_dir = os.path.dirname(os.path.dirname(self.core_file))
        self.path_yaml = '%s/%s' % (self.work_dir, self.relative_path_config)
        self.get_yaml_config()

    def _config(self):
        for my_keys in self.dir_combination_key_list:
            combine_path(self.config, my_keys, prefix=self.work_dir + '/')

    def get_yaml_config(self):
        self._clear_info()

        self.origin_config = yaml_read(self.path_yaml)
        self.dir_combination_key_list = self.origin_config['dir_combination_key_list']
        self.config = self.origin_config.copy()
        self._config()
        self.__dict__.update(self.config)

    def _save_instance_attributes(self, *args):
        """保存指定的实例属性为类属性"""
        for attr_name in args:
            # if attr_name in self.__dict__:
            GlobalConfig.shared_attributes[attr_name] = getattr(self, attr_name)

    def _restore_instance_attributes(self):
        """将类属性转换为实例属性"""
        for attr_name, attr_value in GlobalConfig.shared_attributes.items():
            setattr(self, attr_name, attr_value)
        # 清空已保存的类属性
        GlobalConfig.shared_attributes = {}

    def _clear_info(self):
        """删除所有config的读取记录"""
        self._save_instance_attributes(*self.shared_attributes)
        self.__dict__.clear()
        self._restore_instance_attributes()


if __name__ == '__main__':
    manager_config = GlobalConfig()
