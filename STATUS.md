# Development status

Status snapshot: **19 October 2026**.

Project: **Star Fox Adventures**. Source repository: [PS5_StarFoxAdventures](https://github.com/BaZZtian/PS5_StarFoxAdventures).

- Read-only media parser and synthetic bounds/region tests are implemented.
- Private local ISO registration, hashes and test-report templates are implemented.
- Community report and PR templates are included.
- The common media core was cross-compiled as a PS5 static library during initial
  development; this is not an installable game or a hardware gameplay test.
- The owned PAL revision-0 image has passed real ISO structure and DOL-bounds
  checks; its SHA-256/SHA-1 are stored only in the private local registration.
- No NTSC-U image or physical PS5 gameplay test has been completed.
- No playable PS5 app, console deployment or downloadable game release exists
  for this project.
- The working title **Foxhollow PS5** and proposed identity `PPSA99573` have a
  metadata-only Coming soon reservation in [catalog PR #421](https://github.com/darkxex/ps5-homebrew-catalog/pull/421).
  It is still awaiting maintainer review and contains no download or game data.

## Runtime work

Foxhollow is the native PC reference. Its renderer/platform integration must still be adapted and verified on PS5. This repository currently contains the original media-validation tools and test preparation, with no game runtime.

## Release and store requirements

PAL (`GSAP01`) and NTSC-U (`GSAE01`)
must both pass real gameplay testing on firmware **12.40** using the same candidate
build. Test records require the build ID, exact disc SHA-256 and revision, date,
evidence reference, and boot/gameplay/audio/controller/save-load checks.

Use the release checker before considering a release:

```sh
python3 tools/release_gate.py star-fox-adventures <candidate-folder> <evidence.json>
```

It checks hashes, provenance declarations, required files, version metadata and
regional evidence. It cannot verify rights to mislabeled content or independently
prove that a human ran a console test; maintainer review remains required.
No workflow currently publishes releases. Community source contributions can
proceed while game releases wait for the required evidence.

ProsperoStore integration is planned for a verified native package, with
GitHub as the version source. The current catalog entry is only a Coming soon
placeholder; the package and title rename remain blocked until the release
gates above are satisfied. Catalog submission and updates remain subject to
catalog maintainer review.

## Git release status

This repository is currently an **unreleased development snapshot**. There is
no version tag, GitHub Release or downloadable artifact. The public tree
contains source tooling, build recipes, tests and documentation only. The
next public release decision requires a linked PS5 runtime, real PAL and
NTSC-U gameplay evidence, dependency/provenance review and a package audit
that confirms no original game data is included.
