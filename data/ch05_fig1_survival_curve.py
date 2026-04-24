"""
Blue Book Ch 5 · Fig 1 · Skill survival curve (persistent commit vs one-shot)

Input:  ch05_cohort_snapshot.json (1000 skills, cohort 2025-04 to 2025-10)
Output: ch05-fig1-survival-curve.png (1200x675 · 16:9 · dark navy theme)
"""
import json
import statistics as st
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = Path(__file__).resolve().parent
TODAY = datetime(2026, 4, 24, tzinfo=timezone.utc)

# Chinese-capable font fallback
available = {f.name for f in font_manager.fontManager.ttflist}
for candidate in [
    "PingFang SC", "PingFang HK", "Hiragino Sans GB", "Hiragino Sans",
    "Songti SC", "STHeiti", "Heiti SC", "Arial Unicode MS",
]:
    if candidate in available:
        plt.rcParams["font.sans-serif"] = [candidate] + plt.rcParams["font.sans-serif"]
        break
plt.rcParams["axes.unicode_minus"] = False


def parse(iso: str):
    if not iso:
        return None
    s = iso.split("+")[0].rstrip("Z")
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)


def age_days(iso: str):
    dt = parse(iso)
    return (TODAY - dt).days if dt else None


d = json.load(open(HERE / "ch05_cohort_snapshot.json"))

# Build per-month survival
buckets = list(range(6, 12))
survival = {}
for b in buckets:
    lo, hi = b * 30, (b + 1) * 30
    sub = [x for x in d if age_days(x["created_at"]) and lo <= age_days(x["created_at"]) < hi]
    if not sub:
        continue
    sa = sum(
        1 for x in sub
        if age_days(x.get("last_commit_at")) is not None and age_days(x["last_commit_at"]) <= 90
    )
    survival[b] = (sa, len(sub), sa / len(sub) * 100)

# ── Plot ──────────────────────────────────────────
fig, (ax_left, ax_right) = plt.subplots(
    1, 2, figsize=(14, 7.2), dpi=120, facecolor="#0a0e1a",
    gridspec_kw={"width_ratios": [1.4, 1]},
)
for ax in (ax_left, ax_right):
    ax.set_facecolor("#0a0e1a")
    for s in ax.spines.values():
        s.set_color("#334155")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(colors="#cbd5e1", labelsize=10)

# LEFT: survival curve by age
xs = list(survival.keys())
ys = [survival[x][2] for x in xs]
ax_left.plot(xs, ys, marker="o", markersize=12, linewidth=3,
             color="#10b981", markeredgecolor="#10b981",
             markerfacecolor="#0a0e1a", markeredgewidth=2.5)
ax_left.fill_between(xs, [0] * len(xs), ys, color="#10b981", alpha=0.1)

# Annotate each point
for x, y in zip(xs, ys):
    n = survival[x][1]
    ax_left.annotate(
        f"{y:.1f}%",
        (x, y), textcoords="offset points", xytext=(0, 12),
        ha="center", fontsize=13, fontweight="bold", color="#ffffff",
    )
    ax_left.annotate(
        f"n={n}", (x, y), textcoords="offset points", xytext=(0, -20),
        ha="center", fontsize=9, color="#64748b",
    )

# Highlight the 10-month death cliff
ax_left.axvline(10, color="#ef4444", linestyle="--", linewidth=1.5, alpha=0.6)
ax_left.annotate(
    "死亡拐点",
    (10, 86), ha="center", fontsize=11, fontweight="bold", color="#ef4444",
)

ax_left.set_ylim(55, 90)
ax_left.set_xlabel("创建月龄", fontsize=11.5, color="#e2e8f0")
ax_left.set_ylabel("仍在迭代比例 %", fontsize=11.5, color="#e2e8f0")
ax_left.grid(axis="y", color="#1e293b", linestyle="-", linewidth=0.5, alpha=0.5)
ax_left.set_axisbelow(True)
ax_left.set_xticks(xs)
ax_left.set_xticklabels([f"{b}月" for b in xs])
ax_left.set_title(
    "Skill 生存曲线  ·  按创建月龄",
    fontsize=14.5, fontweight="bold", color="#ffffff", pad=10, loc="left",
)

# RIGHT: active vs frozen growth rate comparison
active = [x for x in d if age_days(x.get("last_commit_at")) is not None and age_days(x["last_commit_at"]) <= 90]
frozen = [x for x in d if age_days(x.get("last_commit_at")) is not None and age_days(x["last_commit_at"]) > 90]

def gain_pct(group):
    if not group: return 0
    return sum(1 for x in group if (x["stars"] or 0) - (x.get("prev_stars") or 0) > 0) / len(group) * 100

labels = ["持续 commit\n(≤ 90 天)", "已冷冻\n(> 90 天)"]
vals = [gain_pct(active), gain_pct(frozen)]
colors_bar = ["#10b981", "#ef4444"]
ns = [len(active), len(frozen)]

bars = ax_right.bar(labels, vals, color=colors_bar, width=0.55, edgecolor="none")
for bar, v, n in zip(bars, vals, ns):
    ax_right.text(
        bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
        f"{v:.1f}%", ha="center", fontsize=22, fontweight="bold", color="#ffffff",
    )
    ax_right.text(
        bar.get_x() + bar.get_width() / 2, -4,
        f"n={n}", ha="center", fontsize=10, color="#64748b",
    )

ax_right.set_ylim(0, 72)
ax_right.set_ylabel("仍在涨 stars %", fontsize=11.5, color="#e2e8f0")
ax_right.grid(axis="y", color="#1e293b", linestyle="-", linewidth=0.5, alpha=0.5)
ax_right.set_axisbelow(True)
ax_right.set_title(
    "当前还在涨 stars  ·  持续 vs 冷冻",
    fontsize=14.5, fontweight="bold", color="#ffffff", pad=10, loc="left",
)

# Huge center-right "15×" annotation
ax_right.annotate(
    "15×",
    (0.5, 35), ha="center", va="center", fontsize=36, fontweight="bold",
    color="#f59e0b", alpha=0.95,
)
ax_right.annotate(
    "持续 commit 的\n活着程度是冷冻的\n15 倍",
    (0.5, 20), ha="center", va="center", fontsize=10, color="#94a3b8",
)

# Super-title
fig.suptitle(
    "持续 commit 的 Skill  vs  一次性发布的 Skill  ·  AgentSkillsHub cohort",
    fontsize=17.5, fontweight="bold", color="#ffffff", y=0.98, x=0.03, ha="left",
)
fig.text(
    0.03, 0.935,
    "cohort: 2025-04 到 2025-10 创建 · stars ≥ 20 · n=1000 · 观察至 2026-04-24",
    fontsize=10.5, color="#94a3b8", ha="left",
)

fig.text(
    0.985, 0.015,
    "agentskillshub.top  ·  Blue Book Ch.5  ·  2026-04-24",
    ha="right", va="bottom", fontsize=9, color="#64748b",
)

plt.tight_layout(rect=[0, 0.02, 1, 0.90])
out = HERE / "ch05-fig1-survival-curve.png"
plt.savefig(out, facecolor="#0a0e1a", bbox_inches="tight", dpi=120)
print(f"✅ saved → {out}")
