# FoxHollow

Status snapshot: **19 October 2026**. The public repository contains the
tooling and build documentation only; it does not contain a game image,
original game executable, extracted content or a playable PS5 package.

Early development toward a native PS5 homebrew port of **Star Fox Adventures**, using each
player's own GameCube ISO. Target firmware: **12.40**.

**There is no playable PS5 port or downloadable game release here yet.**
The implemented code includes a read-only GameCube media layer, regional input
preparation, a release-evidence checker and private native-build recipes.
Synthetic tests and compilation are not evidence of gameplay on a console.

## Current scope

Foxhollow is the native PC reference. Its renderer/platform integration must still be adapted and verified on PS5. This repository currently contains the original media-validation tools and test preparation, with no game runtime.

The pinned, unmodified PC reference has now been built and exercised with the
owned PAL disc: original graphics, German menus, menu input and creation of a
private save slot. The actual game translation units also compile for the open
PS5 toolchain into a private library. This is not a linked or installable PS5
application. See [the current work record](BOOT-WORK.md) and
[the private PS5 compilation recipe](ps5/README.md).

| Region | Expected disc ID | Gameplay on PS5 |
| --- | --- | --- |
| NTSC-U | `GSAE01` | Not tested |
| PAL | `GSAP01` | Not tested |

Disc revisions are recorded separately. Recognizing a header does not establish
that a revision is compatible. Both regional gameplay reports are required for
the exact candidate build before a game release.

## Help wanted

We need owners of the **NTSC-U** version to run local media checks and share
reviewed metadata, and developers to contribute compatibility work through PRs.
See [NTSC testing](community/NTSC-TESTING.md) and [Contributing](CONTRIBUTING.md),
or open a [regional compatibility report](https://github.com/BaZZtian/PS5-FoxHollow/issues/new?template=regional-compatibility.yml).

**Do not upload or send ISOs, original executables, REL modules, extracted game
content, shaders, proprietary SDKs or download links, including in private messages.**
Users always provide their own image locally. Sources and future release packages
must contain no original game files.

## Prepare an owned ISO with one command

Windows, from this repository's folder:

```powershell
.\prepare-ntsc.ps1 -Iso "D:\Own Games\game-ntsc.iso"
```

Add `-Region PAL` for PAL. Optional `-ExpectedSha256 <checksum>` rejects an image
that differs from a known checksum. This uses Python 3.10+, WSL Ubuntu-24.04,
CMake 3.25+, Ninja and Clang/GCC; it does not install software.

Linux:

```sh
python3 tools/prepare_region.py --iso "/media/own/game-ntsc.iso"
```

The command builds the current inspection tool, runs synthetic tests, verifies
the disc identity/region/number, FST and DOL bounds, and computes SHA-256/SHA-1.
It does not modify, copy, upload or execute the ISO. It prepares inputs and test
forms; it does not build a playable game. Native runtime/platform work is pending.

## Public Git and store status

The current work is published as an **unreleased development snapshot**. No
version tag or GitHub download release has been created because the PS5
runtime is not linked, deployed or verified on hardware. The repository is
safe to inspect and contribute to, but it is not a playable release.

The separate Prospero catalog placeholder (`PPSA99573`) was accepted in
[catalog PR #421](https://github.com/darkxex/ps5-homebrew-catalog/pull/421).
The requested current project name is **FoxHollow**; see
[the naming update](publishing/NAME-CHANGE.md) for the catalog change request.
The reservation contains metadata only: it has no download, source artifact,
icon, ISO or game data. A merged placeholder would still not be a release.

Outputs are Git-ignored under `private-inputs/star-fox-adventures/<region>/<sha256>/`:

| File | Purpose | Public sharing |
| --- | --- | --- |
| `input.json` | Private local ISO path and registration | Never |
| `metadata.json` | Disc identity, revision, hashes, size and structure result | After review |
| `ps5-test-template.json` | Empty form for later real PS5 testing | Only report actual results |
| `../current.json` | Local pointer to the latest registration | Keep local |

## Build and test the tools

```sh
cmake -S . -B build/host -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=clang
cmake --build build/host
ctest --test-dir build/host --output-on-failure
```

CI uses synthetic fixtures only. It never uploads original inputs or publishes
game packages. See [STATUS.md](STATUS.md) for the current limitations.

## References and licensing

- [Foxhollow](https://github.com/JackPriceBurns/foxhollow), revision `55371a2354ef36d4aabe53dfb78c19aa7f493737`.

Upstream game sources are not included in this initial tooling repository.
The [MIT license](LICENSE) covers the new code here. It does not cover original
game files or grant rights to upstream projects; their own licenses, authors
and notices must be respected when integrating components.

This is an unofficial project and is not affiliated with the original developers
or publishers.
