"""
系统设置模块
配置连接参数和系统选项
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QSpinBox, QComboBox, QGroupBox,
                             QTabWidget, QFormLayout, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
import serial.tools.list_ports
import json
import os


class SettingsPage(QWidget):
    """设置页面"""

    # 配置文件路径
    CONFIG_FILE = "config.json"

    def __init__(self, robot_controller, main_window):
        super().__init__()
        self.robot_controller = robot_controller
        self.main_window = main_window
        self.config = self.load_config()
        self.init_ui()

    @staticmethod
    def load_config() -> dict:
        """加载配置"""
        default_config = {
            "connection": {
                "type": "serial",
                "serial_port": "COM3",
                "baudrate": 115200,
                "tcp_host": "192.168.1.100",
                "tcp_port": 8080
            },
            "voice": {
                "language": "zh-CN",
                "microphone": 0
            },
            "general": {
                "auto_connect": False,
                "update_interval": 1000
            }
        }

        if os.path.exists(SettingsPage.CONFIG_FILE):
            try:
                with open(SettingsPage.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
            except Exception:
                pass

        return default_config

    def save_config(self):
        """保存配置"""
        try:
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            QMessageBox.warning(self, "保存失败", f"无法保存配置: {e}")
            return False

    @staticmethod
    def get_connection_type() -> str:
        """获取连接类型"""
        config = SettingsPage.load_config()
        return config.get("connection", {}).get("type", "serial")

    @staticmethod
    def get_serial_port() -> str:
        """获取串口配置"""
        config = SettingsPage.load_config()
        return config.get("connection", {}).get("serial_port", "COM3")

    @staticmethod
    def get_tcp_host() -> str:
        """获取TCP主机"""
        config = SettingsPage.load_config()
        return config.get("connection", {}).get("tcp_host", "192.168.1.100")

    @staticmethod
    def get_tcp_port() -> int:
        """获取TCP端口"""
        config = SettingsPage.load_config()
        return config.get("connection", {}).get("tcp_port", 8080)

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # 标题
        title = QLabel("系统设置")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        layout.addWidget(title)

        # 创建标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #ecf0f1;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-size: 13px;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
                font-weight: bold;
            }
        """)

        # 添加各个设置标签页
        self.tab_widget.addTab(self.create_connection_tab(), "连接设置")
        self.tab_widget.addTab(self.create_voice_tab(), "语音设置")
        self.tab_widget.addTab(self.create_general_tab(), "常规设置")

        layout.addWidget(self.tab_widget)

        # 底部按钮
        button_layout = QHBoxLayout()

        reset_btn = QPushButton("恢复默认")
        reset_btn.setFixedHeight(40)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 13px;
                padding: 0 30px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        reset_btn.clicked.connect(self.reset_defaults)

        button_layout.addWidget(reset_btn)
        button_layout.addStretch()

        apply_btn = QPushButton("应用设置")
        apply_btn.setFixedHeight(40)
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 13px;
                font-weight: bold;
                padding: 0 30px;
            }
            QPushButton:hover {
                background-color: #219150;
            }
        """)
        apply_btn.clicked.connect(self.apply_settings)
        button_layout.addWidget(apply_btn)

        save_btn = QPushButton("保存配置")
        save_btn.setFixedHeight(40)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 13px;
                font-weight: bold;
                padding: 0 30px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        save_btn.clicked.connect(self.save_and_apply)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)

    def create_connection_tab(self) -> QWidget:
        """创建连接设置标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # 连接方式选择
        conn_type_group = QGroupBox("连接方式")
        conn_type_layout = QVBoxLayout(conn_type_group)

        self.conn_type_combo = QComboBox()
        self.conn_type_combo.addItems(["串口连接", "TCP/IP连接"])
        self.conn_type_combo.setCurrentText(
            "串口连接" if self.config["connection"]["type"] == "serial" else "TCP/IP连接"
        )
        conn_type_layout.addWidget(self.conn_type_combo)

        layout.addWidget(conn_type_group)

        # 串口设置
        self.serial_group = QGroupBox("串口设置")
        serial_layout = QFormLayout(self.serial_group)

        # 串口选择
        self.serial_combo = QComboBox()
        self.populate_serial_ports()
        self.serial_combo.setCurrentText(self.config["connection"]["serial_port"])
        serial_layout.addRow("串口:", self.serial_combo)

        # 刷新串口按钮
        refresh_serial_btn = QPushButton("刷新")
        refresh_serial_btn.clicked.connect(self.populate_serial_ports)
        serial_layout.addRow("", refresh_serial_btn)

        # 波特率
        baudrate_combo = QComboBox()
        baudrate_combo.addItems(["9600", "19200", "38400", "57600", "115200"])
        baudrate_combo.setCurrentText(str(self.config["connection"]["baudrate"]))
        serial_layout.addRow("波特率:", baudrate_combo)
        self.baudrate_combo = baudrate_combo

        layout.addWidget(self.serial_group)

        # TCP/IP设置
        self.tcp_group = QGroupBox("TCP/IP设置")
        tcp_layout = QFormLayout(self.tcp_group)

        host_input = QLineEdit(self.config["connection"]["tcp_host"])
        tcp_layout.addRow("主机地址:", host_input)
        self.tcp_host_input = host_input

        port_spin = QSpinBox()
        port_spin.setRange(1, 65535)
        port_spin.setValue(self.config["connection"]["tcp_port"])
        tcp_layout.addRow("端口:", port_spin)
        self.tcp_port_spin = port_spin

        layout.addWidget(self.tcp_group)

        # 初始显示/隐藏
        self.conn_type_combo.currentTextChanged.connect(self.on_connection_type_changed)
        self.on_connection_type_changed(self.conn_type_combo.currentText())

        layout.addStretch()
        return widget

    def create_voice_tab(self) -> QWidget:
        """创建语音设置标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        voice_group = QGroupBox("语音识别")
        voice_layout = QFormLayout(voice_group)

        # 语言选择
        lang_combo = QComboBox()
        lang_combo.addItems(["中文", "English"])
        lang_combo.setCurrentText("中文" if self.config["voice"]["language"].startswith("zh") else "English")
        voice_layout.addRow("识别语言:", lang_combo)
        self.lang_combo = lang_combo

        # 麦克风选择
        mic_combo = QComboBox()
        # 这里可以添加麦克风列表
        voice_layout.addRow("麦克风:", mic_combo)
        self.mic_combo = mic_combo

        layout.addWidget(voice_group)

        # 语音合成设置
        tts_group = QGroupBox("语音合成")
        tts_layout = QFormLayout(tts_group)

        # 语速
        speed_spin = QSpinBox()
        speed_spin.setRange(50, 200)
        speed_spin.setValue(100)
        tts_layout.addRow("语速:", speed_spin)

        # 音调
        pitch_spin = QSpinBox()
        pitch_spin.setRange(0, 100)
        pitch_spin.setValue(50)
        tts_layout.addRow("音调:", pitch_spin)

        layout.addWidget(tts_group)

        layout.addStretch()
        return widget

    def create_general_tab(self) -> QWidget:
        """创建常规设置标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # 启动设置
        startup_group = QGroupBox("启动设置")
        startup_layout = QFormLayout(startup_group)

        # 自动连接
        auto_connect_combo = QComboBox()
        auto_connect_combo.addItems(["是", "否"])
        auto_connect_combo.setCurrentText("是" if self.config["general"]["auto_connect"] else "否")
        startup_layout.addRow("启动时自动连接:", auto_connect_combo)
        self.auto_connect_combo = auto_connect_combo

        layout.addWidget(startup_group)

        # 更新设置
        update_group = QGroupBox("更新设置")
        update_layout = QFormLayout(update_group)

        update_spin = QSpinBox()
        update_spin.setRange(100, 5000)
        update_spin.setSuffix(" ms")
        update_spin.setValue(self.config["general"]["update_interval"])
        update_layout.addRow("数据更新间隔:", update_spin)
        self.update_spin = update_spin

        layout.addWidget(update_group)

        # 信息
        info_group = QGroupBox("关于")
        info_layout = QVBoxLayout(info_group)

        info_label = QLabel(
            "优必选小微控制软件 v1.0.0\n\n"
            "支持多种连接方式：\n"
            "• 串口连接\n"
            "• TCP/IP连接\n\n"
            "功能模块：\n"
            "• 运动控制\n"
            "• 语音交互\n"
            "• 编程教学\n"
            "• 远程监控"
        )
        info_label.setStyleSheet("color: #7f8c8d;")
        info_layout.addWidget(info_label)

        layout.addWidget(info_group)

        layout.addStretch()
        return widget

    def populate_serial_ports(self):
        """填充可用串口列表"""
        self.serial_combo.clear()
        ports = serial.tools.list_ports.comports()
        if ports:
            for port in ports:
                self.serial_combo.addItem(port.device)
        else:
            self.serial_combo.addItem("未检测到串口")

    def on_connection_type_changed(self, text: str):
        """连接类型改变"""
        if text == "串口连接":
            self.serial_group.setEnabled(True)
            self.tcp_group.setEnabled(False)
        else:
            self.serial_group.setEnabled(False)
            self.tcp_group.setEnabled(True)

    def reset_defaults(self):
        """恢复默认设置"""
        reply = QMessageBox.question(
            self,
            "确认",
            "确定要恢复默认设置吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.config = self.load_config()
            QMessageBox.information(self, "成功", "已恢复默认设置")

    def apply_settings(self):
        """应用设置"""
        # 更新连接设置
        self.config["connection"]["type"] = "serial" if self.conn_type_combo.currentText() == "串口连接" else "tcp"
        self.config["connection"]["serial_port"] = self.serial_combo.currentText()
        self.config["connection"]["baudrate"] = int(self.baudrate_combo.currentText())
        self.config["connection"]["tcp_host"] = self.tcp_host_input.text()
        self.config["connection"]["tcp_port"] = self.tcp_port_spin.value()

        # 更新语音设置
        self.config["voice"]["language"] = "zh-CN" if self.lang_combo.currentText() == "中文" else "en-US"
        self.config["voice"]["microphone"] = self.mic_combo.currentIndex()

        # 更新常规设置
        self.config["general"]["auto_connect"] = self.auto_connect_combo.currentText() == "是"
        self.config["general"]["update_interval"] = self.update_spin.value()

        QMessageBox.information(self, "成功", "设置已应用")

    def save_and_apply(self):
        """保存并应用设置"""
        self.apply_settings()
        if self.save_config():
            QMessageBox.information(self, "成功", "设置已保存")
