"""
优必选小微机器人控制软件 - Android版本
使用Kivy + KivyMD开发
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp

from android_robot_interface import RobotController


class RobotApp(App):
    """主应用类"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.robot_controller = RobotController()
        self.title = '优必选小微控制'

    def build(self):
        """构建UI"""
        # 设置窗口大小（仅桌面测试时）
        Window.size = (400, 700)

        # 创建屏幕管理器
        self.sm = ScreenManager()

        # 加载KV语言文件
        Builder.load_file('ui_android.kv')

        # 导入各屏幕
        from screens_android.main_screen import MainScreen
        from screens_android.motion_screen import MotionScreen
        from screens_android.voice_screen import VoiceScreen
        from screens_android.code_screen import CodeScreen
        from screens_android.monitor_screen import MonitorScreen
        from screens_android.settings_screen import SettingsScreen

        # 添加屏幕
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(MotionScreen(name='motion'))
        self.sm.add_widget(VoiceScreen(name='voice'))
        self.sm.add_widget(CodeScreen(name='code'))
        self.sm.add_widget(MonitorScreen(name='monitor'))
        self.sm.add_widget(SettingsScreen(name='settings'))

        return self.sm

    def on_start(self):
        """应用启动"""
        print("优必选小微控制软件已启动")

    def on_stop(self):
        """应用停止"""
        self.robot_controller.disconnect()


if __name__ == '__main__':
    RobotApp().run()
