"""
远程监控与数据展示模块
实时显示机器人状态和传感器数据
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QGroupBox, QGridLayout, QPushButton)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np


class MonitorPage(QWidget):
    """监控页面"""

    def __init__(self, robot_controller):
        super().__init__()
        self.robot_controller = robot_controller
        self.monitoring = False
        self.data_history = {
            "battery": [],
            "temperature": [],
            "distance": []
        }
        self.max_history = 100
        self.init_ui()
        self.setup_timer()

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # 标题
        title = QLabel("远程监控")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        layout.addWidget(title)

        # 控制栏
        control_layout = QHBoxLayout()
        self.toggle_btn = QPushButton("开始监控")
        self.toggle_btn.setFixedHeight(40)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 30px;
            }
            QPushButton:hover {
                background-color: #219150;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_monitoring)
        control_layout.addWidget(self.toggle_btn)
        control_layout.addStretch()
        layout.addLayout(control_layout)

        # 状态信息区
        status_group = QGroupBox("机器人状态")
        status_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        status_layout = QGridLayout(status_group)

        # 状态标签
        status_items = [
            ("连接状态", "connection_status", "未连接"),
            ("电池电量", "battery_level", "0%"),
            ("运行模式", "operation_mode", "待机"),
            ("CPU使用率", "cpu_usage", "0%"),
            ("内存使用", "memory_usage", "0 MB"),
            ("温度", "temperature", "0°C")
        ]

        self.status_labels = {}
        row = 0
        for label_text, label_id, default_value in status_items:
            # 创建标签
            label = QLabel(f"{label_text}:")
            label.setStyleSheet("font-size: 13px;")
            status_layout.addWidget(label, row, 0)

            # 创建值标签
            value_label = QLabel(default_value)
            value_label.setObjectName(label_id)
            value_label.setStyleSheet("""
                QLabel {
                    background-color: #34495e;
                    color: white;
                    padding: 8px 15px;
                    border-radius: 4px;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
            status_layout.addWidget(value_label, row, 1)

            self.status_labels[label_id] = value_label
            row += 1

        layout.addWidget(status_group)

        # 传感器数据区
        sensor_group = QGroupBox("传感器数据")
        sensor_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        sensor_layout = QGridLayout(sensor_group)

        sensor_items = [
            ("前方距离", "front_distance", "0.00 m"),
            ("左侧距离", "left_distance", "0.00 m"),
            ("右侧距离", "right_distance", "0.00 m"),
            ("陀螺仪X", "gyro_x", "0.0°"),
            ("陀螺仪Y", "gyro_y", "0.0°"),
            ("陀螺仪Z", "gyro_z", "0.0°")
        ]

        self.sensor_labels = {}
        row = 0
        for label_text, label_id, default_value in sensor_items:
            # 创建标签
            label = QLabel(f"{label_text}:")
            label.setStyleSheet("font-size: 13px;")
            sensor_layout.addWidget(label, row, 0)

            # 创建值标签
            value_label = QLabel(default_value)
            value_label.setObjectName(label_id)
            value_label.setStyleSheet("""
                QLabel {
                    background-color: #2980b9;
                    color: white;
                    padding: 8px 15px;
                    border-radius: 4px;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
            sensor_layout.addWidget(value_label, row, 1)

            self.sensor_labels[label_id] = value_label
            row += 1

        layout.addWidget(sensor_group)

        # 数据图表区
        chart_group = QGroupBox("实时数据曲线")
        chart_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

        chart_layout = QVBoxLayout(chart_group)

        # 创建图表
        self.figure = Figure(figsize=(12, 4), dpi=100)
        self.canvas = FigureCanvasQTAgg(self.figure)
        chart_layout.addWidget(self.canvas)

        # 创建子图
        self.ax1 = self.figure.add_subplot(131)
        self.ax2 = self.figure.add_subplot(132)
        self.ax3 = self.figure.add_subplot(133)

        # 初始化图表
        self.init_charts()

        layout.addWidget(chart_group)

        # 刷新连接状态
        self.update_connection_status()

    def init_charts(self):
        """初始化图表"""
        # 电池电量图
        self.ax1.set_title("电池电量", fontsize=10)
        self.ax1.set_ylim(0, 100)
        self.ax1.set_ylabel("%")
        self.ax1.grid(True, alpha=0.3)
        self.line1, = self.ax1.plot([], [], 'b-', linewidth=2)
        self.ax1.set_xlim(0, self.max_history)

        # 温度图
        self.ax2.set_title("温度", fontsize=10)
        self.ax2.set_ylim(0, 80)
        self.ax2.set_ylabel("°C")
        self.ax2.grid(True, alpha=0.3)
        self.line2, = self.ax2.plot([], [], 'r-', linewidth=2)
        self.ax2.set_xlim(0, self.max_history)

        # 距离图
        self.ax3.set_title("前方距离", fontsize=10)
        self.ax3.set_ylim(0, 5)
        self.ax3.set_ylabel("m")
        self.ax3.grid(True, alpha=0.3)
        self.line3, = self.ax3.plot([], [], 'g-', linewidth=2)
        self.ax3.set_xlim(0, self.max_history)

        self.figure.tight_layout()

    def setup_timer(self):
        """设置定时器"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_data)
        self.update_timer.start(1000)  # 每秒更新一次

    def toggle_monitoring(self):
        """切换监控状态"""
        self.monitoring = not self.monitoring

        if self.monitoring:
            self.toggle_btn.setText("停止监控")
            self.toggle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 0 30px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
        else:
            self.toggle_btn.setText("开始监控")
            self.toggle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 0 30px;
                }
                QPushButton:hover {
                    background-color: #219150;
                }
            """)

    def update_connection_status(self):
        """更新连接状态"""
        if self.robot_controller.is_connected():
            self.status_labels["connection_status"].setText("已连接")
            self.status_labels["connection_status"].setStyleSheet("""
                QLabel {
                    background-color: #27ae60;
                    color: white;
                    padding: 8px 15px;
                    border-radius: 4px;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
        else:
            self.status_labels["connection_status"].setText("未连接")
            self.status_labels["connection_status"].setStyleSheet("""
                QLabel {
                    background-color: #c0392b;
                    color: white;
                    padding: 8px 15px;
                    border-radius: 4px;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)

    def update_data(self):
        """更新数据"""
        if not self.monitoring:
            return

        # 模拟数据（实际应用中从机器人获取）
        self.update_connection_status()

        # 生成模拟数据
        battery = max(0, 100 - len(self.data_history["battery"]) * 0.1)
        temperature = 35 + np.random.uniform(-2, 2)
        distance = 1.5 + np.random.uniform(-0.5, 0.5)

        # 更新状态标签
        self.status_labels["battery_level"].setText(f"{battery:.1f}%")
        self.status_labels["temperature"].setText(f"{temperature:.1f}°C")
        self.status_labels["cpu_usage"].setText(f"{np.random.randint(10, 30)}%")
        self.status_labels["memory_usage"].setText(f"{np.random.randint(200, 400)} MB")

        # 更新传感器标签
        self.sensor_labels["front_distance"].setText(f"{distance:.2f} m")
        self.sensor_labels["left_distance"].setText(f"{distance * np.random.uniform(0.8, 1.2):.2f} m")
        self.sensor_labels["right_distance"].setText(f"{distance * np.random.uniform(0.8, 1.2):.2f} m")
        self.sensor_labels["gyro_x"].setText(f"{np.random.uniform(-1, 1):.1f}°")
        self.sensor_labels["gyro_y"].setText(f"{np.random.uniform(-1, 1):.1f}°")
        self.sensor_labels["gyro_z"].setText(f"{np.random.uniform(-1, 1):.1f}°")

        # 更新历史数据
        self.data_history["battery"].append(battery)
        self.data_history["temperature"].append(temperature)
        self.data_history["distance"].append(distance)

        # 保持历史数据长度
        for key in self.data_history:
            if len(self.data_history[key]) > self.max_history:
                self.data_history[key].pop(0)

        # 更新图表
        self.update_charts()

    def update_charts(self):
        """更新图表"""
        x = range(len(self.data_history["battery"]))

        # 更新电池曲线
        self.line1.set_data(x, self.data_history["battery"])

        # 更新温度曲线
        self.line2.set_data(x, self.data_history["temperature"])

        # 更新距离曲线
        self.line3.set_data(x, self.data_history["distance"])

        # 刷新画布
        self.canvas.draw()

    def closeEvent(self, event):
        """关闭事件"""
        if hasattr(self, 'update_timer'):
            self.update_timer.stop()
        event.accept()
