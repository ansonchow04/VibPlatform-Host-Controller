import socket
import time
from enum import Enum

# set target device IP address and port number


# 振动平台动作枚举
class ACTION(Enum):
    UP = "10"
    DOWN = "11"
    LEFT = "12"
    RIGHT = "13"
    LEFT_UP = "14"
    RIGHT_UP = "15"
    LEFT_DOWN = "16"
    RIGHT_DOWN = "18"
    GATHER = "17"
    CENTER_VERTICAL = "19"
    CENTER_HORIZONTAL = "1A"
    DISPERSE = "1B"
    FLIP = "1C"
    NONE = "1F"


# 柔性振动平台
class platform:
    START = "00 00 00 00 00 06 02 06 00 0F 00 "  # 动作代码待后续补充
    STOP = "00 00 00 00 00 06 02 06 00 08 00 00"

    def __init__(self, sender):
        self._send = sender

    def set_special_action(  # [垂直居中、水平居中、振散、翻转]动作的[电压、频率、时间]设置
        self,
        action: ACTION,
        voltage: float = 10.0,
        frequency: float = 60.0,
        time_sec: float = 20.0,
    ):
        if (
            not 0 <= voltage <= 24
            or not 10 <= frequency <= 200
            or not 0 <= time_sec <= 20
        ):
            print(
                "Voltage must be between 0 and 24, frequency must be between 10 and 200, and time value must be between 0 and 20 seconds."
            )
            return
        voltage = int(voltage * 10)  # 转换为0.1V为单位
        frequency = int(frequency * 10)  # 频率以0.1Hz为单位
        time = int(time_sec * 10)  # 转换为0.1秒为单位
        # 计算寄存器地址
        if action == ACTION.FLIP:
            register_address = 52
        elif (
            action == ACTION.CENTER_HORIZONTAL
            or action == ACTION.CENTER_VERTICAL
            or action == ACTION.DISPERSE
        ):
            register_address = int(action.value, 16) * 3 - 35
        else:
            print(
                "This method only supports FLIP, CENTER_HORIZONTAL, CENTER_VERTICAL, and DISPERSE actions."
            )
            return

        # 设置频率
        freq_high = (frequency >> 8) & 0xFF
        freq_low = frequency & 0xFF
        command = f"00 00 00 00 00 06 02 06 00 {int(register_address+0):02X} {freq_high:02X} {freq_low:02X}"
        self._send(command)
        # 设置电压
        command = (
            f"00 00 00 00 00 06 02 06 00 {int(register_address+1):02X} 00 {voltage:02X}"
        )
        self._send(command)
        # 设置动作时间
        command = (
            f"00 00 00 00 00 06 02 06 00 {int(register_address+2):02X} 00 {time:02X}"
        )
        self._send(command)

    def set_directional_action(  # [上下左右及斜向]动作的[频率、电压、时间、谐振角、谐振量]设置
        self,
        direction: ACTION,
        voltage: float = 10.0,
        frequency: float = 100.0,
        time_sec: float = 0.0,
        resonance_angle: float = 130.0,
        resonance_amount: float = 0.0,
    ):
        if (
            not 0 <= voltage <= 24
            or not 0 <= frequency <= 200
            or not 0 <= time_sec <= 20
            or not 0 <= resonance_angle <= 359
            or not 0 <= resonance_amount <= 100
        ):
            print(
                "Voltage must be between 0 and 24, frequency must be between 0 and 200, time value must be between 0 and 20 seconds, resonance angle must be between 0 and 359, and resonance amount must be between 0 and 100."
            )
            return
        voltage = int(voltage * 10)  # 转换为0.1V为单位
        frequency = int(frequency * 10)  # 频率以0.1Hz为单位
        time = int(time_sec * 10)  # 转换为0.1秒为单位
        # 计算寄存器地址
        if direction == ACTION.RIGHT_DOWN:
            register_address = 37
        elif (
            direction == ACTION.GATHER
            or direction == ACTION.FLIP
            or direction == ACTION.CENTER_HORIZONTAL
            or direction == ACTION.CENTER_VERTICAL
            or direction == ACTION.DISPERSE
            or direction == ACTION.GATHER
        ):
            print("This method only supports directional actions.")
            return
        else:
            register_address = int(direction.value, 16) * 3 - 32
        # 计算谐振相关寄存器地址
        if direction == ACTION.RIGHT_DOWN:
            register_resonance_address = 174
        else:
            register_resonance_address = int(direction.value, 16) * 2 + 128
        # 设置频率
        freq_high = (frequency >> 8) & 0xFF
        freq_low = frequency & 0xFF
        command = f"00 00 00 00 00 06 02 06 00 {int(register_address+0):02X} {freq_high:02X} {freq_low:02X}"
        self._send(command)
        # 设置电压
        command = (
            f"00 00 00 00 00 06 02 06 00 {int(register_address+1):02X} 00 {voltage:02X}"
        )
        self._send(command)
        # 设置动作时间
        command = (
            f"00 00 00 00 00 06 02 06 00 {int(register_address+2):02X} 00 {time:02X}"
        )
        self._send(command)
        # 设置谐振角
        angle_high = (int(resonance_angle) >> 8) & 0xFF
        angle_low = int(resonance_angle) & 0xFF
        command = f"00 00 00 00 00 06 02 06 00 {int(register_resonance_address+0):02X} {angle_high:02X} {angle_low:02X}"
        self._send(command)
        # 设置谐振量
        command = f"00 00 00 00 00 06 02 06 00 {int(register_resonance_address+1):02X} 00 {int(resonance_amount):02X}"
        self._send(command)

    def set_gather(
        self,
        vertical_time: float = 0.5,
        horizontal_time: float = 0.5,
        total_time: float = 0,
    ):
        if not 0 <= vertical_time <= 20 or not 0 <= horizontal_time <= 20:
            print("Time value must be between 0 and 20 seconds.")
            return
        vertical_time *= 10  # 转换为0.1秒为单位
        horizontal_time *= 10
        total_time *= 10
        # 设置垂直运动时间
        command = f"00 00 00 00 00 06 02 06 00 31 00 {int(vertical_time):02X}"
        self._send(command)
        # 设置水平运动时间
        command = f"00 00 00 00 00 06 02 06 00 32 00 {int(horizontal_time):02X}"
        self._send(command)
        # 设置总运动时间
        command = f"00 00 00 00 00 06 02 06 00 33 00 {int(total_time):02X}"
        self._send(command)

    def start(self, action: ACTION = ACTION.NONE):
        command = self.START + action.value
        print(command)
        self._send(command)

    def stop(self):
        self._send(self.STOP)


# BLA 内部光源
class lightA:
    OPEN = "00 00 00 00 00 06 02 06 00 06 FF 00"
    CLOSE = "00 00 00 00 00 06 02 06 00 06 00 00"

    def __init__(self, sender):  # 为发送函数提供接口
        self._send = sender

    def open(self):
        self._send(self.OPEN)

    def close(self):
        self._send(self.CLOSE)

    # 亮度调节
    def adjust_brightness(self, level: int):
        # 亮度，线性映射到寄存器允许的6~999范围
        if not 6 <= level <= 999:
            print("Brightness level must be between 6 and 999.")
            return
        high = (level >> 8) & 0xFF
        low = level & 0xFF
        command = f"00 00 00 00 00 06 02 06 00 50 {high:02X} {low:02X}"
        self._send(command)

    # 振散、翻面后自动开启
    def auto_open(self):
        self._send("00 00 00 00 00 06 02 06 00 56 00 01")

    def auto_open_cancel(self):
        self._send("00 00 00 00 00 06 02 06 00 56 00 00")


# BLB 外部光源
class lightB:
    OPEN = "00 00 00 00 00 06 02 06 00 07 FF 00"
    CLOSE = "00 00 00 00 00 06 02 06 00 07 00 00"

    def __init__(self, sender):
        self._send = sender

    def open(self):
        self._send(self.OPEN)

    def close(self):
        self._send(self.CLOSE)


# 料仓
class hopper:
    START = "00 00 00 00 00 06 02 06 00 05 FF 00"
    STOP = "00 00 00 00 00 06 02 06 00 05 00 00"

    def __init__(self, sender):
        self._send = sender

    def start(self):
        self._send(self.START)

    def stop(self):
        self._send(self.STOP)

    def set(self, voltage: float = 8.0, frequency: float = 100, time: float = 0):
        if not 0 <= voltage <= 24 or not 20 <= frequency <= 400 or not 0 <= time <= 9.9:
            print(
                "Voltage must be between 0 and 24, frequency must be between 20 and 400, and time value must be between 0 and 9.9 seconds."
            )
            return
        voltage = int(voltage * 10)  # 转换为0.1V为单位
        frequency = int(frequency * 10)  # 频率以0.1Hz为单位
        time_val = int(time * 10)  # 转换为0.1秒为单位
        # 设置电压
        command = f"00 00 00 00 00 06 02 06 00 C0 00 {voltage:02X}"
        self._send(command)
        # 设置频率
        freq_high = (frequency >> 8) & 0xFF
        freq_low = frequency & 0xFF
        command = f"00 00 00 00 00 06 02 06 00 C1 {freq_high:02X} {freq_low:02X}"
        self._send(command)
        # 设置动作时间
        command = f"00 00 00 00 00 06 02 06 00 C2 00 {time_val:02X}"
        self._send(command)


# 料仓门
class gate:
    OPEN = "00 00 00 00 00 06 02 06 00 0A FF 00"
    CLOSE = "00 00 00 00 00 06 02 06 00 0A 00 00"

    def __init__(self, sender):
        self._send = sender

    def open(self):
        self._send(self.OPEN)

    def close(self):
        self._send(self.CLOSE)

    # 设置仓门开启时间
    def set_open_time(self, time_sec: float):
        if not 0 <= time_sec <= 9.9:
            print("Time value must be between 0 and 9.9 seconds.")
            return
        time_val = int(time_sec * 10)  # 转换为0.1秒为单位
        command = f"00 00 00 00 00 06 02 06 00 B0 00 {time_val:02X}"
        self._send(command)

    # 设置仓门绑定振动平台动作及其延迟打开时间
    def bind_platform_action(self, action: ACTION, delay_sec: float = 0.0):
        if not 0 <= delay_sec <= 20.0 or not action in [
            ACTION.UP,
            ACTION.DOWN,
            ACTION.LEFT,
            ACTION.RIGHT,
            ACTION.NONE,
        ]:
            print(
                "Delay time must be between 0 and 20.0 seconds, and action must be one of UP, DOWN, LEFT, RIGHT, or NONE."
            )
            return
        if action == ACTION.NONE:
            direction = 0
        else:
            direction = int(action.value, 16) - 15  # 转换为寄存器要求的数值
        delay_val = int(delay_sec * 10)  # 转换为0.1秒为单位
        command = f"00 00 00 00 00 06 02 06 00 B1 00 {direction:02X}"
        self._send(command)
        command = f"00 00 00 00 00 06 02 06 00 B2 00 {delay_val:02X}"
        self._send(command)


# 控制板，包含以上components
class device:
    def __init__(self, host: str = "", port: str = ""):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 提供异常接口
        self.connected = self.connect_device(self.host, self.port)
        sender = self.send_command
        self.platform = platform(sender)
        self.lightA = lightA(sender)
        self.lightB = lightB(sender)
        self.hopper = hopper(sender)
        self.gate = gate(sender)

    def __enter__(self):
        if not self.connected:
            raise ConnectionError("Failed to connect to the device.")
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close_connection()

    # connect to target device
    def connect_device(self, host: str = "", port: str = ""):
        try:
            self.client_socket.settimeout(5)
            print(f"Connecting to {self.host}:{self.port}...")
            self.client_socket.connect((self.host, int(self.port)))
            print("Connected.")
            return True
        except socket.timeout:
            print("Connection timed out.")
            return False
        except ConnectionRefusedError:
            print("Connection refused by the target device.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    # send command and receive response
    def send_command(self, command_hex):
        command_bytes = bytes.fromhex(command_hex)
        print(f"Sending command: {command_hex}")
        self.client_socket.sendall(command_bytes)
        print("Command sent.")
        response = self.client_socket.recv(1024)
        print(f"Received response: {response.hex(' ').upper()}")

    # close connection
    def close_connection(self):
        self.client_socket.close()
        print("Socket closed.")
