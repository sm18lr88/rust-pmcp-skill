from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL_ROOT / "scripts" / "validate_skill.py"
REQUIRED_REFS = (
    "references/pmcp-production-guide.md",
    "references/cargo-pmcp-workflow.md",
    "references/testing-security-deploy.md",
    "references/migration-rmcp-to-pmcp.md",
    "references/version-matrix.md",
)
MAX_RAW_BYTES = 256 * 1024
MAX_FRONTMATTER_BYTES = 16 * 1024
MAX_BODY_BYTES = 240 * 1024


class SkillValidatorTests(unittest.TestCase):
    def make_skill(
        self,
        *,
        name: str = "rust-pmcp-skill",
        directory_name: str = "rust-pmcp-skill",
        description: str = "d",
        frontmatter_bytes: int | None = None,
        body_bytes: int | None = None,
        raw_bytes: int | None = None,
        utf8: bool = True,
        include_refs: bool = True,
    ) -> Path:
        temp_dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, temp_dir)
        root = temp_dir / directory_name
        root.mkdir()

        if raw_bytes is not None and frontmatter_bytes is None:
            frontmatter_bytes = MAX_FRONTMATTER_BYTES

        frontmatter_lines = (f"name: {name}", f"description: {description}")
        frontmatter = ("---\n" + "\n".join(frontmatter_lines) + "\n---\n").encode("utf-8")
        if frontmatter_bytes is not None:
            header = (
                b"---\n"
                + f"name: {name}\ndescription: {description}\nmetadata: ".encode("utf-8")
            )
            footer = b"\n---\n"
            padding = frontmatter_bytes - len(header) - len(footer)
            self.assertGreaterEqual(padding, 0)
            frontmatter = header + b"x" * padding + footer
            self.assertEqual(len(frontmatter), frontmatter_bytes)

        body = b"body\n" if body_bytes is None else b"x" * body_bytes
        if raw_bytes is not None:
            body = b"x" * (raw_bytes - len(frontmatter))
        payload = frontmatter + body
        if not utf8:
            payload = b"---\nname: rust-pmcp-skill\ndescription: d\n---\n\xff"
        (root / "SKILL.md").write_bytes(payload)

        if include_refs:
            for reference in REQUIRED_REFS:
                path = root / reference
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("reference\n", encoding="utf-8")
        return root

    def validate(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(root)],
            capture_output=True,
            check=False,
            encoding="utf-8",
        )

    def assert_valid(self, root: Path) -> None:
        result = self.validate(root)
        self.assertEqual(result.returncode, 0, result.stderr)

    def assert_invalid(self, root: Path, message: str) -> None:
        result = self.validate(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(message, result.stderr)

    def make_symlink(self, link: Path, target: Path) -> None:
        os.symlink(target, link, target_is_directory=target.is_dir())

    def add_frontmatter_lines(self, root: Path, lines: tuple[str, ...]) -> None:
        skill = root / "SKILL.md"
        frontmatter, delimiter, body = skill.read_text(encoding="utf-8").partition("\n---\n")
        self.assertTrue(delimiter)
        skill.write_bytes((frontmatter + "\n" + "\n".join(lines) + delimiter + body).encode("utf-8"))

    def test_accepts_body_larger_than_1024_bytes(self) -> None:
        # Given a valid skill with a reference-routed body over the legacy cap
        root = self.make_skill(body_bytes=1025)
        # When validation runs
        # Then independent safety caps accept it
        self.assert_valid(root)

    def test_accepts_one_character_unicode_description(self) -> None:
        root = self.make_skill(description="é")
        self.assert_valid(root)

    def test_accepts_1024_character_unicode_description(self) -> None:
        root = self.make_skill(description="é" * 1024)
        self.assert_valid(root)

    def test_rejects_blank_description(self) -> None:
        root = self.make_skill(description="")
        self.assert_invalid(root, "missing frontmatter description")

    def test_rejects_single_quoted_whitespace_description(self) -> None:
        root = self.make_skill(description="'   '")
        self.assert_invalid(root, "missing frontmatter description")

    def test_rejects_double_quoted_whitespace_description(self) -> None:
        root = self.make_skill(description='"   "')
        self.assert_invalid(root, "missing frontmatter description")

    def test_rejects_1025_character_unicode_description(self) -> None:
        root = self.make_skill(description="é" * 1025)
        self.assert_invalid(root, "description exceeds 1024 Unicode characters")

    def test_accepts_raw_file_at_256_kib(self) -> None:
        root = self.make_skill(raw_bytes=MAX_RAW_BYTES)
        self.assert_valid(root)

    def test_rejects_raw_file_over_256_kib(self) -> None:
        root = self.make_skill(raw_bytes=MAX_RAW_BYTES + 1)
        self.assert_invalid(root, "SKILL.md exceeds 262144 raw bytes")

    def test_accepts_frontmatter_at_16_kib(self) -> None:
        root = self.make_skill(frontmatter_bytes=MAX_FRONTMATTER_BYTES)
        self.assert_valid(root)

    def test_rejects_frontmatter_over_16_kib(self) -> None:
        root = self.make_skill(frontmatter_bytes=MAX_FRONTMATTER_BYTES + 1)
        self.assert_invalid(root, "frontmatter exceeds 16384 bytes")

    def test_accepts_body_at_240_kib(self) -> None:
        root = self.make_skill(body_bytes=MAX_BODY_BYTES)
        self.assert_valid(root)

    def test_rejects_body_over_240_kib(self) -> None:
        root = self.make_skill(body_bytes=MAX_BODY_BYTES + 1)
        self.assert_invalid(root, "body exceeds 245760 bytes")

    def test_rejects_malformed_utf8(self) -> None:
        root = self.make_skill(utf8=False)
        self.assert_invalid(root, "valid UTF-8")

    def test_rejects_invalid_name(self) -> None:
        root = self.make_skill(name="Rust_PMCP")
        self.assert_invalid(root, "invalid name")

    def test_accepts_name_at_64_characters(self) -> None:
        name = "a" * 64
        root = self.make_skill(name=name, directory_name=name)
        self.assert_valid(root)

    def test_rejects_name_at_65_characters(self) -> None:
        name = "a" * 65
        root = self.make_skill(name=name, directory_name=name)
        self.assert_invalid(root, "name exceeds 64 characters")

    def test_rejects_name_directory_mismatch(self) -> None:
        root = self.make_skill(directory_name="different-skill")
        self.assert_invalid(root, "directory name")

    def test_rejects_missing_required_reference(self) -> None:
        root = self.make_skill(include_refs=False)
        self.assert_invalid(root, "missing referenced file")

    def test_rejects_duplicate_normalized_known_frontmatter_key(self) -> None:
        # Given equivalent known keys after NFC, strip, and casefold
        root = self.make_skill()
        self.add_frontmatter_lines(root, (" Name : shadow",))
        # When validation runs
        # Then duplicate metadata is rejected instead of overwritten
        self.assert_invalid(root, "duplicate frontmatter key")

    def test_rejects_duplicate_normalized_unknown_frontmatter_key(self) -> None:
        root = self.make_skill()
        self.add_frontmatter_lines(root, ("E\u0301: first", " é : second"))
        self.assert_invalid(root, "duplicate frontmatter key")

    def test_rejects_blank_normalized_frontmatter_key(self) -> None:
        root = self.make_skill()
        self.add_frontmatter_lines(root, ("   : value",))
        self.assert_invalid(root, "frontmatter key must not be blank")

    def test_rejects_colon_frontmatter_key(self) -> None:
        root = self.make_skill()
        self.add_frontmatter_lines(root, ("unknown:key: value",))
        self.assert_invalid(root, "frontmatter key must not contain ':'")

    def test_rejects_reparse_skill_root(self) -> None:
        root = self.make_skill()
        alias = root.parent / "root-link"
        self.make_symlink(alias, root)
        self.assert_invalid(alias, "skill root contains a reparse point")

    def test_rejects_reparse_ancestor_of_skill_root(self) -> None:
        root = self.make_skill()
        alias_parent = root.parent / "ancestor-link"
        self.make_symlink(alias_parent, root.parent)
        self.assert_invalid(alias_parent / root.name, "skill root contains a reparse point")

    def test_rejects_reparse_skill_file(self) -> None:
        root = self.make_skill()
        source = root / "skill-source.md"
        (root / "SKILL.md").rename(source)
        self.make_symlink(root / "SKILL.md", source)
        self.assert_invalid(root, "SKILL.md contains a reparse point")

    def test_rejects_skill_file_directory(self) -> None:
        root = self.make_skill()
        (root / "SKILL.md").unlink()
        (root / "SKILL.md").mkdir()
        self.assert_invalid(root, "SKILL.md must be a regular file")

    def test_rejects_reparse_reference_directory(self) -> None:
        root = self.make_skill()
        source = root / "reference-source"
        (root / "references").rename(source)
        self.make_symlink(root / "references", source)
        self.assert_invalid(root, "contains a reparse point")

    def test_rejects_reparse_reference_file(self) -> None:
        root = self.make_skill()
        reference = root / REQUIRED_REFS[0]
        source = root / "reference-source.md"
        reference.rename(source)
        self.make_symlink(reference, source)
        self.assert_invalid(root, "referenced file: references/pmcp-production-guide.md contains a reparse point")

    def test_rejects_canonical_skill_file_escape(self) -> None:
        root = self.make_skill()
        outside = root.parent / "outside.md"
        outside.write_text("outside\n", encoding="utf-8")
        (root / "SKILL.md").unlink()
        self.make_symlink(root / "SKILL.md", outside)
        self.assert_invalid(root, "SKILL.md escapes the skill root")

    def test_accepts_invocation_from_skill_root(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR)],
            cwd=SKILL_ROOT,
            capture_output=True,
            check=False,
            encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
