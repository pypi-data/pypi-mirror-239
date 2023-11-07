# -*- coding: utf-8 -*-
# @File    : threadstatus.py
# @Create_Time    : 2023-11-07 9:59
# @Author  : cwc
# @Description : 线程状态
from enum import Enum, unique


@unique
class ThreadStatus(Enum):
    # 未运行
    IDLE = 0
    # 运行中
    RUNNING = 1
    # 暂停中
    PAUSING = 2
    # 停止中
    STOPPING = 3