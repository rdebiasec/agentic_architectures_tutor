#!/usr/bin/env python3
"""Verify local and cloud-prod Chroma indexes contain identical chunks."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

MANIFEST_LOCAL = ROOT / ".rag" / "manifest-local.json"
MANIFEST_CLOUD = ROOT / ".rag" / "manifest-cloud.json"


def run_manifest(env_file: str, output: Path) -> None:
    env = os.environ.copy()
    env_path = ROOT / env_file
    if not env_path.exists():
        raise SystemExit(f"Missing {env_file}")

    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()

    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "export_index_manifest.py"),
        "-o",
        str(output),
    ]
    subprocess.run(cmd, check=True, env=env, cwd=ROOT)


def load_manifest(path: Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {row["chunk_id"]: row for row in data["records"]}


def compare(local: dict[str, dict], cloud: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    local_ids = set(local)
    cloud_ids = set(cloud)

    if len(local_ids) != len(cloud_ids):
        errors.append(f"Chunk count mismatch: local={len(local_ids)} cloud={len(cloud_ids)}")

    only_local = sorted(local_ids - cloud_ids)
    only_cloud = sorted(cloud_ids - local_ids)
    if only_local:
        errors.append(f"IDs only in local ({len(only_local)}): {only_local[:5]}")
    if only_cloud:
        errors.append(f"IDs only in cloud ({len(only_cloud)}): {only_cloud[:5]}")

    hash_mismatches = 0
    for chunk_id in sorted(local_ids & cloud_ids):
        if local[chunk_id]["text_hash"] != cloud[chunk_id]["text_hash"]:
            hash_mismatches += 1
            if hash_mismatches <= 5:
                errors.append(
                    f"Hash mismatch for {chunk_id}: "
                    f"local={local[chunk_id]['text_hash'][:12]} "
                    f"cloud={cloud[chunk_id]['text_hash'][:12]}"
                )
    if hash_mismatches > 5:
        errors.append(f"... and {hash_mismatches - 5} more hash mismatches")

    return errors


def main() -> None:
    print("==> Exporting local manifest")
    run_manifest(".env.local", MANIFEST_LOCAL)
    print("==> Exporting cloud-prod manifest")
    run_manifest(".env.cloud-prod", MANIFEST_CLOUD)

    local = load_manifest(MANIFEST_LOCAL)
    cloud = load_manifest(MANIFEST_CLOUD)

    errors = compare(local, cloud)
    if errors:
        print("\nPARITY CHECK FAILED:")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)

    print(f"\nPARITY OK: {len(local)} chunks match (ids + text hashes)")


if __name__ == "__main__":
    main()
