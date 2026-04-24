#!/usr/bin/env python3
"""
Generate Tweet 1 / 4 / 6 companion images for Chapter 1 X Thread
via apimart gpt-image-2.
"""
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

API_BASE = "https://api.apimart.ai/v1"
TOKEN = os.environ.get("APIMART_KEY") or sys.exit("Set APIMART_KEY env var")
OUT_DIR = Path(__file__).resolve().parent.parent / "social"
OUT_DIR.mkdir(parents=True, exist_ok=True)


UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"


def submit(prompt: str, size: str = "1:1") -> str:
    req = urllib.request.Request(
        f"{API_BASE}/images/generations",
        data=json.dumps(
            {"model": "gpt-image-2", "prompt": prompt, "n": 1, "size": size}
        ).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": UA,
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        body = json.loads(r.read().decode())
    if body.get("code") != 200:
        raise RuntimeError(f"submit failed: {body}")
    return body["data"][0]["task_id"]


def poll(task_id: str, max_wait: int = 300) -> str:
    """Return image URL once task completes."""
    waited = 0
    while waited < max_wait:
        req = urllib.request.Request(
            f"{API_BASE}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {TOKEN}", "User-Agent": UA},
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            body = json.loads(r.read().decode())
        data = body.get("data", {})
        status = data.get("status")
        if status == "completed":
            imgs = data["result"]["images"]
            url = imgs[0]["url"]
            return url[0] if isinstance(url, list) else url
        if status == "failed":
            raise RuntimeError(f"task {task_id} failed: {body}")
        time.sleep(5)
        waited += 5
    raise TimeoutError(f"task {task_id} exceeded {max_wait}s")


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        dest.write_bytes(r.read())


def generate(name: str, prompt: str, size: str = "1:1") -> Path:
    out = OUT_DIR / f"{name}.png"
    print(f"[{name}] submitting...")
    task_id = submit(prompt, size=size)
    print(f"[{name}] task={task_id}, polling...")
    url = poll(task_id)
    print(f"[{name}] done, downloading from {url[:80]}...")
    download(url, out)
    print(f"[{name}] saved → {out} ({out.stat().st_size // 1024} KB)")
    return out


# ─── Prompts ───────────────────────────────────────────────────────

TWEET1 = """Editorial split-screen comparison illustration, 1:1 square, deep navy blue background (#1a1f3a to #0a0e1a gradient).

Top center large white text: "Who Would You Hire?"

Left half: A young Asian man in his mid-20s wearing a lab coat and glasses, standing in front of a math equations blackboard, holding a thick textbook. Below him, a clean text block in light blue (#4a9eff):
MAHESH
— MIT PhD in Mathematics
— IQ 150
— Fresh graduate, 0 experience

Right half: A wise older man in his late 50s with grey hair, wearing a cardigan, sitting at a wooden desk covered with accounting ledgers, tax forms, a vintage calculator, and a coffee mug. Warm desk lamp light. Below him, same clean text block in warm amber (#ff9f40):
BARRY
— Community College
— 30 years of accounting
— Thousands of real clients

Bottom-center small tag in faded white text: "AgentSkillsHub · Blue Book of Agent Skills · Chapter 1"

Clean editorial design, magazine-quality illustration, no extra decorations.
"""

TWEET4 = """Clean infographic donut chart, 1:1 square composition, deep navy blue background (#0a0e1a to #1a1f3a gradient).

Top title in large bold white sans-serif: "Barry's 30 Years of Experience"
Subtitle below in smaller muted blue (#8aa4c8): "What's actually transferable to a Skill file?"

Central donut chart (large, takes up 60% of canvas):
- 65% arc in vibrant orange (#ff9f40), labeled inside the arc: "65% WRITABLE" in bold white caps, with smaller caption below: "Rules · Checklists · Procedures · Edge cases"
- 35% arc in cool purple (#8b5cf6), labeled: "35% INTUITION" in bold white caps, with smaller caption: "Gut feeling · Client reading · Pattern sense"

Below the chart, one-line takeaway in light white text: "Today's AI has zero of both. Skills transfer the 65% first."

Bottom-right small corner tag: "AgentSkillsHub · Blue Book 2026"

Minimal, clean, data-journalism style, high contrast, no extra clutter.
"""

TWEET6 = """Clean comparison infographic, 1:1 square canvas, deep navy blue gradient background (#0a0e1a top to #1a1f3a bottom).

Top bold white title: "5 Ways to Extend an AI Agent"
Subtitle in muted blue: "Only one teaches it how to DO the job"

Five vertical columns arranged horizontally, each with a circular icon on top and two text lines below:

Column 1 — Icon: silhouette of a person's head in blue (#4a9eff). Label bold white: "SYSTEM PROMPT". Caption muted blue: "Permanent persona"

Column 2 — Icon: robotic arm/limb in blue. Label: "TOOL". Caption: "Limbs (what to do)"

Column 3 — Icon: two connected hands in blue. Label: "MCP". Caption: "Remote limbs"

Column 4 — Icon: encyclopedia book in blue. Label: "RAG". Caption: "Facts on demand"

Column 5 (HIGHLIGHTED) — Icon: open notebook with a pencil in vibrant orange (#ff9f40), with subtle glow. Label in orange: "SKILL". Caption in orange: "Coach's playbook"

A thin orange arrow or underline pointing specifically to column 5.

Below all columns, bottom banner in light white text: "The scarcest piece? The coach's playbook."

Bottom-right small corner: "AgentSkillsHub · Blue Book of Agent Skills"

Flat modern design, editorial quality, minimal decoration, high information density.
"""


def main():
    configs = [
        ("ch01-fig1-mahesh-vs-barry", TWEET1),
        ("ch01-fig2-barry-experience-pie", TWEET4),
        ("ch01-fig3-five-extensions", TWEET6),
    ]
    results = []
    for name, prompt in configs:
        try:
            path = generate(name, prompt)
            results.append((name, str(path), "ok"))
        except Exception as e:
            print(f"[{name}] FAILED: {e}", file=sys.stderr)
            results.append((name, "", f"fail: {e}"))
    print("\n=== SUMMARY ===")
    for name, path, status in results:
        print(f"{status:8s}  {name:40s}  {path}")


if __name__ == "__main__":
    main()
