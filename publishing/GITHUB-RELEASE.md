# GitHub release status

Updated: 19 October 2026 (Europe/Berlin).

The repository is published as an **unreleased development snapshot**. This
is a synchronized source and documentation update, not a game release.

## Current state

- No version tag has been created.
- No GitHub Release or downloadable artifact exists.
- No ISO, original executable, extracted game content, shader, save image or
  derived game binary is published.
- The PC reference has been built privately and the game translation units
  have been compiled privately for the open PS5 toolchain. There is still no
  linked PS5 executable, deployment or verified PS5 gameplay.
- The public tooling verification for this snapshot is green: CTest 3/3 and
  the Python preparation/release suite 27/27 in the existing WSL environment.
  These checks validate the tooling only; they are not console gameplay proof.
- The Coming soon catalog reservation is [PR #421](https://github.com/darkxex/ps5-homebrew-catalog/pull/421)
  for **Foxhollow PS5** (`PPSA99573`); it remains pending maintainer review.

## Release gate

The first downloadable release remains blocked until one candidate build has
passed the documented native PS5 integration checks, real PAL and NTSC-U
gameplay evidence, DualSense/audio/save-load checks, dependency and license
review, and a package audit that confirms only user-provided game media is
read locally. A catalog placeholder does not waive these requirements.

When those conditions are met, create a separately reviewed version tag and
GitHub Release whose assets contain only the newly authored code and permitted
open-source dependencies. Keep the user's disc image and all derived game
data outside the release.
