#!/usr/bin/env python3
"""Generate clean standalone HTML viewer pages for each StageAI .md file."""
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
BACK_HREF = "StageAI GTM Strategy — founder report.html"

FILES = [
    "StageAI Roadmap.md",
    "POV — how to build (Strategic POV framework).md",
    "GTM — finance-first motion (strategy & prep).md",
    "Vuzix — POV and business case (illustration).md",
    "POV — finance-first outbound (enterprise wearables).md",
    "Diagram — ML workflow classic vs Stage AI.md",
    "ICP use cases — Reddit-style stories.md",
    "Stage AI — understanding brief.md",
]

STYLE = """
:root {
  --bg: #fafaf9;
  --ink: #1a1a1a;
  --ink-2: #374151;
  --muted: #6b7280;
  --line: #e5e7eb;
  --accent: #1e40af;
  --accent-bg: #eff6ff;
  --code-bg: #f3f4f6;
  --warn: #d97706;
}
* { box-sizing: border-box; }
html { -webkit-font-smoothing: antialiased; }
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: var(--bg);
  color: var(--ink);
  line-height: 1.7;
  margin: 0;
  padding: 0;
  font-size: 15px;
}
.topbar {
  background: var(--accent);
  color: white;
  padding: 11px 28px;
  display: flex;
  align-items: center;
  gap: 14px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 6px rgba(0,0,0,0.12);
}
.topbar a {
  color: rgba(255,255,255,0.85);
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  transition: color 0.15s;
}
.topbar a:hover { color: white; }
.topbar .sep { color: rgba(255,255,255,0.3); }
.topbar .doc-title {
  font-size: 13px;
  font-weight: 600;
  color: rgba(255,255,255,0.92);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.content {
  max-width: 740px;
  margin: 0 auto;
  padding: 48px 28px 96px;
}
.content h1 {
  font-size: 26px;
  font-weight: 700;
  letter-spacing: -0.4px;
  line-height: 1.25;
  margin: 0 0 10px;
  color: var(--ink);
}
.content h2 {
  font-size: 19px;
  font-weight: 700;
  margin: 44px 0 12px;
  color: var(--ink);
  padding-bottom: 8px;
  border-bottom: 2px solid var(--line);
}
.content h3 {
  font-size: 15px;
  font-weight: 700;
  margin: 30px 0 8px;
  color: var(--ink);
}
.content h4 {
  font-size: 13px;
  font-weight: 700;
  margin: 20px 0 6px;
  color: var(--ink-2);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.content p { margin: 0 0 14px; color: var(--ink-2); }
.content ul, .content ol {
  margin: 0 0 14px;
  padding-left: 22px;
  color: var(--ink-2);
}
.content li { margin: 6px 0; }
.content strong { color: var(--ink); font-weight: 700; }
.content em { font-style: italic; color: var(--ink-2); }
.content a { color: var(--accent); }
.content hr {
  border: none;
  border-top: 1px solid var(--line);
  margin: 36px 0;
}
.content blockquote {
  border-left: 3px solid var(--accent);
  margin: 16px 0;
  padding: 10px 16px;
  background: var(--accent-bg);
  border-radius: 0 6px 6px 0;
  color: var(--ink-2);
  font-style: italic;
}
.content blockquote p { margin: 0; }
.content code {
  background: var(--code-bg);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'SF Mono', Menlo, Consolas, monospace;
  font-size: 0.86em;
  color: #be185d;
}
.content pre {
  background: #1e293b;
  color: #e2e8f0;
  padding: 18px 22px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 16px 0;
  font-size: 13px;
  line-height: 1.6;
}
.content pre code { background: none; padding: 0; color: inherit; font-size: inherit; }
.content table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
  font-size: 13.5px;
}
.content th {
  background: var(--accent);
  color: white;
  padding: 9px 13px;
  text-align: left;
  font-weight: 600;
  font-size: 11.5px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.content td {
  padding: 8px 13px;
  border-bottom: 1px solid var(--line);
  color: var(--ink-2);
  vertical-align: top;
}
.content tr:nth-child(even) td { background: var(--accent-bg); }
.content .mermaid {
  background: white;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 24px;
  margin: 20px 0;
  text-align: center;
  overflow-x: auto;
}
@media (max-width: 600px) {
  .content { padding: 24px 16px 60px; }
  .topbar { padding: 10px 14px; }
  .content h1 { font-size: 20px; }
  .content h2 { font-size: 16px; }
}
"""

TEMPLATE = """\
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
{style}
</style>
</head>
<body>

<div class="topbar">
  <a href="{back_href}">← Назад</a>
  <span class="sep">|</span>
  <span class="doc-title">{title}</span>
</div>

<div class="content" id="content"></div>

<script src="https://cdn.jsdelivr.net/npm/marked@4/marked.min.js"></script>
{mermaid_include}
<script>
{mermaid_setup}
const md = {content_json};
const renderer = new marked.Renderer();
let mc = 0;
renderer.code = function(code, lang) {{
  if (lang === 'mermaid') {{
    return '<div class="mermaid" id="m' + (++mc) + '">' + code + '</div>';
  }}
  return '<pre><code>' + code.replace(/</g,'&lt;').replace(/>/g,'&gt;') + '</code></pre>';
}};
marked.use({{ renderer }});
document.getElementById('content').innerHTML = marked.parse(md);
{mermaid_run}
</script>
</body>
</html>
"""

MERMAID_INCLUDE = '<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>'
MERMAID_SETUP = """mermaid.initialize({
  startOnLoad: false,
  theme: 'base',
  themeVariables: {
    primaryColor: '#eff6ff',
    primaryBorderColor: '#1e40af',
    primaryTextColor: '#1a1a1a',
    lineColor: '#6b7280',
    fontSize: '13px'
  }
});
"""
MERMAID_RUN = "mermaid.run({ querySelector: '.mermaid' });"


def has_mermaid(text):
    return '```mermaid' in text or '~~~mermaid' in text


def md_to_html_filename(md_name):
    return os.path.splitext(md_name)[0] + ".html"


def make_title(md_name):
    return os.path.splitext(md_name)[0]


def generate(md_filename):
    src = os.path.join(BASE, md_filename)
    with open(src, encoding='utf-8') as f:
        text = f.read()

    use_mermaid = has_mermaid(text)
    content_json = json.dumps(text)
    title = make_title(md_filename)
    html_filename = md_to_html_filename(md_filename)

    html = TEMPLATE.format(
        title=title,
        style=STYLE,
        back_href=BACK_HREF,
        mermaid_include=MERMAID_INCLUDE if use_mermaid else '',
        mermaid_setup=MERMAID_SETUP if use_mermaid else '',
        mermaid_run=MERMAID_RUN if use_mermaid else '',
        content_json=content_json,
    )

    dest = os.path.join(BASE, html_filename)
    with open(dest, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  ✓  {html_filename}")


if __name__ == '__main__':
    print("Generating HTML doc pages…")
    for fname in FILES:
        generate(fname)
    print("Done.")
