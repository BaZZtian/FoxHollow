<p align="center">
  <img src="assets/branding/foxhollow-icon-v2.png" width="160" height="160" alt="FoxHollow project icon">
</p>

<h1 align="center">FoxHollow</h1>

<p align="center">
  <strong>Star Fox Adventures on PlayStation 5</strong><br>
  An independent native PS5 homebrew project by <a href="https://github.com/BaZZtian">BaZZtian</a>.
</p>

<p align="center">
  <a href="#status-and-availability"><img src="https://img.shields.io/badge/status-in%20development-orange" alt="Status: in development"></a>
  <img src="https://img.shields.io/badge/platform-PS5%20homebrew-003791" alt="Platform: PS5 homebrew">
  <a href="#requirements"><img src="https://img.shields.io/badge/game%20data-Own%20GameCube%20ISO-555555" alt="Game data: Own GameCube ISO"></a>
</p>

<p align="center">
  <a href="#status-and-availability">Status</a> &middot;
  <a href="#installation">Installation</a> &middot;
  <a href="#compatibility">Compatibility</a> &middot;
  <a href="#support">Support</a> &middot;
  <a href="#credits-and-licenses">Credits &amp; licenses</a>
</p>

## About

FoxHollow brings the native [Foxhollow](https://github.com/JackPriceBurns/foxhollow)
foundation to a dedicated PS5 homebrew project. That foundation is built on
[SFA-Decomp](https://github.com/zcanann/SFA-Decomp) and
[Aurora](https://github.com/encounter/aurora).

Maintained by **BaZZtian**, with the goal of a standalone PS5 homebrew title
using native graphics, audio and DualSense input. FoxHollow is dedicated to
this game and uses the native PC port as its foundation.

<p align="center">
  <img src="assets/branding/foxhollow-background-v3.png" width="900" alt="FoxHollow original project artwork; not a gameplay screenshot">
</p>

## Status and availability

> [!WARNING]
> **In development. No playable PS5 download is available yet.**

The project is still being implemented and tested. A planned disc profile is not verified PS5 gameplay support.

## Requirements

- A homebrew-capable PlayStation 5. Target firmware: **12.40**.
- Your own legally obtained **Star Fox Adventures** GameCube disc image.

**No game data is included.** Disc images, original game code, textures, music
and saves must not be uploaded to this repository or attached to issues.

## Installation

Installation instructions will accompany the first tested app release on the
[Releases page](https://github.com/BaZZtian/PS5-FoxHollow/releases).

## Compatibility

| GameCube edition | Disc ID | PS5 gameplay |
| --- | --- | --- |
| Europe / PAL | `GSAP01` | Not verified |
| North America / NTSC-U | `GSAE01` | Not verified |

These are planned disc profiles. Disc identification does not establish gameplay compatibility or support for every revision.

## Support

Use [GitHub Issues](https://github.com/BaZZtian/PS5-FoxHollow/issues) for project questions and reproducible problem reports. Include the project revision, disc region and revision, reproduction steps, expected result and actual result.

Do not attach disc images, extracted game files, music, saves, memory dumps, keys, credentials or proprietary SDK material. Remove personal information before sharing reports.

## Credits and licenses

This project depends on the work of the following upstream communities:

| Project | Authors / maintainers | Contribution |
| --- | --- | --- |
| [SFA-Decomp](https://github.com/zcanann/SFA-Decomp) | zcanann and SFA-Decomp contributors | Star Fox Adventures decompilation forming the native foundation |
| [Foxhollow](https://github.com/JackPriceBurns/foxhollow) | JackPriceBurns and Foxhollow contributors | Native PC port used as the PS5 integration reference |
| [Aurora](https://github.com/encounter/aurora) | encounter and Aurora contributors | Graphics compatibility framework used by the native foundation |
| [ps5-payload-sdk](https://github.com/ps5-payload-dev/sdk) | Open PS5 payload SDK contributors | Open homebrew target toolchain |

### Licensing

SFA-Decomp and Foxhollow publish CC0-1.0 declarations. Their notices and those
of separately licensed dependencies remain applicable. A root license does
not automatically cover every nested component or the original game data.

The existing [MIT license](LICENSE) covers the independently authored code
previously distributed under that grant. Upstream components retain their own
licenses, copyright notices and attribution.

This is an unofficial homebrew project, not affiliated with, endorsed by or
sponsored by Nintendo or Rare. Original game content remains the property of
its respective rights holders.
