#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time:   2023/7/30 20:18
# File:   tools_extra.py
# Author: He Ma
# Email:  1692303843@qq.com


import concurrent
import concurrent.futures


def multi_threading(task_func, args_list, max_concurrent=4, tasks_display_interval=5, verbose=1):
    """


    Args:
        task_func: func(args)
        args_list: list: args for func(args)
        max_concurrent: int: 最大并发数量
        tasks_display_interval: int: 每完成n个任务显示一次总数
        verbose: int: > 0 显示进度细节

    Returns:
        results: list


    >>> import time
    >>> def func(t):
    >>>     time.sleep(t*1)
    >>> return t * 2

    >>> task_func = func
    >>> args_list = [1,2,3,4,5,6]

    """

    tasks_completed = 0  # 已完成的任务数量

    # 创建线程池执行器，并设置最大并发数
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        # 提交任务到线程池，并保留Future对象的顺序
        futures = [executor.submit(task_func, *x) for x in args_list]

        if verbose == 0:
            # 获取任务的结果，按照顺序解析结果
            results = [future.result() for future in futures]
            return results

        # 获取任务的结果，按照顺序解析结果
        results = []
        # 迭代处理完成的任务
        for future in concurrent.futures.as_completed(futures):
            # 获取任务的结果
            result = future.result()

            # 显示任务的完成状态
            if future.done():
                print(f"Task: {args_list[tasks_completed]} is done.")
                results.append(result)
            else:
                print(f"Task with result {result} is not done.")

            tasks_completed += 1

            # 完成进度
            if tasks_completed % tasks_display_interval == 0:
                print(f"Total tasks completed: {tasks_completed} / {len(args_list)}")

    return results
