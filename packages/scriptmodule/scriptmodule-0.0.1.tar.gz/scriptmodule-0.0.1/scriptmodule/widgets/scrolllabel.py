# -*- coding: utf-8 -*-
# @File    : scrolllabel.py
# @Create_Time    : 2023-11-07 10:13
# @Author  : cwc
# @Description : 
from PyQt5.QtWidgets import QLabel, QScrollArea
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class ScrollLabel(QScrollArea):
    def __init__(self, width=280, height=550):
        super().__init__()
        self.label = QLabel()
        self.label.setFont(QFont('SansSerif', 10))
        # 设置换行
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setStyleSheet("border: 3px solid grey;border-radius:5px;color:green;background-color:rgba(0,0,0,1)")
        self.label.setMinimumSize(width, height)

        self.setWidget(self.label)
        # 设置 QScrollArea 只显示垂直滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setFixedSize(width, height)

    def set_text(self, text_str):
        scroll_text = self.label.text() + '\n'
        if len(scroll_text) > 10000:
            scroll_text = ''
        scroll_text = scroll_text + text_str
        self.label.setText(scroll_text)
        self.label.adjustSize()
        self.verticalScrollBar().setValue(self.label.height())

    def clear_text(self):
        """
        清空屏幕
        """
        self.label.setText('')
        self.label.adjustSize()
        self.verticalScrollBar().setValue(self.label.height())
