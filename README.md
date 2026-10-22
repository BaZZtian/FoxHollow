<p align="center">
  <img src="assets/branding/foxhollow-icon-v2.png" width="160" alt="FoxHollow fox emblem">
</p>

<h1 align="center">FoxHollow</h1>
<p align="center"><strong>A dedicated native PlayStation 5 port project for Star Fox Adventures.</strong></p>
<p align="center">Target firmware 12.40 | Bring your own GameCube disc image</p>

![FoxHollow original project artwork](assets/branding/foxhollow-background-v3.png)

## About

FoxHollow brings the native [Foxhollow](https://github.com/JackPriceBurns/foxhollow)
foundation to a dedicated PS5 homebrew project. That foundation is built on
[SFA-Decomp](https://github.com/zcanann/SFA-Decomp) and
[Aurora](https://github.com/encounter/aurora).

Maintained by **BaZZtian**, with the goal of a standalone PS5 homebrew title
using native graphics, audio and DualSense input. FoxHollow is dedicated to
this game and uses the native PC port as its foundation.

**Status: in development. A playable PS5 download is not available yet.**

## Requirements

- A homebrew-capable PlayStation 5. Target firmware: **12.40**.
- Your own legally obtained **Star Fox Adventures** GameCube disc image.

The planned disc profiles are **Europe / PAL (`GSAP01`)** and
**North America / NTSC-U (`GSAE01`)**. PS5 gameplay compatibility is still
being implemented and tested.

**No game data is included.** Disc images, original game code, textures, music
and saves must not be uploaded to this repository or attached to issues.

## Download and installation

Installation instructions will accompany the first tested app release on the
[Releases page](https://github.com/BaZZtian/PS5-FoxHollow/releases).

## Credits

This project depends on the work of the following upstream communities:

| Project | Authors / maintainers | Contribution |
| --- | --- | --- |
| [SFA-Decomp](https://github.com/zcanann/SFA-Decomp) | zcanann and SFA-Decomp contributors | Star Fox Adventures decompilation forming the native foundation |
| [Foxhollow](https://github.com/JackPriceBurns/foxhollow) | JackPriceBurns and Foxhollow contributors | Native PC port used as the PS5 integration reference |
| [Aurora](https://github.com/encounter/aurora) | encounter and Aurora contributors | Graphics compatibility framework used by the native foundation |
| [ps5-payload-sdk](https://github.com/ps5-payload-dev/sdk) | Open PS5 payload SDK contributors | Open homebrew target toolchain |

## Licensing and attribution

SFA-Decomp and Foxhollow publish CC0-1.0 declarations. Their notices and those
of separately licensed dependencies remain applicable. A root license does
not automatically cover every nested component or the original game data.

The existing [MIT license](LICENSE) covers the independently authored code
previously distributed under that grant. Upstream components retain their own
licenses, copyright notices and attribution.

This is an unofficial homebrew project, not affiliated with, endorsed by or
sponsored by Nintendo or Rare. Original game content remains the property of
its respective rights holders.
