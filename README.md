# 《Skill 蓝皮书 2026》

> Blue Book of Agent Skills
> AgentSkillsHub 出品｜Jason Zhu 著

这是一本关于 **AI Agent Skills 生态** 的工作手册，不是教科书，不是综述，不是宣传材料。

它的特点是：

1. **基于真实数据**。所有关键结论都建立在 AgentSkillsHub 数据库 61,776+ 条 skill 的实测之上。分析脚本公开在 `data/` 目录。
2. **自我解剖**。第 3 章开始就会暴露 Hub 自己的数据漏洞——刊书不是为了护短，是为了推进问题的解决。
3. **有立场**。"Distribution 是三角的第四条边"、"54% 的 Skill 从未被看见"、"Skill 半衰期 6-12 个月"——这些是观点，不是共识。你可以不同意。

---

## 目录

### Part 1｜基础：Skill 是什么
- [第 1 章 · 为什么需要 Skill：从 Mahesh 到 Barry](part1-foundation/ch01-mahesh-to-barry.md)（待写）
- [第 2 章 · 三层渐进加载：Skill 的真正魔法](part1-foundation/ch02-three-layer-loading.md)（待写）
- [**第 3 章 · Skill 市场全景 2026**](part1-foundation/ch03-market-landscape.md) ✅

### Part 2｜实战：怎么写好 Skill
- [第 4 章 · 站在 Agent 角度设计 Skill](part2-practice/ch04-agent-perspective.md)（待写）
- [第 5 章 · 迭代优化的闭环：从踩坑到飞轮](part2-practice/ch05-iteration-loop.md)（待写）
- [第 6 章 · 9 种 Skill 类型 × 4 级分享路径](part2-practice/ch06-types-and-sharing.md)（待写）

### Part 3｜生态：Skill 正在吞噬一切
- [第 7 章 · 四大框架的对标与选择](part3-ecosystem/ch07-four-frameworks.md)（待写）
- [第 8 章 · Skill 正在吞噬其他柱子](part3-ecosystem/ch08-consuming-pillars.md)（待写）
- [第 9 章 · Distribution：商业化三角少的那条边](part3-ecosystem/ch09-distribution-edge.md)（待写）

### Part 4｜实践：AgentSkillsHub 运营手记
- [第 10 章 · Verified Creator：不是花钱买的认证](part4-hub/ch10-verified-creator.md)（待写）
- [第 11 章 · 咨询撮合 + 企业目录：Service-on-Open 怎么跑](part4-hub/ch11-consulting-enterprise.md)（待写）
- [第 12 章 · 未来：当 Claude 自己开始创建 Skills](part4-hub/ch12-future.md)（待写）

### 附录
- [A · Skill 设计速查表](appendix/A-design-cheatsheet.md)（待写）
- [B · AgentSkillsHub 使用指南](appendix/B-hub-usage-guide.md)（待写）
- [C · Verified Creator 申请流程](appendix/C-verified-creator-apply.md)（待写）
- [D · 参考文献 · 延伸阅读](appendix/D-references.md)（待写）

---

## 进度

| 章节 | 状态 | 字数 | 配图 |
|------|------|-----:|-----:|
| 第 3 章 · 市场全景 | ✅ 完稿 | ~8,500 | 4 张 matplotlib |
| 其余 11 章 | 🔲 待写 | - | - |

---

## 数据可复现

所有统计、图表、数字快照都在 [`data/`](data/) 目录：

```
data/
├── ch03_analysis.py     # 第 3 章数据分析脚本（可重跑）
├── ch03-stats.json      # 数字快照（2026-04-22 样本 61,776）
├── ch03-fig1-long-tail.png
├── ch03-fig2-supply-surge.png
├── ch03-fig3-gini-compare.png
└── ch03-fig4-lifecycle.png
```

如果你想验证某个数字：

```bash
cd /Users/zhuyansen/content/agent-skills-hub/backend
source venv/bin/activate
python /Users/zhuyansen/content/skill-blue-book/data/ch03_analysis.py
```

---

## 引用与反馈

- **网站**：https://agentskillshub.top
- **作者 X**：[@GoSailGlobal](https://x.com/GoSailGlobal)
- **作者邮箱**：m17551076169@gmail.com

欢迎在 X 或邮箱反馈错误、补充数据、提出异议。蓝皮书每季度修订一次。

---

© 2026 Jason Zhu · AgentSkillsHub · CC BY-NC-SA 4.0
