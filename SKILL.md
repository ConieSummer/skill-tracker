---
name: skill-tracker
version: "1.0"
description: >
  WorkBuddy 开发伴侣 skill，在开发其他 skill 时自动追踪每个执行步骤，
  实时记录结构化 JSON，提供本地可视化流程图，并维护「探索中」与「已确认」双轨流程文件。
  触发词：开始跟踪、步骤追踪、flow 追踪、skill-tracker、记录步骤、追踪开发过程
---

# Skill-Tracker 执行规范

## 0. 加载即激活

当用户在对话中加载本 skill（@skill-tracker 或直接引用），**立刻执行以下初始化**，无需用户补充指令：

```
1. 确认 runtime 目录：skill-tracker 目录下的 runtime/ 子目录
2. 创建（或清空）steps.json，写入空数组 []
3. 向用户回复一行简短提示：
   "✅ skill-tracker 已启动，开始追踪步骤。流程图：http://localhost:7788/viewer.html"
4. 继续执行主任务，不阻塞
```

---

## 1. 每步执行后：追加 JSON 节点

**每完成一个有意义的操作步骤**，立即用 replace_in_file 将以下 JSON 对象追加到 `steps.json` 末尾（插入到 `]` 之前）。

### JSON 字段规范

| 字段 | 类型 | 说明 |
|------|------|------|
| step | number | 步骤序号，从 1 开始递增 |
| description | string | 步骤的中文描述（10~30字） |
| impl_type | string | `playwright` / `agent` / `api` / `file_io` / `shell` / `manual` |
| method | string | 具体调用方式，如 `page.click()` / `write_to_file` / `execute_command` |
| selector | string | 元素定位符，无则填 `""` |
| selector_type | string | `css` / `xpath` / `text` / `""` |
| status | string | `exploring`（初始）/ `confirmed`（用户确认后）/ `error`（失败） |
| note | string | 可选备注，记录关键心得或待验证点 |

### 追加格式

steps.json 为一个 JSON 数组，追加时：
- 如果数组为空（`[]`），替换为 `[\n  {节点}\n]`
- 如果数组已有内容，将最后的 `\n]` 替换为 `,\n  {节点}\n]`

---

## 2. 确认机制（轻量询问）

每追加一个步骤后，在 AI 回复末尾附上一行简短询问（**不用 ask_followup_question**，避免阻塞主流程）：

> 💬 Step N「描述」已记录 — 是否确认写入 true_skill.md？回复「确认」或直接继续。

**用户回复「确认」时**：
1. 将该步骤的 `status` 从 `exploring` 改为 `confirmed`（replace_in_file 更新 steps.json）
2. 追加到 `true_skill.md`（见第 3 节格式）

**用户继续开发不回答**：直接记录下一步，状态保持 `exploring`。

---

## 3. true_skill.md 格式

文件路径：**当前被跟踪 skill 的目录下**，由用户首次确认时自动创建。

```markdown
# {Skill名称} - 已确认流程

> 状态：开发中 | 确认步骤数：{N} | 最后更新：{YYYY-MM-DD}

## 已确认步骤

### Step 1：{描述}
- **实现方式**：{impl_type 中文名}
- **具体方法**：{method}
- **定位方式**：{selector_type} → {selector}（无则填"无"）
- **状态**：🟢 已确认
```

---

## 4. 终止跟踪

用户说「停止跟踪」时：

1. 不再追加 JSON
2. 统计：总步骤数 / 已确认 / 探索中 / 出错
3. 回复一行摘要：
   > "⏹ skill-tracker 已停止。共记录 {N} 步：✅{confirmed} 已确认 / 🟡{exploring} 探索中 / 🔴{error} 出错"

---

## 5. 关键约束

- **不污染主流程**：本 skill 的所有文件操作只写 runtime/ 或 true_skill.md，不修改正在开发的 skill 文件
- **最小 token 消耗**：每步追加 JSON 不超过 30 token，不做多余解析
- **viewer.html 只读**：AI 不修改 viewer.html，用户自行用浏览器打开刷新查看

---

## 6. runtime 路径参考（跨平台自动检测）

skill 目录由 AI 自动检测，优先从环境变量读取，不写死路径。

```
runtime/
├── steps.json        ← AI 每步追加
```

**Windows**：`%USERPROFILE%\.workbuddy\skills\skill-tracker\runtime\steps.json`
**macOS**：`~/.workbuddy/skills/skill-tracker/runtime/steps.json`
**Linux**：`~/.workbuddy/skills/skill-tracker/runtime/steps.json`

启动本地服务器（Mac / Linux 终端）：
```bash
python3 /path/to/skill-tracker/serve.py
# 浏览器自动打开 http://localhost:7788/viewer.html
```

**禁止在 SKILL.md 中硬编码绝对路径**，一律用环境变量或相对路径。
