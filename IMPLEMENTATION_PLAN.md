# 基于手机软件使用行为的网络防沉迷预警系统实现方案

## 1. 项目目标

本项目面向本科毕业设计《基于手机软件使用行为的网络防沉迷预警系统设计与实现》，目标是构建一个具备真实数据采集、行为画像分析、风险识别和分级预警能力的系统原型。

系统要形成完整闭环：

1. Android 端采集用户授权范围内的 App 使用行为数据。
2. 服务端完成数据清洗、特征工程、风险评分和预警决策。
3. Web 前端展示趋势、画像、风险等级和解释信息。
4. 通过规则引擎与机器学习模型结合，实现可解释的风险识别。

## 2. 总体架构

项目采用混合架构，而不是纯 B/S 架构。

- `mobile-app/`：Android 采集端，负责权限引导、使用行为采集、本地缓存、同步和轻量本地提醒。
- `backend/`：Django REST 服务端，负责用户、设备、日志接收、分析、画像、预警、实验评估。
- `frontend/`：Vue3 可视化前端，负责仪表盘、趋势图、画像展示、预警解释。
- `scripts/`：数据准备、特征生成、训练评估和演示数据脚本。

核心数据流如下：

```text
Android UsageStatsManager
-> 本地 Room 缓存
-> 周期同步到 Django API
-> MySQL 存储原始会话与日聚合
-> 特征工程与风险评分
-> 输出预警记录与可视化数据
-> Vue3 前端展示
```

## 3. 技术选型

### 3.1 Android 端

- Kotlin
- Android Jetpack
- Room
- WorkManager
- Retrofit

主要依赖系统能力：

- `UsageStatsManager`
- `UsageEvents`
- `PackageManager`

### 3.2 后端

- Python 3.11
- Django 5.x
- Django REST Framework
- MySQL 8.x
- Redis
- Celery 或 APScheduler
- Pandas
- NumPy
- scikit-learn

### 3.3 前端

- Vue3
- Vite
- TypeScript
- Pinia
- Vue Router
- ECharts
- Element Plus

## 4. 核心模块设计

## 4.1 Android 采集端

Android 端功能模块拆分如下：

1. 权限引导模块
- 引导用户开启 Usage Access 权限。
- 展示隐私协议与数据使用说明。

2. 使用行为采集模块
- 周期性读取 `UsageEvents`。
- 将前后台切换事件拼接为可分析的会话数据。

3. 本地缓存模块
- 使用 Room 保存原始会话和小时级聚合结果。
- 记录最近同步时间，支持断网补传。

4. 同步模块
- 使用 WorkManager 定时上传。
- 上传脱敏后的会话与统计特征。

5. 本地预警模块
- 对超长单次娱乐使用做即时提醒。
- 接收服务端下发的风险等级和建议。

建议采集字段：

- `device_id`
- `user_id`
- `package_name`
- `app_name`
- `category`
- `session_start`
- `session_end`
- `duration_sec`
- `hour_bucket`
- `event_date`
- `is_night_session`

## 4.2 后端服务

建议 Django 内按业务拆分应用：

- `users`：注册登录、JWT 鉴权
- `devices`：设备绑定、同步状态
- `usage`：日志接收、原始会话、日聚合
- `analysis`：特征工程、趋势分析、行为画像
- `warnings`：风险评分、预警记录、反馈
- `questionnaires`：问卷标签、实验数据

### 4.2.1 数据库核心表

| 表名 | 说明 |
| --- | --- |
| `user` | 用户账号信息 |
| `device` | 绑定设备信息 |
| `app_profile` | 应用名称、类别映射 |
| `usage_session` | 原始会话数据 |
| `usage_daily_agg` | 日级聚合结果 |
| `feature_daily` | 日级特征结果 |
| `risk_result` | 风险评分结果 |
| `warning_record` | 预警记录 |
| `intervention_feedback` | 用户反馈 |
| `questionnaire_result` | 问卷分数与标签 |

### 4.2.2 后端接口

用户与设备：

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/profile`
- `POST /api/devices/bind`
- `GET /api/devices/status`

数据上传：

- `POST /api/usage/sessions/upload`
- `POST /api/usage/daily/upload`
- `GET /api/usage/sync-config`

分析与预警：

- `GET /api/dashboard/summary`
- `GET /api/analysis/trend`
- `GET /api/analysis/categories`
- `GET /api/risk/latest`
- `GET /api/warnings/list`
- `POST /api/warnings/feedback`
- `POST /api/questionnaire/submit`

## 4.3 Web 前端

前端页面建议如下：

1. 登录注册页
- 登录、注册、隐私说明。

2. 仪表盘首页
- 今日总使用时长
- 高风险等级提示
- 高频 App Top10
- 时间热力图
- 应用类别占比

3. 行为画像页
- 近 7 日和近 30 日趋势
- 夜间使用比例
- 娱乐类与学习类占比变化
- 高风险时间段分布

4. 预警中心页
- 历史预警记录
- 触发原因解释
- 用户反馈记录

5. 实验分析页
- 模型对比指标
- 特征重要性
- 问卷统计结果

## 5. 风险识别方案

## 5.1 设计原则

不直接上复杂深度学习模型，而采用“规则引擎 + 机器学习”的渐进式方案：

1. 先保证冷启动和实时预警能力。
2. 再引入机器学习提升准确率。
3. 保留解释能力，支持论文论证和用户理解。

## 5.2 特征工程

### 5.2.1 日级特征

- 当日总使用时长
- 启动次数
- 平均单次会话时长
- 最长连续使用时长
- 夜间使用时长占比
- 娱乐类占比
- 社交类占比
- 学习/工具类占比
- Top1 应用时长占比
- 应用切换次数

### 5.2.2 滑动窗口特征

- 近 3 天总时长增长率
- 近 7 天夜间使用增长率
- 近 7 天娱乐类占比均值
- 周末与工作日差异
- 风险分数连续上升天数

### 5.2.3 个体基线

为减少误判，需要构建用户个体基线：

- 近 7 天平均总时长
- 近 7 天平均娱乐类占比
- 近 7 天平均夜间时长
- 近 7 天平均切换频率

风险判断优先使用“相对个人基线的偏离量”，而不是完全依赖全局固定阈值。

## 5.3 规则引擎

建议规则评分项：

| 评分项 | 分值范围 |
| --- | --- |
| 总使用时长偏高 | 0-25 |
| 夜间使用偏高 | 0-20 |
| 娱乐/短视频占比偏高 | 0-20 |
| 最长连续使用过长 | 0-15 |
| 应用切换频繁 | 0-10 |
| 近 3 天增长过快 | 0-10 |

规则总分：

```text
rule_score = S1 + S2 + S3 + S4 + S5 + S6
```

风险分级：

- `0-34`：低风险
- `35-59`：关注
- `60-79`：中风险
- `80-100`：高风险

实时触发条件建议：

1. 娱乐类 App 连续使用超过 45 分钟。
2. 22:00 后娱乐类 App 连续使用超过 30 分钟。
3. 近 2 小时娱乐类占比超过 70%，且切换频率明显上升。

## 5.4 机器学习模型

推荐主模型：

- `RandomForestClassifier`

推荐对比模型：

- `LogisticRegression`
- `XGBoost`

标签构造方式：

1. 每周由测试用户填写一次简版 SAS-SV 问卷。
2. 按问卷得分划分低、中、高风险标签。
3. 将问卷提交日前 7 天的行为特征作为训练样本。

融合策略：

```text
if history_days < 7:
    final_score = rule_score
else:
    final_score = 0.4 * rule_score + 0.6 * (ml_probability * 100)
```

需要输出解释信息：

- 贡献最高的三个特征
- 风险上升最明显的时间段
- 主要风险来源类别

## 6. 分阶段开发计划

## 阶段一：最小闭环

目标：先打通“采集 -> 上传 -> 展示”

工作项：

1. Android 端完成授权和会话采集。
2. Django 后端完成登录和上传接口。
3. MySQL 完成用户、设备、会话表。
4. 前端展示总时长和 Top10 App。

## 阶段二：行为画像

目标：从统计提升到分析

工作项：

1. 完成日聚合和类别映射。
2. 实现趋势图、热力图和类别占比。
3. 加入个体基线计算。

## 阶段三：风险识别

目标：从分析提升到预警

工作项：

1. 实现规则引擎。
2. 完成风险等级和预警记录。
3. Android 端接收预警提示。

## 阶段四：实验评估

目标：从能运行提升到可论文论证

工作项：

1. 接入问卷标签。
2. 训练随机森林和对比模型。
3. 输出评估指标和特征重要性图。
4. 收集用户反馈和接受度结果。

## 7. 实验与测试设计

功能测试重点：

- 权限引导是否正确
- 日志补传是否可用
- 重复会话是否被正确处理
- 风险结果是否正确回传
- 预警记录是否正确入库

算法评估指标：

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

用户接受度问卷建议：

- 提醒是否打扰正常使用
- 提醒是否足够温和
- 是否愿意继续使用系统
- 风险解释是否容易理解

## 8. 交付重点

优秀毕设的关键不在于模型越复杂越好，而在于以下三点同时成立：

1. 能从真机采到真实行为数据。
2. 风险识别逻辑清晰且可解释。
3. 前后端联调完整，能够稳定演示。

因此，推荐的落地顺序是：

1. 先完成 Android 采集端和后端上传闭环。
2. 再完成前端仪表盘和行为画像。
3. 然后实现规则引擎预警。
4. 最后加入机器学习模型和实验评估。
