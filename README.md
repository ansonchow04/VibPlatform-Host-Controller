# VibPlatform-Host-Controller

控制微振动平台及相关外设（光源、料仓、门）的 Python 控制库与示例。

## 功能概览
- 通过 TCP/套接字向设备发送 Modbus 风格的十六进制指令。
- 封装的硬件组件类：`platform`（振动平台）、`lightA`（内部光源）、`lightB`（外部光源）、`hopper`（料仓）、`gate`（料仓门）。
- 支持：启动/停止、光源亮度调节、时间/频率/电压参数设置等操作。

## 快速开始
1. 克隆仓库并切换到项目目录：

```powershell
git clone <repo-url>
cd VibPlatform-Host-Controller
```

2. 在 Python 环境中运行脚本（推荐使用 conda/venv）：

```powershell
python VibPlatformHostCtrl.py
```

3. 使用 `device` 上下文管理器连接并调用组件：

```python
from VibPlatformHostCtrl import device, ACTION, PlatformAction
 
d = device()
d.platform.start(ACTION.UP)
time.sleep(2)
d.platform.stop()
```

（注：示例中 IP/端口 在文件顶部的 `HOST` / `PORT` 常量中配置）

## API 概要
- `device(host=HOST, port=PORT)`：连接设备并创建组件实例，包含 `platform`、`lightA`、`lightB`、`hopper`、`gate`。
- `platform.start(action)`：启动振动平台，支持 `ACTION` 枚举（带 IDE 自动补全）。
- `platform.stop()`：停止振动平台。
- `platform.set_gather_time(v_sec, h_sec, total_sec)`：设置聚拢（垂直/水平/总）时间（单位：秒）。
- `platform.set_direction_action_time(direction, time_sec)`：设置方向动作时间。
- `platform.set_special_action_time(action, voltage, frequency, time_sec)`：为特殊动作设置电压、频率、时间。
- `lightA.open()/close()/adjust_brightness(current_ma)`：内部光源控制。
- `lightB.open()/close()`：外部光源控制。
- `hopper.start()/stop()`：料仓控制。
- `gate.open()/close()`：料仓门控制。

## 注意事项
- 设备使用的是十六进制命令串，`send_command` 方法会将字符串用 `bytes.fromhex()` 转为字节发送。
- 请确保 `HOST` 与 `PORT` 指向正确的设备，并在安全网络下操作。
- 在调用带参数的方法前请确认参数范围（代码中包含范围检查并会打印错误信息）。
