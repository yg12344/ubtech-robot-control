"""
机器人通信接口层
支持多种通信方式：串口、TCP/IP、WebSocket
"""

import serial
import socket
import json
import time
from typing import Optional, Callable, Dict, Any
from threading import Thread, Event


class RobotConnection:
    """机器人连接基类"""

    def __init__(self):
        self.connected = False
        self.callback: Optional[Callable] = None

    def connect(self) -> bool:
        """连接机器人"""
        raise NotImplementedError

    def disconnect(self):
        """断开连接"""
        raise NotImplementedError

    def send_command(self, command: Dict[str, Any]) -> bool:
        """发送指令"""
        raise NotImplementedError

    def receive_data(self) -> Optional[Dict[str, Any]]:
        """接收数据"""
        raise NotImplementedError

    def set_data_callback(self, callback: Callable):
        """设置数据回调"""
        self.callback = callback


class SerialConnection(RobotConnection):
    """串口连接"""

    def __init__(self, port: str, baudrate: int = 115200):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.serial_conn: Optional[serial.Serial] = None
        self.receive_thread: Optional[Thread] = None
        self.stop_event = Event()

    def connect(self) -> bool:
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1
            )
            self.connected = True

            # 启动接收线程
            self.receive_thread = Thread(target=self._receive_loop, daemon=True)
            self.receive_thread.start()

            return True
        except Exception as e:
            print(f"串口连接失败: {e}")
            return False

    def disconnect(self):
        self.stop_event.set()
        self.connected = False
        if self.serial_conn:
            self.serial_conn.close()
        if self.receive_thread:
            self.receive_thread.join(timeout=1)

    def send_command(self, command: Dict[str, Any]) -> bool:
        if not self.connected or not self.serial_conn:
            return False

        try:
            data = json.dumps(command).encode('utf-8')
            self.serial_conn.write(data)
            return True
        except Exception as e:
            print(f"发送指令失败: {e}")
            return False

    def receive_data(self) -> Optional[Dict[str, Any]]:
        return None

    def _receive_loop(self):
        """接收数据线程"""
        while not self.stop_event.is_set() and self.connected:
            try:
                if self.serial_conn and self.serial_conn.in_waiting > 0:
                    data = self.serial_conn.read_all().decode('utf-8')
                    if data and self.callback:
                        try:
                            result = json.loads(data)
                            self.callback(result)
                        except json.JSONDecodeError:
                            pass
                time.sleep(0.01)
            except Exception as e:
                print(f"接收数据错误: {e}")
                break


class TCPConnection(RobotConnection):
    """TCP连接"""

    def __init__(self, host: str, port: int):
        super().__init__()
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.receive_thread: Optional[Thread] = None
        self.stop_event = Event()

    def connect(self) -> bool:
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True

            # 启动接收线程
            self.receive_thread = Thread(target=self._receive_loop, daemon=True)
            self.receive_thread.start()

            return True
        except Exception as e:
            print(f"TCP连接失败: {e}")
            return False

    def disconnect(self):
        self.stop_event.set()
        self.connected = False
        if self.socket:
            self.socket.close()
        if self.receive_thread:
            self.receive_thread.join(timeout=1)

    def send_command(self, command: Dict[str, Any]) -> bool:
        if not self.connected or not self.socket:
            return False

        try:
            data = json.dumps(command).encode('utf-8')
            self.socket.sendall(data)
            return True
        except Exception as e:
            print(f"发送指令失败: {e}")
            return False

    def receive_data(self) -> Optional[Dict[str, Any]]:
        return None

    def _receive_loop(self):
        """接收数据线程"""
        buffer = ""
        while not self.stop_event.is_set() and self.connected:
            try:
                if self.socket:
                    data = self.socket.recv(1024).decode('utf-8')
                    if data:
                        buffer += data
                        try:
                            result = json.loads(buffer)
                            buffer = ""
                            if self.callback:
                                self.callback(result)
                        except json.JSONDecodeError:
                            pass
                    else:
                        self.connected = False
                time.sleep(0.01)
            except Exception as e:
                print(f"接收数据错误: {e}")
                break


class RobotController:
    """机器人控制器"""

    def __init__(self):
        self.connection: Optional[RobotConnection] = None

    def connect_serial(self, port: str, baudrate: int = 115200) -> bool:
        """连接串口"""
        if self.connection:
            self.connection.disconnect()

        self.connection = SerialConnection(port, baudrate)
        return self.connection.connect()

    def connect_tcp(self, host: str, port: int) -> bool:
        """连接TCP"""
        if self.connection:
            self.connection.disconnect()

        self.connection = TCPConnection(host, port)
        return self.connection.connect()

    def disconnect(self):
        """断开连接"""
        if self.connection:
            self.connection.disconnect()
            self.connection = None

    def send_command(self, command_type: str, **kwargs) -> bool:
        """发送指令"""
        command = {
            "type": command_type,
            "timestamp": time.time(),
            **kwargs
        }
        if self.connection:
            return self.connection.send_command(command)
        return False

    def is_connected(self) -> bool:
        """是否已连接"""
        return self.connection and self.connection.connected

    def set_data_callback(self, callback: Callable):
        """设置数据回调"""
        if self.connection:
            self.connection.set_data_callback(callback)


# 预定义动作指令
class Actions:
    """动作指令集"""

    @staticmethod
    def stand():
        return {"type": "motion", "action": "stand"}

    @staticmethod
    def walk(distance: float):
        return {"type": "motion", "action": "walk", "distance": distance}

    @staticmethod
    def wave():
        return {"type": "motion", "action": "wave"}

    @staticmethod
    def dance(dance_type: str):
        return {"type": "motion", "action": "dance", "dance_type": dance_type}

    @staticmethod
    def speak(text: str):
        return {"type": "speech", "action": "speak", "text": text}

    @staticmethod
    def listen():
        return {"type": "speech", "action": "listen"}

    @staticmethod
    def get_status():
        return {"type": "query", "action": "status"}
