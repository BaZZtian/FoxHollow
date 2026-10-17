#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Cross-compile the pinned private game source, without making a runnable title."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess

from build_pc_reference import PIN, ROOT, sha, verify_private_source

SDK_PIN = "611893fc25ef3e138f5bc2c90d829d8b58174cd2"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-work-dir", type=Path, required=True)
    parser.add_argument("--build-dir", type=Path, required=True)
    parser.add_argument("--sdk", type=Path, required=True)
    parser.add_argument("--zlib-headers", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    if platform.system() != "Linux" or not 1 <= args.jobs <= 16:
        parser.error("Requires Linux and one to sixteen workers")
    work = args.reference_work_dir.resolve(strict=True)
    stamp = json.loads((work / "source.json").read_text())
    pc = json.loads((ROOT / "local-tests/pc-reference/build-receipt.json").read_text())
    if stamp["revision"] != PIN or stamp["archive_sha256"] != pc["archive_sha256"]:
        raise ValueError("Private source differs from the recorded PC reference")
    archive = ROOT / "local-tests/pc-reference" / f"foxhollow-{PIN}.tar"
    source_files = verify_private_source(work / "source", archive)
    sdk = args.sdk.resolve(strict=True)
    if (sdk / ".ps5-sdk-revision").read_text().strip() != SDK_PIN:
        raise ValueError("Payload SDK revision differs from the audited reference")
    zlib = args.zlib_headers.resolve(strict=True)
    zlib_hashes = {name: sha(zlib / name) for name in ("zlib.h", "zconf.h")}
    build = args.build_dir.resolve()
    if build in (Path("/"), Path("/tmp"), work, work / "source", ROOT):
        parser.error("Use a dedicated build directory")
    if ROOT in build.parents and ROOT / "local-tests" not in build.parents:
        parser.error("Game build outputs inside this repository must stay under local-tests")
    build.mkdir(parents=True, exist_ok=True)
    private = ROOT / "local-tests/ps5-game"
    private.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PS5_CLANG="/usr/bin/clang-18")
    compiler = subprocess.run([str(sdk / "bin/prospero-clang"), "--version"], env=env,
                              capture_output=True, text=True, check=True).stdout
    if "Target: x86_64-sie-ps5" not in compiler.splitlines():
        raise ValueError("Compiler wrapper does not target the PS5")
    configure = ["cmake", "-S", str(ROOT / "ps5"), "-B", str(build), "-G", "Ninja",
        "-DCMAKE_TOOLCHAIN_FILE=" + str(sdk / "toolchain/prospero.cmake"),
        "-DCMAKE_TRY_COMPILE_TARGET_TYPE=STATIC_LIBRARY", "-DCMAKE_BUILD_TYPE=Release",
        "-DSFA_SOURCE_DIR=" + str(work / "source"), "-DSFA_ZLIB_INCLUDE_DIR=" + str(zlib)]
    record = {"kind": "sfa-ps5-game-archive", "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_revision": PIN, "source_archive_sha256": stamp["archive_sha256"],
        "verified_source_files": source_files,
        "target_zlib_header_sha256": zlib_hashes,
        "sdk_revision": SDK_PIN, "sdk_toolchain_sha256": sha(sdk / "toolchain/prospero.cmake"),
        "compiler_version": compiler.splitlines(),
        "compiler_wrapper_sha256": sha(sdk / "bin/prospero-clang"),
        "configure_command": configure, "build_completed": False,
        "runtime_linked": False, "ps5_executed": False, "gameplay_verified": False}
    receipt = private / "build-receipt.json"
    receipt.write_text(json.dumps(record, indent=2) + "\n")
    for name, command in (("configure", configure), ("compile", ["cmake", "--build", str(build),
        "--target", "sfa_game", "--parallel", str(args.jobs)])):
        print(json.dumps({"stage": name, "private_log": str(private / (name + ".log"))}), flush=True)
        with (private / (name + ".log")).open("wb") as log:
            subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
    archive = build / "libsfa_game.a"
    record.update(build_completed=True, archive_sha256=sha(archive), archive_bytes=archive.stat().st_size)
    members = subprocess.run([str(sdk / "bin/prospero-ar"), "t", str(archive)], env=env,
                              capture_output=True, text=True, check=True).stdout.splitlines()
    record["archive_members"] = len(members)
    checkpoint = private / ("sfa-game-" + record["archive_sha256"][:12] + ".a")
    if checkpoint.exists() and sha(checkpoint) != record["archive_sha256"]:
        raise ValueError("Refusing to replace a different game archive checkpoint")
    if not checkpoint.exists():
        shutil.copy2(archive, checkpoint)
    record["private_archive"] = str(checkpoint)
    receipt.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"stage": "game-archive-built", "archive_bytes": record["archive_bytes"],
                      "runtime_linked": False, "ps5_executed": False}), flush=True)


if __name__ == "__main__":
    main()
