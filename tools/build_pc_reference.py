#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Build the pinned, unmodified SFA PC reference privately under native Linux."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import tarfile

PIN = "55371a2354ef36d4aabe53dfb78c19aa7f493737"
ARCHIVE_SHA256 = "dd9050c7b3683db7e1660a97099da0174e2fd7b74e633531c1e09fd19272b200"
ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def run_logged(command, log, cwd=None):
    with log.open("wb") as output:
        result = subprocess.run(command, cwd=cwd, stdout=output, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f"Step failed with exit {result.returncode}; private log: {log}")


def verify_private_source(source, archive):
    if sha(archive) != ARCHIVE_SHA256:
        raise ValueError("Source archive differs from the pinned private export")
    count = 0
    expected_paths = set()
    with tarfile.open(archive) as bundle:
        for member in bundle:
            path = source / member.name
            if member.isfile() or member.issym():
                expected_paths.add(member.name)
            if member.isfile():
                with bundle.extractfile(member) as stream:
                    expected = hashlib.file_digest(stream, "sha256").hexdigest()
                if path.is_symlink() or not path.is_file() or sha(path) != expected:
                    raise ValueError("Private source cache has been modified; preserving it")
                count += 1
            elif member.issym() and (not path.is_symlink() or str(path.readlink()) != member.linkname):
                raise ValueError("Private source link differs from the pinned export")
    actual_paths = {path.relative_to(source).as_posix() for path in source.rglob("*")
                    if path.is_file() or path.is_symlink()}
    if actual_paths != expected_paths:
        raise ValueError("Unexpected files in the private source cache; preserving it")
    return count


def dependency_evidence(build):
    cache = (build / "CMakeCache.txt").read_text()
    pins = {line.split(":", 1)[0]: line.split("=", 1)[1] for line in cache.splitlines()
            if line.startswith(("AURORA_DAWN_VERSION:", "AURORA_DAWN_REF:",
                                "AURORA_SDL3_REF:", "AURORA_NOD_VERSION:"))}
    libraries = {}
    for name in ("dawn_prebuilt-src/lib/libwebgpu_dawn.a", "nod_prebuilt-src/lib/libnod.a"):
        path = build / "_deps" / name
        libraries[name] = {"sha256": sha(path), "bytes": path.stat().st_size}
    tools = {}
    for command in ("/usr/bin/clang-18", "cmake", "ninja", "python3"):
        result = subprocess.run([command, "--version"], capture_output=True, text=True, check=True)
        tools[command] = result.stdout.splitlines()[0]
    return {"cmake_dependency_pins": pins, "prebuilt_libraries": libraries, "host_tools": tools}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    if platform.system() != "Linux" or not 1 <= args.jobs <= 16:
        parser.error("Requires native Linux and between one and sixteen workers")
    archive = args.archive.resolve(strict=True)
    private = (ROOT / "local-tests/pc-reference").resolve()
    private.mkdir(parents=True, exist_ok=True)
    if archive.parent != private or archive.name != f"foxhollow-{PIN}.tar":
        parser.error("Use the exact pinned git archive in the private reference directory")
    if sha(archive) != ARCHIVE_SHA256:
        parser.error("The archive digest differs from the recorded private export")
    work = args.work_dir.resolve()
    if work == Path("/") or work == Path("/tmp") or work == ROOT:
        parser.error("Use a dedicated build directory")
    if ROOT in work.parents and ROOT / "local-tests" not in work.parents:
        parser.error("Game source/build caches inside this repository must stay under local-tests")
    work.mkdir(parents=True, exist_ok=True)
    source = work / "source"
    stamp = work / "source.json"
    expected = {"revision": PIN, "archive_sha256": sha(archive)}
    if source.exists():
        if not stamp.is_file() or json.loads(stamp.read_text()) != expected:
            raise ValueError("Existing source cache has a different origin; preserving it")
    else:
        source.mkdir()
        with tarfile.open(archive) as bundle:
            bundle.extractall(source, filter="data")
        stamp.write_text(json.dumps(expected, indent=2) + "\n")
    source_files = verify_private_source(source, archive)
    print(json.dumps({"stage": "source-ready", **expected}), flush=True)

    debs = work / "debs"
    debs.mkdir(exist_ok=True)
    package_version = "8.5.0-2ubuntu10.16"
    packages = list(debs.glob(f"libcurl4-openssl-dev_{package_version}_amd64.deb"))
    if not packages:
        run_logged(["apt-get", "download", "libcurl4-openssl-dev=" + package_version],
                   private / "curl-download.log", cwd=debs)
        packages = list(debs.glob(f"libcurl4-openssl-dev_{package_version}_amd64.deb"))
    if len(packages) != 1:
        raise ValueError("Missing or ambiguous host development package")
    prefix = work / "host-dev"
    run_logged(["dpkg-deb", "-x", str(packages[0]), str(prefix)], private / "curl-extract.log")
    curl_header = prefix / "usr/include/x86_64-linux-gnu/curl/curl.h"
    curl_library = Path("/usr/lib/x86_64-linux-gnu/libcurl.so.4").resolve(strict=True)
    if not curl_header.is_file():
        raise ValueError("Isolated curl development headers missing")
    compiler = Path("/usr/bin/clang-18")
    cxx = Path("/usr/bin/clang++-18")
    build = work / "build"
    command = ["cmake", "-S", str(source), "-B", str(build), "-G", "Ninja",
               "-DCMAKE_BUILD_TYPE=Release", "-DCMAKE_C_COMPILER=" + str(compiler),
               "-DCMAKE_CXX_COMPILER=" + str(cxx), "-DFOXHOLLOW_VERSION=1.0.19",
               "-DFOXHOLLOW_DEBUG_SHORTCUTS=OFF", "-DAURORA_DAWN_PROVIDER=package",
               "-DAURORA_SDL3_PROVIDER=vendor", "-DCURL_INCLUDE_DIR=" + str(curl_header.parent.parent),
               "-DCURL_LIBRARY_RELEASE=" + str(curl_library)]
    record = {"kind": "sfa-unmodified-pc-reference-build", "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
              "upstream": "https://github.com/JackPriceBurns/foxhollow", **expected,
              "compiler_sha256": sha(compiler), "cxx_sha256": sha(cxx),
              "curl_development_package": {"version": package_version, "sha256": sha(packages[0])},
              "configure_command": command, "source_patched": False, "build_completed": False,
              "verified_source_files": source_files,
              "host_game_started": False, "pal_gameplay_verified": False,
              "ps5_executed": False, "public_release_created": False}
    receipt = private / "build-receipt.json"
    receipt.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"stage": "configure", "private_log": str(private / "configure.log")}), flush=True)
    run_logged(command, private / "configure.log")
    print(json.dumps({"stage": "compile", "jobs": args.jobs, "private_log": str(private / "build.log")}), flush=True)
    run_logged(["cmake", "--build", str(build), "--target", "foxhollow", "--parallel", str(args.jobs)],
               private / "build.log")
    binary = build / "foxhollow"
    record.update(build_completed=True, binary_sha256=sha(binary), binary_bytes=binary.stat().st_size)
    record.update(dependency_evidence(build))
    copied = private / ("foxhollow-linux-" + record["binary_sha256"][:12])
    if copied.exists() and sha(copied) != record["binary_sha256"]:
        raise ValueError("Refusing to replace a different checkpoint")
    if not copied.exists():
        shutil.copy2(binary, copied)
    record["private_binary"] = str(copied)
    receipt.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"stage": "build-completed", "binary_sha256": record["binary_sha256"],
                      "binary_bytes": record["binary_bytes"], "host_game_started": False,
                      "ps5_executed": False}), flush=True)


if __name__ == "__main__":
    main()
