"""
编程与教学模块
提供代码编辑器和示例代码
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QComboBox, QTextEdit, QTabWidget,
                             QMessageBox, QSplitter)
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
import json


class PythonSyntaxHighlighter(QSyntaxHighlighter):
    """Python语法高亮"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # 关键字格式
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor("#7f0055"))
        self.keyword_format.setFontWeight(QFont.Weight.Bold)

        # 字符串格式
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#008000"))

        # 注释格式
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#808080"))
        self.comment_format.setFontItalic(True)

        # 函数格式
        self.function_format = QTextCharFormat()
        self.function_format.setForeground(QColor("#0000FF"))
        self.function_format.setFontWeight(QFont.Weight.Bold)

        # 定义高亮规则
        self.highlighting_rules = []

        # 关键字
        keywords = [
            "def", "class", "if", "elif", "else", "for", "while",
            "return", "import", "from", "as", "try", "except", "finally",
            "with", "True", "False", "None", "and", "or", "not", "in",
            "is", "pass", "break", "continue", "yield", "lambda", "global"
        ]
        for keyword in keywords:
            pattern = QRegularExpression(rf"\b{keyword}\b")
            self.highlighting_rules.append((pattern, self.keyword_format))

        # 字符串
        self.highlighting_rules.append((QRegularExpression(r'".*"'), self.string_format))
        self.highlighting_rules.append((QRegularExpression(r"'.*'"), self.string_format))

        # 注释
        self.highlighting_rules.append((QRegularExpression(r"#.*"), self.comment_format))

    def highlightBlock(self, text):
        """高亮文本块"""
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)


class CodeEditorPage(QWidget):
    """编程与教学页面"""

    def __init__(self, robot_controller):
        super().__init__()
        self.robot_controller = robot_controller
        self.example_codes = self.load_example_codes()
        self.init_ui()

    def load_example_codes(self):
        """加载示例代码"""
        return {
            "基础": {
                "打招呼": '''# 让机器人打招呼
robot.speak("你好，我是小微")
robot.wave()

# 等待2秒
time.sleep(2)

# 再次说话
robot.speak("很高兴见到你！")
''',
                "行走": '''# 让机器人前进1米
robot.walk("forward", distance=1.0, speed=5)

# 转向
robot.turn("left", angle=90)

# 再次前进
robot.walk("forward", distance=0.5, speed=3)
''',
                "跳舞": '''# 播放舞蹈
robot.dance("摆臂舞")

# 等待舞蹈完成
time.sleep(10)

# 挥手结束
robot.wave()
'''
            },
            "进阶": {
                "条件判断": '''# 根据距离选择行动
distance = robot.get_distance_to_object()

if distance < 0.5:
    # 距离太近，后退
    robot.walk("backward", distance=0.3)
    robot.speak("请保持距离")
elif distance > 2.0:
    # 距离太远，靠近
    robot.walk("forward", distance=0.5)
else:
    # 距离合适，打招呼
    robot.wave()
''',
                "循环动作": '''# 循环跳舞3次
for i in range(3):
    robot.dance("机械舞")
    time.sleep(5)
    robot.wave()
    time.sleep(1)

# 完成后鞠躬
robot.bow()
''',
                "异常处理": '''# 安全的运动控制
try:
    robot.walk("forward", distance=2.0)
except RobotError as e:
    robot.speak("遇到错误")
    print(f"错误: {e}")
finally:
    # 确保机器人停止
    robot.stop()
'''
            },
            "高级": {
                "传感器数据": '''# 读取传感器数据
distance = robot.get_distance()
angle = robot.get_joint_angle("left_arm")
battery = robot.get_battery_level()

print(f"距离: {distance}米")
print(f"左臂角度: {angle}度")
print(f"电量: {battery}%")
''',
                "语音交互": '''# 语音交互循环
while True:
    # 监听用户语音
    text = robot.listen()

    if "你好" in text:
        robot.wave()
        robot.speak("你好！")
    elif "再见" in text:
        robot.speak("再见！")
        break
    elif "跳舞" in text:
        robot.dance("迪斯科")
''',
                "自定义动作": '''# 创建自定义动作序列
action_sequence = [
    ("raise_arm", "left"),
    ("wave", 3),
    ("lower_arm", "left"),
    ("bow",),
]

# 执行动作序列
for action in action_sequence:
    robot.execute_action(*action)
    time.sleep(1)
'''
            }
        }

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # 标题
        title = QLabel("编程与教学")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        layout.addWidget(title)

        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        # 左侧面板 - 示例代码
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # 示例代码选择
        example_label = QLabel("示例代码")
        example_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #34495e;
            }
        """)
        left_layout.addWidget(example_label)

        # 分类选择
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("分类:"))
        self.category_combo = QComboBox()
        self.category_combo.addItems(["基础", "进阶", "高级"])
        self.category_combo.currentTextChanged.connect(self.update_example_list)
        category_layout.addWidget(self.category_combo)
        category_layout.addStretch()
        left_layout.addLayout(category_layout)

        # 示例列表
        self.example_combo = QComboBox()
        self.example_combo.currentTextChanged.connect(self.load_example)
        left_layout.addWidget(self.example_combo)

        left_layout.addStretch()

        # 右侧面板 - 代码编辑器
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # 工具栏
        toolbar_layout = QHBoxLayout()

        # 代码标题
        right_layout.addWidget(QLabel("代码编辑器"))

        # 操作按钮
        run_btn = QPushButton("运行代码")
        run_btn.setFixedHeight(35)
        run_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #219150;
            }
        """)
        run_btn.clicked.connect(self.run_code)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(run_btn)

        clear_btn = QPushButton("清空")
        clear_btn.setFixedHeight(35)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        clear_btn.clicked.connect(self.clear_code)
        toolbar_layout.addWidget(clear_btn)

        right_layout.addLayout(toolbar_layout)

        # 代码编辑器
        self.code_editor = QTextEdit()
        self.code_editor.setPlaceholderText("# 在此编写控制代码...")
        self.code_editor.setStyleSheet("""
            QTextEdit {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                padding: 10px;
            }
        """)
        self.code_editor.setFont(QFont("Courier New", 11))

        # 添加语法高亮
        self.highlighter = PythonSyntaxHighlighter(self.code_editor.document())

        right_layout.addWidget(self.code_editor)

        # 输出区域
        output_label = QLabel("输出:")
        output_label.setStyleSheet("font-weight: bold;")
        right_layout.addWidget(output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMaximumHeight(200)
        self.output_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: #f8f9fa;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                padding: 10px;
            }
        """)
        right_layout.addWidget(self.output_text)

        # 添加到分割器
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([250, 600])

        layout.addWidget(splitter)

        # 初始化示例列表
        self.update_example_list("基础")

    def update_example_list(self, category: str):
        """更新示例列表"""
        self.example_combo.clear()
        if category in self.example_codes:
            self.example_combo.addItems(self.example_codes[category].keys())
        if self.example_combo.count() > 0:
            self.load_example(self.example_combo.currentText())

    def load_example(self, example_name: str):
        """加载示例代码"""
        category = self.category_combo.currentText()
        if category in self.example_codes and example_name in self.example_codes[category]:
            code = self.example_codes[category][example_name]
            self.code_editor.setPlainText(code)
            self.output_text.clear()

    def clear_code(self):
        """清空代码"""
        self.code_editor.clear()
        self.output_text.clear()

    def run_code(self):
        """运行代码"""
        code = self.code_editor.toPlainText()
        if not code.strip():
            QMessageBox.warning(self, "警告", "请先输入代码！")
            return

        self.output_text.append("=" * 50)
        self.output_text.append(f"执行代码: {self.code_editor.toPlainText()[:50]}...")
        self.output_text.append("=" * 50)

        # 在实际应用中，这里会将代码发送给机器人执行
        # 现在模拟执行
        self.output_text.append("正在执行...")
        self.output_text.append("✓ 代码已发送到机器人")
        self.output_text.append("注意: 实际执行需要机器人API支持")

        # 发送到机器人（示例）
        self.robot_controller.send_command("code", action="execute", code=code)
