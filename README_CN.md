# Turbo IMS

<div align="center">
  <img src="Turboims.png" width="200" alt="Turbo IMS Logo"/>

  <h3>Google Pixel 设备增强版 IMS 配置工具</h3>

  [![Android](https://img.shields.io/badge/Android-14%2B-green.svg)](https://www.android.com/)
  [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
  [![Version](https://img.shields.io/badge/Version-3.0-brightgreen.svg)](https://github.com/Turbo1123/TurboIMS/releases)

  [English](README.md) | 简体中文
</div>

---

## 📱 关于项目

**Turbo IMS** 是 [vvb2060 的 IMS 项目](https://github.com/vvb2060/Ims) 的增强版分支，专为 Google Pixel 手机设计，通过系统级权限配置启用 VoLTE、VoWiFi、VoNR 等高级 IMS 功能。

这个增强版本在保持与原版完全兼容的同时，提供了现代化的用户界面、改进的用户体验、自动语言检测以及更多便利功能。

## ✨ Turbo IMS 新增功能

### 🎨 **现代化 UI 重设计**
- 专业的 Logo 和品牌形象
- 简洁的 Material Design 风格界面
- 增强的启动页面和版本显示
- 改进的视觉反馈和状态指示

### 🌍 **自动语言检测**
- 首次启动自动检测系统语言
- 中文用户自动显示中文界面（支持简体、繁体、香港等）
- 其他地区用户显示英文界面
- 支持手动切换语言

### 📡 **快速网络设置跳转**
- 配置成功后一键跳转到网络设置
- 便捷的对话框提示
- 简化的 IMS 功能测试流程

### 🎯 **单卡配置支持**
- 选择特定 SIM 卡（SIM 1 或 SIM 2）
- 可单独为某张卡配置或同时配置所有 SIM 卡
- 清晰的选中卡状态反馈

### 🔄 **改进的用户体验**
- 配置后自动返回应用
- 清晰的成功/失败通知
- Android 版本检测及 QPR2 Beta 3+ 警告
- 实时 Shizuku 状态监控

## 🎯 核心功能

### IMS 功能配置
- ✅ **VoLTE**（4G 语音）- 4G LTE 高清语音通话
- ✅ **VoWiFi**（WiFi 通话）- 通过 WiFi 网络拨打电话
- ✅ **VT**（视频通话）- 基于 IMS 的视频通话
- ✅ **VoNR**（5G 语音）- 5G NR 高清语音通话
- ✅ **跨 SIM 通话** - 双卡互通功能
- ✅ **UT 补充服务** - 呼叫转移、呼叫等待等
- ✅ **5G NR**（NSA/SA）- 启用 5G 独立/非独立组网

### 系统要求
- Google Pixel 设备（在 Pixel 6+ 上测试通过）
- Android 14 或更高版本
- 已安装并运行 [Shizuku](https://github.com/RikkaApps/Shizuku)
- 已授予 Turbo IMS Shizuku 权限

## 🚀 安装方法

### 方法 1：下载 APK（推荐）
1. 从 [Releases](https://github.com/Turbo1123/TurboIMS/releases) 下载最新 APK
2. 在你的 Pixel 设备上安装 APK
3. 授予必要的权限

### 方法 2：从源码构建
```bash
# 克隆仓库
git clone https://github.com/Turbo1123/TurboIMS.git
cd TurboIMS

# 构建 debug APK
./gradlew assembleDebug

# 安装到已连接的设备
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

## 📖 使用指南

### 前置准备

1. **安装 Shizuku**
   - 从 [GitHub](https://github.com/RikkaApps/Shizuku/releases) 或 Google Play 下载
   - 启动 Shizuku 服务（通过无线调试或 Root）

2. **授予权限**
   - 打开 Turbo IMS
   - 在提示时授予 Shizuku 权限

### 配置 IMS 功能

1. **检查系统状态**
   - 确认显示了 Android 版本
   - 确保 Shizuku 状态显示"✅ 已就绪"

2. **选择 SIM 卡**
   - 点击"选择 SIM 卡"按钮
   - 选择 SIM 1、SIM 2 或"应用到所有 SIM 卡"

3. **启用功能**
   - 切换所需 IMS 功能的开关
   - 所有功能默认已启用

4. **应用配置**
   - 点击蓝色的"应用配置"按钮
   - 等待 3 秒完成配置
   - 应用会自动返回前台
   - 选择"前往网络设置"验证功能

### 重要提示

⚠️ **Android 16 QPR2 Beta 3+ 用户**
- Android 16 Beta 版本上配置不是持久化的
- 重启后设置会重置
- 每次重启后需要重新应用配置

✅ **验证配置**
- 进入 设置 → 网络和互联网 → SIM 卡
- 检查 VoLTE、VoWiFi 选项是否可见
- 拨打测试电话验证功能

## 🛠️ 技术细节

### 架构
- **特权进程**：使用 Android Instrumentation 以系统权限运行
- **Shizuku 集成**：利用 Shizuku 框架进行权限提升
- **CarrierConfigManager**：直接修改运营商配置包
- **Shell 权限委托**：临时获取 NETWORK_SETTINGS 权限

### 修改的配置键
应用会修改以下运营商配置键：
- `KEY_CARRIER_VOLTE_AVAILABLE_BOOL`
- `KEY_CARRIER_VT_AVAILABLE_BOOL`
- `KEY_CARRIER_WFC_IMS_AVAILABLE_BOOL`
- `KEY_ENHANCED_4G_LTE_ON_BY_DEFAULT_BOOL`
- `KEY_EDITABLE_ENHANCED_4G_LTE_BOOL`
- `KEY_HIDE_ENHANCED_4G_LTE_BOOL`
- 还有更多...（完整列表请查看源代码）

### 包详情
- **包名**：`io.github.turboims.pixel`
- **最低 SDK**：Android 14 (API 34)
- **目标 SDK**：Android 15 (API 35)
- **版本**：3.0 (Build 5)

## 🤝 致谢

### 原始项目
本项目是优秀的 [**IMS by vvb2060**](https://github.com/vvb2060/Ims) 的分支。

特别感谢：
- **[@vvb2060](https://github.com/vvb2060)** - IMS 配置工具的原作者和创建者
- 原 IMS 项目让成千上万的 Pixel 用户能够使用运营商功能

### 上游项目
请访问原项目：**[https://github.com/vvb2060/Ims](https://github.com/vvb2060/Ims)**

如果这个工具对你有帮助，请考虑为本仓库和原项目点个星！⭐

### 依赖项目
- [Shizuku](https://github.com/RikkaApps/Shizuku) by RikkaApps - 权限提升框架
- [HiddenApiBypass](https://github.com/LSPosed/AndroidHiddenApiBypass) by LSPosed - 访问隐藏的 Android API

## ⚠️ 特别重要说明（针对拨打中国移动号“秒挂”或“闪断”问题）

如果您在使用本工具开通 IMS 功能后，遇到**拨打部分中国移动号码时电话秒挂、瞬间断开**的问题，请务必阅读以下说明：

### 问题原因
1. **视频彩铃冲突**：中国移动目前为大量号码默认开通了“视频彩铃”服务。当您呼叫这些号码时，移动网络会在响铃阶段下发视频数据包。
2. **基带固件 Bug**：Google Pixel 6、7、8、9 系列搭载的是三星生产的 **Shannon 调制解调器（基带）**。由于基带层级的信令解析漏洞，当它在通话协商阶段收到并解析运营商的视频彩铃 SDP 数据包时，会直接发生内部协议栈崩溃，底层抛出 `1610 (CODE_REJECT_UNSUPPORTED_SDP_HEADERS)` 错误，导致电话瞬间被切断。
3. **基带闭源无法修改**：基带（Modem/CP）运行在独立的闭源实时操作系统上，物理隔离于 Android 应用层，第三方软件或刷机包无法对其进行修补。

### 解决办法
为了彻底规避此问题，我们在本项目中引入了**系统级强制关闭视频通话 (VT)** 的功能：
1. **本地禁用 VT**：在应用中，将 **“视频通话 (VT)”** 开关设为 **关闭（Disabled）**（默认已为您关闭），然后点击 **应用配置 (Apply)**。
2. App 将通过 Shizuku 权限并使用反射技术调用系统隐藏 API `ImsMmTelManager.setVtSettingEnabled(false)`，强制将您手机本地的“运营商视频通话”开关切到关闭状态。
3. **原理**：这样手机向网络注册时会宣告“我没有视频通话能力”。移动网络在获悉后，会**自动将彩铃降级为纯语音彩铃**发给您，从而完美绕过基带的解析 Bug，解决秒挂问题。
4. **运营商端（备选）**：如果拨打时依旧遇到秒挂，代表核心网仍然强推了视频。请拨打 **10000** 呼叫电信客服，要求人工客服 **“关闭我手机号的视频通话（VT）服务”**（保留 VoLTE 高清语音通话），即可彻底解决。

## 📄 许可证

```
Copyright 2024 Turbo IMS Contributors
Copyright 2023 vvb2060 (Original IMS Project)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## ⚠️ 免责声明

- 本工具会修改系统级运营商配置
- 使用风险自负
- 作者不对可能出现的任何问题负责
- 在依赖 IMS 功能之前，请务必验证其是否与你的运营商兼容
- 这是一个非官方工具，未经 Google 或任何运营商认可

## 🐛 问题反馈与支持

如果你遇到任何问题或有功能请求：
1. 查看 [现有 Issues](https://github.com/Turbo1123/TurboIMS/issues)
2. 创建新 Issue 并提供详细信息：
   - 设备型号
   - Android 版本
   - Shizuku 版本
   - 复现步骤
   - Logcat 输出（如适用）

## 🌟 贡献

欢迎贡献！请随时提交 Pull Request 或创建 Issue：
- Bug 修复
- 新功能
- UI 改进
- 翻译
- 文档

## 💬 社区

- **酷安**：可以在酷安分享使用体验
- **XDA Developers**：国际技术交流论坛
- **Reddit r/GooglePixel**：Pixel 用户社区

---

<div align="center">

  **用 ❤️ 为 Pixel 社区制作**

  如果这个项目帮到了你，请给个 ⭐！

</div>
