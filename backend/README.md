# Backend

后端采用 Django REST Framework，负责：

- 用户与设备管理
- 行为数据接收与存储
- 特征工程和风险评分
- 预警记录与反馈

## 当前定位

后端默认使用 `SQLite`，目标是降低环境配置难度，方便本地开发、老师演示和论文实验。

当前阶段不引入以下复杂依赖：

- `MySQL`
- `Redis`
- `Celery`

## 启动步骤

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

## 关键接口

- `POST /api/auth/login`
- `GET /api/auth/profile`
- `POST /api/devices/register`
- `POST /api/usage/sessions/bulk`
- `GET /api/dashboard/summary`
- `GET /api/dashboard/trend`
- `GET /api/dashboard/categories`
- `GET /api/risk/latest`
- `GET /api/warnings/list`
- `GET /api/experiments/metrics`

## 回归测试

```bash
. .venv/bin/activate
cd backend
python manage.py test
python manage.py check
```
