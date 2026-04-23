from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "paper_assets" / "figures" / "diagrams"


PALETTE = {
    "bg": "#f7f4ee",
    "card": "#fffaf2",
    "card_alt": "#eef6f8",
    "card_blue": "#dff0f4",
    "card_orange": "#fde7cc",
    "card_red": "#f7d8d2",
    "line": "#274248",
    "accent": "#b35c2e",
    "text": "#1f2f35",
    "muted": "#5a6d72",
}


@dataclass
class Node:
    x: int
    y: int
    w: int
    h: int
    title: str
    body: list[str]
    fill: str = PALETTE["card"]


def svg_header(width: int, height: int, title: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <title>{title}</title>
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="{PALETTE["line"]}" />
    </marker>
    <style>
      .title {{ font: 700 28px 'PingFang SC', 'Microsoft YaHei', sans-serif; fill: {PALETTE["text"]}; }}
      .subtitle {{ font: 500 14px 'PingFang SC', 'Microsoft YaHei', sans-serif; fill: {PALETTE["muted"]}; }}
      .node-title {{ font: 700 18px 'PingFang SC', 'Microsoft YaHei', sans-serif; fill: {PALETTE["text"]}; }}
      .node-body {{ font: 500 14px 'PingFang SC', 'Microsoft YaHei', sans-serif; fill: {PALETTE["muted"]}; }}
      .edge-label {{ font: 600 13px 'PingFang SC', 'Microsoft YaHei', sans-serif; fill: {PALETTE["accent"]}; }}
    </style>
  </defs>
  <rect x="0" y="0" width="{width}" height="{height}" fill="{PALETTE["bg"]}" rx="28" />
"""


def draw_node(node: Node) -> str:
    content = [
        f'<rect x="{node.x}" y="{node.y}" width="{node.w}" height="{node.h}" rx="20" fill="{node.fill}" stroke="{PALETTE["line"]}" stroke-width="2"/>',
        f'<text class="node-title" x="{node.x + 20}" y="{node.y + 34}">{node.title}</text>',
    ]
    start_y = node.y + 62
    for index, line in enumerate(node.body):
        content.append(
            f'<text class="node-body" x="{node.x + 20}" y="{start_y + index * 22}">• {line}</text>'
        )
    return "\n  ".join(content)


def draw_arrow(x1: int, y1: int, x2: int, y2: int, label: str | None = None) -> str:
    parts = [
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{PALETTE["line"]}" stroke-width="3" marker-end="url(#arrow)"/>'
    ]
    if label:
        label_x = (x1 + x2) / 2
        label_y = (y1 + y2) / 2 - 8
        parts.append(
            f'<text class="edge-label" x="{label_x}" y="{label_y}" text-anchor="middle">{label}</text>'
        )
    return "\n  ".join(parts)


def write_svg(name: str, content: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / name).write_text(content, encoding="utf-8")


def system_architecture() -> None:
    width, height = 1600, 920
    content = [svg_header(width, height, "系统总体架构图")]
    content.append('<text class="title" x="60" y="70">基于手机软件使用行为的网络防沉迷预警系统总体架构</text>')
    content.append('<text class="subtitle" x="60" y="100">面向论文第二章和第四章，可直接说明采集层、服务层、分析层与展示层之间的关系。</text>')

    nodes = [
        Node(70, 180, 300, 210, "Android 移动端", ["UsageStats 授权采集", "Room 本地缓存", "WorkManager 周期同步", "本地长时使用提醒"], PALETTE["card_blue"]),
        Node(430, 180, 300, 210, "Django REST 后端", ["Token 登录鉴权", "设备注册与批量上传", "日聚合与风险评估", "预警记录与实验指标"], PALETTE["card_alt"]),
        Node(790, 180, 300, 210, "分析与模型层", ["规则引擎打分", "特征工程构建", "RandomForest/Logistic", "模型缺失时规则回退"], PALETTE["card_orange"]),
        Node(1150, 180, 300, 210, "Vue 可视化前端", ["仪表盘展示", "行为画像分析", "预警中心说明", "实验结果对比"], PALETTE["card_blue"]),
        Node(430, 500, 300, 180, "SQLite 数据层", ["UsageSession 原始会话", "DailyUsageAggregate 日聚合", "RiskResult 风险结果", "WarningRecord 预警记录"], PALETTE["card"]),
        Node(790, 500, 300, 180, "论文与演示资产", ["metrics.json 指标文件", "CSV 导出报表", "系统截图与图表", "可直接嵌入论文"], PALETTE["card_red"]),
    ]
    content.extend(draw_node(node) for node in nodes)

    content.append(draw_arrow(370, 285, 430, 285, "上传使用会话"))
    content.append(draw_arrow(730, 285, 790, 285, "触发分析"))
    content.append(draw_arrow(1090, 285, 1150, 285, "读取结果"))
    content.append(draw_arrow(580, 390, 580, 500, "存储"))
    content.append(draw_arrow(940, 390, 940, 500, "导出"))
    content.append(draw_arrow(730, 590, 790, 590, "训练产物"))
    content.append(draw_arrow(1150, 320, 1090, 560, "展示/引用"))

    content.append("</svg>")
    write_svg("01_system_architecture.svg", "\n".join(content))


def business_flow() -> None:
    width, height = 1680, 820
    content = [svg_header(width, height, "业务流程图")]
    content.append('<text class="title" x="60" y="70">防沉迷预警业务闭环流程图</text>')
    content.append('<text class="subtitle" x="60" y="100">适合放在系统分析章节，强调“采集-上传-分析-反馈-展示”的闭环。</text>')

    steps = [
        Node(70, 210, 220, 180, "1. 用户登录", ["输入 demo 或真实账号", "保存 Token", "初始化服务地址"], PALETTE["card_blue"]),
        Node(360, 210, 220, 180, "2. 授权采集", ["开启 Usage Access", "读取 App 前后台事件", "本地生成会话记录"], PALETTE["card_alt"]),
        Node(650, 210, 220, 180, "3. 批量同步", ["设备注册", "批量上传会话", "去重与断网补传"], PALETTE["card_orange"]),
        Node(940, 210, 220, 180, "4. 风险分析", ["构建日聚合特征", "规则引擎评分", "ML 评分融合"], PALETTE["card_red"]),
        Node(1230, 210, 220, 180, "5. 预警输出", ["生成中/高风险预警", "解释触发原因", "下发柔性建议"], PALETTE["card_alt"]),
        Node(520, 500, 280, 180, "6. Web 端展示", ["仪表盘看总览", "行为画像看趋势", "实验页看指标"], PALETTE["card_blue"]),
        Node(900, 500, 280, 180, "7. 论文写作素材", ["截图直接入文", "表格与图表复用", "系统流程可解释"], PALETTE["card"]),
    ]
    content.extend(draw_node(node) for node in steps)

    content.append(draw_arrow(290, 300, 360, 300))
    content.append(draw_arrow(580, 300, 650, 300))
    content.append(draw_arrow(870, 300, 940, 300))
    content.append(draw_arrow(1160, 300, 1230, 300))
    content.append(draw_arrow(1340, 390, 1040, 500, "结果入库"))
    content.append(draw_arrow(800, 680, 900, 680, "导出图片/表格"))
    content.append(draw_arrow(660, 390, 660, 500, "前端可视化"))

    content.append("</svg>")
    write_svg("02_business_flow.svg", "\n".join(content))


def data_flow() -> None:
    width, height = 1660, 860
    content = [svg_header(width, height, "数据流图")]
    content.append('<text class="title" x="60" y="70">系统数据流图</text>')
    content.append('<text class="subtitle" x="60" y="100">突出从原始会话到聚合、风险结果、预警记录和实验指标的演进过程。</text>')

    nodes = [
        Node(90, 210, 250, 190, "原始输入", ["App 前后台事件", "开始时间 / 结束时间", "包名 / 应用名 / 类别"], PALETTE["card_blue"]),
        Node(410, 210, 250, 190, "UsageSession", ["原始会话表", "去重唯一键", "来源: android/sample"], PALETTE["card_alt"]),
        Node(730, 210, 250, 190, "DailyUsageAggregate", ["日总时长", "夜间时长", "用途占比", "最长单次时长"], PALETTE["card_orange"]),
        Node(1050, 210, 250, 190, "RiskResult", ["规则分", "机器学习分", "最终风险等级", "原因摘要"], PALETTE["card_red"]),
        Node(1370, 210, 210, 190, "WarningRecord", ["触发时间", "等级", "原因文本", "建议文本"], PALETTE["card"]),
        Node(530, 520, 260, 170, "metrics.json / CSV", ["训练评估指标", "特征重要性", "风险导出报表"], PALETTE["card_blue"]),
        Node(920, 520, 320, 170, "Vue 图表与论文图片", ["仪表盘/画像/预警/实验页", "论文图、截图、表格复用"], PALETTE["card_alt"]),
    ]
    content.extend(draw_node(node) for node in nodes)

    content.append(draw_arrow(340, 305, 410, 305, "批量写入"))
    content.append(draw_arrow(660, 305, 730, 305, "聚合"))
    content.append(draw_arrow(980, 305, 1050, 305, "评分"))
    content.append(draw_arrow(1300, 305, 1370, 305, "阈值触发"))
    content.append(draw_arrow(855, 400, 660, 520, "训练数据"))
    content.append(draw_arrow(1180, 400, 1080, 520, "查询与导出"))
    content.append(draw_arrow(790, 605, 920, 605, "前端读取"))

    content.append("</svg>")
    write_svg("03_data_flow.svg", "\n".join(content))


def er_diagram() -> None:
    width, height = 1720, 960
    content = [svg_header(width, height, "数据库关系图")]
    content.append('<text class="title" x="60" y="70">核心数据库实体关系图</text>')
    content.append('<text class="subtitle" x="60" y="100">适合放在数据库设计章节，字段保持论文级抽象，不必把所有列全部写满。</text>')

    nodes = [
        Node(70, 180, 280, 210, "User", ["id", "username", "password", "date_joined"], PALETTE["card_blue"]),
        Node(400, 180, 320, 230, "Device", ["device_code", "brand", "model", "android_version", "last_sync_at"], PALETTE["card_alt"]),
        Node(780, 130, 360, 300, "UsageSession", ["package_name", "app_name", "category", "purpose_group", "start_time / end_time", "duration_sec / is_night_session"], PALETTE["card_orange"]),
        Node(1200, 130, 360, 260, "DailyUsageAggregate", ["date", "total_duration_sec", "night_duration_sec", "entertainment_ratio", "switch_count / top_app_name"], PALETTE["card"]),
        Node(1200, 450, 360, 220, "RiskResult", ["rule_score / ml_score / final_score", "risk_level", "reason_summary", "model_name / version"], PALETTE["card_red"]),
        Node(780, 500, 360, 220, "WarningRecord", ["warning_time", "risk_level", "trigger_type", "reason_text / action_text"], PALETTE["card_blue"]),
    ]
    content.extend(draw_node(node) for node in nodes)

    content.append(draw_arrow(350, 285, 400, 285, "1:N"))
    content.append(draw_arrow(720, 285, 780, 285, "1:N"))
    content.append(draw_arrow(1140, 260, 1200, 260, "1:N 聚合"))
    content.append(draw_arrow(1380, 390, 1380, 450, "1:1/天"))
    content.append(draw_arrow(1140, 610, 1200, 560, "N:1 来源"))
    content.append(draw_arrow(300, 390, 860, 610, "用户拥有"))
    content.append(draw_arrow(560, 410, 920, 500, "设备触发"))

    content.append("</svg>")
    write_svg("04_database_er.svg", "\n".join(content))


def model_pipeline() -> None:
    width, height = 1660, 860
    content = [svg_header(width, height, "模型训练与推理流程图")]
    content.append('<text class="title" x="60" y="70">模型训练与在线推理流程图</text>')
    content.append('<text class="subtitle" x="60" y="100">可放实验设计章节，用于说明离线训练与在线推理如何衔接。</text>')

    nodes = [
        Node(80, 220, 230, 170, "样例/真实日聚合", ["DailyUsageAggregate", "历史使用行为", "多日趋势特征"], PALETTE["card_blue"]),
        Node(370, 220, 230, 170, "特征构建", ["build_features.py", "组合比例与基线特征", "输出 training_features.csv"], PALETTE["card_alt"]),
        Node(660, 220, 230, 170, "离线训练", ["LogisticRegression", "RandomForestClassifier", "生成 metrics.json"], PALETTE["card_orange"]),
        Node(950, 220, 230, 170, "模型产物", ["active_model.joblib", "feature_importance.json", "版本号写入"], PALETTE["card_red"]),
        Node(1240, 220, 250, 170, "在线推理", ["predict_ml_score()", "返回 ml_score", "与规则分融合"], PALETTE["card"]),
        Node(510, 520, 280, 170, "规则引擎", ["总时长 / 夜间时长", "娱乐占比 / 最长会话", "缺模时直接兜底"], PALETTE["card_blue"]),
        Node(940, 520, 320, 170, "最终风险输出", ["RiskResult", "WarningRecord", "前端实验页与预警页"], PALETTE["card_alt"]),
    ]
    content.extend(draw_node(node) for node in nodes)

    content.append(draw_arrow(310, 305, 370, 305))
    content.append(draw_arrow(600, 305, 660, 305))
    content.append(draw_arrow(890, 305, 950, 305))
    content.append(draw_arrow(1180, 305, 1240, 305))
    content.append(draw_arrow(775, 390, 650, 520, "规则特征共用"))
    content.append(draw_arrow(1490, 390, 1210, 520, "融合评分"))
    content.append(draw_arrow(790, 605, 940, 605, "0.4 规则 + 0.6 ML"))

    content.append("</svg>")
    write_svg("05_model_pipeline.svg", "\n".join(content))


def main() -> None:
    system_architecture()
    business_flow()
    data_flow()
    er_diagram()
    model_pipeline()
    print(f"Generated thesis diagrams under {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
