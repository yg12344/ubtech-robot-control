"""
语音交互控制模块
支持语音识别和语音合成
"""

import speech_recognition as sr
import threading
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTextEdit, QLabel, QComboBox, QGroupBox)
from PyQt6.QtCore import pyqtSignal, QTimer
from PyQt6.QtGui import QTextCursor


class VoiceControlPage(QWidget):
    """语音交互控制页面"""

    # 自定义信号
    speech_recognized = pyqtSignal(str)

    def __init__(self, robot_controller):
        super().__init__()
        self.robot_controller = robot_controller
        self.is_listening = False
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # 标题
        title = QLabel("语音交互控制")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        layout.addWidget(title)

        # 语音识别区
        recognition_group = QGroupBox("语音识别")
        recognition_group.setStyleSheet("""
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
        recognition_layout = QVBoxLayout(recognition_group)

        # 麦克风选择
        mic_layout = QHBoxLayout()
        mic_layout.addWidget(QLabel("选择麦克风:"))
        self.mic_combo = QComboBox()
        self.populate_microphones()
        mic_layout.addWidget(self.mic_combo)
        mic_layout.addStretch()
        recognition_layout.addLayout(mic_layout)

        # 识别语言选择
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("识别语言:"))
        self.language_combo = QComboBox()
        self.language_combo.addItems(["中文", "English"])
        lang_layout.addWidget(self.language_combo)
        lang_layout.addStretch()
        recognition_layout.addLayout(lang_layout)

        # 识别按钮
        btn_layout = QHBoxLayout()
        self.listen_btn = QPushButton("开始监听")
        self.listen_btn.setFixedHeight(45)
        self.listen_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        self.listen_btn.clicked.connect(self.toggle_listening)
        btn_layout.addWidget(self.listen_btn)
        recognition_layout.addLayout(btn_layout)

        # 识别结果显示
        self.recognition_result = QTextEdit()
        self.recognition_result.setPlaceholderText("识别的语音将显示在这里...")
        self.recognition_result.setMaximumHeight(150)
        self.recognition_result.setStyleSheet("""
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
            }
        """)
        recognition_layout.addWidget(self.recognition_result)

        layout.addWidget(recognition_group)

        # 语音合成区
        tts_group = QGroupBox("语音合成")
        tts_group.setStyleSheet("""
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
        tts_layout = QVBoxLayout(tts_group)

        # 文本输入
        tts_input_label = QLabel("输入要朗读的文本:")
        tts_layout.addWidget(tts_input_label)

        self.tts_input = QTextEdit()
        self.tts_input.setPlaceholderText("输入要让机器人说的话...")
        self.tts_input.setMaximumHeight(100)
        self.tts_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
            }
        """)
        tts_layout.addWidget(self.tts_input)

        # 合成按钮
        tts_btn_layout = QHBoxLayout()
        speak_btn = QPushButton("让机器人说话")
        speak_btn.setFixedHeight(40)
        speak_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #219150;
            }
        """)
        speak_btn.clicked.connect(self.speak_text)
        tts_btn_layout.addStretch()
        tts_btn_layout.addWidget(speak_btn)
        tts_btn_layout.addStretch()
        tts_layout.addLayout(tts_btn_layout)

        layout.addWidget(tts_group)

        # 预设指令区
        preset_group = QGroupBox("预设语音指令")
        preset_group.setStyleSheet("""
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
        preset_layout = QHBoxLayout(preset_group)

        preset_commands = [
            ("你好", "你好，我是小微"),
            ("自我介绍", "我是优必选的小微机器人"),
            ("跳舞", "好的，让我来跳舞"),
            ("再见", "再见，很高兴见到你")
        ]

        for name, text in preset_commands:
            btn = QPushButton(name)
            btn.setFixedSize(100, 40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #9b59b6;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #8e44ad;
                }
            """)
            btn.clicked.connect(lambda checked, t=text: self.quick_speak(t))
            preset_layout.addWidget(btn)

        layout.addWidget(preset_group)

        layout.addStretch()

    def setup_connections(self):
        """设置信号连接"""
        self.speech_recognized.connect(self.on_speech_recognized)

    def populate_microphones(self):
        """填充麦克风列表"""
        try:
            mic_list = sr.Microphone.list_microphone_names()
            for i, mic_name in enumerate(mic_list):
                self.mic_combo.addItem(f"{i}: {mic_name}")
        except Exception as e:
            self.mic_combo.addItem("默认麦克风")

    def toggle_listening(self):
        """切换监听状态"""
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()

    def start_listening(self):
        """开始监听"""
        self.is_listening = True
        self.listen_btn.setText("停止监听")
        self.listen_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        # 在新线程中监听
        thread = threading.Thread(target=self.listen_thread, daemon=True)
        thread.start()

    def stop_listening(self):
        """停止监听"""
        self.is_listening = False
        self.listen_btn.setText("开始监听")
        self.listen_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

    def listen_thread(self):
        """监听线程"""
        try:
            with self.microphone as source:
                # 调整环境噪音
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

                while self.is_listening:
                    try:
                        # 监听语音
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)

                        # 识别语音
                        lang = "zh-CN" if self.language_combo.currentIndex() == 0 else "en-US"
                        text = self.recognizer.recognize_google(audio, language=lang)

                        # 发送信号
                        self.speech_recognized.emit(text)

                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError:
                        self.speech_recognized.emit("语音识别服务不可用")
                        break
                    except Exception as e:
                        self.speech_recognized.emit(f"识别错误: {str(e)}")
                        break

        except Exception as e:
            self.speech_recognized.emit(f"麦克风错误: {str(e)}")

    def on_speech_recognized(self, text: str):
        """处理识别结果"""
        self.recognition_result.append(f"> {text}")

        # 自动滚动到底部
        cursor = self.recognition_result.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.recognition_result.setTextCursor(cursor)

        # 将识别结果发送给机器人
        self.robot_controller.send_command("speech", action="listen", text=text)

    def speak_text(self):
        """让机器人说话"""
        text = self.tts_input.toPlainText().strip()
        if text:
            self.robot_controller.send_command("speech", action="speak", text=text)
        else:
            self.tts_input.setFocus()

    def quick_speak(self, text: str):
        """快速说话"""
        self.tts_input.setText(text)
        self.speak_text()
