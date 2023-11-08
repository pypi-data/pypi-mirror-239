#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time:   2023/4/20 22:20
# File:   __init__.py.py
# Author: He Ma
# Email:  1692303843@qq.com


from .tool import *
from .tool_class import MyLog, VariableTracker, GlobalConfig

# from .CONSTANTS import DefaultInfo, BASE_DICT

# 全局参数
# default_info = DefaultInfo(**BASE_DICT)
manager_config = GlobalConfig()
plt_global(font_path=manager_config.font_path, font=14)

# 日志管理器
mylog = MyLog()
mylog.setting('console', verbose=2)

# 变量跟踪管理器
tracker = VariableTracker()
