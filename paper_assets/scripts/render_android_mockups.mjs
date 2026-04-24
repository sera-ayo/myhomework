import fs from "node:fs/promises";
import path from "node:path";

import { chromium } from "playwright";


const ROOT = path.resolve(import.meta.dirname, "..", "..");
const outputDir = path.join(ROOT, "paper_assets", "figures", "android");

const palette = {
  bg: "#EEF4F8",
  card: "#F9FCFF",
  text: "#102033",
  muted: "#58728D",
  accent: "#0A84C6",
  accentSoft: "#DCEFFA",
  accentWarm: "#F5B95F",
  line: "#D3E1EA",
};

const baseCss = `
  * { box-sizing: border-box; }
  body {
    margin: 0;
    min-height: 100vh;
    display: grid;
    place-items: center;
    background: radial-gradient(circle at top, #fdf8ef 0%, ${palette.bg} 48%, #dbe9ef 100%);
    font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
    color: ${palette.text};
  }
  .page-wrap {
    padding: 40px 24px;
  }
  .phone {
    width: 430px;
    min-height: 900px;
    border-radius: 42px;
    padding: 18px;
    background: #0d1823;
    box-shadow: 0 28px 90px rgba(11, 31, 45, 0.25);
  }
  .screen {
    min-height: 864px;
    border-radius: 32px;
    background: ${palette.bg};
    overflow: hidden;
    position: relative;
  }
  .status {
    display: flex;
    justify-content: space-between;
    padding: 18px 24px 8px;
    font-size: 14px;
    color: ${palette.muted};
  }
  .content {
    padding: 20px 24px 28px;
  }
  h1 {
    margin: 10px 0 0;
    font-size: 30px;
    line-height: 1.2;
  }
  .desc {
    margin: 14px 0 0;
    font-size: 16px;
    line-height: 1.8;
    color: ${palette.muted};
  }
  .field {
    margin-top: 18px;
    border-radius: 18px;
    border: 1px solid ${palette.line};
    background: ${palette.card};
    padding: 14px 16px;
  }
  .field label {
    display: block;
    margin-bottom: 8px;
    font-size: 13px;
    color: ${palette.muted};
  }
  .field .value {
    font-size: 16px;
  }
  .button {
    margin-top: 20px;
    width: 100%;
    border: 0;
    border-radius: 18px;
    padding: 15px 18px;
    font-size: 16px;
    font-weight: 700;
    text-align: center;
  }
  .button.primary {
    background: ${palette.accent};
    color: white;
  }
  .button.outline {
    background: transparent;
    color: ${palette.accent};
    border: 1.5px solid ${palette.accent};
  }
  .card {
    margin-top: 18px;
    border-radius: 22px;
    background: ${palette.card};
    border: 1px solid ${palette.line};
    padding: 18px;
  }
  .eyebrow {
    font-size: 13px;
    color: ${palette.muted};
  }
  .metric {
    margin-top: 10px;
    font-size: 36px;
    font-weight: 800;
  }
  .risk-pill {
    display: inline-block;
    margin-top: 10px;
    padding: 8px 14px;
    border-radius: 999px;
    background: ${palette.accentSoft};
    color: ${palette.accent};
    font-size: 14px;
    font-weight: 700;
  }
  .hint {
    margin-top: 12px;
    font-size: 14px;
    color: ${palette.muted};
    line-height: 1.7;
  }
  .switch-row {
    margin-top: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 18px;
    border-radius: 20px;
    background: ${palette.card};
    border: 1px solid ${palette.line};
  }
  .switch {
    width: 52px;
    height: 32px;
    border-radius: 999px;
    background: ${palette.accent};
    position: relative;
  }
  .switch::after {
    content: '';
    position: absolute;
    right: 4px;
    top: 4px;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: white;
  }
`;

function renderTemplate(content) {
  return `<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8" /><style>${baseCss}</style></head><body><div class="page-wrap"><div class="phone"><div class="screen"><div class="status"><span>9:41</span><span>5G 82%</span></div><div class="content">${content}</div></div></div></div></body></html>`;
}

const screens = [
  {
    file: "06_android_login_mockup.png",
    html: renderTemplate(`
      <p class="eyebrow">Android 采集端</p>
      <h1>网络防沉迷预警系统</h1>
      <p class="desc">当前移动端采用 Demo 账号登录，便于真机采集展示与答辩演示。</p>
      <div class="field"><label>用户名</label><div class="value">demo</div></div>
      <div class="field"><label>密码</label><div class="value">demo123456</div></div>
      <p class="hint">登录后可进入授权、采集、同步与本地提醒链路。</p>
      <div class="button primary">登录并继续</div>
    `),
  },
  {
    file: "07_android_permission_mockup.png",
    html: renderTemplate(`
      <p class="eyebrow">权限引导</p>
      <h1>授权使用情况访问权限</h1>
      <p class="desc">为了采集手机软件的使用行为，本应用需要你手动开启 Usage Access。系统只分析应用使用时长、启动频率和时段分布，不读取聊天或内容数据。</p>
      <div class="button primary">打开 Usage Access 设置</div>
      <div class="button outline">我已完成授权</div>
      <div class="card">
        <div class="eyebrow">论文说明点</div>
        <p class="hint">可用于阐述系统的数据采集边界、用户授权机制和隐私保护设计。</p>
      </div>
    `),
  },
  {
    file: "08_android_dashboard_mockup.png",
    html: renderTemplate(`
      <p class="eyebrow">今日概览</p>
      <h1>移动端本地总览</h1>
      <div class="card">
        <div class="eyebrow">今日累计使用时长</div>
        <div class="metric">4.6 小时</div>
      </div>
      <div class="card">
        <div class="eyebrow">最近风险结果</div>
        <div class="risk-pill">中风险</div>
        <p class="hint">娱乐类应用占比超过 60%；单次连续使用时长超过 60 分钟。</p>
      </div>
      <p class="hint">最近同步：2026-04-23 12:25</p>
      <p class="hint">同步完成：上传 18 条会话记录。</p>
      <div class="button primary">立即同步</div>
      <div class="button outline">同步设置</div>
      <div class="button outline">检查权限</div>
    `),
  },
  {
    file: "09_android_settings_mockup.png",
    html: renderTemplate(`
      <p class="eyebrow">同步设置</p>
      <h1>设备与服务配置</h1>
      <div class="field"><label>设备标识</label><div class="value">antiaddiction-demo-device</div></div>
      <div class="field"><label>后端服务地址</label><div class="value">http://10.0.2.2:8000/</div></div>
      <div class="switch-row"><div><div style="font-weight:700;">启用样例模式</div><div class="hint" style="margin-top:6px;">课堂展示时可关闭真机上传</div></div><div class="switch"></div></div>
      <p class="hint">启用后移动端不再上传真机采集结果，仅保留本地只读展示，适合课堂或无权限场景演示。</p>
      <div class="button primary">立即同步</div>
      <div class="button outline">清空本地缓存</div>
    `),
  },
];

await fs.mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 900, height: 1200 }, deviceScaleFactor: 2 });

try {
  for (const screen of screens) {
    await page.setContent(screen.html, { waitUntil: "load" });
    await page.locator(".phone").screenshot({
      path: path.join(outputDir, screen.file),
    });
    console.log(`Rendered ${screen.file}`);
  }
} finally {
  await browser.close();
}
