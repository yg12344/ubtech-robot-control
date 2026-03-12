"""
主屏幕
"""

from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDRaisedButton, MDIconButton


class MainScreen(MDScreen):
    """主屏幕"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main'

    def on_enter(self, *args):
        """进入屏幕时更新状态"""
        # 在这里更新连接状态显示
        pass

    def connect_robot(self):
        """连接机器人"""
        app = self.manager.parent.app
        from screens_android.settings_screen import SettingsScreen

        # 获取连接配置
        conn_type = SettingsScreen.get_connection_type()
        mac_address = SettingsScreen.get_bluetooth_address()
        host = SettingsScreen.get_tcp_host()
        port = SettingsScreen.get_tcp_port()

        success = False
        if conn_type == 'bluetooth':
            success = app.robot_controller.connect_bluetooth(mac_address)
        elif conn_type == 'tcp':
            success = app.robot_controller.connect_tcp(host, port)

        if success:
            self.show_snackbar('连接成功', color=(0.15, 0.8, 0.44, 1))
            self.on_enter()
        else:
            self.show_snackbar('连接失败', color=(0.93, 0.26, 0.26, 1))

    def show_snackbar(self, text, color=(0.2, 0.6, 0.87, 1)):
        """显示提示信息"""
        from kivymd.uix.snackbar import MDSnackbar

        snackbar = MDSnackbar(
            text=text,
            md_bg_color=color,
            y=dp(20),
            duration=2
        )
        snackbar.open()
