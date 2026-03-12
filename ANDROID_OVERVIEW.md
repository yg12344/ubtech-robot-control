# 优必选小微机器人控制软件 - Android版本项目概述

## 项目完成情况

已成功将Python桌面应用转换为完整的Android APK应用，使用Kivy + KivyMD框架开发。

## 项目结构

```
优必选小微控制软件/
├── 桌面版本（PyQt6）
│   ├── main.py                      # 桌面版入口
│   ├── robot_interface.py           # 桌面版通信接口
│   ├── requirements.txt             # 桌面版依赖
│   ├── ui/                         # 桌面版UI模块
│   └── modules/                    # 桌面版功能模块
│
├── Android版本（Kivy）
│   ├── android_main.py             # Android版入口
│   ├── android_robot_interface.py  # Android版通信接口
│   ├── requirements_android.txt    # Android版依赖
│   ├── buildozer.spec             # APK打包配置
│   ├── ui_android.kv              # Android版UI定义（KV语言）
│   └── screens_android/           # Android版屏幕模块
│       ├── main_screen.py        # 主屏幕
│       ├── motion_screen.py      # 运动控制
│       ├── voice_screen.py       # 语音交互
│       ├── code_screen.py        # 编程教学
│       ├── monitor_screen.py     # 远程监控
│       └── settings_screen.py    # 系统设置
│
├── 文档
│   ├── README.md                 # 桌面版说明
│   ├── README_ANDROID.md         # Android版说明
│   ├── 打包说明.md               # APK打包指南
│   └── PROJECT_OVERVIEW.md       # 项目总览
```

## Android版核心特性

### ✅ 技术栈
- **开发框架**: Kivy 2.3.0
- **UI库**: KivyMD 1.1.1（Material Design）
- **打包工具**: Buildozer
- **Python版本**: 3.9
- **目标平台**: Android 5.0+ (API 21+)

### ✅ 功能模块

#### 1. 主界面（main_screen.py）
- 网格布局的功能卡片
- 实时连接状态显示
- 快速连接按钮
- 底部导航栏

#### 2. 运动控制（motion_screen.py）
- 基础动作按钮（站立、坐下、行走、停止）
- 手势动作按钮（挥手、点头、摇头、鞠躬）
- 行走参数控制（方向、距离、速度滑块）
- 舞蹈选择和播放
- 紧急停止功能

#### 3. 语音交互（voice_screen.py）
- 语音监听开关
- 语言选择（中文/英文）
- 识别结果显示
- 语音合成输入框
- 快速语音指令预设

#### 4. 编程教学（code_screen.py）
- 示例代码分类选择
- Python代码编辑器
- 代码运行功能
- 输出结果显示
- 清空和运行按钮

#### 5. 远程监控（monitor_screen.py）
- 机器人状态显示
- 传感器数据显示
- 实时数据监控开关
- 数据趋势进度条
- 自动更新数据

#### 6. 系统设置（settings_screen.py）
- 连接方式选择（蓝牙/TCP）
- 蓝牙MAC地址配置
- TCP/IP地址和端口配置
- 语音语言设置
- 配置保存和应用

### ✅ 通信接口（android_robot_interface.py）

#### 蓝牙连接（BluetoothConnection）
- 支持Android Bluetooth API
- 自动配对和连接
- 双向数据传输

#### TCP/IP连接（TCPConnection）
- 支持TCP socket连接
- 网络通信
- 实时数据接收

#### 预定义动作（Actions类）
- 基础动作指令
- 手势指令
- 舞蹈指令
- 语音指令
- 查询指令

## 打包APK

### 前置要求
- Python 3.8+
- Java JDK 11+
- Android SDK和NDK
- Buildozer工具

### 快速打包

```bash
# 1. 安装依赖
pip install -r requirements_android.txt

# 2. 安装buildozer
pip install buildozer

# 3. 创建资源目录
mkdir -p assets
# 添加icon.png和presplash.png到assets/

# 4. 调试打包（快速）
buildozer android debug

# 5. 发布打包
buildozer android release
```

### 输出文件
APK文件位置：`bin/ubtech_robot_control-1.0.0-arm64-v8a-release.apk`

## 使用流程

### 用户端
1. 下载并安装APK
2. 授予必要权限（蓝牙、网络、录音）
3. 进入系统设置配置连接
4. 点击连接机器人
5. 使用各项功能

### 开发者端
1. 克隆代码库
2. 安装依赖
3. 修改buildozer.spec配置
4. 运行打包命令
5. 测试APK

## 主要改进

### 相比桌面版的优势
- ✅ 移动便携性
- ✅ 触摸操作优化
- ✅ 蓝牙原生支持
- ✅ Material Design界面
- ✅ 无需安装Python环境

### 技术改进
- ✅ 使用KV语言声明式UI
- ✅ 异步网络通信
- ✅ 自动权限请求
- ✅ 配置持久化
- ✅ 实时数据更新

## 权限配置

```ini
android.permissions = BLUETOOTH, BLUETOOTH_ADMIN,
                     BLUETOOTH_SCAN, BLUETOOTH_CONNECT,
                     INTERNET, RECORD_AUDIO,
                     ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE
```

## 系统要求

### 最低要求
- Android 5.0 (API 21)
- 2GB RAM
- 50MB存储空间
- 蓝牙4.0+（如使用蓝牙连接）

### 推荐配置
- Android 8.0+ (API 26)
- 4GB RAM
- 1GB可用存储
- 蓝牙5.0+

## 开发文档

### 核心文件说明

| 文件 | 说明 |
|-----|------|
| android_main.py | 应用入口，初始化屏幕管理器 |
| android_robot_interface.py | 机器人通信接口层 |
| ui_android.kv | UI界面定义（KV语言） |
| screens_android/*.py | 各功能屏幕实现 |
| buildozer.spec | APK打包配置 |
| requirements_android.txt | Python依赖列表 |

### 扩展功能

添加新功能模块：
1. 在`screens_android/`创建新屏幕文件
2. 继承`MDScreen`类
3. 在`android_main.py`中注册屏幕
4. 在`ui_android.kv`中添加UI定义

## 测试建议

### 功能测试
- [ ] 蓝牙连接
- [ ] TCP连接
- [ ] 运动控制指令
- [ ] 语音交互
- [ ] 代码编辑和执行
- [ ] 数据监控
- [ ] 配置保存

### � 兼容性测试
- [ ] Android 5.0
- [ ] Android 6.0
- [ ] Android 7.0
- [ ] Android 8.0+
- [ ] 不同屏幕尺寸
- [ ] 不同CPU架构

### 性能测试
- [ ] 启动速度
- [ ] 内存占用
- [ ] CPU使用率
- [ ] 电量消耗

## 常见问题

### 编译相关
- 首次编译时间长（正常现象）
- 需要稳定网络下载SDK/NDK
- 确保足够的存储空间

### 运行相关
- 权限未授予会导致功能异常
- 不同Android版本UI可能有差异
- 蓝牙需要设备支持

## 后续优化建议

1. **性能优化**
   - 减小APK体积
   - 优化内存使用
   - 提升启动速度

2. **功能扩展**
   - 添加更多机器人动作
   - 支持脚本录制
   - 添加云端服务

3. **UI优化**
   - 支持深色模式
   - 自定义主题
   - 更多动画效果

4. **稳定性**
   - 异常处理完善
   - 断线重连机制
   - 日志记录功能

## 版本信息

- **当前版本**: v1.0.0
- **发布日期**: 2026-03-12
- **支持平台**: Android 5.0+
- **开发框架**: Kivy + KivyMD

---

**项目已完成，可立即打包成APK使用！**
