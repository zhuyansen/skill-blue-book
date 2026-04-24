# 修订记录

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
