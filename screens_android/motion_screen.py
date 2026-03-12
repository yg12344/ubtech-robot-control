"""
运动控制屏幕
"""

from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.slider import MDSlider
from kivy.metrics import dp


class MotionScreen(MDScreen):
    """运动控制屏幕"""

    title = StringProperty('运动控制')
    right_action_items = [['refresh', lambda x: None]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.walk_speed = 5
        self.walk_distance = 1.0
        self.walk_direction = 'forward'
        self.add_content()

    def add_content(self):
        """添加内容"""
        from kivy.uix.scrollview import ScrollView
        from kivymd.uix.boxlayout import MDBoxLayout

        content = MDBoxLayout(orientation='vertical', spacing=dp(10))

        # 基础动作
        content.add_widget(self.create_section_label('基础动作'))
        basic_grid = MDGridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(160))
        for name, action in [('站立', 'stand'), ('坐下', 'sit'), ('行走', 'walk'), ('停止', 'stop')]:
            btn = self.create_action_button(name, action, '#3498db')
            basic_grid.add_widget(btn)
        content.add_widget(basic_grid)

        # 手势动作
        content.add_widget(self.create_section_label('手势动作'))
        gesture_grid = MDGridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(160))
        for name, gesture in [('挥手', 'wave'), ('点头', 'nod'), ('摇头', 'shake'), ('鞠躬', 'bow')]:
            btn = self.create_gesture_button(name, gesture, '#9b59b6')
            gesture_grid.add_widget(btn)
        content.add_widget(gesture_grid)

        # 行走控制
        content.add_widget(self.create_section_label('行走控制'))
        content.add_widget(self.create_walk_controls())

        # 舞蹈动作
        content.add_widget(self.create_section_label('舞蹈动作'))
        content.add_widget(self.create_dance_controls())

        # 紧急停止
        emergency_btn = MDRaisedButton(
            text='紧急停止',
            size_hint=(1, None),
            height=dp(60),
            md_bg_color='#c0392b',
            font_size=dp(16)
        )
        emergency_btn.bind(on_release=self.emergency_stop)
        content.add_widget(emergency_btn)

        # 滚动视图
        scroll = ScrollView()
        scroll.add_widget(content)

        # 将滚动视图添加到屏幕
        self.ids.content_container.add_widget(scroll)

    def create_section_label(self, text):
        """创建章节标签"""
        from kivymd.uix.label import MDLabel
        return MDLabel(text=text, font_size=dp(18), font_style='H6', size_hint_y=None, height=dp(40))

    def create_action_button(self, text, action, color):
        """创建动作按钮"""
        btn = MDRaisedButton(
            text=text,
            md_bg_color=color,
            size_hint=(1, None),
            height=dp(70),
            font_size=dp(16)
        )
        btn.bind(on_release=lambda x, a=action: self.send_basic_action(a))
        return btn

    def create_gesture_button(self, text, gesture, color):
        """创建手势按钮"""
        btn = MDRaisedButton(
            text=text,
            md_bg_color=color,
            size_hint=(1, None),
            height=dp(70),
            font_size=dp(16)
        )
        btn.bind(on_release=lambda x, g=gesture: self.send_gesture(g))
        return btn

    def create_walk_controls(self):
        """创建行走控制"""
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.label import MDLabel
        from kivymd.uix.spinner import MDSpinner

        layout = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))

        # 方向选择
        layout.add_widget(MDLabel(text='行走方向', font_size=dp(14)))
        direction_box = MDBoxLayout(spacing=dp(5))
        self.direction_buttons = {}
        for direction, label in [('forward', '前进'), ('backward', '后退'), ('left', '左转'), ('right', '右转')]:
            btn = MDRaisedButton(
                text=label,
                size_hint=(1, None),
                height=dp(40)
            )
            if direction == 'forward':
                btn.md_bg_color = '#3498db'
                self.walk_direction = direction
            else:
                btn.md_bg_color = '#95a5a6'
            btn.bind(on_release=lambda x, d=direction: self.set_direction(d, btn))
            direction_box.add_widget(btn)
            self.direction_buttons[direction] = btn
        layout.add_widget(direction_box)

        # 距离和速度
        layout.add_widget(MDLabel(text='行走距离(米)', font_size=dp(14)))
        self.distance_label = MDLabel(text='1.0', halign='center')
        distance_slider = MDSlider(
            min=0.1,
            max=10.0,
            value=1.0,
            step=0.1
        )
        distance_slider.bind(value=lambda x, v: setattr(self, 'walk_distance', v))
        distance_slider.bind(value=lambda x, v: self.distance_label.__setattr__('text', f'{v:.1f}'))
        layout.add_widget(distance_slider)
        layout.add_widget(self.distance_label)

        layout.add_widget(MDLabel(text='行走速度', font_size=dp(14)))
        self.speed_label = MDLabel(text='5', halign='center')
        speed_slider = MDSlider(
            min=1,
            max=10,
            value=5
        )
        speed_slider.bind(value=lambda x, v: setattr(self, 'walk_speed', int(v)))
        speed_slider.bind(value=lambda x, v: self.speed_label.__setattr__('text', str(int(v))))
        layout.add_widget(speed_slider)
        layout.add_widget(self.speed_label)

        # 执行按钮
        execute_btn = MDRaisedButton(
            text='执行行走',
            size_hint=(1, None),
            height=dp(50),
            md_bg_color='#34495e'
        )
        execute_btn.bind(on_release=self.execute_walk)
        layout.add_widget(execute_btn)

        return layout

    def create_dance_controls(self):
        """创建舞蹈控制"""
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.label import MDLabel

        layout = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))

        layout.add_widget(MDLabel(text='选择舞蹈', font_size=dp(14)))

        dances = ['摆臂舞', '太空步', '机械舞', '迪斯科', '民族舞']
        dance_grid = MDGridLayout(cols=3, spacing=dp(10), size_hint_y=None)
        for i, dance in enumerate(dances):
            btn = MDRaisedButton(
                text=dance,
                size_hint=(1, None),
                height=dp(50)
            )
            btn.bind(on_release=lambda x, d=dance: self.play_dance(d))
            dance_grid.add_widget(btn)
            if i == 2:  # 3个一行
                dance_grid.height += dp(60)

        layout.add_widget(dance_grid)
        return layout

    def set_direction(self, direction, btn):
        """设置行走方向"""
        self.walk_direction = direction
        for d, b in self.direction_buttons.items():
            if d == direction:
                b.md_bg_color = '#3498db'
            else:
                b.md_bg_color = '#95a5a6'

    def send_basic_action(self, action):
        """发送基础动作"""
        app = self.manager.parent.app
        app.robot_controller.send_command('motion', action=action)
        self.show_snackbar(f'执行: {action}')

    def send_gesture(self, gesture):
        """发送手势"""
        app = self.manager.parent.app
        app.robot_controller.send_command('motion', action='gesture', gesture=gesture)
        self.show_snackbar(f'执行手势: {gesture}')

    def execute_walk(self, *args):
        """执行行走"""
        app = self.manager.parent.app
        app.robot_controller.send_command(
            'motion',
            action='walk',
            direction=self.walk_direction,
            distance=self.walk_distance,
            speed=self.walk_speed
        )
        self.show_snackbar(f'执行行走: {self.walk_direction} {self.walk_distance}m 速度{self.walk_speed}')

    def play_dance(self, dance_type):
        """播放舞蹈"""
        app = self.manager.parent.app
        app.robot_controller.send_command('motion', action='dance', dance_type=dance_type)
        self.show_snackbar(f'播放舞蹈: {dance_type}')

    def emergency_stop(self, *args):
        """紧急停止"""
        app = self.manager.parent.app
        app.robot_controller.send_command('motion', action='stop')
        self.show_snackbar('紧急停止', color='#c0392b')

    def show_snackbar(self, text, color='#3498db'):
        """显示提示"""
        from kivymd.uix.snackbar import MDSnackbar
        snackbar = MDSnackbar(text=text, md_bg_color=color, y=dp(20), duration=2)
        snackbar.open()
