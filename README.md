# Host Controller Python 库使用说明

这是一个用于控制硬件设备（包括振动平台、光源、料仓、料仓门）的 Python 库。

## 0. 部署方式
device.py是封装好的库，调用时直接将main.py放在与该文件同级即可

## 1. 连接设备 (`device` Class)

`device` 类用于建立和管理与硬件设备的 TCP 连接，并提供对各个组件的访问接口。

| 方法 | 描述 |
| :--- | :--- |
| `device(host: str, port: str)` | 构造函数，用于连接设备。 |
| `close_connection()` | 显式关闭 socket 连接。 |

**推荐用法（使用上下文管理器）：**

```python
from HostController import device

HOST = "192.168.60.69"
PORT = "502"

with device(HOST, PORT) as d:
    # 在这里操作 d.platform, d.lightA, d.hopper 等
    d.lightA.open()
```

## 2. 振动平台动作枚举 (`ACTION` Enum)

`ACTION` 枚举定义了振动平台的所有预设动作。

| 成员 | 描述 |
| :--- | :--- |
| `UP`, `DOWN`, `LEFT`, `RIGHT` | 四个基本方向。 |
| `LEFT_UP`, `RIGHT_UP`, `LEFT_DOWN`, `RIGHT_DOWN` | 四个斜向。 |
| `GATHER` | 聚集动作。 |
| `CENTER_VERTICAL` | 垂直居中动作。 |
| `CENTER_HORIZONTAL` | 水平居中动作。 |
| `DISPERSE` | 振散动作。 |
| `FLIP` | 翻转动作。 |
| `NONE` | 无动作（用于 `start` 时的停止状态或默认状态）。 |

## 3. 柔性振动平台 (`platform` Class)

用于控制振动平台的动作和参数设置。

| 方法 | 描述 | 参数及约束 |
| :--- | :--- | :--- |
| `set_special_action` | 设置 [垂直居中、水平居中、振散、翻转] 动作的参数。 | `action`: `ACTION.FLIP`, `CENTER_HORIZONTAL`, `CENTER_VERTICAL`, `DISPERSE`。 `voltage`: 电压，`0.0` 到 `24.0` V。 `frequency`: 频率，`10.0` 到 `200.0` Hz。 `time_sec`: 动作持续时间，`0.0` 到 `20.0` 秒。 |
| `set_directional_action` | 设置 [上下左右及斜向] 动作的参数。 | `direction`: 方向性 `ACTION`（非特殊动作）。 `voltage`: 电压，`0.0` 到 `24.0` V。 `frequency`: 频率，`0.0` 到 `200.0` Hz。 `time_sec`: 动作持续时间，`0.0` 到 `20.0` 秒。 `resonance_angle`: 谐振角，`0` 到 `359` 度。 `resonance_amount`: 谐振量，`0` 到 `100`。 |
| `set_gather` | 设置聚集 (`ACTION.GATHER`) 动作的垂直/水平/总时间。 | `vertical_time`: 垂直运动时间，`0.0` 到 `20.0` 秒。 `horizontal_time`: 水平运动时间，`0.0` 到 `20.0` 秒。 `total_time`: 总运动时间，`0.0` 到 `20.0` 秒。 |
| `start` | 开始振动平台的动作。 | `action`: 指定要执行的 `ACTION`。 |
| `stop` | 停止振动平台的当前动作。 | 无 |

## 4. 内部光源 (`lightA` Class)

控制 BLA 内部光源。

| 方法 | 描述 | 参数及约束 |
| :--- | :--- | :--- |
| `open()` | 打开内部光源。 | 无 |
| `close()` | 关闭内部光源。 | 无 |
| `adjust_brightness` | 调节光源亮度。 | `level`: 亮度级别，**6** 到 **999**。 |
| `auto_open()` | 开启“振散、翻面后自动开启”功能。 | 无 |
| `auto_open_cancel()` | 取消“振散、翻面后自动开启”功能。 | 无 |

## 5. 外部光源 (`lightB` Class)

控制 BLB 外部光源。

| 方法 | 描述 | 参数及约束 |
| :--- | :--- | :--- |
| `open()` | 打开外部光源。 | 无 |
| `close()` | 关闭外部光源。 | 无 |

## 6. 料仓 (`hopper` Class)

控制料仓（喂料器）的运行。

| 方法 | 描述 | 参数及约束 |
| :--- | :--- | :--- |
| `start()` | 启动料仓（使用预设参数）。 | 无 |
| `stop()` | 停止料仓。 | 无 |
| `set` | 设置料仓的电压、频率和时间参数。 | `voltage`: 电压，`0.0` 到 `24.0` V。 `frequency`: 频率，`20.0` 到 `400.0` Hz。 `time`: 动作持续时间，`0.0` 到 `9.9` 秒。 |

## 7. 料仓门 (`gate` Class)

控制料仓门的开关和绑定平台动作设置。

| 方法 | 描述 | 参数及约束 |
| :--- | :--- | :--- |
| `open()` | 打开料仓门。 | 无 |
| `close()` | 关闭料仓门。 | 无 |
| `set_open_time` | 设置仓门自动关闭的开启时间。 | `time_sec`: 持续时间，`0.0` 到 `9.9` 秒。 |
| `bind_platform_action` | 绑定平台动作，平台启动时延迟打开仓门。 | `action`: 绑定的 `ACTION`，**必须**是 `UP`, `DOWN`, `LEFT`, `RIGHT`, 或 `NONE`。 `delay_sec`: 延迟打开时间，`0.0` 到 `20.0` 秒。 |

---

## 示例用法
[ (参考 `example.py`)](example.py)