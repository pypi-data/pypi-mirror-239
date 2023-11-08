#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time:   2023/4/20 22:21
# File:   tool_sql.py
# Author: He Ma
# Email:  1692303843@qq.com

import sqlite3
import pandas as pd


class SQLReader:
    """
    本项目目前放弃了数据库处理部分，后期重新启用时，可参考其他项目的数据库部分代码
    """

    def __init__(self, path_db='./test.db', table_name='table1', table_columns=[]):

        # path_db 数据库文件所在路径 './test.db'
        self.table_columns = table_columns  # 数据表的列名列表
        self.path_db = path_db
        self.table_name = table_name

        self.DB_TYPES = ['NULL', 'INTEGER', 'REAL', 'TEXT', 'BLOB']

        if self.path_db is None:
            self.path_db = ':memory:'
        # 内存创建数据库，临时使用，不产生本地数据库文件
        # conn = sqlite3.connect(':memory:')
        self.conn = sqlite3.connect(self.path_db)
        # 创建一个游标 cursor
        self.cur = self.conn.cursor()

    def get_table_columns(self):
        """
        查看数据表所有字段信息, 更新列表self.table_columns
        :return: self.table_columns list 列名列表
        """

        # 查看指定表所有字段信息
        sql_text_info = "PRAGMA table_info(%s)" % self.table_name
        self.cur.execute(sql_text_info)
        # 获取查询结果
        table_info = pd.DataFrame(self.cur.fetchall())
        columns = table_info.columns.tolist()
        columns[0] = 'column_id'
        columns[1] = 'column_name'
        columns[2] = 'column_type'
        table_info.columns = columns
        # self.table_info = table_info

        self.table_columns = table_info['column_name'].tolist()
        return self.table_columns

    def insert_data(self, params_list):
        """
        向数据表table_name中插入len(params_list)行数据

        :param params_list: list
            params_list = [params 1, params 2, ... , params n]
            准备写入数据库的多行数据列表.
            列表的每个元素是一行数据params，
            每行数据params = [var 1, var 2, ... , var m]
            len(params)是数据表的列数
            缺失值应提前以None占位
        :return: bool 成功标识符.
        """
        placeholder_text = ('?,' * len(params_list[0]))[: -1]
        sql_text = "INSERT INTO %s VALUES (%s)" % (self.table_name, placeholder_text)
        self.cur.executemany(sql_text, params_list)
        self.conn.commit()

        return True

    def delete_data(self, condition_text=1):
        """
        删除指定数据表

        # 全部删除
        sql_reader.delete_data()

        # 条件删除
        sql_reader.delete_data('"TVD">1500')

        """
        sql_text = "DELETE FROM %s WHERE (%s)" % (self.table_name, condition_text)
        self.cur.execute(sql_text)
        self.conn.commit()
        return True

    # TODO 更新数据表部分数据
    def select_all(self):
        """
        显示数据表中所有数据
        :return: table_df pd.DataFrame 以pd矩阵的方式展示
        """
        sql_text_select_all = "SELECT * FROM %s" % self.table_name
        self.cur.execute(sql_text_select_all)
        table_df = pd.DataFrame(self.cur.fetchall())
        table_df.columns = self.table_columns
        return table_df

    def create_table(self, table_name, table_columns, table_types=None):
        """
        创建数据表
        :param table_name: str 数据表名
        :param table_columns: list 列名列表
        :param table_types: list Optional 列类型列表
        :return:
        """
        # 更新数据表名
        self.table_name = table_name

        if (table_types is None) or (len(table_types) != len(table_columns)):
            table_types = ['BLOB'] * len(table_columns)

        # columns_info_text = 'col_1 TEXT, col_2 BLOB'
        columns_info_text = ''
        for i_column, column in enumerate(table_columns):
            column_types = table_types[i_column]
            if column_types not in self.DB_TYPES:
                column_types = 'BLOB'
            column_text = '%s %s' % (str(column), column_types)
            columns_info_text += column_text
            if i_column != len(table_columns) - 1:
                columns_info_text += ', '

        # 建表的sql语句
        # 可能该表名已经存在, IF NOT EXISTS 避免对已有表进行创建
        sql_text = """CREATE TABLE IF NOT EXISTS %s (%s);""" % \
                   (self.table_name, columns_info_text)
        # 执行sql语句
        try:
            self.cur.execute(sql_text)
        except Exception as e:
            import os
            print('相对路径问题, 当前路径:', os.getcwd())
            print('当前执行的SQL语句:', sql_text)
            raise e
        self.conn.commit()
        return True

    def delete_table(self, table_name):
        """删除指定数据表"""
        sql_text = """DROP TABLE %s;""" % table_name
        # 执行sql语句
        self.cur.execute(sql_text)
        self.conn.commit()
        return True

    def close(self):
        """关闭数据库调用，释放资源"""
        # 关闭游标
        self.cur.close()
        # 关闭连接
        self.conn.close()
        return True
