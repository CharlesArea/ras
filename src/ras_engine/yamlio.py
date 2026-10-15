"""Small YAML compatibility layer.

RAS prefers PyYAML when it is present, but the reference CLI deliberately has
no mandatory runtime dependency. The fallback parser supports the YAML subset
used by report manifests, source ledgers, brand profiles, and block
frontmatter. Generated YAML is conservative and valid JSON-compatible YAML.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


class YamlError(ValueError):
    """Raised when a manifest cannot be read as YAML."""


def load_yaml(path_or_text: str | Path) -> Any:
    text = Path(path_or_text).read_text(encoding="utf-8") if isinstance(path_or_text, Path) else path_or_text
    stripped = text.strip()
    if not stripped:
        return {}
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text)
    except ImportError:
        return _parse_fallback(text)
    except Exception as exc:  # pragma: no cover - depends on optional parser
        raise YamlError(f"Unable to parse YAML: {exc}") from exc


def dump_yaml(value: Any) -> str:
    """Return stable, human-readable YAML without requiring PyYAML."""

    lines: list[str] = []

    def emit(node: Any, level: int, prefix: str = "") -> None:
        pad = "  " * level
        if isinstance(node, dict):
            if not node:
                lines.append(f"{pad}{prefix}{{}}")
                return
            if prefix:
                lines.append(f"{pad}{prefix}")
                level += 1
                pad = "  " * level
            for key, item in node.items():
                key_text = str(key)
                if isinstance(item, (dict, list)):
                    lines.append(f"{pad}{key_text}:")
                    emit(item, level + 1)
                else:
                    lines.append(f"{pad}{key_text}: {_scalar_text(item)}")
        elif isinstance(node, list):
            if not node:
                lines.append(f"{pad}{prefix}[]")
                return
            for item in node:
                if isinstance(item, dict) and item:
                    first = True
                    for key, subitem in item.items():
                        subpad = "  " * level
                        if first:
                            first = False
                            if isinstance(subitem, (dict, list)):
                                lines.append(f"{subpad}- {key}:")
                                emit(subitem, level + 2)
                            else:
                                lines.append(f"{subpad}- {key}: {_scalar_text(subitem)}")
                        else:
                            if isinstance(subitem, (dict, list)):
                                lines.append(f"{subpad}  {key}:")
                                emit(subitem, level + 2)
                            else:
                                lines.append(f"{subpad}  {key}: {_scalar_text(subitem)}")
                elif isinstance(item, (dict, list)):
                    lines.append(f"{'  ' * level}-")
                    emit(item, level + 1)
                else:
                    lines.append(f"{'  ' * level}- {_scalar_text(item)}")
        else:
            lines.append(f"{pad}{prefix}{_scalar_text(node)}")

    emit(value, 0)
    return "\n".join(lines) + "\n"


def write_yaml(path: str | Path, value: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(dump_yaml(value), encoding="utf-8", newline="\n")


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Split a Markdown document with `---` YAML frontmatter."""

    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        raise YamlError("Block frontmatter starts with --- but has no closing ---")
    front = "\n".join(lines[1:end])
    body = "\n".join(lines[end + 1 :]).lstrip("\n")
    parsed = load_yaml(front) or {}
    if not isinstance(parsed, dict):
        raise YamlError("Block frontmatter must be a mapping")
    return parsed, body


def _scalar_text(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        if value and re.fullmatch(r"[A-Za-z0-9_./@%+()\- ]+", value) and not value.startswith(("-", "?")):
            return value
        return json.dumps(value, ensure_ascii=False)
    return json.dumps(value, ensure_ascii=False)


def _parse_fallback(text: str) -> Any:
    raw_lines = text.splitlines()
    lines: list[tuple[int, str]] = []
    for raw in raw_lines:
        if not raw.strip() or raw.lstrip().startswith("#") or raw.strip() in {"---", "..."}:
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        content = _strip_comment(raw[indent:].rstrip())
        if content:
            lines.append((indent, content))
    if not lines:
        return {}

    def next_indent(index: int, current: int) -> int | None:
        if index >= len(lines) or lines[index][0] <= current:
            return None
        return lines[index][0]

    def parse_node(index: int, indent: int) -> tuple[Any, int]:
        if index >= len(lines) or lines[index][0] != indent:
            return {}, index
        if lines[index][1] in {"{}", "[]"} or lines[index][1].startswith(("[", "{")) and ":" not in lines[index][1]:
            return _parse_scalar(lines[index][1]), index + 1
        if lines[index][1].startswith("- ") or lines[index][1] == "-":
            return parse_list(index, indent)
        return parse_map(index, indent)

    def parse_map(index: int, indent: int) -> tuple[dict[str, Any], int]:
        result: dict[str, Any] = {}
        while index < len(lines):
            line_indent, content = lines[index]
            if line_indent < indent:
                break
            if line_indent > indent:
                raise YamlError(f"Unexpected indentation near: {content}")
            if content.startswith("- ") or content == "-":
                break
            key, sep, rest = content.partition(":")
            if not sep or not key.strip():
                raise YamlError(f"Expected mapping entry near: {content}")
            key = key.strip().strip('"\'')
            rest = rest.strip()
            index += 1
            if rest in {"|", ">"}:
                collected: list[str] = []
                while index < len(lines) and lines[index][0] > indent:
                    collected.append(lines[index][1])
                    index += 1
                result[key] = ("\n" if rest == "|" else " ").join(collected)
            elif rest:
                result[key] = _parse_scalar(rest)
            else:
                child = next_indent(index, indent)
                if child is None:
                    result[key] = None
                else:
                    result[key], index = parse_node(index, child)
        return result, index

    def parse_list(index: int, indent: int) -> tuple[list[Any], int]:
        result: list[Any] = []
        while index < len(lines):
            line_indent, content = lines[index]
            if line_indent != indent or not (content == "-" or content.startswith("- ")):
                break
            rest = content[1:].strip()
            index += 1
            if not rest:
                child = next_indent(index, indent)
                if child is None:
                    result.append(None)
                else:
                    item, index = parse_node(index, child)
                    result.append(item)
                continue
            key, sep, value = rest.partition(":")
            if sep and key.strip() and not rest.startswith(("http:", "https:")):
                item: dict[str, Any] = {}
                key = key.strip().strip('"\'')
                value = value.strip()
                if value:
                    item[key] = _parse_scalar(value)
                else:
                    child = next_indent(index, indent)
                    if child is None:
                        item[key] = None
                    else:
                        item[key], index = parse_node(index, child)
                child = next_indent(index, indent)
                if child is not None:
                    extra, index = parse_map(index, child)
                    item.update(extra)
                result.append(item)
            else:
                result.append(_parse_scalar(rest))
        return result, index

    parsed, end = parse_node(0, lines[0][0])
    if end != len(lines):
        raise YamlError(f"Could not parse YAML near: {lines[end][1]}")
    return parsed


def _strip_comment(text: str) -> str:
    quoted = False
    quote = ""
    for index, char in enumerate(text):
        if char in {'"', "'"}:
            if not quoted:
                quoted, quote = True, char
            elif quote == char:
                quoted = False
        elif char == "#" and not quoted and (index == 0 or text[index - 1].isspace()):
            return text[:index].rstrip()
    return text


def _parse_scalar(text: str) -> Any:
    value = text.strip()
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if value in {"true", "True", "TRUE"}:
        return True
    if value in {"false", "False", "FALSE"}:
        return False
    if value.startswith(("[", "{")):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    if re.fullmatch(r"[-+]?\d+", value):
        try:
            return int(value)
        except ValueError:
            pass
    if re.fullmatch(r"[-+]?(?:\d+\.\d*|\d*\.\d+)(?:[eE][-+]?\d+)?", value):
        try:
            return float(value)
        except ValueError:
            pass
    return value
