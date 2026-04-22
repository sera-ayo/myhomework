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
