#!/usr/bin/env python3
"""
Generate 2 matplotlib figures for Chapter 6:
- fig1: Category distribution (horizontal bar)
- fig2: 9 functional types × 4 sharing tiers heat-matrix
"""
import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager

DATA = Path(__file__).resolve().parent / "ch06-category-stats.json"
OUT = Path(__file__).resolve().parent

# Try to find a Chinese-capable font
CN_FONTS = ["PingFang SC", "Heiti SC", "STHeiti", "Arial Unicode MS",
            "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Zen Hei", "DejaVu Sans"]
for fname in CN_FONTS:
    try:
        font_manager.findfont(fname, fallback_to_default=False)
        plt.rcParams["font.sans-serif"] = [fname]
        plt.rcParams["axes.unicode_minus"] = False
        print(f"Using font: {fname}")
        break
    except Exception:
        continue


def fig1_category_distribution():
    d = json.load(open(DATA))
    rows = sorted(d["rows"], key=lambda r: r["n"])
    # Drop trivial rows (count < 50)
    rows = [r for r in rows if r["n"] >= 50]
    cats = [r["cat"] for r in rows]
    counts = [r["n"] for r in rows]
    pcts = [r["pct"] for r in rows]
    avg_qs = [r["avg_qs"] for r in rows]

    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=150)
    bars = ax.barh(cats, counts, color=["#94a3b8" if c < 1000 else "#4f46e5" for c in counts])

    for i, (b, n, p, q) in enumerate(zip(bars, counts, pcts, avg_qs)):
        # right side: count + percent
        ax.text(n + max(counts) * 0.01, i, f"{n:,}  ({p:.1f}%)",
                va="center", fontsize=10, color="#1e293b")
        # inside bar: avg quality score (only when wide enough)
        if n > max(counts) * 0.05:
            ax.text(n * 0.97, i, f"avgQS {q:.0f}",
                    va="center", ha="right", fontsize=9, color="white", fontweight="bold")

    ax.set_title(f"AgentSkillsHub 七大分类分布 · {d['total']:,} 条 · 2026-04-23 快照",
                 fontsize=13, pad=14)
    ax.set_xlabel("Skill 数量")
    ax.set_xlim(0, max(counts) * 1.18)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    plt.tight_layout()
    out = OUT / "ch06-fig1-category-distribution.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"saved {out}")


def fig2_9x4_matrix():
    types = [
        "1 · Reference",
        "2 · Data Acq",
        "3 · Scaffolding",
        "4 · CI/CD",
        "5 · Code Quality",
        "6 · Documentation",
        "7 · Workflow",
        "8 · Persona",
        "9 · Communication",
    ]
    tiers = ["Personal", "Project", "Team", "Global"]

    # 0 = none, 1 = ✅, 2 = ✅✅ (高频), 3 = ✅✅✅ (主战场), -1 = ⚠️ 不推荐
    matrix = [
        [3, 2, 2, 2],   # Reference
        [1, 2, 1, 3],   # Data Acq
        [1, 3, 2, 1],   # Scaffolding
        [1, 3, 3, 1],   # CI/CD
        [1, 3, 3, 2],   # Code Quality
        [1, 2, 1, -1],  # Documentation
        [1, 2, 2, 1],   # Workflow
        [3, -1, -1, 1], # Persona
        [1, 2, 3, 1],   # Communication
    ]

    fig, ax = plt.subplots(figsize=(10, 7.2), dpi=150)
    color_map = {
        -1: "#fee2e2",  # warning red
         0: "#f1f5f9",  # bg gray
         1: "#dbeafe",  # light blue
         2: "#93c5fd",  # mid blue
         3: "#3b82f6",  # main blue (主战场)
    }
    label_map = {-1: "不推荐", 0: "", 1: "常见", 2: "高频", 3: "主战场"}

    for i, row in enumerate(matrix):
        for j, v in enumerate(row):
            ax.add_patch(plt.Rectangle((j, len(types) - 1 - i), 1, 1,
                                        facecolor=color_map[v], edgecolor="white", linewidth=2))
            text_color = "white" if v == 3 else "#dc2626" if v == -1 else "#1e293b"
            weight = "bold" if v == 3 else "normal"
            ax.text(j + 0.5, len(types) - 1 - i + 0.5, label_map[v],
                    ha="center", va="center", fontsize=11, color=text_color, fontweight=weight)

    ax.set_xticks([j + 0.5 for j in range(len(tiers))])
    ax.set_xticklabels(tiers, fontsize=11)
    ax.set_yticks([len(types) - 1 - i + 0.5 for i in range(len(types))])
    ax.set_yticklabels(types, fontsize=11)
    ax.set_xlim(0, len(tiers))
    ax.set_ylim(0, len(types))
    ax.set_aspect("equal")
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False, length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title("9 种功能类型 × 4 级分享路径 · 哪里是主战场",
                 fontsize=13, pad=24)

    # legend
    legend_handles = [
        mpatches.Patch(color="#3b82f6", label="主战场（最常见）"),
        mpatches.Patch(color="#93c5fd", label="高频"),
        mpatches.Patch(color="#dbeafe", label="常见"),
        mpatches.Patch(color="#fee2e2", label="不推荐"),
    ]
    ax.legend(handles=legend_handles, loc="upper center",
              bbox_to_anchor=(0.5, -0.04), ncol=4, frameon=False, fontsize=10)
    plt.tight_layout()
    out = OUT / "ch06-fig2-9x4-matrix.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"saved {out}")


if __name__ == "__main__":
    fig1_category_distribution()
    fig2_9x4_matrix()
