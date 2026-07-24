#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import stat
import sys
import unicodedata
from pathlib import Path

MAX_RAW_BYTES = 256 * 1024
MAX_FRONTMATTER_BYTES = 16 * 1024
MAX_BODY_BYTES = 240 * 1024
MAX_DESCRIPTION_CHARACTERS = 1024
MAX_NAME_CHARACTERS = 64
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REQUIRED_REFERENCES = (
    "references/pmcp-production-guide.md",
    "references/cargo-pmcp-workflow.md",
    "references/testing-security-deploy.md",
    "references/migration-rmcp-to-pmcp.md",
    "references/version-matrix.md",
)


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def split_frontmatter(data: bytes) -> tuple[bytes, bytes]:
    if not data.startswith(b"---\n"):
        fail("SKILL.md must start with YAML frontmatter")
    end = data.find(b"\n---\n", 4)
    if end == -1:
        fail("SKILL.md frontmatter must be closed with ---")
    frontmatter_end = end + len(b"\n---\n")
    return data[:frontmatter_end], data[frontmatter_end:]


def normalize_frontmatter_key(key: str) -> str:
    return unicodedata.normalize("NFC", key.strip()).casefold()


def parse_frontmatter(text: str) -> dict[str, str]:
    meta: dict[str, str] = {}
    for line in text.splitlines()[1:-1]:
        if not line.strip():
            continue
        separator = re.search(r":(?=[ \t]|$)", line)
        if separator is None:
            fail("unsupported frontmatter line")
        key = normalize_frontmatter_key(line[: separator.start()])
        if not key:
            fail("frontmatter key must not be blank")
        if ":" in key:
            fail("frontmatter key must not contain ':'")
        if key in meta:
            fail("duplicate frontmatter key")
        value = line[separator.end() :]
        meta[key] = value.strip().strip('"').strip("'").strip()
    return meta


def contains_reparse_point(path: Path) -> bool:
    current = Path(os.path.abspath(path))
    while True:
        try:
            status = current.lstat()
        except FileNotFoundError:
            pass
        else:
            attributes = getattr(status, "st_file_attributes", 0)
            reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
            if stat.S_ISLNK(status.st_mode) or attributes & reparse_flag:
                return True
        parent = current.parent
        if parent == current:
            return False
        current = parent


def validate_regular_file(root: Path, relative_path: str, label: str) -> Path:
    path = root / relative_path
    if not path.exists():
        fail(f"missing {label}")
    if not path.resolve().is_relative_to(root):
        fail(f"{label} escapes the skill root")
    if contains_reparse_point(path):
        fail(f"{label} contains a reparse point")
    if not path.is_file():
        fail(f"{label} must be a regular file")
    return path


def main() -> None:
    requested_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    absolute_root = Path(os.path.abspath(requested_root))
    if contains_reparse_point(absolute_root):
        fail("skill root contains a reparse point")
    if not absolute_root.is_dir():
        fail("skill root must be a directory")
    root = absolute_root.resolve()
    skill = validate_regular_file(root, "SKILL.md", "SKILL.md")

    data = skill.read_bytes()
    if len(data) > MAX_RAW_BYTES:
        fail(f"SKILL.md exceeds {MAX_RAW_BYTES} raw bytes")

    frontmatter, body = split_frontmatter(data)
    if len(frontmatter) > MAX_FRONTMATTER_BYTES:
        fail(f"frontmatter exceeds {MAX_FRONTMATTER_BYTES} bytes")
    if len(body) > MAX_BODY_BYTES:
        fail(f"body exceeds {MAX_BODY_BYTES} bytes")

    try:
        frontmatter_text = frontmatter.decode("utf-8")
        body.decode("utf-8")
    except UnicodeDecodeError:
        fail("SKILL.md must contain valid UTF-8")

    meta = parse_frontmatter(frontmatter_text)

    name = meta.get("name", "")
    desc = meta.get("description", "")
    if not name:
        fail("missing frontmatter name")
    if not desc:
        fail("missing frontmatter description")
    if len(name) > MAX_NAME_CHARACTERS:
        fail("name exceeds 64 characters")
    if not NAME_RE.match(name):
        fail(f"invalid name: {name}")
    if root.name != name:
        fail(f"directory name {root.name!r} must match skill name {name!r}")
    if len(desc) > MAX_DESCRIPTION_CHARACTERS:
        fail("description exceeds 1024 Unicode characters")

    for ref in REQUIRED_REFERENCES:
        validate_regular_file(root, ref, f"referenced file: {ref}")

    print(
        f"OK: {name} ({len(data)} raw bytes, {len(frontmatter)} frontmatter bytes, "
        f"{len(body)} body bytes)"
    )


if __name__ == "__main__":
    main()
