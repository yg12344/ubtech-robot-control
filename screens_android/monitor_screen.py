"""
远程监控屏幕
"""

from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, BooleanProperty
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.clock import Clock
from kivy.metrics import dp
import random


class MonitorScreen(MDScreen):
    """监控屏幕"""

    title = StringProperty('远程监控')
    right_action_items = [['refresh', lambda x: None]]
    monitoring = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_history = {
            'battery': [],
            'temperature': [],
            'distance': []
        }
        self.max_history = 50

    def on_enter(self, *args):
        """进入屏幕"""
        self.add_content()

    def add_content(self):
        """添加内容"""
        from kivy.uix.scrollview import ScrollView

        content = MDBoxLayout(orientation='vertical', spacing=dp(10))

        # 控制按钮
        control_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        self.toggle_btn = MDRaisedButton(
            text='开始监控',
            md_bg_color='#27ae60',
            size_hint=(1, None),
            height=dp(50)
        )
        self.toggle_btn.bind(on_release=self.toggle_monitoring)
        control_box.add_widget(self.toggle_btn)
        content.add_widget(control_box)

        # 状态信息
        content.add_widget(self.create_section_label('机器人状态'))
        status_grid = self.create_status_grid()
        content.add_widget(status_grid)

        # 传感器数据
        content.add_widget(self.create_section_label('传感器数据'))
        sensor_grid = self.create_sensor_grid()
        content.add_widget(sensor_grid)

        # 数据图表（简化显示）
        content.add_widget(self.create_charts())

        # 滚动视图
        scroll = ScrollView()
        scroll.add_widget(content)
        self.ids.content_container.add_widget(scroll)

        # 初始化状态更新
        Clock.schedule_once(lambda dt: self.update_status())

    def create_section_label(self, text):
        """创建章节标签"""
        from kivymd.uix.label import MDLabel
        return MDLabel(text=text, font_size=dp(18), font_style='H6', size_hint_y=None, height=dp(40))

    def create_status_grid(self):
        """创建状态网格"""
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel

        card = MDCard(padding=dp(10))
        grid = MDGridLayout(cols=2, spacing=dp(10))

        status_items = [
            ('连接状态', 'connection_status', '未连接'),
            ('电池电量', 'battery_level', '0%'),
            ('CPU使用率', 'cpu_usage', '0%'),
            ('温度', 'temperature', '0°C')
        ]

        self.status_labels = {}
        for label_text, label_id, default_value in status_items:
            item_box = MDBoxLayout(orientation='vertical', spacing=dp(5))
            item_box.add_widget(MDLabel(text=label_text, font_size=dp(12)))
            value_label = MDLabel(
                text=default_value,
                font_size=dp(16),
                halign='center',
                theme_text_color='Custom'
            )
            if label_id == 'connection_status':
                value_label.text_color = 0.93, 0.26, 0.26, 1
            else:
                value_label.text_color = 1, 1, 1, 1
            item_box.add_widget(value_label)
            self.status_labels[label_id] = value_label
            grid.add_widget(item_box)

        card.add_widget(grid)
        return card

    def create_sensor_grid(self):
        """创建传感器网格"""
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel

        card = MDCard(padding=dp(10))
        grid = MDGridLayout(cols=2, spacing=dp(10))

        sensor_items = [
            ('前方距离', 'front_distance', '0.00 m'),
            ('左侧距离', 'left_distance', '0.00 m'),
            ('右侧距离', 'right_distance', '0.00 m'),
            ('陀螺仪Z', 'gyro_z', '0.0°')
        ]

        self.sensor_labels = {}
        for label_text, label_id, default_value in sensor_items:
            item_box = MDBoxLayout(orientation='vertical', spacing=dp(5))
            item_box.add_widget(MDLabel(text=label_text, font_size=dp(12)))
            value_label = MDLabel(
                text=default_value,
                font_size=dp(16),
                halign='center',
                theme_text_color='Custom',
                text_color=1, 1, 1, 1
            )
            item_box.add_widget(value_label)
            self.sensor_labels[label_id] = value_label
            grid.add_widget(item_box)

        card.add_widget(grid)
        return card

    def create_charts(self):
        """创建图表"""
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel

        card = MDCard(padding=dp(10), size_hint_y=None, height=dp(200))

        chart_box = MDBoxLayout(orientation='vertical')
        chart_box.add_widget(MDLabel(text='实时数据趋势', font_size=dp(14)))

        # 简化显示，使用进度条代替图表
        progress_box = MDBoxLayout(orientation='vertical', spacing=dp(10))

        # 电池电量
        battery_box = MDBoxLayout(orientation='vertical', size_hint_y=None, height=dp(40))
        battery_box.add_widget(MDLabel(text='电池电量', font_size=dp(10)))
        self.battery_progress = MDProgressBar(
            value=0,
            size_hint=(1, None),
            height=dp(20),
            color=(0.2, 0.6, 0.87, 1)
        )
        battery_box.add_widget(self.battery_progress)
        progress_box.add_widget(battery_box)

        # 温度
        temp_box = MDBoxLayout(orientation='vertical', size_hint_y=None, height=dp(40))
        temp_box.add_widget(MDLabel(text='温度', font_size=dp(10)))
        self.temp_progress = MDProgressBar(
            value=0,
            size_hint=(1, None),
            height=dp(20),
            color=(0.93, 0.26, 0.26, 1)
        )
        temp_box.add_widget(self.temp_progress)
        progress_box.add_widget(temp_box)

        chart_box.add_widget(progress_box)
        card.add_widget(chart_box)
        return card

    def toggle_monitoring(self, *args):
        """切换监控状态"""
        self.monitoring = not self.monitoring

        if self.monitoring:
            self.toggle_btn.text = '停止监控'
            self.toggle_btn.md_bg_color = '#e74c3c'
            Clock.schedule_interval(self.update_data, 1.0)
        else:
            self.toggle_btn.text = '开始监控'
            self.toggle_btn.md_bg_color = '#27ae60'
            Clock.unschedule(self.update_data)

    def update_status(self):
        """更新状态"""
        app = self.manager.parent.app
        if app.robot_controller.is_connected():
            self.status_labels['connection_status'].text = '已连接'
            self.status_labels['connection_status'].text_color = 0.15, 0.8, 0.44, 1
        else:
            self.status_labels['connection_status'].text = '未连接'
            self.status_labels['connection_status'].text_color = 0.93, 0.26, 0.26, 1

    def update_data(self, dt):
        """更新数据"""
        self.update_status()

        # 模拟数据（实际应用中从机器人获取）
        battery = max(0, 100 - len(self.data_history['battery']) * 0.2)
        temperature = 35 + random.uniform(-2, 2)
        distance = 1.5 + random.uniform(-0.5, 0.5)

        # 更新状态标签
        self.status_labels['battery_level'].text = f'{battery:.1f}%'
        self.status_labels['temperature'].text = f'{temperature:.1f}°C'
        self.status_labels['cpu_usage'].text = f'{random.randint(10, 30)}%'

        # 更新传感器标签
        self.sensor_labels['front_distance'].text = f'{distance:.2f} m'
        self.sensor_labels['left_distance'].text = f'{distance * random.uniform(0.8, 1.2):.2f} m'
        self.sensor_labels['right_distance'].text = f'{distance * random.uniform(0.8, 1.2):.2f} m'
        self.sensor_labels['gyro_z'].text = f'{random.uniform(-1, 1):.1f}°'

        # 更新进度条
        self.battery_progress.value = battery
        self.temp_progress.value = temperature * 1.25  # 缩放到0-100

        # 更新历史数据
        self.data_history['battery'].append(battery)
        self.data_history['temperature'].append(temperature)
        self.data_history['distance'].append(distance)

        # 保持历史长度
        for key in self.data_history:
            if len(self.data_history[key]) > self.max_history:
                self.data_history[key].pop(0)

    def show_snackbar(self, text, color='#3498db'):
        """显示提示"""
        from kivymd.uix.snackbar import MDSnackbar
        snackbar = MDSnackbar(text=text, md_bg_color=color, y=dp(20), duration=2)
        snackbar.open()


# 导入必要的组件
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
