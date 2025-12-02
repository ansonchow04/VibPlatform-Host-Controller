"""example.py
示例：控制内部光源（lightA）。

说明：将此文件放在项目根并从该目录运行。建议用上下文管理器（with）或在结束时显式关闭连接。
"""

from device import device
import time

# 目标设备地址（请根据实际设备修改）
HOST = "192.168.60.69"
PORT = "502"

# 使用上下文管理器确保退出时连接被关闭
with device(HOST, PORT) as d:
    # 设置内部光源亮度
    d.lightA.adjust_brightness(100)  # 设置为 100

    # 打开内部光源
    d.lightA.open()
    time.sleep(2)  # 等待 2 秒观察效果

    # 调低亮度
    d.lightA.adjust_brightness(30)  # 设置为 30
    time.sleep(2)

    # 关闭内部光源
    d.lightA.close()

# 说明：如果不使用 with，请在完成后调用 d.close_connection() 以释放 socket
