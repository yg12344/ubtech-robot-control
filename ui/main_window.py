"""
主窗口 - 综合控制平台
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QStackedWidget, QFrame,
                             QStatusBar, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QFont

from robot_interface import RobotController


class MainWindow(QMainWindow):
    """主窗口类"""

    # 自定义信号
    status_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.robot_controller = RobotController()
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("优必选小微机器人控制软件")
        self.setGeometry(100, 100, 1200, 800)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 创建侧边栏
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        # 创建内容区
        self.content_area = self.create_content_area()
        main_layout.addWidget(self.content_area)

        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("未连接到机器人")

    def create_sidebar(self) -> QFrame:
        """创建侧边栏"""
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-right: 1px solid #34495e;
            }
        """)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(10)

        # 标题
        title = QLabel("小微控制台")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #34495e;")
        layout.addWidget(separator)

        # 连接状态
        self.connection_label = QLabel("● 未连接")
        self.connection_label.setStyleSheet("""
            QLabel {
                color: #e74c3c;
                font-size: 12px;
                padding: 8px;
                border: 1px solid #34495e;
                border-radius: 4px;
            }
        """)
        self.connection_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.connection_label)

        # 连接按钮
        connect_btn = QPushButton("连接机器人")
        connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        connect_btn.clicked.connect(self.connect_robot)
        layout.addWidget(connect_btn)

        # 分隔线
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setStyleSheet("background-color: #34495e;")
        layout.addWidget(separator2)

        # 导航按钮
        self.nav_buttons = []
        nav_items = [
            ("运动控制", "motion"),
            ("语音交互", "voice"),
            ("编程教学", "code"),
            ("数据监控", "monitor"),
            ("系统设置", "settings")
        ]

        for name, page_id in nav_items:
            btn = QPushButton(name)
            btn.setProperty("page_id", page_id)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #ecf0f1;
                    border: none;
                    padding: 12px;
                    text-align: left;
                    border-radius: 5px;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #34495e;
                }
                QPushButton:checked {
                    background-color: #1abc9c;
                    font-weight: bold;
                }
            """)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, pid=page_id: self.switch_page(pid))
            layout.addWidget(btn)
            self.nav_buttons.append(btn)

        # 选中第一个按钮
        self.nav_buttons[0].setChecked(True)

        layout.addStretch()

        # 版本信息
        version_label = QLabel("v1.0.0")
        version_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 11px;
                padding: 5px;
            }
        """)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        return sidebar

    def create_content_area(self) -> QStackedWidget:
        """创建内容区域"""
        self.stacked_widget = QStackedWidget()

        # 导入各个功能模块
        from modules.motion_control import MotionControlPage
        from modules.voice_control import VoiceControlPage
        from modules.code_editor import CodeEditorPage
        from modules.monitor import MonitorPage
        from modules.settings import SettingsPage

        # 添加各个页面
        self.stacked_widget.addWidget(MotionControlPage(self.robot_controller))
        self.stacked_widget.addWidget(VoiceControlPage(self.robot_controller))
        self.stacked_widget.addWidget(CodeEditorPage(self.robot_controller))
        self.stacked_widget.addWidget(MonitorPage(self.robot_controller))
        self.stacked_widget.addWidget(SettingsPage(self.robot_controller, self))

        return self.stacked_widget

    def switch_page(self, page_id: str):
        """切换页面"""
        # 更新按钮状态
        for btn in self.nav_buttons:
            if btn.property("page_id") == page_id:
                btn.setChecked(True)
            else:
                btn.setChecked(False)

        # 切换页面
        page_index = {
            "motion": 0,
            "voice": 1,
            "code": 2,
            "monitor": 3,
            "settings": 4
        }
        self.stacked_widget.setCurrentIndex(page_index[page_id])

    def connect_robot(self):
        """连接机器人"""
        from modules.settings import SettingsPage

        # 获取保存的连接配置
        connection_type = SettingsPage.get_connection_type()
        port = SettingsPage.get_serial_port()
        host = SettingsPage.get_tcp_host()
        port_num = SettingsPage.get_tcp_port()

        success = False
        if connection_type == "serial":
            success = self.robot_controller.connect_serial(port)
        elif connection_type == "tcp":
            success = self.robot_controller.connect_tcp(host, port_num)

        if success:
            self.connection_label.setText("● 已连接")
            self.connection_label.setStyleSheet("""
                QLabel {
                    color: #2ecc71;
                    font-size: 12px;
                    padding: 8px;
                    border: 1px solid #2ecc71;
                    border-radius: 4px;
                }
            """)
            self.status_bar.showMessage("已连接到机器人")

            # 设置数据回调
            self.robot_controller.set_data_callback(self.on_robot_data)
        else:
            QMessageBox.warning(self, "连接失败", f"无法连接到机器人\n连接方式: {connection_type}")

    def on_robot_data(self, data: dict):
        """处理机器人数据"""
        self.status_bar.showMessage(f"收到数据: {data}")

    def setup_connections(self):
        """设置信号连接"""
        self.status_updated.connect(self.status_bar.showMessage)

    def closeEvent(self, event):
        """关闭事件"""
        self.robot_controller.disconnect()
        event.accept()
