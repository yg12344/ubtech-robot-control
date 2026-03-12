"""
语音交互屏幕
"""

from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, BooleanProperty
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp


class VoiceScreen(MDScreen):
    """语音交互屏幕"""

    title = StringProperty('语音交互')
    right_action_items = [['microphone', lambda x: None]]
    is_listening = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recognition_history = []

    def on_enter(self, *args):
        """进入屏幕"""
        self.add_content()

    def add_content(self):
        """添加内容"""
        from kivy.uix.scrollview import ScrollView

        content = MDBoxLayout(orientation='vertical', spacing=dp(10))

        # 语音识别区
        content.add_widget(self.create_section_label('语音识别'))

        # 监听按钮
        self.listen_btn = MDRaisedButton(
            text='开始监听',
            size_hint=(1, None),
            height=dp(60),
            md_bg_color='#3498db',
            font_size=dp(16)
        )
        self.listen_btn.bind(on_release=self.toggle_listening)
        content.add_widget(self.listen_btn)

        # 语言选择
        lang_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        lang_box.add_widget(MDLabel(text='识别语言:', size_hint_x=0.4))
        self.language_spinner = MDSpinner(
            text='中文',
            values=('中文', 'English'),
            size_hint_x=0.6
        )
        lang_box.add_widget(self.language_spinner)
        content.add_widget(lang_box)

        # 识别结果显示
        content.add_widget(MDLabel(text='识别结果:', font_size=dp(14)))
        self.recognition_text = MDTextField(
            multiline=True,
            size_hint=(1, None),
            height=dp(120),
            hint_text='识别的语音将显示在这里...',
            readonly=True
        )
        content.add_widget(self.recognition_text)

        # 语音合成区
        content.add_widget(self.create_section_label('语音合成'))

        content.add_widget(MDLabel(text='输入要朗读的文本:', font_size=dp(14)))
        self.tts_input = MDTextField(
            multiline=True,
            size_hint=(1, None),
            height=dp(100),
            hint_text='输入要让机器人说的话...'
        )
        content.add_widget(self.tts_input)

        speak_btn = MDRaisedButton(
            text='让机器人说话',
            size_hint=(1, None),
            height=dp(50),
            md_bg_color='#27ae60'
        )
        speak_btn.bind(on_release=self.speak_text)
        content.add_widget(speak_btn)

        # 预设指令
        content.add_widget(self.create_section_label('快速指令'))
        preset_box = MDBoxLayout(spacing=dp(10))
        presets = [
            ('你好', '你好，我是小微'),
            ('自我介绍', '我是优必选的小微机器人'),
            ('跳舞', '好的，让我来跳舞'),
            ('再见', '再见，很高兴见到你')
        ]
        for name, text in presets:
            btn = MDRaisedButton(
                text=name,
                size_hint=(1, None),
                height=dp(45),
                md_bg_color='#9b59b6'
            )
            btn.bind(on_release=lambda x, t=text: self.quick_speak(t))
            preset_box.add_widget(btn)
        content.add_widget(preset_box)

        # 滚动视图
        scroll = ScrollView()
        scroll.add_widget(content)
        self.ids.content_container.add_widget(scroll)

    def create_section_label(self, text):
        """创建章节标签"""
        from kivymd.uix.label import MDLabel
        return MDLabel(text=text, font_size=dp(18), font_style='H6', size_hint_y=None, height=dp(40))

    def toggle_listening(self, *args):
        """切换监听状态"""
        self.is_listening = not self.is_listening

        if self.is_listening:
            self.listen_btn.text = '停止监听'
            self.listen_btn.md_bg_color = '#e74c3c'
            self.start_listening()
        else:
            self.listen_btn.text = '开始监听'
            self.listen_btn.md_bg_color = '#3498db'
            self.stop_listening()

    def start_listening(self):
        """开始监听"""
        self.show_snackbar('正在监听...')

        # 在实际应用中，这里会调用语音识别API
        # 由于Kivy在Android上的语音识别需要额外配置
        # 这里做简化处理

    def stop_listening(self):
        """停止监听"""
        self.show_snackbar('已停止监听')

    def on_speech_recognized(self, text):
        """处理识别结果"""
        self.recognition_history.append(text)
        self.recognition_text.text = '\n'.join(self.recognition_history)

        # 发送给机器人
        app = self.manager.parent.app
        app.robot_controller.send_command('speech', action='listen', text=text)

        self.show_snackbar(f'识别: {text}')

    def speak_text(self, *args):
        """让机器人说话"""
        text = self.tts_input.text.strip()
        if text:
            app = self.manager.parent.app
            app.robot_controller.send_command('speech', action='speak', text=text)
            self.show_snackbar('已发送语音指令')
        else:
            self.show_snackbar('请输入文本', color='#e74c3c')

    def quick_speak(self, text):
        """快速说话"""
        self.tts_input.text = text
        self.speak_text()

    def show_snackbar(self, text, color='#3498db'):
        """显示提示"""
        from kivymd.uix.snackbar import MDSnackbar
        snackbar = MDSnackbar(text=text, md_bg_color=color, y=dp(20), duration=2)
        snackbar.open()


# 为了兼容性导入
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.label import MDLabel
