"""
Blue Book Chapter 4 · Fig 1: README size vs quality score (Top 500 skills)
Output: ch04-fig1-size-quality.png (X-post ready, 1200x675 16:9)
"""
import json
import statistics
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import font_manager

# Ensure a Chinese-capable font is picked up.
available = {f.name for f in font_manager.fontManager.ttflist}
for candidate in [
    "PingFang SC", "PingFang HK", "Hiragino Sans GB", "Hiragino Sans",
    "Songti SC", "STHeiti", "Heiti SC", "Heiti TC", "Arial Unicode MS",
]:
    if candidate in available:
        plt.rcParams["font.sans-serif"] = [candidate] + plt.rcParams["font.sans-serif"]
        break

HERE = Path(__file__).resolve().parent
data = json.load(open(HERE / "ch04_top500_snapshot.json"))
data = [x for x in data if x.get("readme_size") is not None and x.get("quality_score") is not None]

buckets = [
    ("<2KB",    0,       2_000),
    ("2-5KB",   2_000,   5_000),
    ("5-10KB",  5_000,   10_000),
    ("10-20KB", 10_000,  20_000),
    ("20-40KB", 20_000,  40_000),
    ("40KB+",   40_000,  10**9),
]

labels, counts, avg_qs = [], [], []
for name, lo, hi in buckets:
    sub = [x for x in data if lo <= x["readme_size"] < hi]
    if not sub:
        continue
    labels.append(name)
    counts.append(len(sub))
    avg_qs.append(statistics.mean(x["quality_score"] for x in sub))

# ── Plot ──────────────────────────────────────────────
plt.rcParams["axes.unicode_minus"] = False

fig, ax = plt.subplots(figsize=(12, 6.75), dpi=120, facecolor="#0a0e1a")
ax.set_facecolor("#0a0e1a")

colors = ["#ef4444", "#f97316", "#f59e0b", "#10b981", "#f59e0b", "#ef4444"]
bars = ax.bar(labels, avg_qs, color=colors, edgecolor="none", width=0.72)

# Sweet-spot highlight band
sweet = labels.index("10-20KB")
ax.add_patch(patches.Rectangle(
    (sweet - 0.5, 0), 1, 66, linewidth=2,
    edgecolor="#10b981", facecolor="none", linestyle="-", alpha=0.6,
))
ax.text(sweet, 60, "SWEET SPOT", ha="center", va="bottom",
        fontsize=13, fontweight="bold", color="#10b981")

# Bar labels — number on top (white, bold), n= below x-axis tick (muted)
for bar, q, n in zip(bars, avg_qs, counts):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.2,
            f"{q:.1f}", ha="center", va="bottom",
            fontsize=15, fontweight="bold", color="#ffffff")
    ax.text(bar.get_x() + bar.get_width() / 2, -3,
            f"n={n}", ha="center", va="top",
            fontsize=9.5, color="#64748b")

# Axes & title
ax.set_ylim(0, 68)
ax.set_ylabel("平均质量分 (0–100)", fontsize=12, color="#e2e8f0")
ax.set_xlabel("README 大小", fontsize=12, color="#e2e8f0")
ax.tick_params(colors="#cbd5e1", labelsize=11)
for spine in ax.spines.values():
    spine.set_color("#334155")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", color="#1e293b", linestyle="-", linewidth=0.5, alpha=0.5)
ax.set_axisbelow(True)

ax.set_title(
    "Skill 质量 vs README 大小  ·  AgentSkillsHub Top 500",
    fontsize=17, fontweight="bold", color="#ffffff", pad=34, loc="left",
)
ax.text(-0.4, 64,
        "原子化 ≠ 最小化 · 太小没信息，太大 scope creep · 甜区是 10-20KB（+15 分 vs <2KB）",
        fontsize=11.5, color="#94a3b8")

fig.text(0.99, 0.02,
         "agentskillshub.top · Blue Book Ch.4 · 2026-04-24",
         ha="right", va="bottom", fontsize=9, color="#64748b")

plt.tight_layout()
out = HERE / "ch04-fig1-size-quality.png"
plt.savefig(out, facecolor="#0a0e1a", bbox_inches="tight", dpi=120)
print(f"✅ saved → {out}")
