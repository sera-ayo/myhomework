# Paper Assets

本目录用于集中管理毕业论文与答辩所需图片资产，避免截图散落在聊天记录、桌面或本地临时目录中。

## 目录结构

- `figures/diagrams/`: 论文静态图，包括架构图、流程图、数据流图、ER 图、模型流程图
- `figures/web/`: Web 系统真实截图
- `figures/android/`: Android 端截图或移动端演示图
- `scripts/`: 图片生成与截图脚本

## 当前图片清单

### 静态图

- `01_system_architecture.svg/.png`: 系统总体架构图
- `02_business_flow.svg/.png`: 业务闭环流程图
- `03_data_flow.svg/.png`: 数据流图
- `04_database_er.svg/.png`: 数据库关系图
- `05_model_pipeline.svg/.png`: 模型训练与在线推理流程图

### Web 截图

- `01_web_login.png`: 登录页
- `02_web_dashboard.png`: 仪表盘
- `03_web_analysis.png`: 行为画像页
- `04_web_warnings.png`: 预警中心页
- `05_web_experiments.png`: 实验结果页

### Android 截图

- 计划包含：登录页、权限引导页、仪表盘页、同步设置页

## 生成方法

生成静态图 SVG：

```bash
python3 paper_assets/scripts/generate_thesis_figures.py
```

将静态图渲染为 PNG：

```bash
cd paper_assets
npm install
npm run render:diagrams
```

导出 Web 系统截图：

```bash
cd backend
../.venv/bin/python manage.py runserver 127.0.0.1:8000
```

```bash
cd frontend
npm run dev -- --host 127.0.0.1 --port 4173
```

```bash
cd paper_assets
npm run capture:web
```
