# 修订记录

## 2026-04-26 · v0.4

### 新增
- **第 9 章 · Distribution：商业化三角少的那条边**（~7,000 字 + 三角+第四条边对比图）
  - 承接南川（lovstudio）《商业化三角不可能定理》
  - 三个活案例：`emilkowalski/skill`（Service-on-Open）× `vercel-labs/skills`（Hosted Runtime）× `steipete/*`（Distribution Channel 复利）
  - **Hub 全量数据揭示**：
    - 65,729 总 skills · **53.8% 是 0 star**（35,396 个，distribution 失败）
    - Top 1000 skills 中位年龄 **320 天**（平均 513 天） · 90 天破百只占 22%
    - **9.6% 多产作者占 24.5% Top 1000 slots**（distribution 复利效应）
    - Top 15 多产作者无一例外是大公司/官方/已成名 KOL
  - **核心论点**："南川三角对 10% 已有用户的作者成立。剩下 90% 卡在 distribution 这条第四条边"
  - 自我反省 · Hub 自身 distribution 也很弱，月独立访问 5K，需要 6 个月做到 50K
- 可复现脚本 `data/ch09_distribution_analysis.py` + 1000 skill 快照 + 作者分布快照
- 三角+第四条边对比图 `data/ch09-fig1-triangle.png`

### 第 5 章传播复盘（2026-04-25）
- X 短推 24h 数据：**631 views · 0.32% 互动率**（vs Ch4 的 2.75%）
- 失败原因：hook 不够反直觉 + 推文超 280 字符被 Show more 截断 + 双图信息过载
- 学到的教训写进 part2-practice/ch05 反思区

---

## 2026-04-24 · v0.3

### 新增
- **第 5 章 · 迭代优化的闭环：从踩坑到飞轮**（~6,500 字 + 1 张生存曲线图）
  - 三个活案例对比：`NousResearch/autoreason`（3 路锦标赛 + Borda 投票）× `LufzzLiz/news-aggregator-skill`（MISTAKES.md 工程复盘）× Hub 原创生存数据
  - 开篇借 Autoreason 论文揭示迭代的 3 个隐藏 bug：prompt bias · scope creep · lack of restraint
  - **Hub 原创发现**（cohort = 2025-04 到 2025-10 创建的 1000 个 stars ≥ 20 skill）：
    - 持续 commit 的 skill 58.8% 还在涨 stars
    - 冷冻 90+ 天的 skill 只有 3.8% 在涨 stars（**15× 差距**）
    - 生存率从 6 月 80.6% 降到 10 月 69.3%（**第 10 个月是死亡拐点**）
    - Top 10% stars 的 92% 仍在活，bottom 50% 的 74.5% 仍在活
  - 提出 3 种迭代机制的递进路径：MISTAKES.md → 规律 commit → Autoreason（仅 Top 1% skill 值得投入算力）
- 可复现分析脚本 `data/ch05_survival_analysis.py` + 1000 skill 快照 `data/ch05_cohort_snapshot.json`
- 生存曲线图生成器 `data/ch05_fig1_survival_curve.py` → `data/ch05-fig1-survival-curve.png`

### 第 4 章传播数据（2026-04-24）
- X 短推（"原子化不是最小化"）34 分钟互动率 **2.75%**（Ch1 thread 的 3.3×）
- 宝玉 + LufzzLiz（cclank）均 organic like → 第 4 章论点获得 namesake 认可
- @ 点名的 Emil / Leon / LufzzLiz 三位作者均收到 notification

---

## 2026-04-24 · v0.2

### 新增
- **第 4 章 · 站在 Agent 角度设计 Skill（宝玉四条哲学）**（~7,000 字 + 5 张数据表 + 1 张 matplotlib 图）
  - 三个活案例对比：`emilkowalski/skill`（禅意）× `Leonxlnx/taste-skill`（法条）× `cclank/news-aggregator-skill`（复盘）
  - Hub Top 500 数据验证：Agent 视角 +7.7 分 · 脚本优先 +7.7 分 · 自我迭代 +8.6 分 · 原子化 +15 分
  - 独家发现：README 质量 sweet spot 是 10–20KB（<2KB 降到 36 分，>40KB 降到 45 分）
- **第 1 章公众号版** `social/ch01-wechat.md`（~3,000 字，已于 2026-04-24 发布）
- **3 张 Ch1 视觉素材**（gpt-image-2 生成）：`social/ch01-fig1/2/3-*.png`
  - Mahesh vs Barry 对比卡（hook）
  - Barry 65% vs 35% 经验饼图
  - 5 种扩展机制对比（Tool/MCP/RAG/System Prompt/Skill）
- **可复现脚本**：
  - `data/ch04_atomicity.py` — Top 500 原子化分析
  - `data/ch04_fig1_size_quality.py` — 图表生成器
  - `data/ch04_top500_snapshot.json` — 228KB 数据快照
  - `scripts/gen_ch01_figs.py` — 图片生成器（apimart gpt-image-2 API）

### 发布动作
- 公众号长文《今天的 LLM 都是 MIT 博士，但 Agent 需要的是 30 年老会计》(2026-04-24)
- X 短推 · 基于 Ch4 的 README 大小 vs 质量数据（2026-04-24）

---

## 2026-04-22 · v0.1

### 新增
- **第 3 章 · Skill 市场全景 2026**（~8,500 字 + 4 张 matplotlib 图）
- **第 1 章 · 从 Mahesh 到 Barry**（~8,000 字初稿）
- 项目骨架（README / preface / outline / LICENSE）
- 可复现的数据分析脚本 `data/ch03_analysis.py`
- 数字快照 `data/ch03-stats.json`（n = 61,776，取数时间 2026-04-22 09:00 UTC）
- 4 张 matplotlib 图表：长尾分布、供给爆炸、基尼对比、生命状态饼图
- 1 张 cover 图 `assets/cover.png`（HTML + headless Chrome 渲染，1200×630）
- 第 3 章 X Thread（16 条）+ Article 版发布素材 `social/ch03-x-post.md`

### 数据动作
- 清理 15 个批量污染账号共 **972 条垃圾记录**
  - TeleAI-mcp · mcp-tool-shop-org · Icattj · pipeworx-io · 等
  - 删除后 Hub 总量：62,748 → 61,776
- 标记 Hub 评分算法问题：76.8% 的 skill 挤在 20-39 分，Top 20 项目平均仅 46.8
  - 根因：`quality_examples` + `quality_agent_readiness` 对 README 风格要求过严
  - Q2 计划：引入 `adoption_signal` 作为第 10 维重新校准

### 书籍定位
- 写作风格：数据驱动 + 自我解剖 + 立场明确，不做综述合集
- 引用守则：涉及他人（花叔 / 宝玉 / lovstudio）观点必须原文 + 链接
- 更新节奏：每季度修订一次（0.1 / 0.2 / 1.0 ...）

---

## 待办（Roadmap）

**第 2 周**：第 2 章（三层渐进加载）

**第 3 周**：第 4-5 章（Agent 视角 + 迭代闭环）

**第 4 周**：第 6-7 章（9 类 × 4 路径 + 四大框架）

**第 5 周**：第 8-9 章（Skill 吞噬 + Distribution）

**第 6 周**：第 10-12 章（Verified Creator + 企业 + 未来）

**第 7 周**：附录 + 全书修订 + 配图统一

**第 8 周**：PDF 双语版 + ISBN 申请（如果决定做正式出版物）

---

## 如何反馈

- **数据错误**：发 [issue](https://github.com/zhuyansen/skill-blue-book/issues) 或 DM [@GoSailGlobal](https://x.com/GoSailGlobal)
- **论点异议**：开 [discussion](https://github.com/zhuyansen/skill-blue-book/discussions) 附上你的证据
- **想引用某段**：无需许可，但请带上链接到原文
