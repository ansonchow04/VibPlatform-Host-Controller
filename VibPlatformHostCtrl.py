import socket
import time

# set target device IP address and port number
HOST = "192.168.60.69"
PORT = "502"

"""
classes for different components
"""


class platform:
    START = "00 00 00 00 00 06 02 06 00 08 FF 00"
    STOP = "00 00 00 00 00 06 02 06 00 08 00 00"

    def __init__(self, sender):
        self._send = sender

    def start(self):
        self._send(self.START)

    def stop(self):
        self._send(self.STOP)


class lightA:
    OPEN = "00 00 00 00 00 06 02 06 00 06 FF 00"
    CLOSE = "00 00 00 00 00 06 02 06 00 06 00 00"

    def __init__(self, sender):
        self._send = sender

    def open(self):
        self._send(self.OPEN)

    def close(self):
        self._send(self.CLOSE)

    def adjust_brightness(self, current_ma: float):
        # 电流(12~2000mA)，线性映射到寄存器允许的6~999范围
        if not 12 <= current_ma <= 2000:
            print("Brightness level must be between 12 and 2000 (mA).")
            return
        level = int(round(6 + (current_ma - 12) / (2000 - 12) * (999 - 6)))
        print(level)
        high = (level >> 8) & 0xFF
        low = level & 0xFF
        command = f"00 00 00 00 00 06 02 06 00 50 {high:02X} {low:02X}"
        self._send(command)


class lightB:
    OPEN = "00 00 00 00 00 06 02 06 00 07 FF 00"
    CLOSE = "00 00 00 00 00 06 02 06 00 07 00 00"

    def __init__(self, sender):
        self._send = sender

    def open(self):
        self._send(self.OPEN)

    def close(self):
        self._send(self.CLOSE)


class hopper:
    START = "00 00 00 00 00 06 02 06 00 05 FF 00"
    STOP = "00 00 00 00 00 06 02 06 00 05 00 00"

    def __init__(self, sender):
        self._send = sender

    def start(self):
        self._send(self.START)

    def stop(self):
        self._send(self.STOP)


class gate:
    OPEN = "00 00 00 00 00 06 02 06 00 0A FF 00"
    CLOSE = "00 00 00 00 00 06 02 06 00 0A 00 00"

    def __init__(self, sender):
        self._send = sender

    def open(self):
        self._send(self.OPEN)

    def close(self):
        self._send(self.CLOSE)


class device:
    def __init__(self, host: str = HOST, port: str = PORT):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_device()
        sender = self.send_command
        self.platform = platform(sender)
        self.lightA = lightA(sender)
        self.lightB = lightB(sender)
        self.hopper = hopper(sender)
        self.gate = gate(sender)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close_connection()

    # connect to target device
    def connect_device(self):
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


"""
main program
"""

with device() as d:
    d.lightA.close()
