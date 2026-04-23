# Mobile App

移动端负责：

- 引导用户开启 Usage Access 权限
- 采集 App 使用会话
- 本地缓存和断网补传
- 接收预警并触发温和提醒

当前已实现 Android Studio 可继续扩展的工程骨架，核心能力包括：

- Demo 账号登录
- UsageStats 授权引导
- 本地 Room 缓存
- WorkManager 周期同步
- Retrofit 调用 Django 接口
- 本地长时使用提醒
- 手动同步与样例模式开关

默认服务地址为 `http://10.0.2.2:8000/`，适用于 Android Emulator。

如果使用真机，需要在“同步设置”页改成电脑的局域网 IP，例如：

`http://192.168.1.100:8000/`

建议包名：

`com.lxy.antiaddiction`

## 本地构建环境

本项目已经按以下组合验证通过：

- JDK 17
- Android Gradle Plugin 8.7.2
- Kotlin 2.0.21
- Android SDK Platform 35
- Android SDK Build-Tools 35.0.0
- Android SDK Build-Tools 34.0.0
- Platform-Tools 37.0.0

macOS + Homebrew 推荐环境变量如下：

```bash
export JAVA_HOME="/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
export ANDROID_HOME="/opt/homebrew/share/android-commandlinetools"
export ANDROID_SDK_ROOT="$ANDROID_HOME"
export PATH="/opt/homebrew/opt/openjdk@17/bin:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$PATH"
```

若首次配置命令行工具，可安装：

```bash
brew install openjdk@17
brew install --cask android-commandlinetools
yes | sdkmanager --licenses
sdkmanager "platform-tools" "platforms;android-35" "build-tools;35.0.0" "build-tools;34.0.0"
```

## 构建验证

已验证通过的命令：

```bash
cd mobile-app
./gradlew tasks
./gradlew :app:assembleDebug
```

Debug APK 输出位置：

`app/build/outputs/apk/debug/app-debug.apk`
