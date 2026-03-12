"""
系统设置屏幕
"""

from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
import json
import os


class Tab(MDFloatLayout, MDTabsBase):
    """标签页基类"""
    pass


class SettingsScreen(MDScreen):
    """设置屏幕"""

    title = StringProperty('系统设置')
    right_action_items = [['cog', lambda x: None]]

    CONFIG_FILE = 'config.json'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = self.load_config()

    @staticmethod
    def load_config():
        """加载配置"""
        default_config = {
            'connection': {
                'type': 'tcp',
                'bluetooth_address': '00:00:00:00:00:00',
                'tcp_host': '192.168.1.100',
                'tcp_port': 8080
            },
            'voice': {
                'language': 'zh-CN'
            },
            'general': {
                'auto_connect': False,
                'update_interval': 1000
            }
        }

        if os.path.exists(SettingsScreen.CONFIG_FILE):
            try:
                with open(SettingsScreen.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    default_config.update(loaded)
            except:
                pass

        return default_config

    @staticmethod
    def get_connection_type():
        """获取连接类型"""
        config = SettingsScreen.load_config()
        return config.get('connection', {}).get('type', 'tcp')

    @staticmethod
    def get_bluetooth_address():
        """获取蓝牙地址"""
        config = SettingsScreen.load_config()
        return config.get('connection', {}).get('bluetooth_address', '00:00:00:00:00:00')

    @staticmethod
    def get_tcp_host():
        """获取TCP主机"""
        config = SettingsScreen.load_config()
        return config.get('connection', {}).get('tcp_host', '192.168.1.100')

    @staticmethod
    def get_tcp_port():
        """获取TCP端口"""
        config = SettingsScreen.load_config()
        return config.get('connection', {}).get('tcp_port', 8080)

    def on_enter(self, *args):
        """进入屏幕"""
        self.add_content()

    def add_content(self):
        """添加内容"""
        from kivymd.uix.tabs import MDTabs

        tabs = MDTabs()
        tabs.add_widget(self.create_connection_tab())
        tabs.add_widget(self.create_voice_tab())
        tabs.add_widget(self.create_general_tab())

        # 底部按钮
        button_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(70), spacing=dp(10))

        apply_btn = MDRaisedButton(
            text='应用',
            md_bg_color='#27ae60',
            size_hint=(0.5, None),
            height=dp(50)
        )
        apply_btn.bind(on_release=self.apply_settings)
        button_box.add_widget(apply_btn)

        save_btn = MDRaisedButton(
            text='保存',
            md_bg_color='#3498db',
            size_hint=(0.5, None),
            height=dp(50)
        )
        save_btn.bind(on_release=self.save_settings)
        button_box.add_widget(save_btn)

        # 主布局
        main_box = MDBoxLayout(orientation='vertical', spacing=dp(10))
        main_box.add_widget(tabs)
        main_box.add_widget(button_box)

        # 滚动视图
        scroll = ScrollView()
        scroll.add_widget(main_box)
        self.ids.content_container.add_widget(scroll)

    def create_connection_tab(self):
        """创建连接设置标签页"""
        tab = Tab(title='连接')

        content = MDBoxLayout(orientation='vertical', spacing=dp(15), padding=dp(15))

        # 连接方式
        content.add_widget(MDLabel(text='连接方式', font_size=dp(14)))
        self.connection_spinner = MDSpinner(
            text='TCP/IP连接',
            values=('蓝牙连接', 'TCP/IP连接'),
            size_hint=(1, None),
            height=dp(45)
        )

        conn_type = self.config.get('connection', {}).get('type', 'tcp')
        self.connection_spinner.text = '蓝牙连接' if conn_type == 'bluetooth' else 'TCP/IP连接'

        content.add_widget(self.connection_spinner)

        # 蓝牙设置
        self.bluetooth_box = MDBoxLayout(orientation='vertical', spacing=dp(10))
        self.bluetooth_box.add_widget(MDLabel(text='蓝牙MAC地址', font_size=dp(14)))
        self.bluetooth_input = MDTextField(
            text=self.config.get('connection', {}).get('bluetooth_address', ''),
            hint_text='00:00:00:00:00:00',
            size_hint=(1, None),
            height=dp(50)
        )
        self.bluetooth_box.add_widget(self.bluetooth_input)

        # TCP设置
        self.tcp_box = MDBoxLayout(orientation='vertical', spacing=dp(10))
        self.tcp_box.add_widget(MDLabel(text='主机地址', font_size=dp(14)))
        self.tcp_host_input = MDTextField(
            text=self.config.get('connection', {}).get('tcp_host', '192.168.1.100'),
            hint_text='192.168.1.100',
            size_hint=(1, None),
            height=dp(50)
        )
        self.tcp_box.add_widget(self.tcp_host_input)

        self.tcp_box.add_widget(MDLabel(text='端口', font_size=dp(14)))
        self.tcp_port_input = MDTextField(
            text=str(self.config.get('connection', {}).get('tcp_port', 8080)),
            hint_text='8080',
            size_hint=(1, None),
            height=dp(50)
        )
        self.tcp_box.add_widget(self.tcp_port_input)

        # 根据连接类型显示/隐藏
        self.on_connection_type_change(self.connection_spinner, self.connection_spinner.text)
        self.connection_spinner.bind(text=self.on_connection_type_change)

        content.add_widget(self.bluetooth_box)
        content.add_widget(self.tcp_box)

        scroll = ScrollView()
        scroll.add_widget(content)
        tab.add_widget(scroll)

        return tab

    def create_voice_tab(self):
        """创建语音设置标签页"""
        tab = Tab(title='语音')

        content = MDBoxLayout(orientation='vertical', spacing=dp(15), padding=dp(15))

        # 识别语言
        content.add_widget(MDLabel(text='识别语言', font_size=dp(14)))
        self.language_spinner = MDSpinner(
            text='中文',
            values=('中文', 'English'),
            size_hint=(1, None),
            height=dp(45)
        )

        lang = self.config.get('voice', {}).get('language', 'zh-CN')
        self.language_spinner.text = '中文' if lang.startswith('zh') else 'English'

        content.add_widget(self.language_spinner)

        scroll = ScrollView()
        scroll.add_widget(content)
        tab.add_widget(scroll)

        return tab

    def create_general_tab(self):
        """创建常规设置标签页"""
        tab = Tab(title='常规')

        content = MDBoxLayout(orientation='vertical', spacing=dp(15), padding=dp(15))

        # 自动连接
        content.add_widget(MDLabel(text='启动时自动连接', font_size=dp(14)))
        self.auto_connect_spinner = MDSpinner(
            text='否',
            values=('是', '否'),
            size_hint=(1, None),
            height=dp(45)
        )

        auto_connect = self.config.get('general', {}).get('auto_connect', False)
        self.auto_connect_spinner.text = '是' if auto_connect else '否'

        content.add_widget(self.auto_connect_spinner)

        # 更新间隔
        content.add_widget(MDLabel(text='数据更新间隔(ms)', font_size=dp(14)))
        self.update_interval_input = MDTextField(
            text=str(self.config.get('general', {}).get('update_interval', 1000)),
            hint_text='1000',
            size_hint=(1, None),
            height=dp(50)
        )
        content.add_widget(self.update_interval_input)

        scroll = ScrollView()
        scroll.add_widget(content)
        tab.add_widget(scroll)

        return tab

    def on_connection_type_change(self, spinner, text):
        """连接类型改变"""
        if '蓝牙' in text:
            self.bluetooth_box.height = dp(100)
            self.bluetooth_box.opacity = 1
            self.tcp_box.height = 0
            self.tcp_box.opacity = 0
        else:
            self.bluetooth_box.height = 0
            self.bluetooth_box.opacity = 0
            self.tcp_box.height = dp(120)
            self.tcp_box.opacity = 1

    def apply_settings(self, *args):
        """应用设置"""
        # 更新连接设置
        conn_type = 'bluetooth' if '蓝牙' in self.connection_spinner.text else 'tcp'
        self.config['connection']['type'] = conn_type
        self.config['connection']['bluetooth_address'] = self.bluetooth_input.text
        self.config['connection']['tcp_host'] = self.tcp_host_input.text

        try:
            port = int(self.tcp_port_input.text)
            self.config['connection']['tcp_port'] = port
        except:
            pass

        # 更新语音设置
        self.config['voice']['language'] = 'zh-CN' if self.language_spinner.text == '中文' else 'en-US'

        # 更新常规设置
        self.config['general']['auto_connect'] = self.auto_connect_spinner.text == '是'

        try:
            interval = int(self.update_interval_input.text)
            self.config['general']['update_interval'] = interval
        except:
            pass

        self.show_snackbar('设置已应用')

    def save_settings(self, *args):
        """保存设置"""
        self.apply_settings()

        try:
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            self.show_snackbar('设置已保存')
        except Exception as e:
            self.show_snackbar(f'保存失败: {e}', color='#e74c3c')

    def show_snackbar(self, text, color='#3498db'):
        """显示提示"""
        from kivymd.uix.snackbar import MDSnackbar
        snackbar = MDSnackbar(text=text, md_bg_color=color, y=dp(20), duration=2)
        snackbar.open()


# 导入必要的组件
from kivymd.uix.label import MDLabel
from kivymd.uix.spinner import MDSpinner
