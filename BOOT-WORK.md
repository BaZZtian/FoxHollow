# SFA: current native-port work

Updated: 17 October 2026. This checkout is exclusively for Star Fox Adventures.
No other game's runtime, store identity or automation belongs to this project.

## Established reference

Use Foxhollow revision `55371a2354ef36d4aabe53dfb78c19aa7f493737`.
An existing clean local checkout was exported with `git archive`; the original
checkout has not been changed. The private source cache was compared against
all 2,429 files in that export. The archive and generated game programs are
private inputs, not files to publish.

`tools/build_pc_reference.py` builds this source unmodified under native Linux
with Clang 18.1.3, CMake 3.28.3, Ninja, Release settings, and debug shortcuts off.
It checks the exact exported archive before extraction or cache reuse. Python
3.12 is used for this recipe. A missing curl development package was extracted
into a dedicated build prefix; no global package installation was performed.

The native PC executable was built successfully. Its private receipt records
the source/compiler/dependency/binary hashes and actual build commands.
The real owned PAL revision-0 disc was read through a read-only mount and its
entire SHA-256 was checked again before the boot probes.

Observed on the unmodified native PC build:

- Original introductory/attract sequences and the rendered main-menu scene.
- German menus after selecting the existing German language setting.
- Actual keyboard navigation through the existing controls configuration.
- Creation of a new named save slot in a fresh, isolated memory-card image.
- Starting that slot reaches the original German story-introduction screen.
- The saved slot is recognized after restarting the executable with the same
  private profile; starting it reaches the original opening ship/dragon scene.
- The in-game pause screen responds to the configured Start input.
- Returning from pause shows the opening ship/dragon encounter with the original
  German action prompt. Independent movement/action verification remains open.

The probes use an isolated Xvfb display, software Vulkan (Lavapipe), and dummy
audio. They do not establish hardware performance, audible audio, DualSense
operation or PS5 gameplay. A controllable scene and a saved gameplay checkpoint
are the next PC checks; recognizing a new slot does not prove complete save/load.
Do not label an attract video as playable gameplay.

All captures, runtime logs, memory cards, disc registrations, source exports,
game libraries and executables remain under ignored private directories or
dedicated Linux build caches. Do not attach them to a public issue or release.

## Actual PS5 compilation

`ps5/CMakeLists.txt` and `tools/build_ps5_game.py` cross-compile the 794 real game
translation units from Foxhollow's existing source list into a private archive.
This completed successfully with the open payload SDK revision
`611893fc25ef3e138f5bc2c90d829d8b58174cd2`, Clang 18.1.3, target
`x86_64-sie-ps5`, and the actual MusyX and target-generated zlib headers.
The archive contains x86-64 ELF objects; an ELF object header alone cannot
distinguish this target from other x86-64 systems, so the compiler target and
recipe are recorded separately.

This target has no executable, platform replacements, package or deployment.
Unresolved references are expected in an archive and have not been passed off
as a successful runtime link. No console application or CPU-test toast was sent.

## Next integration work

1. Finish the PC reference checks with the private profile: verify movement and
   action effects in an original scene, then test audio and a gameplay checkpoint
   save/load. Keep the source reference unchanged.
2. Add the real SFA PS5 platform build around that reference. The locally
   inspected MIT platform code from PS5_Dusklight revision
   `577c76212bec33198d69ca727433573ec00beb78` is a platform reference only.
   Its general code may be adapted with notices; do not copy the other game's
   assets, identity, menus, installed app, data or save paths.
3. Foxhollow and the existing open PS5 reference use the same Dawn source pin,
   `1155e0ed531126f33a1279afa029349651ca1c93`, and SDL `release-3.4.10`.
   Adapt the actual Aurora surface binding, patched Dawn Vulkan/display path,
   SDL video/audio/DualSense drivers, disc reader, startup and link recipe.
   Do not replace missing graphics or input with success-returning stubs.
4. Inspect optional Foxhollow code-mod/network/crash facilities for the PS5.
   The hook resolver explicitly handles Windows, Apple and Linux. Do not
   assume a Linux implementation works on the PS5's FreeBSD-derived target.
   Disabling optional features must be explicit and must preserve required
   controls/frame-pump/game initialization.
5. Keep user data outside replaceable app files, determine a separate title
   identity, and then test an actual graphical PS5 candidate on hardware.

PC output uses a Dawn prebuilt package; it is not a PS5 library. A successful
PS5 game archive does not supply Dawn, SDL, audio, disc access or the OS startup.

## Publication boundary

No playable PS5 port, public game release or SFA store listing exists yet.
No version or release-candidate status was advanced for this tooling work.
Keep the owned disc and all original/derived game programs and assets private.
Upstream CC0/MIT notices are a preliminary dependency check, not comprehensive
rights clearance for distribution. Retain all applicable notices and perform
the package/provenance audit before publishing any runtime.

The existing PAL and NTSC-U gameplay-evidence requirements remain in effect.
The user does not own an NTSC-U image; use the existing community workflow
rather than asking again or claiming an unperformed regional test.

Private evidence: `local-tests/pc-reference/build-receipt.json`, the timestamped
PC probe directories, `local-tests/pc-reference/reviewed-observations.json`, and
`local-tests/ps5-game/build-receipt.json`.
