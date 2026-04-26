"""
Blue Book Ch 9 · Fig 1 · 商业化三角 + Distribution 第四条边

左图：南川的商业化三角（标准化 Runtime / 本地运行 / 源码保护）+ 三条路径
右图：扩展为四元结构（Distribution 在顶点）+ 90% 作者卡在哪里

输出: ch09-fig1-triangle.png · 1500×750 · 16:9
"""
import json, statistics as st
from datetime import datetime, timezone
from pathlib import Path
import math

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import font_manager

HERE = Path(__file__).resolve().parent

# ── Chinese font ───────────────────────────
available = {f.name for f in font_manager.fontManager.ttflist}
for cand in ["PingFang SC", "PingFang HK", "Hiragino Sans GB", "Hiragino Sans",
             "Songti SC", "STHeiti", "Heiti SC", "Arial Unicode MS"]:
    if cand in available:
        plt.rcParams["font.sans-serif"] = [cand] + plt.rcParams["font.sans-serif"]
        break
plt.rcParams["axes.unicode_minus"] = False

# ── Theme ──────────────────────────────────
BG = "#0a0e1a"
INK = "#ffffff"
MUTED = "#94a3b8"
GREEN = "#10b981"
ORANGE = "#f59e0b"
RED = "#ef4444"
PURPLE = "#a78bfa"
BLUE = "#4a9eff"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7.5), dpi=120, facecolor=BG)
for ax in (ax1, ax2):
    ax.set_facecolor(BG)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect("equal")

# ─────────────────────────────────────────────
# LEFT · 南川的商业化三角
# ─────────────────────────────────────────────
# Triangle vertices
top = (0, 0.55)
left = (-0.65, -0.45)
right = (0.65, -0.45)

triangle = plt.Polygon([top, left, right], closed=True,
                        edgecolor=BLUE, facecolor=BLUE, alpha=0.10, linewidth=2.5)
ax1.add_patch(triangle)

# Vertex labels
ax1.text(0, 0.70, "标准化 Runtime", ha="center", fontsize=14, fontweight="bold", color=INK)
ax1.text(0, 0.62, "（能不能被装）", ha="center", fontsize=9, color=MUTED)

ax1.text(-0.78, -0.55, "本地运行", ha="center", fontsize=14, fontweight="bold", color=INK)
ax1.text(-0.78, -0.63, "（不依赖云）", ha="center", fontsize=9, color=MUTED)

ax1.text(0.78, -0.55, "源码保护", ha="center", fontsize=14, fontweight="bold", color=INK)
ax1.text(0.78, -0.63, "（保留 IP）", ha="center", fontsize=9, color=MUTED)

# Edge labels (paths)
ax1.text(-0.40, 0.10, "Open Source", ha="center", fontsize=11,
         color=GREEN, fontweight="bold", rotation=53)
ax1.text(0.40, 0.10, "Hosted SaaS", ha="center", fontsize=11,
         color=ORANGE, fontweight="bold", rotation=-53)
ax1.text(0, -0.50, "Closed Runtime", ha="center", fontsize=11,
         color=PURPLE, fontweight="bold")

# Title
ax1.text(0, 0.93, "南川 · 商业化三角", ha="center",
         fontsize=18, fontweight="bold", color=INK)
ax1.text(0, 0.85, "三选二 · 必舍其一", ha="center",
         fontsize=11, color=MUTED)

ax1.text(0, -0.85, "对 10% 已经有用户的作者成立",
         ha="center", fontsize=10, color=MUTED)

# ─────────────────────────────────────────────
# RIGHT · 四元结构 + 90% 卡点
# ─────────────────────────────────────────────
# 4-element structure: tetrahedron in 2D projection
# Top vertex: Distribution (highlighted)
top_d = (0, 0.70)
v1 = (-0.65, -0.10)   # 标准化 Runtime
v2 = (0.65, -0.10)    # 源码保护
v3 = (0, -0.55)       # 本地运行

# Triangle base
base = plt.Polygon([v1, v2, v3], closed=True,
                    edgecolor=BLUE, facecolor=BLUE, alpha=0.08, linewidth=1.5,
                    linestyle="--")
ax2.add_patch(base)

# Lines from top to each base vertex
for v in [v1, v2, v3]:
    ax2.plot([top_d[0], v[0]], [top_d[1], v[1]],
             color=GREEN, linewidth=2.5, alpha=0.9, zorder=2)

# Top vertex · Distribution (BIG, highlighted)
ax2.scatter([top_d[0]], [top_d[1]], s=600, color=GREEN,
            zorder=5, edgecolors=INK, linewidths=2)
ax2.text(0, 0.86, "★ Distribution", ha="center",
         fontsize=15, fontweight="bold", color=GREEN)
ax2.text(0, 0.78, "（第四条边）", ha="center",
         fontsize=10, color=GREEN)

# Base vertices · 三角原 3 个
ax2.scatter([v1[0]], [v1[1]], s=180, color=BLUE, edgecolors=INK, linewidths=1, zorder=4)
ax2.scatter([v2[0]], [v2[1]], s=180, color=BLUE, edgecolors=INK, linewidths=1, zorder=4)
ax2.scatter([v3[0]], [v3[1]], s=180, color=BLUE, edgecolors=INK, linewidths=1, zorder=4)
ax2.text(-0.78, -0.10, "标准化\nRuntime", ha="center", fontsize=10, color=INK)
ax2.text(0.78, -0.10, "源码\n保护", ha="center", fontsize=10, color=INK)
ax2.text(0, -0.66, "本地运行", ha="center", fontsize=10, color=INK)

# 90% blocked annotation
ax2.text(0, 0.30,
         "90% 作者\n卡在这里",
         ha="center", va="center",
         fontsize=12, fontweight="bold", color=RED,
         bbox=dict(boxstyle="round,pad=0.5", facecolor=BG,
                   edgecolor=RED, linewidth=2))

# Title
ax2.text(0, 0.93, "Skill 作者实际面对的", ha="center",
         fontsize=18, fontweight="bold", color=INK)

ax2.text(0, -0.85, "Hub 数据：53.8% 0 star · 中位 320 天破百",
         ha="center", fontsize=10, color=MUTED)

# ── Super title ───────────────────────────
fig.suptitle("商业化三角 + Distribution · 90% 作者面对的真实瓶颈",
             fontsize=18, fontweight="bold", color=INK, y=0.97, x=0.03, ha="left")
fig.text(0.03, 0.92,
         "南川的三角描述 commercial control 的不可能。Distribution 是必须先解决的发现问题。",
         fontsize=11, color=MUTED, ha="left")

fig.text(0.985, 0.015,
         "agentskillshub.top  ·  Blue Book Ch.9  ·  2026-04-26",
         ha="right", va="bottom", fontsize=9, color="#64748b")

plt.tight_layout(rect=[0, 0.02, 1, 0.88])
out = HERE / "ch09-fig1-triangle.png"
plt.savefig(out, facecolor=BG, bbox_inches="tight", dpi=120)
print(f"✅ saved → {out}")
