# -*- coding: utf-8 -*-
# @File    : menuaction.py
# @Create_Time    : 2023-11-07 10:01
# @Author  : cwc
# @Description : 主页->表格  鼠标右键菜单动作
from enum import Enum, unique


@unique
class MenuAction(Enum):
    # 启动
    START = 0
    # 暂停/恢复
    PAUSE = 1
    # 停止
    STOP = 2