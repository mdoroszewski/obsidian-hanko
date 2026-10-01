# Changelog

All notable changes to Hanko are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.1] - 2026-10-01

Fixes the 63 warnings from the automated review on community.obsidian.md: 58 for `:has()` selectors and 5 for `text-decoration` properties that Obsidian 1.5.8 supports only partially. Apart from the points below, nothing changes on screen.

### Fixed

- File explorer: top-level folder colours no longer need `:has()`. The colour sits on the folder title and the list below it; open folders look as before, also with soft folder colours.
- Home Tab: the seal replaces the Obsidian logo without `:has()`.
- Links: the red underline is a 1px border instead of `text-decoration-color`. Unresolved links keep a dashed grey line. Bases group headings and card titles, day cards and Readwise sources stay without a line.

### Changed

- Links: on external links the red line also runs under the small arrow icon.
- Empty tab: actions are underlined in ink instead of red on hover.

### Removed

- Readwise: the cards around highlights. They required `:has()`. The small cover and the grey "View Highlight" source stay.

### Added

- Contributing guide.

## [1.0.0] - 2026-10-01

First release.

### Added

- Paper on concrete in light mode, Wada's Black in dark mode.
- Top-level folders as solid pills on Sanzo Wada's plates No. 279 (light) and No. 293 (dark), Raw Sienna always first. Plate No. 327 as an alternative in light mode. Folders whose name contains "archive" turn grey.
- The seal on notes with `cssclasses: seal`, on the empty tab and next to the vault name.
- Bold text in the anchor colour: Burnt Sienna in light mode, Raw Sienna in dark mode. Other tones selectable.
- Note building blocks: focus mode, daily, weekly and monthly pages, `[!days]` cards, evidence and status tags, Bullet Journal task states, role callouts, footnotes as "Sources".
- Plugin styles for Bases, Kanban, Canvas, Keep the Rhythm, Home Tab, Readwise, Tasks, Iconize and Style Settings.
- Style Settings options for the seal, colour, focus and form.
- Mobile refinements.

[Unreleased]: https://github.com/mdoroszewski/obsidian-hanko/compare/1.0.1...HEAD
[1.0.1]: https://github.com/mdoroszewski/obsidian-hanko/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/mdoroszewski/obsidian-hanko/releases/tag/1.0.0
