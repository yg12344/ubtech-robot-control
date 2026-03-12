"""
编程教学屏幕
"""

from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp


class CodeScreen(MDScreen):
    """编程教学屏幕"""

    title = StringProperty('编程教学')
    right_action_items = [['code-braces', lambda x: None]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.example_codes = self.load_examples()
        self.current_category = '基础'

    def load_examples(self):
        """加载示例代码"""
        return {
            '基础': {
                '打招呼': '''# 让机器人打招呼
robot.speak("你好，我是小微")
robot.wave()

# 等待2秒
time.sleep(2)

# 再次说话
robot.speak("很高兴见到你！")
''',
                '行走': '''# 让机器人前进1米
robot.walk("forward", distance=1.0, speed=5)

# 转向
robot.turn("left", angle=90)

# 再次前进
robot.walk("forward", distance=0.5, speed=3)
''',
                '跳舞': '''# 播放舞蹈
robot.dance("摆臂舞")

# 等待舞蹈完成
time.sleep(10)

# 挥手结束
robot.wave()
'''
            },
            '进阶': {
                '条件判断': '''# 根据距离选择行动
distance = robot.get_distance_to_object()

if distance < 0.5:
    robot.walk("backward", distance=0.3)
    robot.speak("请保持距离")
elif distance > 2.0:
    robot.walk("forward", distance=0.5)
else:
    robot.wave()
''',
                '循环动作': '''# 循环跳舞3次
for i in range(3):
    robot.dance("机械舞")
    time.sleep(5)
    robot.wave()
    time.sleep(1)

# 完成后鞠躬
robot.bow()
'''
            },
            '高级': {
                '传感器数据': '''# 读取传感器数据
distance = robot.get_distance()
angle = robot.get_joint_angle("left_arm")
battery = robot.get_battery_level()

print(f"距离: {distance}米")
print(f"左臂角度: {angle}度")
print(f"电量: {battery}%")
'''
            }
        }

    def on_enter(self, *args):
        """进入屏幕"""
        self.add_content()

    def add_content(self):
        """添加内容"""
        from kivy.uix.scrollview import ScrollView

        content = MDBoxLayout(orientation='horizontal', spacing=dp(10))

        # 左侧：示例选择
        left_panel = MDBoxLayout(orientation='vertical', size_hint_x=0.3, spacing=dp(10))
        left_panel.add_widget(MDLabel(text='示例代码', font_size=dp(16)))

        # 分类选择
        category_box = MDBoxLayout(orientation='vertical', size_hint_y=None, height=dp(100))
        category_box.add_widget(MDLabel(text='分类:', font_size=dp(14)))
        self.category_spinner = MDSpinner(
            text='基础',
            values=('基础', '进阶', '高级'),
            size_hint=(1, None),
            height=dp(45)
        )
        self.category_spinner.bind(text=self.on_category_change)
        category_box.add_widget(self.category_spinner)
        left_panel.add_widget(category_box)

        # 示例列表
        left_panel.add_widget(MDLabel(text='选择示例:', font_size=dp(14)))
        self.example_spinner = MDSpinner(
            text='打招呼',
            values=list(self.example_codes['基础'].keys()),
            size_hint=(1, None),
            height=dp(45)
        )
        self.example_spinner.bind(text=self.on_example_change)
        left_panel.add_widget(self.example_spinner)
        left_panel.add_widget(MDBoxLayout())

        # 右侧：代码编辑器
        right_panel = MDBoxLayout(orientation='vertical', size_hint_x=0.7, spacing=dp(10))

        # 代码标题和按钮
        title_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        title_box.add_widget(MDLabel(text='代码编辑器', size_hint_x=0.6))
        run_btn = MDRaisedButton(
            text='运行',
            md_bg_color='#27ae60',
            size_hint_x=0.2
        )
        run_btn.bind(on_release=self.run_code)
        title_box.add_widget(run_btn)
        clear_btn = MDRaisedButton(
            text='清空',
            md_bg_color='#e74c3c',
            size_hint_x=0.2
        )
        clear_btn.bind(on_release=self.clear_code)
        title_box.add_widget(clear_btn)
        right_panel.add_widget(title_box)

        # 代码编辑器
        self.code_editor = MDTextField(
            multiline=True,
            text=self.example_codes['基础']['打招呼'],
            size_hint=(1, 0.5),
            hint_text='# 在此编写控制代码...',
            font_size=dp(12)
        )
        right_panel.add_widget(self.code_editor)

        # 输出区域
        right_panel.add_widget(MDLabel(text='输出:', font_size=dp(14)))
        self.output_text = MDTextField(
            multiline=True,
            readonly=True,
            size_hint=(1, 0.3),
            hint_text='代码执行结果...'
        )
        right_panel.add_widget(self.output_text)

        # 添加到主容器
        content.add_widget(left_panel)
        content.add_widget(right_panel)

        # 滚动视图
        scroll = ScrollView()
        scroll.add_widget(content)
        self.ids.content_container.add_widget(scroll)

    def on_category_change(self, spinner, text):
        """分类改变"""
        self.current_category = text
        self.example_spinner.values = list(self.example_codes[text].keys())
        self.example_spinner.text = self.example_spinner.values[0]

    def on_example_change(self, spinner, text):
        """示例改变"""
        if text in self.example_codes[self.current_category]:
            self.code_editor.text = self.example_codes[self.current_category][text]
            self.output_text.text = ''

    def clear_code(self, *args):
        """清空代码"""
        self.code_editor.text = ''
        self.output_text.text = ''

    def run_code(self, *args):
        """运行代码"""
        code = self.code_editor.text.strip()
        if code:
            self.output_text.text = '=' * 40 + '\n'
            self.output_text.text += '正在执行...\n'
            self.output_text.text += '✓ 代码已发送到机器人\n'
            self.output_text.text += '注意: 实际执行需要机器人API支持'

            app = self.manager.parent.app
            app.robot_controller.send_command('code', action='execute', code=code)

            self.show_snackbar('代码已发送')
        else:
            self.show_snackbar('请输入代码', color='#e74c3c')

    def show_snackbar(self, text, color='#3498db'):
        """显示提示"""
        from kivymd.uix.snackbar import MDSnackbar
        snackbar = MDSnackbar(text=text, md_bg_color=color, y=dp(20), duration=2)
        snackbar.open()


# 导入必要的组件
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.label import MDLabel
