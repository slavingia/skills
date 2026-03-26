# The Minimalist Entrepreneur Skills 项目分析

## 项目概览

**项目名称**: The Minimalist Entrepreneur — Claude Code Skills  
**作者**: Sahil Lavingia  
**仓库**: https://github.com/slavingia/skills  
**类型**: Claude Code Skills 集合  
**关联书籍**: [The Minimalist Entrepreneur](https://www.minimalistentrepreneur.com/)

### 核心价值
基于《The Minimalist Entrepreneur》一书，提供 10 个 Claude Code Skills，帮助创业者：
- 找到社区
- 验证想法
- 构建 MVP
- 流程化
- 获取首批客户
- 定价
- 营销计划
- 可持续增长
- 建立公司价值观
- 极简主义审查

---

## 项目结构

```
skills/
├── .claude-plugin/              # Claude Code 插件配置
│   └── marketplace.json         # 插件市场清单
├── skills/                       # 10 个 Skills
│   ├── find-community/          # 找到社区
│   ├── validate-idea/           # 验证想法
│   ├── mvp/                     # 最小可行产品
│   ├── processize/              # 流程化
│   ├── first-customers/         # 首批客户
│   ├── pricing/                 # 定价
│   ├── marketing-plan/          # 营销计划
│   ├── grow-sustainably/        # 可持续增长
│   ├── company-values/          # 公司价值观
│   └── minimalist-review/       # 极简主义审查
└── README.md                     # 项目文档
```

---

## 10 个 Skills 详解

| Skill | 命令 | 使用场景 |
|-------|------|----------|
| **Find Community** | `/find-community` | 寻找商业想法，尝试找到你的社区 |
| **Validate Idea** | `/validate-idea` | 测试商业想法是否值得追求 |
| **MVP** | `/mvp` | 准备构建第一个产品，纠结于范围 |
| **Processize** | `/processize` | 有产品想法，想在写代码前手工交付价值 |
| **First Customers** | `/first-customers` | 有产品，需要找到前 100 个客户 |
| **Pricing** | `/pricing` | 设定价格，考虑价格变动 |
| **Marketing Plan** | `/marketing-plan` | 有产品市场匹配，准备通过内容扩展 |
| **Grow Sustainably** | `/grow-sustainably` | 做关于支出、招聘或扩展的决策 |
| **Company Values** | `/company-values` | 定义文化，准备招聘 |
| **Minimalist Review** | `/minimalist-review` | 对任何商业决策进行直觉检查 |

---

## The Minimalist Entrepreneur 创业旅程

Skills 遵循书中的进度：

1. **Community（社区）** — 从找到你的人开始
2. **Validate（验证）** — 确保问题值得解决
3. **Build（构建）** — 交付一个手工流程，然后产品化
4. **Processize（流程化）** — 将你的产品想法变成今天就能交付的手工流程
5. **Sell（销售）** — 逐个获得 100 个客户
6. **Price（定价）** — 从第一天开始收费
7. **Market（营销）** — 通过内容建立受众
8. **Grow（增长）** — 保持盈利，可持续增长
9. **Culture（文化）** — 建造你想住的房子
10. **Review（审查）** — 将极简主义原则应用于每个决策

---

## 安装方式

### Claude Code 插件市场安装

```
/plugin marketplace add slavingia/skills
/plugin install minimalist-entrepreneur
```

### 本地克隆安装

```bash
git clone https://github.com/slavingia/skills.git ~/.claude/plugins/skills
```

然后在 Claude Code 中：

```
/plugin marketplace add ~/.claude/plugins/skills
/plugin install minimalist-entrepreneur
```

---

## Skill 结构模式

每个 Skill 遵循标准的 Claude Code Skill 结构：

```
skill-name/
└── SKILL.md    # Skill 定义和说明
```

---

## 项目亮点

1. **书籍驱动** — 基于《The Minimalist Entrepreneur》的完整方法论
2. **端到端** — 覆盖从想法到规模化的完整创业旅程
3. **极简主义** — 专注于核心，避免过度工程
4. **实践导向** — 每个 Skill 解决具体的创业问题
5. **Claude Code 集成** — 原生支持 Claude Code 插件系统

---

## 进一步探索

- 查看每个 skill 的 `SKILL.md` 了解详细使用方法
- 阅读《The Minimalist Entrepreneur》书籍理解底层方法论
- 查看 `.claude-plugin/marketplace.json` 了解插件配置
