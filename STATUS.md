# Development status

Project: **Star Fox Adventures**. Source repository: [PS5_StarFoxAdventures](https://github.com/BaZZtian/PS5_StarFoxAdventures).

- Read-only media parser and synthetic bounds/region tests are implemented.
- Private local ISO registration, hashes and test-report templates are implemented.
- Community report and PR templates are included.
- The common media core was cross-compiled as a PS5 static library during initial
  development; this is not an installable game or a hardware gameplay test.
- No original NTSC-U ISO has been tested by the maintainer. Real ISO byte-level
  testing, runtime integration and physical PS5 gameplay tests remain pending.
- No game release, console deployment or ProsperoStore listing exists for this project.

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

ProsperoStore integration is planned for verified native packages, with GitHub
as the version source. Catalog submission and updates remain subject to catalog
maintainer review. Immediate store approval is not guaranteed.
