# 基于手机软件使用行为的网络防沉迷预警系统

本仓库用于实现本科毕业设计《基于手机软件使用行为的网络防沉迷预警系统设计与实现》。

## 项目简介

系统围绕手机软件使用行为的采集、分析、风险识别和分级预警展开，形成完整闭环：

1. Android 端采集用户授权范围内的 App 使用行为数据。
2. 后端完成数据清洗、特征工程、风险评分和预警策略执行。
3. Web 前端展示行为画像、趋势分析和预警解释结果。
4. 通过规则引擎与机器学习模型结合，提高识别效果与可解释性。

本项目定位为“完整但不过度复杂”的本科毕设版本，重点保证：

- 数据库使用 `SQLite`
- 后端使用 `Django + Django REST Framework`
- 前端使用 `Vue3 + Vite`
- 模型使用 `scikit-learn` 轻量方案
- 不引入 `MySQL`
- 不引入 `Redis`
- 不引入 `Celery`
- 不要求 Docker 或复杂部署环境

## 仓库结构

- `backend/`: Django REST 后端
- `frontend/`: Vue3 可视化前端
- `mobile-app/`: Android 数据采集端
- `scripts/`: 数据准备、特征构建、训练评估脚本
- `demo_data/`: 脱敏样例数据
- `artifacts/`: 模型、指标和导出结果

## 快速启动

### 1. 后端

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r backend/requirements.txt
cd backend
python manage.py migrate
python manage.py seed_demo_user
python manage.py seed_app_catalog
python manage.py import_sample_usage
python manage.py train_models
python manage.py export_metrics
python manage.py runserver
```

后端启动后默认地址为 `http://127.0.0.1:8000/`。

### 2. 前端

```bash
cd frontend
npm install
npm run dev
```

前端默认地址为 `http://127.0.0.1:5173/`，已通过 Vite 代理转发 `/api` 到后端。

### 3. Demo 账号

- 用户名：`demo`
- 密码：`demo123456`

### 4. 训练与实验脚本

如果需要单独执行脚本而不是 Django 管理命令：

```bash
. .venv/bin/activate
python scripts/import_sample_usage.py
python scripts/build_features.py
python scripts/train_models.py
python scripts/export_demo_report.py
```

## 演示流程

建议按下面顺序给老师展示：

1. 启动后端与前端，使用 `demo` 账号登录 Web 端。
2. 在“仪表盘”展示今日总时长、近 7 日趋势和用途分布。
3. 在“行为画像”展示近 30 日使用变化和夜间使用情况。
4. 在“预警中心”展示风险解释和历史预警记录。
5. 在“实验结果”展示规则法与轻量模型对比指标。
6. 如果使用 Android 端，再展示登录、授权、同步和本地提醒。

## 回归验证

后端关键回归测试：

```bash
. .venv/bin/activate
cd backend
python manage.py test
```

前端构建验证：

```bash
cd frontend
npm run build
```

## Android 端说明

Android 工程目录为 [mobile-app](/Users/sdh/Documents/软院/lxy/myhomework/mobile-app)。

当前移动端已实现：

- Demo 账号登录
- UsageStats 授权引导
- 本地 Room 缓存
- WorkManager 周期同步
- Retrofit 上传数据
- 本地长时使用提醒
- 手动同步和样例模式开关

默认服务地址为 `http://10.0.2.2:8000/`，适用于 Android Emulator。真机演示时需要在“同步设置”页改成电脑局域网 IP。

## 当前交付状态

当前仓库已完成以下模块：

1. Django + SQLite 后端闭环
2. 样例数据、训练脚本和实验指标
3. Vue 前端可视化系统
4. Android 采集端工程骨架与核心同步逻辑
5. Git 分阶段提交历史
