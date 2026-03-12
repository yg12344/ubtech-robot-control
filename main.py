"""
优必选小微机器人控制软件
综合控制平台 - 支持语音交互、运动控制、编程教学和远程监控
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # 设置应用程序信息
    app.setApplicationName("优必选小微控制软件")
    app.setOrganizationName("UBTECH Controller")

    # 创建主窗口
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
