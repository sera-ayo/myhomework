# Frontend

前端采用 Vue3 + Vite + TypeScript，用于展示：

- 今日使用概览
- 高频应用排行
- 行为趋势和类别占比
- 风险等级和解释信息

当前已实现：

- 登录页
- 仪表盘页
- 行为画像页
- 预警中心页
- 实验结果页

## 启动步骤

```bash
cd frontend
npm install
npm run dev
```

前端默认通过 Vite 代理将 `/api` 请求转发到 `http://127.0.0.1:8000`。

## 构建验证

```bash
cd frontend
npm run build
```
