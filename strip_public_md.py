#!/usr/bin/env python3
"""Strip internal headers and markdown file links from published StageAI .md files."""
import re
import sys

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

HEADER_PATTERNS = (
    r"^\*\*Для:\*\*.*\n"
    r"(\*\*Motion:\*\*.*\n)?"
    r"(\*\*ICP:\*\*.*\n)?"
    r"(\*\*Тикер:\*\*.*\n)?"
    r"(\*\*Методология.*\n)?"
    r"(\*\*StageAI.*\n)?"
    r"(\*\*Связанные документы:\*\*.*\n)?"
    r"(\*\*Founder-ready:\*\*.*\n)?"
    r"(\*\*Структура sprint.*\n)?"
    r"(\*\*Контекст:\*\*.*\n)?"
    r"(\*\*Канонический.*\n)?"
    r"(\*\*StageAI-контекст:\*\*.*\n)?"
    r"(\*\*Связь:\*\*.*\n)?"
    r"(\*\*Шаблон-аккаунт:\*\*.*\n)?"
    r"(\*\*Дата:\*\*.*\n)?"
    r"(\*\*Роль документа:\*\*.*\n)?"
    r"(\*\*Язык:\*\*.*\n)?"
    r"(\*\*Собрано из:\*\*.*\n)?"
    r"(> .*\n)*"
    r"(\*\*Содержание:\*\*.*\n)?"
    r"(\n---\n)?"
)

LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")


def strip_header(text: str) -> str:
    lines = text.splitlines(keepends=True)
    if not lines:
        return text
    i = 1  # after # title line
    while i < len(lines):
        line = lines[i]
        if line.strip() == "---":
            i += 1
            break
        if re.match(
            r"^\*\*(Для|Motion|ICP|Тикер|Методология|StageAI|Связанные|Founder-ready|"
            r"Структура|Контекст|Канонический|Связь|Шаблон|Дата|Роль|Язык|Собрано|Содержание):",
            line,
        ):
            i += 1
            continue
        if line.startswith("> "):
            i += 1
            continue
        if line.strip() == "":
            i += 1
            continue
        break
    if i < len(lines) and lines[i].strip() == "---":
        i += 1
    return lines[0] + "".join(lines[i:])


def strip_links(text: str) -> str:
    return LINK_RE.sub(r"\1", text)


def drop_related_sections(text: str) -> str:
    """Remove trailing ## Related / ## 10. Related reading blocks."""
    for marker in (
        "\n## 10. Related reading",
        "\n## Related reading",
        "\n## Related",
        "\n## 11. Related",
    ):
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx].rstrip() + "\n"
    return text


def process(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = strip_header(text)
    text = strip_links(text)
    text = drop_related_sections(text)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"  stripped {path}")


if __name__ == "__main__":
    for name in FILES:
        process(name)
