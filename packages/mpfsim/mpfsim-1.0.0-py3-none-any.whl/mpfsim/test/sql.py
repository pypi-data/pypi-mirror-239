# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 16:43:57 2023

@author: 马赫
"""
from core import tool_sql
from ast import literal_eval

# %% 确定数据表
table_name = 'q1'
sql_reader = tool_sql.SQLReader()
# %% 创建数据表
new_table_name = table_name
new_table_columns = ['col_a', 'col_b']
status = sql_reader.create_table(table_name=new_table_name, table_columns=new_table_columns)
print(status)
# %% 显示数据表结构
table_columns = sql_reader.get_table_columns()
print(table_columns)

# %% 为数据表增添多行数据

params_list = [
    [5, '2'],
    [5, "{'q':1, 'w':'w'}"],
    # 恶意代码，避免用户输入时，通过eval执行
    [1, "__import__('os').system('dir')"],
]

# 新增n行数据params_list
status = sql_reader.insert_data(params_list)
print(status)
# %% TODO 更新数据表部分数据


# %% 显示数据表所有数据
table_df = sql_reader.select_all()
print(table_df)

# %%
user_info = table_df.iloc[1, 1]
user_dict = literal_eval(user_info)
print(user_dict, type(user_dict))

# %% 删除指定数据表
status = sql_reader.delete_table('q1')
print(status)
# %% 释放SQL数据库资源
status = sql_reader.close()
print(status)
