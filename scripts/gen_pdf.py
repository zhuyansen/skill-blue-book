#!/usr/bin/env python3
"""
Generate Skill 蓝皮书 2026 v1.0 PDF.

Pipeline:
  1. Concatenate all 12 chapter MDs into a single HTML
  2. Apply print-friendly CSS + cover page + TOC
  3. Headless Chrome → PDF

No external Python deps — uses minimal regex-based MD→HTML.
"""
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_HTML = ROOT / "_book.html"
OUT_PDF = ROOT / "skill-blue-book-2026-v1.0.pdf"
COVER = ROOT / "assets" / "cover.png"

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CHAPTERS = [
    ("part1-foundation", "ch01-mahesh-to-barry.md", 1, "Part 1 · 基础"),
    ("part1-foundation", "ch02-three-layer-loading.md", 2, "Part 1 · 基础"),
    ("part1-foundation", "ch03-market-landscape.md", 3, "Part 1 · 基础"),
    ("part2-practice", "ch04-baoyu-four-principles.md", 4, "Part 2 · 实战"),
    ("part2-practice", "ch05-iteration-loop.md", 5, "Part 2 · 实战"),
    ("part2-practice", "ch06-types-and-tiers.md", 6, "Part 2 · 实战"),
    ("part3-ecosystem", "ch07-four-frameworks.md", 7, "Part 3 · 生态"),
    ("part3-ecosystem", "ch08-skill-eats-pillars.md", 8, "Part 3 · 生态"),
    ("part3-ecosystem", "ch09-distribution-fourth-edge.md", 9, "Part 3 · 生态"),
    ("part4-hub", "ch10-verified-creator.md", 10, "Part 4 · Hub 实操"),
    ("part4-hub", "ch11-consulting-and-enterprise.md", 11, "Part 4 · Hub 实操"),
    ("part4-hub", "ch12-when-claude-writes-skills.md", 12, "Part 4 · Hub 实操"),
]

APPENDICES = [
    ("appendix", "A-skill-design-cheatsheet.md", "A", "附录 · 速查表"),
    ("appendix", "B-hub-user-guide.md", "B", "附录 · Hub 指南"),
    ("appendix", "C-verified-creator-application.md", "C", "附录 · Verified 申请"),
    ("appendix", "D-references-and-reading.md", "D", "附录 · 参考文献"),
]


def esc(s):
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def strip_frontmatter(md):
    if md.startswith("---"):
        end = md.find("\n---", 3)
        if end > 0:
            return md[end + 4 :].lstrip()
    return md


def inline(line):
    """Apply inline markdown: bold, italic, code, links, images."""
    # Images first (they look like links)
    line = re.sub(
        r"!\[([^\]]*)\]\(([^)]+)\)",
        lambda m: f'<img src="{img_src(m.group(2))}" alt="{esc(m.group(1))}" />',
        line,
    )
    # Links
    line = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: f'<a href="{esc(m.group(2))}">{esc(m.group(1))}</a>',
        line,
    )
    # Inline code
    line = re.sub(r"`([^`]+)`", lambda m: f"<code>{esc(m.group(1))}</code>", line)
    # Bold
    line = re.sub(r"\*\*([^*]+)\*\*", lambda m: f"<strong>{m.group(1)}</strong>", line)
    # Italic
    line = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", lambda m: f"<em>{m.group(1)}</em>", line)
    return line


def img_src(src):
    """Resolve image path. /book/assets/foo.png → file:// path."""
    if src.startswith("/book/assets/"):
        p = ROOT / "data" / src.replace("/book/assets/", "")
        if not p.exists():
            p = ROOT / "assets" / src.replace("/book/assets/", "")
        return f"file://{p}"
    return src


def md_to_html(md):
    md = strip_frontmatter(md)
    lines = md.split("\n")
    out = []
    in_code = False
    code_buf = []
    in_list = False
    list_type = None
    in_table = False
    table_buf = []

    def flush_list():
        nonlocal in_list, list_type
        if in_list:
            out.append(f"</{list_type}>")
            in_list = False
            list_type = None

    def flush_table():
        nonlocal in_table, table_buf
        if not in_table:
            return
        # First row = header, second = separator, rest = body
        rows = [r.strip("|").split("|") for r in table_buf]
        rows = [[c.strip() for c in r] for r in rows]
        out.append("<table>")
        if len(rows) >= 2:
            out.append("<thead><tr>")
            for c in rows[0]:
                out.append(f"<th>{inline(esc(c))}</th>")
            out.append("</tr></thead>")
            out.append("<tbody>")
            for r in rows[2:]:
                out.append("<tr>")
                for c in r:
                    out.append(f"<td>{inline(esc(c))}</td>")
                out.append("</tr>")
            out.append("</tbody>")
        out.append("</table>")
        in_table = False
        table_buf = []

    for raw in lines:
        line = raw.rstrip()

        # Code fences
        if line.startswith("```"):
            if in_code:
                code = "\n".join(code_buf)
                out.append(f"<pre><code>{esc(code)}</code></pre>")
                code_buf = []
                in_code = False
            else:
                flush_list()
                flush_table()
                in_code = True
            continue
        if in_code:
            code_buf.append(line)
            continue

        # Tables (line starts/ends with |)
        if line.startswith("|") and line.endswith("|"):
            flush_list()
            in_table = True
            table_buf.append(line)
            continue
        elif in_table:
            flush_table()

        # Headings
        h = re.match(r"^(#{1,6})\s+(.+)$", line)
        if h:
            flush_list()
            level = len(h.group(1))
            text = inline(esc(h.group(2)))
            out.append(f"<h{level}>{text}</h{level}>")
            continue

        # Lists
        ul = re.match(r"^[-*]\s+(.+)$", line)
        ol = re.match(r"^\d+\.\s+(.+)$", line)
        if ul or ol:
            tp = "ul" if ul else "ol"
            if not in_list or list_type != tp:
                flush_list()
                out.append(f"<{tp}>")
                in_list = True
                list_type = tp
            out.append(f"<li>{inline(esc((ul or ol).group(1)))}</li>")
            continue

        # Blockquote
        if line.startswith("> "):
            flush_list()
            out.append(f"<blockquote>{inline(esc(line[2:]))}</blockquote>")
            continue
        if line.strip() == ">":
            flush_list()
            continue

        # Horizontal rule
        if re.match(r"^---+\s*$", line):
            flush_list()
            out.append("<hr/>")
            continue

        # Empty
        if line.strip() == "":
            flush_list()
            continue

        flush_list()
        out.append(f"<p>{inline(esc(line))}</p>")

    flush_list()
    flush_table()
    if in_code and code_buf:
        out.append(f"<pre><code>{esc(chr(10).join(code_buf))}</code></pre>")

    return "\n".join(out)


CSS = """
@page {
  size: A4;
  margin: 22mm 18mm 22mm 18mm;
  @top-right {
    content: "Skill 蓝皮书 2026 · Jason Zhu";
    font-size: 9pt;
    color: #94a3b8;
    font-family: "PingFang SC", "Heiti SC", sans-serif;
  }
  @bottom-center {
    content: counter(page);
    font-size: 9pt;
    color: #94a3b8;
  }
}
@page :first {
  margin: 0;
  @top-right { content: none; }
  @bottom-center { content: none; }
}
* { box-sizing: border-box; }
html, body {
  margin: 0;
  padding: 0;
  font-family: "PingFang SC", "Hiragino Sans GB", "Heiti SC", "Microsoft YaHei", sans-serif;
  font-size: 10.5pt;
  line-height: 1.7;
  color: #1e293b;
  -webkit-font-smoothing: antialiased;
}
.cover {
  page: cover;
  page-break-after: always;
  height: 297mm;
  width: 210mm;
  background: linear-gradient(135deg, #1a1f3a 0%, #0a0e1a 100%);
  color: white;
  padding: 60mm 25mm;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.cover h1 {
  font-size: 56pt;
  margin: 0;
  letter-spacing: -0.02em;
  color: white;
  border: none;
  padding: 0;
}
.cover .subtitle {
  font-size: 18pt;
  color: #4a9eff;
  margin: 8pt 0;
}
.cover .meta { color: #8aa4c8; font-size: 11pt; margin-top: 30pt; }
.cover .meta strong { color: white; font-weight: 600; }
.cover .footer {
  font-size: 10pt;
  color: #6b7c9a;
  border-top: 1px solid #2d3548;
  padding-top: 12pt;
}
.toc {
  page-break-after: always;
  padding: 0 4mm;
}
.toc h1 { color: #4f46e5; border-bottom: 2px solid #e2e8f0; padding-bottom: 8pt; }
.toc ul { list-style: none; padding: 0; }
.toc li {
  padding: 8pt 0;
  border-bottom: 1px dotted #cbd5e1;
  display: flex;
  justify-content: space-between;
  font-size: 11pt;
}
.toc .num { color: #4f46e5; font-weight: 600; min-width: 60pt; display: inline-block; }
.toc .title { flex: 1; color: #1e293b; }
.toc .part { color: #94a3b8; font-size: 9pt; margin-left: 8pt; }
.chapter {
  page-break-before: always;
  padding: 0 4mm;
}
.chapter-meta {
  font-size: 9pt;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0 0 8pt;
}
h1 {
  font-size: 22pt;
  margin: 12pt 0 8pt;
  color: #0f172a;
  border-bottom: 2px solid #4f46e5;
  padding-bottom: 6pt;
  letter-spacing: -0.01em;
}
h2 {
  font-size: 14pt;
  margin: 18pt 0 6pt;
  color: #0f172a;
  border-top: 1px solid #e2e8f0;
  padding-top: 10pt;
  page-break-after: avoid;
}
h3 {
  font-size: 12pt;
  margin: 12pt 0 4pt;
  color: #1e293b;
  page-break-after: avoid;
}
h4 { font-size: 11pt; margin: 10pt 0 4pt; color: #334155; }
p { margin: 0 0 8pt; orphans: 2; widows: 2; }
strong { color: #0f172a; font-weight: 600; }
a { color: #4f46e5; text-decoration: underline; text-underline-offset: 2pt; }
ul, ol { margin: 6pt 0; padding-left: 18pt; }
li { margin: 3pt 0; }
blockquote {
  margin: 10pt 0;
  padding: 6pt 12pt;
  border-left: 3pt solid #4f46e5;
  background: #f8fafc;
  color: #475569;
  font-style: italic;
  page-break-inside: avoid;
}
code {
  background: #f1f5f9;
  color: #1e293b;
  padding: 1pt 4pt;
  border-radius: 3pt;
  font-size: 9.5pt;
  font-family: "SF Mono", Menlo, "Courier New", monospace;
}
pre {
  margin: 10pt 0;
  padding: 10pt 12pt;
  background: #0f172a;
  color: #e2e8f0;
  border-radius: 6pt;
  overflow-x: auto;
  font-size: 8.5pt;
  line-height: 1.5;
  page-break-inside: avoid;
}
pre code {
  background: transparent;
  color: inherit;
  padding: 0;
  font-size: inherit;
}
img {
  max-width: 100%;
  height: auto;
  margin: 10pt auto;
  display: block;
  border: 1px solid #e2e8f0;
  border-radius: 4pt;
  page-break-inside: avoid;
}
table {
  margin: 10pt 0;
  border-collapse: collapse;
  width: 100%;
  font-size: 9.5pt;
  page-break-inside: avoid;
}
th, td {
  border: 1px solid #cbd5e1;
  padding: 4pt 8pt;
  text-align: left;
  vertical-align: top;
}
th { background: #f1f5f9; font-weight: 600; color: #0f172a; }
hr { margin: 16pt 0; border: 0; border-top: 1px solid #e2e8f0; }
"""


def build_html():
    cover_uri = f"file://{COVER}" if COVER.exists() else ""
    parts = [
        "<!doctype html><html lang='zh-CN'><head>",
        "<meta charset='utf-8'/>",
        "<title>Skill 蓝皮书 2026 · v1.0</title>",
        f"<style>{CSS}</style>",
        "</head><body>",
        # Cover
        "<section class='cover'>",
        "<div>",
        "<div style='font-size:11pt;color:#4a9eff;letter-spacing:0.1em;margin-bottom:30pt;'>AGENTSKILLSHUB · BLUE BOOK OF AGENT SKILLS</div>",
        "<h1>Skill 蓝皮书</h1>",
        "<div class='subtitle'>2026 · v1.0</div>",
        "<p style='color:#cbd5e1;font-size:13pt;line-height:1.7;margin-top:30pt;max-width:140mm;'>"
        "基于 AgentSkillsHub 67,000+ 真实 Skill 数据的原生研究——"
        "不是再写一遍 Anthropic 已经讲过的 Skill Spec，是去回答没人答过的问题："
        "现在的 Skill 生态长什么样、谁活下来了、谁要饿死。</p>",
        "</div>",
        "<div class='footer'>",
        "<div class='meta' style='display:flex;gap:30pt;flex-wrap:wrap;'>",
        "<div><strong>67,196</strong><br/>Skills</div>",
        "<div><strong>0.983</strong><br/>Gini 系数</div>",
        "<div><strong>54.1%</strong><br/>0 star 比例</div>",
        "<div><strong>~70K 字</strong><br/>12 章</div>",
        "</div>",
        "<div style='margin-top:18pt;'>Jason Zhu (@GoSailGlobal) · 2026-04-28<br/>"
        "<span style='color:#6b7c9a;'>github.com/zhuyansen/skill-blue-book · agentskillshub.top/book/</span><br/>"
        "<span style='color:#6b7c9a;'>CC BY-NC-SA 4.0</span>"
        "</div>",
        "</div>",
        "</section>",
        # TOC
        "<section class='toc'>",
        "<h1>目录</h1>",
        "<ul>",
    ]

    def chapter_title(content, num):
        # Try YAML frontmatter title (with · separator)
        m = re.search(r"^title:\s*第\s*\d+\s*章\s*[·｜:\-]\s*(.+)$", content, re.M)
        if m:
            return m.group(1).strip().rstrip("·｜")
        # Fallback to first H1 with same pattern
        m = re.search(r"^#\s*第\s*\d+\s*章\s*[·｜:\-]\s*(.+)$", content, re.M)
        if m:
            return m.group(1).strip().rstrip("·｜")
        return f"Chapter {num}"

    for d, f, num, part in CHAPTERS:
        content = (ROOT / d / f).read_text()
        title = chapter_title(content, num)
        parts.append(
            f"<li><span><span class='num'>第 {num} 章</span>"
            f"<span class='title'>{esc(title)}</span></span>"
            f"<span class='part'>{esc(part)}</span></li>"
        )
    parts.append("</ul></section>")

    # Each chapter
    for d, f, num, part in CHAPTERS:
        md = (ROOT / d / f).read_text()
        body_html = md_to_html(md)
        parts.append(
            f"<section class='chapter'>"
            f"<p class='chapter-meta'>{esc(part)} · 第 {num} 章</p>"
            f"{body_html}"
            f"</section>"
        )

    # Appendices
    for d, f, letter, part in APPENDICES:
        md = (ROOT / d / f).read_text()
        body_html = md_to_html(md)
        parts.append(
            f"<section class='chapter'>"
            f"<p class='chapter-meta'>{esc(part)} · {letter}</p>"
            f"{body_html}"
            f"</section>"
        )

    parts.append("</body></html>")
    return "\n".join(parts)


def main():
    print(f"Building HTML → {OUT_HTML}")
    html = build_html()
    OUT_HTML.write_text(html)
    print(f"  HTML size: {len(html) // 1024} KB")

    print(f"Rendering PDF via headless Chrome → {OUT_PDF}")
    if OUT_PDF.exists():
        OUT_PDF.unlink()
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={OUT_PDF}",
        "--virtual-time-budget=10000",
        f"file://{OUT_HTML}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print("Chrome stderr:", result.stderr[:500], file=sys.stderr)
        sys.exit(1)
    if not OUT_PDF.exists():
        print("PDF not produced", file=sys.stderr)
        sys.exit(1)
    size_mb = OUT_PDF.stat().st_size / 1024 / 1024
    print(f"  ✓ PDF saved → {OUT_PDF} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
