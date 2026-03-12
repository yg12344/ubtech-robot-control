"""
运动控制模块
支持机器人动作控制和自定义动作编辑
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QGroupBox, QSpinBox, QDoubleSpinBox,
                             QComboBox, QSlider, QScrollArea)
from PyQt6.QtCore import Qt


class MotionControlPage(QWidget):
    """运动控制页面"""

    def __init__(self, robot_controller):
        super().__init__()
        self.robot_controller = robot_controller
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        # 主滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # 内容部件
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # 标题
        title = QLabel("运动控制")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        layout.addWidget(title)

        # 基础动作区
        basic_group = QGroupBox("基础动作")
        basic_group.setStyleSheet("""
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
        basic_layout = QVBoxLayout(basic_group)

        # 基础动作按钮网格
        basic_btn_layout = QHBoxLayout()

        basic_actions = [
            ("站立", "stand", "#3498db"),
            ("坐下", "sit", "#2ecc71"),
            ("行走", "walk", "#e67e22"),
            ("停止", "stop", "#e74c3c")
        ]

        for name, action, color in basic_actions:
            btn = QPushButton(name)
            btn.setFixedSize(120, 60)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {self.darken_color(color)};
                }}
                QPushButton:pressed {{
                    background-color: {self.darken_color(color, 0.8)};
                }}
            """)
            btn.clicked.connect(lambda checked, a=action: self.send_basic_action(a))
            basic_btn_layout.addWidget(btn)

        basic_layout.addLayout(basic_btn_layout)
        layout.addWidget(basic_group)

        # 手势动作区
        gesture_group = QGroupBox("手势动作")
        gesture_group.setStyleSheet("""
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
        gesture_layout = QVBoxLayout(gesture_group)

        # 手势按钮
        gesture_btn_layout = QHBoxLayout()

        gestures = [
            ("挥手", "wave", "#9b59b6"),
            ("点头", "nod", "#1abc9c"),
            ("摇头", "shake", "#f39c12"),
            ("鞠躬", "bow", "#e91e63")
        ]

        for name, gesture, color in gestures:
            btn = QPushButton(name)
            btn.setFixedSize(120, 60)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {self.darken_color(color)};
                }}
            """)
            btn.clicked.connect(lambda checked, g=gesture: self.send_gesture(g))
            gesture_btn_layout.addWidget(btn)

        gesture_layout.addLayout(gesture_btn_layout)
        layout.addWidget(gesture_group)

        # 行走控制区
        walk_group = QGroupBox("行走控制")
        walk_group.setStyleSheet("""
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
        walk_layout = QVBoxLayout(walk_group)

        # 方向控制
        direction_layout = QHBoxLayout()
        direction_layout.addWidget(QLabel("行走方向:"))
        self.direction_combo = QComboBox()
        self.direction_combo.addItems(["前进", "后退", "左转", "右转"])
        direction_layout.addWidget(self.direction_combo)
        direction_layout.addStretch()
        walk_layout.addLayout(direction_layout)

        # 距离控制
        distance_layout = QHBoxLayout()
        distance_layout.addWidget(QLabel("行走距离(米):"))
        self.distance_spin = QDoubleSpinBox()
        self.distance_spin.setRange(0.1, 10.0)
        self.distance_spin.setValue(1.0)
        self.distance_spin.setSingleStep(0.1)
        distance_layout.addWidget(self.distance_spin)
        distance_layout.addStretch()
        walk_layout.addLayout(distance_layout)

        # 速度控制
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("行走速度:"))
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(1, 10)
        self.speed_slider.setValue(5)
        speed_layout.addWidget(self.speed_slider)
        self.speed_label = QLabel("5")
        self.speed_label.setFixedWidth(30)
        speed_layout.addWidget(self.speed_label)
        speed_layout.addStretch()
        walk_layout.addLayout(speed_layout)

        # 连接滑块信号
        self.speed_slider.valueChanged.connect(lambda v: self.speed_label.setText(str(v)))

        # 执行按钮
        walk_btn_layout = QHBoxLayout()
        walk_btn = QPushButton("执行行走")
        walk_btn.setFixedHeight(45)
        walk_btn.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2c3e50;
            }
        """)
        walk_btn.clicked.connect(self.execute_walk)
        walk_btn_layout.addStretch()
        walk_btn_layout.addWidget(walk_btn)
        walk_btn_layout.addStretch()
        walk_layout.addLayout(walk_btn_layout)

        layout.addWidget(walk_group)

        # 舞蹈动作区
        dance_group = QGroupBox("舞蹈动作")
        dance_group.setStyleSheet("""
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
        dance_layout = QVBoxLayout(dance_group)

        # 舞蹈选择
        dance_select_layout = QHBoxLayout()
        dance_select_layout.addWidget(QLabel("选择舞蹈:"))
        self.dance_combo = QComboBox()
        self.dance_combo.addItems([
            "摆臂舞",
            "太空步",
            "机械舞",
            "迪斯科",
            "民族舞"
        ])
        dance_select_layout.addWidget(self.dance_combo)
        dance_select_layout.addStretch()
        dance_layout.addLayout(dance_select_layout)

        # 舞蹈按钮
        dance_btn_layout = QHBoxLayout()
        play_dance_btn = QPushButton("播放舞蹈")
        play_dance_btn.setFixedHeight(45)
        play_dance_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff6b6b;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ee5a5a;
            }
        """)
        play_dance_btn.clicked.connect(self.play_dance)
        dance_btn_layout.addStretch()
        dance_btn_layout.addWidget(play_dance_btn)
        dance_btn_layout.addStretch()
        dance_layout.addLayout(dance_btn_layout)

        layout.addWidget(dance_group)

        # 紧急停止
        stop_layout = QHBoxLayout()
        stop_btn = QPushButton("紧急停止")
        stop_btn.setFixedHeight(50)
        stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #c0392b;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #a93226;
            }
        """)
        stop_btn.clicked.connect(self.emergency_stop)
        stop_layout.addStretch()
        stop_layout.addWidget(stop_btn)
        stop_layout.addStretch()
        layout.addLayout(stop_layout)

        layout.addStretch()

        scroll.setWidget(content)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def darken_color(self, hex_color: str, factor: float = 0.9) -> str:
        """加深颜色"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(int(c * factor) for c in rgb)
        return f'#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}'

    def send_basic_action(self, action: str):
        """发送基础动作指令"""
        self.robot_controller.send_command("motion", action=action)
        print(f"发送动作指令: {action}")

    def send_gesture(self, gesture: str):
        """发送手势指令"""
        self.robot_controller.send_command("motion", action="gesture", gesture=gesture)
        print(f"发送手势指令: {gesture}")

    def execute_walk(self):
        """执行行走指令"""
        direction_map = {
            "前进": "forward",
            "后退": "backward",
            "左转": "left",
            "右转": "right"
        }
        direction = direction_map[self.direction_combo.currentText()]
        distance = self.distance_spin.value()
        speed = self.speed_slider.value()

        self.robot_controller.send_command(
            "motion",
            action="walk",
            direction=direction,
            distance=distance,
            speed=speed
        )
        print(f"执行行走: {direction}, 距离: {distance}m, 速度: {speed}")

    def play_dance(self):
        """播放舞蹈"""
        dance_type = self.dance_combo.currentText()
        self.robot_controller.send_command("motion", action="dance", dance_type=dance_type)
        print(f"播放舞蹈: {dance_type}")

    def emergency_stop(self):
        """紧急停止"""
        self.robot_controller.send_command("motion", action="stop")
        print("紧急停止")
