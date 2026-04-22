# 修订记录

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
