#!/usr/bin/env python3
"""
build.py — Build the Sentrava C2 documentation site.

Reads Markdown files from content/, converts them to HTML, injects each
into template.html, and writes the result to dist/.

Usage:
    pip install markdown pygments --break-system-packages
    python3 build.py

This script is idempotent: running it multiple times produces the same output.
"""

import os
import re
import sys

try:
    import markdown
except ImportError:
    print(
        "ERROR: 'markdown' package not found.\n"
        "Install it with: pip install markdown pygments --break-system-packages",
        file=sys.stderr,
    )
    sys.exit(1)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(SCRIPT_DIR, "content")
DIST_DIR = os.path.join(SCRIPT_DIR, "dist")
TEMPLATE_PATH = os.path.join(SCRIPT_DIR, "template.html")

MD_EXTENSIONS = ["fenced_code", "tables", "toc"]


def parse_frontmatter(text):
    """Parse simple YAML-like frontmatter delimited by ---. Returns (meta dict, body str)."""
    meta = {}
    if not text.startswith("---"):
        return meta, text
    end = text.find("\n---", 3)
    if end == -1:
        return meta, text
    front = text[3:end].strip()
    body = text[end + 4:].lstrip("\n")
    for line in front.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip()
    return meta, body


def wrap_code_blocks(html):
    """Wrap bare <pre><code> blocks in a .code-block div with a copy button toolbar."""

    def _wrap(lang, code):
        label = lang if lang not in ("", "text") else "code"
        return (
            f'<div class="code-block">'
            f'<div class="code-toolbar">'
            f'<span>{label}</span>'
            f'<button class="copy-button" type="button" data-copy aria-label="Copy {label}">Copy</button>'
            f'</div>'
            f'<pre><code class="language-{lang if lang else "text"}">{code}</code></pre>'
            f'</div>'
        )

    # fenced_code with a language tag
    html = re.sub(
        r'<pre><code class="language-(\w+)">(.*?)</code></pre>',
        lambda m: _wrap(m.group(1), m.group(2)),
        html,
        flags=re.DOTALL,
    )
    # plain <pre><code> (no class)
    html = re.sub(
        r'<pre><code>(.*?)</code></pre>',
        lambda m: _wrap("text", m.group(1)),
        html,
        flags=re.DOTALL,
    )
    return html


def wrap_tables(html):
    """Wrap <table> elements in a scrollable container."""
    html = re.sub(
        r'<table>',
        '<div class="table-scroll" role="region" tabindex="0"><table>',
        html,
    )
    html = html.replace('</table>', '</table></div>')
    return html


def make_breadcrumb(category, title):
    home = '<a href="../index.html">Home</a><span aria-hidden="true">/</span>'
    if category:
        return f'{home}<span>{category}</span><span aria-hidden="true">/</span><span>{title}</span>'
    return f'{home}<span>{title}</span>'


def build():
    os.makedirs(DIST_DIR, exist_ok=True)

    if not os.path.isfile(TEMPLATE_PATH):
        print(f"ERROR: template not found at {TEMPLATE_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        template = f.read()

    if not os.path.isdir(CONTENT_DIR):
        print(f"ERROR: content directory not found at {CONTENT_DIR}", file=sys.stderr)
        sys.exit(1)

    pages = sorted(f for f in os.listdir(CONTENT_DIR) if f.endswith(".md"))
    if not pages:
        print("WARNING: no .md files found in content/", file=sys.stderr)
        return

    md = markdown.Markdown(extensions=MD_EXTENSIONS)
    built = 0

    for filename in pages:
        slug = filename[:-3]
        src = os.path.join(CONTENT_DIR, filename)
        dst = os.path.join(DIST_DIR, slug + ".html")

        with open(src, encoding="utf-8") as f:
            raw = f.read()

        meta, body = parse_frontmatter(raw)
        title = meta.get("title", slug.replace("-", " ").title())
        category = meta.get("category", "")

        md.reset()
        content_html = md.convert(body)
        content_html = wrap_code_blocks(content_html)
        content_html = wrap_tables(content_html)

        breadcrumb = make_breadcrumb(category, title)

        page_html = template
        page_html = page_html.replace("{{TITLE}}", title)
        page_html = page_html.replace("{{BREADCRUMB}}", breadcrumb)
        page_html = page_html.replace("{{CONTENT}}", content_html)

        # Mark the active sidebar link for this page
        page_html = page_html.replace(
            f'href="{slug}.html"',
            f'href="{slug}.html" aria-current="page"',
        )

        with open(dst, "w", encoding="utf-8") as f:
            f.write(page_html)

        print(f"  built  dist/{slug}.html  [{title}]")
        built += 1

    print(f"\n{built} pages written to dist/")


if __name__ == "__main__":
    build()
