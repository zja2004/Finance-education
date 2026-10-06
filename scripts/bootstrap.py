"""Fetch pinned teaching repositories without overwriting existing learner work."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent


def git(directory: Path, *arguments: str, ntfs_workaround: bool = False) -> str:
    command = ["git"]
    if ntfs_workaround:
        command += ["-c", "core.protectNTFS=false"]
    command += ["-C", str(directory), *arguments]
    environment = dict(os.environ)
    environment["GIT_TERMINAL_PROMPT"] = "0"
    result = subprocess.run(
        command, env=environment, capture_output=True, text=True, encoding="utf-8"
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "Git command failed")
    return result.stdout.strip()


def prepare_repository(root: Path, specification: dict, check_only: bool) -> dict:
    name = specification["name"]
    commit = specification["commit"]
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", name) or not re.fullmatch(r"[a-f0-9]{40}", commit):
        raise RuntimeError("Invalid repository name or pinned commit in manifest")
    directory = root / "repos" / name
    created = False
    if not directory.exists():
        if check_only:
            raise RuntimeError(f"Missing repository: {name}; run bootstrap without --check")
        directory.parent.mkdir(parents=True, exist_ok=True)
        git(directory.parent, "-c", "core.longpaths=true", "clone", "--no-checkout",
            specification["url"], str(directory))
        created = True

    if git(directory, "remote", "get-url", "origin") != specification["url"]:
        raise RuntimeError(f"Origin differs for {name}; existing directory preserved")
    git(directory, "cat-file", "-e", f"{commit}^{{commit}}")

    if created:
        exclusions = specification.get("windows_excluded_paths", []) if os.name == "nt" else []
        if exclusions:
            tracked = git(directory, "ls-tree", "-r", "--name-only", commit).splitlines()
            if any(path not in tracked for path in exclusions):
                raise RuntimeError(f"Compatibility mapping differs for {name}")
            # Only a freshly created clone is materialized here. The override is
            # command-scoped, and excluded names are never written to Windows.
            git(directory, "sparse-checkout", "set", "--no-cone", "/*",
                *("!/" + path for path in exclusions), ntfs_workaround=True)
        git(directory, "checkout", "--force", "--detach", commit,
            ntfs_workaround=bool(exclusions))
    else:
        if git(directory, "rev-parse", "HEAD") != commit:
            raise RuntimeError(f"Pinned commit differs for {name}; existing checkout preserved")
        if git(directory, "status", "--porcelain"):
            raise RuntimeError(f"Local changes found in {name}; existing work preserved")

    if git(directory, "rev-parse", "--is-shallow-repository") != "false":
        raise RuntimeError(f"Shallow repository found: {name}; full history is required")
    if not (directory / "README.md").is_file():
        raise RuntimeError(f"README is not checked out: {name}")
    if git(directory, "status", "--porcelain"):
        raise RuntimeError(f"Working tree is not clean: {name}")
    git(directory, "fsck", "--full", "--no-dangling")
    return {
        "name": name,
        "origin": specification["url"],
        "head_commit": commit,
        "is_shallow": False,
        "working_tree_clean": True,
        "git_fsck": "passed",
    }


def prepare_compatibility_copy(root: Path, specification: dict, check_only: bool) -> None:
    directory = root / "repos" / specification["repository"]
    payload = subprocess.check_output(
        ["git", "-C", str(directory), "show", "HEAD:" + specification["source_path"]]
    )
    if hashlib.sha256(payload).hexdigest() != specification["sha256"]:
        raise RuntimeError("Compatibility source differs from the pinned SHA-256")
    notebook = json.loads(payload)
    if notebook.get("nbformat") != 4 or not isinstance(notebook.get("cells"), list):
        raise RuntimeError("Invalid compatibility Notebook")
    destination = root / specification["destination"]
    if not destination.resolve().is_relative_to(root.resolve()):
        raise RuntimeError("Compatibility destination must remain in the workspace")
    if destination.exists():
        if destination.read_bytes() != payload:
            raise RuntimeError("Compatibility copy has local changes; preserved without overwrite")
    elif check_only:
        raise RuntimeError("Missing compatibility copy; run bootstrap without --check")
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)


def initialize(root: Path, check_only: bool = False) -> list[dict]:
    manifest = json.loads((root / "upstreams.json").read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1:
        raise RuntimeError("Unsupported upstream manifest version")
    if not check_only and (root / ".git").exists():
        git(root, "submodule", "init")
    results = []
    for specification in manifest["repositories"]:
        print("Checking" if check_only else "Preparing", specification["name"], flush=True)
        results.append(prepare_repository(root, specification, check_only))
    prepare_compatibility_copy(root, manifest["compatibility_copy"], check_only)

    progress = root / "学习进度.md"
    if not progress.exists():
        if check_only:
            raise RuntimeError("Missing learning progress; run bootstrap without --check")
        shutil.copyfile(root / "学习进度模板.md", progress)
    if not check_only:
        report = {
            "manifest_verified_date": manifest["verified_date"],
            "repositories": results,
            "compatibility_copy_matches_git_blob": True,
            "applications_executed": False,
        }
        (root / "repos" / "克隆核验.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify without cloning or writing files")
    options = parser.parse_args()
    try:
        results = initialize(ROOT, check_only=options.check)
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Verified {len(results)} repositories; learner records remain local.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
