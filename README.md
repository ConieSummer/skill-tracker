# skill-tracker

> WorkBuddy (CodeBuddy) 开发伴侣 — 实时追踪 AI 开发过程中的每一个步骤，以可视化流程图呈现。

✨ **功能亮点**
- ⚡ 零侵入 — `@skill-tracker` 立即激活，不打断主工作流
- 📊 实时可视化 — 浏览器打开流程图，每步实时刷新
- 🔄 双轨记录 — 「探索中」与「已确认」分离，避免半成品污染最终代码
- 🖥️ 跨平台 — Windows / macOS / Linux 开箱即用

---

## 📸 效果预览

```
🟡 Step 1  探索中  ·  创建 SKILL.md 基础结构
🟡 Step 2  探索中  ·  定义 step JSON Schema
🟡 Step 3  探索中  ·  实现 viewer 可视化页面
🟢 Step 4  已确认  ·  配置 serve.py 本地服务器  ← 用户已确认
🟢 Step 5  已确认  ·  编写启动脚本  ← 用户已确认
```

---

## 🚀 快速开始

### 第一步：安装 skill

将整个仓库克隆到本地 skill 目录：

```bash
# Windows PowerShell
git clone https://github.com/YOUR_USERNAME/skill-tracker.git "$HOME/.workbuddy/skills/skill-tracker"

# macOS / Linux
git clone https://github.com/YOUR_USERNAME/skill-tracker.git ~/.workbuddy/skills/skill-tracker
```

> 也可以直接下载 ZIP，解压后放入 `~/.workbuddy/skills/skill-tracker/` 目录。

### 第二步：启动本地可视化服务

**Windows**：双击运行 `启动viewer.bat`

**macOS / Linux**：双击运行 `启动viewer.command`

或手动运行：
```bash
python3 /path/to/skill-tracker/serve.py
# 浏览器自动打开 http://localhost:7788/viewer.html
```

> ⚠️ 需要 Python 3.6+，无其他依赖。

### 第三步：开始追踪

在 WorkBuddy / CodeBuddy 对话中输入：

```
@skill-tracker
```

或直接说：

```
开始跟踪
```

---

## 📖 使用说明

### 追踪流程

1. **激活** → `@skill-tracker` 或说「开始跟踪」，runtime/steps.json 初始化为空数组
2. **开发** → AI 每完成一步操作，自动追加一条 JSON 记录到 steps.json
3. **查看** → 刷新浏览器 http://localhost:7788/viewer.html，流程图实时更新
4. **确认** → 回复「确认」，该步骤从 🟡 探索中 → 🟢 已确认，写入 true_skill.md
5. **停止** → 说「停止跟踪」，输出统计摘要

### 节点状态

| 状态 | 颜色 | 含义 |
|------|------|------|
| `exploring` | 🟡 黄色 | 探索中，尚未确认，可能调整或废弃 |
| `confirmed` | 🟢 绿色 | 用户确认后固化，可信可用 |
| `error` | 🔴 红色 | 执行失败或已废弃 |

### 步骤 JSON 格式

```json
{
  "step": 1,
  "description": "创建 SKILL.md 基础结构",
  "impl_type": "file_io",
  "method": "write_to_file",
  "selector": "",
  "selector_type": "",
  "status": "exploring",
  "note": ""
}
```

> 详细字段说明见 [references/step-json-schema.md](references/step-json-schema.md)

---

## 📁 项目结构

```
skill-tracker/
├── SKILL.md                    # 核心指令（WorkBuddy 加载入口）
├── viewer.html                 # 可视化流程图页面
├── serve.py                    # Python 本地服务器
├── 启动viewer.bat              # Windows 快速启动
├── 启动viewer.command          # macOS 快速启动
├── runtime/
│   └── steps.json             # AI 追加的步骤数据（运行时生成）
└── references/
    ├── step-json-schema.md    # JSON Schema 规范
    └── viewer-usage.md        # viewer.html 使用说明
```

---

## ⚙️ 工作原理

```
用户: "@skill-tracker"
    ↓
AI: 初始化 steps.json = []
    ↓
AI: 执行开发步骤
    ↓
AI: replace_in_file 追加 JSON 到 steps.json
    ↓
用户: 浏览器自动刷新 → 看到流程图更新
    ↓
用户: 回复「确认」
    ↓
AI: status → confirmed，写入 true_skill.md
```

---

## 🔧 技术栈

| 组件 | 技术 |
|------|------|
| Skill 指令 | Markdown（SKILL.md） |
| 数据格式 | JSON |
| 可视化 | 原生 HTML + CSS + JavaScript（零依赖） |
| 本地服务 | Python 3 标准库（socketserver + http.server） |
| 自动刷新 | XMLHttpRequest 轮询 |

---

## 📌 注意事项

- `runtime/steps.json` 由 AI 自动生成，**请勿手动修改**
- `viewer.html` 不需要 AI 修改，用户自行在浏览器中刷新即可
- 如果端口 7788 被占用，修改 `serve.py` 中的 `PORT` 变量

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 License

MIT License — 随便用，随便改。
