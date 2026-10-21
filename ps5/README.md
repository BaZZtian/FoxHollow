# Private PS5 game compilation

This is a build target for the actual SFA game translation units, using the
unmodified private Foxhollow export. It produces `libsfa_game.a`, not a PS5
application. It does not supply the runtime, resolve all imports, package a
title, install anything or test console gameplay.

After building the pinned PC reference, run on Linux:

```sh
python3 tools/build_ps5_game.py \
  --reference-work-dir /tmp/sfa-ps5-pc-reference-55371a2354ef \
  --build-dir /tmp/sfa-ps5-game-55371a2354ef \
  --sdk /path/to/pinned/open-payload-sdk \
  --zlib-headers /path/to/actual/ps5-zlib-generated-headers \
  --jobs 8
```

The SDK must record revision `611893fc25ef3e138f5bc2c90d829d8b58174cd2`.
The wrapper must report target `x86_64-sie-ps5`. zlib compatibility headers
must come from the real target dependency build, not fabricated declarations.
MusyX headers and definitions come from the same Foxhollow source revision.

The source export, game archive and build logs stay private. The ignored
`local-tests/ps5-game/build-receipt.json` records the source/header/compiler
provenance, build result and the fact that no runtime or gameplay was tested.
