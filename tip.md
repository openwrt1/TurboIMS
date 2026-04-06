# TurboIMS 项目工作原理说明

## 项目概述

TurboIMS 是一个 Android 应用程序，旨在帮助用户在没有 root 权限的情况下启用和配置 IMS（IP Multimedia Subsystem）功能，如 VoLTE、VoWiFi、视频通话等。该应用利用 Shizuku 框架来获取必要的系统权限。

## 核心技术

### 1. Shizuku 框架

- **作用**: 提供一种无需 root 的方式来执行需要系统权限的操作
- **原理**: 通过 ADB 或其他方式启动特权服务，应用通过 binder IPC 与该服务通信
- **优势**: 比 root 更安全，不需要修改系统分区

### 2. Instrumentation API

- **作用**: 在应用进程中启动特权代码执行
- **实现**: `PrivilegedProcess` 类继承 `Instrumentation`，通过 Shizuku 启动
- **目的**: 在有权限的上下文中修改系统配置
- **Manifest 配置**:
  ```xml
  <instrumentation
      android:name="io.github.vvb2060.ims.PrivilegedProcess"
      android:targetPackage="${applicationId}"
      android:label="IMS Configurator" />
  ```
- **自我注入机制**: 是的，这是一种"自己注入自己的程序"的机制。`targetPackage="${applicationId}"` 指定目标包是应用本身，意味着 instrumentation 在应用自己的进程中运行，但通过 Shizuku 获得系统权限来执行特权操作
- **工作原理**: Shizuku 调用 `startInstrumentation()` 来启动这个 instrumentation，它允许在应用进程内执行需要系统权限的代码，而不必创建新的进程或修改应用签名

## 权限提升详解

### 为什么"自己注入自己"可以修改系统配置？

1. **进程上下文**: Instrumentation 在应用进程中运行，共享应用的内存空间和生命周期

2. **权限委托**: 通过 `startDelegateShellPermissionIdentity()` 获取 shell 用户权限：

   ```java
   am.startDelegateShellPermissionIdentity(Os.getuid(), null);
   ```

   这使得当前进程暂时获得系统 shell 的权限

3. **系统 API 调用**: 获得权限后，可以调用需要系统级权限的 API：

   - `CarrierConfigManager.overrideConfig()` - 修改运营商配置
   - 这些 API 原本只能由系统服务调用

4. **配置生效**: 修改的配置存储在系统数据库中，影响：
   - Phone 应用的 IMS 功能
   - 运营商服务的行为
   - 整个系统的通话和数据功能

### CarrierConfigManager.overrideConfig() 详解

#### 修改方式：内存 vs 持久存储

- **内存修改**: `overrideConfig(subId, config, false)` - 临时修改，只在内存中生效，重启后丢失
- **持久存储**: `overrideConfig(subId, config, true)` - 保存到系统存储，重启后仍然有效
- **存储位置**: 持久配置通常保存到 `/data/system/carrier_config/` 或类似的系统目录

#### Android 配置验证和回滚机制

- **配置验证**: 系统会验证配置的格式和内容有效性
- **自动回滚**: 如果配置导致系统不稳定或不符合要求，Android 可能会：
  - 自动回滚到之前的配置
  - 重启相关服务
  - 在某些情况下重启设备
- **安全机制**:
  - 配置有版本控制（`vvb2060_config_version`）
  - 只有更高版本的配置才会覆盖旧配置
  - 防止恶意或损坏的配置永久生效

#### 实际使用中的处理

TurboIMS 中的代码会尝试两种方式：

```java
try {
    // 尝试非持久方式
    cm.getClass().getMethod("overrideConfig", int.class, PersistableBundle.class)
        .invoke(cm, subId, values);
} catch (NoSuchMethodException e) {
    // 回退到持久方式
    cm.getClass().getMethod("overrideConfig", int.class, PersistableBundle.class, boolean.class)
        .invoke(cm, subId, values, false);
}
```

这样设计确保了兼容性和安全性。

### 安全边界

- **隔离性**: 尽管在应用进程中运行，但权限委托是临时的，只在配置期间有效
- **范围限制**: 只能修改特定的系统配置，不能任意修改其他应用的代码或数据
- **审计**: 所有操作都通过 Shizuku 记录，便于追踪

### 3. CarrierConfigManager

- **作用**: 管理系统运营商配置
- **方法**: 使用反射调用 `overrideConfig` 方法修改 IMS 相关配置
- **配置项**: VoLTE、VoWiFi、VT、VoNR、跨 SIM 通话等功能开关
- **存储位置**: 配置存储在系统的运营商配置数据库中，通常位于 `/data/user_de/0/com.android.phone/databases/carrier_config.db` 或类似位置，由系统 Phone 应用管理
- **权限要求**: 需要系统级权限，通过 Shizuku 获得 shell 权限委托来访问

## 技术细节解答

### 关于签名和权限

#### 为什么不会遇到签名问题？

- **Instrumentation 机制**: `PrivilegedProcess` 继承 `Instrumentation`，但不是通过标准的 Android 签名机制启动，而是通过 Shizuku 的特权服务启动
- **Shizuku 绕过**: Shizuku 提供了一种无需修改应用签名的方式来执行特权操作，它通过 ADB 或系统服务获得权限
- **权限委托**: 代码中使用 `startDelegateShellPermissionIdentity()` 获取 shell 用户权限，绕过了标准的应用签名检查

#### 不同包的修改签名要求

- **不修改其他应用**: TurboIMS 不直接修改其他应用的包或代码，只修改系统级的运营商配置
- **系统配置修改**: `CarrierConfigManager.overrideConfig()` 是系统 API，不需要应用签名验证，只需要相应的系统权限
- **无需重新签名**: 因为不是修改 APK 文件本身，而是运行时修改系统配置，所以不需要重新签名应用

#### 系统运营商配置的位置

- **存储位置**: 运营商配置通常存储在 Android 系统的 Phone 应用数据目录中：
  - 数据库文件: `/data/data/com.android.phone/databases/carrier_config.db`
  - 配置缓存: `/data/data/com.android.phone/shared_prefs/carrier_config.xml`
- **管理组件**: 由 `com.android.phone` 包（Phone 服务）管理
- **持久性**: 配置可以是临时的（重启后丢失）或持久的，取决于 `overrideConfig` 的参数

## 工作流程

### 1. 应用启动

- `SplashActivity`: 显示启动画面，2秒后跳转到主界面
- `MainActivity`: 初始化 UI，检查 Shizuku 状态，加载用户配置

### 2. 用户配置

- 用户选择要启用的 IMS 功能（VoLTE、VoWiFi 等）
- 选择应用的目标 SIM 卡（单个或全部）
- 点击"应用配置"按钮

### 3. 权限检查

- 检查 Shizuku 服务是否运行
- 检查应用是否有 Shizuku 权限
- 如果权限不足，请求用户授权

### 4. 配置应用

- `MainActivity.applyConfiguration()` 保存设置并启动特权进程
- `ShizukuProvider.startInstrument()` 使用 Instrumentation API 启动 `PrivilegedProcess`
- `PrivilegedProcess.onCreate()` 等待 Shizuku 准备，然后调用 `overrideConfig()`

### 5. 特权操作

- 获取 shell 权限委托
- 读取用户配置，构建 `PersistableBundle`
- 为选定的 SIM 卡调用 `CarrierConfigManager.overrideConfig()`
- 停止权限委托

### 6. 结果反馈

- 应用重新启动，显示配置成功对话框
- 提供跳转到系统网络设置的选项

## 关键组件

### MainActivity.java

- 主界面，处理用户交互
- 管理 Shizuku 状态监听
- 协调配置应用流程

### PrivilegedProcess.java

- 特权进程，实际执行配置修改
- 继承 Instrumentation，在系统权限下运行

### ImsConfigHelper.java

- 配置构建工具
- 根据用户设置生成运营商配置包

### ShizukuProvider.java

- Shizuku 服务提供者
- 负责启动特权进程

### LocaleHelper.java

- 多语言支持
- 自动检测系统语言或使用用户设置

## 配置项说明

- **VoLTE**: Voice over LTE，4G 语音通话
- **VoWiFi**: Voice over WiFi，WiFi 语音通话
- **VT**: Video Telephony，视频通话
- **VoNR**: Voice over NR，5G 语音通话
- **Cross SIM**: 跨 SIM 卡通话
- **UT**: Supplementary Services over UT，补充服务
- **5G NR**: 5G 新无线电支持

## 安全考虑

- 使用 Shizuku 而非 root，降低安全风险
- 只在用户明确操作时应用配置
- 配置修改可通过重启或恢复出厂设置撤销
- 应用开源，代码可审查

## 兼容性

- 需要 Android 9.0+ (API 28)
- 需要 Shizuku 12+
- 支持多 SIM 卡设备
- 支持中文和英文界面

## 注意事项

- 配置修改可能需要重启设备才能生效
- 某些运营商可能限制某些功能
- 在 Android 12+ 上可能需要额外权限
- 建议在应用配置前备份当前设置

## 故障排除

### 移动网络掉线或打不通电话

#### 可能原因

1. **运营商配置冲突**: TurboIMS 修改的 IMS 配置可能与移动运营商的网络设置冲突
2. **VoLTE/VoWiFi 设置不当**: 移动网络对 VoLTE 的要求可能与其他运营商不同
3. **5G NR 配置问题**: 某些移动网络的 5G 配置可能不兼容
4. **跨 SIM 设置影响**: 如果启用了跨 SIM 通话，可能干扰主 SIM 的网络连接

#### 解决方法

1. **检查配置设置**:

   - 尝试关闭 VoLTE 功能：`KEY_CARRIER_VOLTE_AVAILABLE_BOOL`
   - 调整 VoWiFi 设置：检查 `KEY_CARRIER_WFC_IMS_AVAILABLE_BOOL`
   - 禁用 5G NR：`KEY_CARRIER_NR_AVAILABILITIES_INT_ARRAY`

2. **运营商特定调整**:

   - 移动网络可能需要特定的 MCC/MNC 配置
   - 检查是否启用了不兼容的补充服务 (UT)

3. **重置配置**:

   - 在应用中重新应用配置
   - 或重启设备让系统重新加载配置
   - 极端情况下：恢复出厂设置或卸载应用

4. **验证步骤**:
   - 检查运营商配置版本：`vvb2060_config_version`
   - 查看系统日志中的错误信息
   - 确认 Shizuku 权限正常

#### 代码相关性分析

是的，这个问题很可能与 TurboIMS 的代码有关：

- **配置覆盖**: `overrideConfig()` 方法直接修改系统运营商配置
- **反射调用**: 使用反射调用私有 API，可能在某些设备上不稳定
- **权限委托**: `startDelegateShellPermissionIdentity()` 的权限提升可能不完整
- **版本兼容**: 不同 Android 版本对配置的处理方式不同

#### 建议

- 先尝试禁用部分 IMS 功能，看是否解决问题
- 检查设备日志：`adb logcat | grep -i carrier` 或 `grep -i ims`
- 考虑向项目提交 issue，提供设备信息和运营商详情
