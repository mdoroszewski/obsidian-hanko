# Changelog

All notable changes to Hanko are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.1.2] - 2026-10-05

Clears the remaining size warning of the directory's scan. Nothing changes on screen.

### Changed

- `theme.css` is 97.8 KB instead of 110.9 KB. The multi-line comments that explained design decisions are gone; the reasons live in `README.md` and this changelog. Short notes such as colour names stay. The contributing guide now states the 100 KB limit and the comment rule, and the tests check it.

## [1.1.1] - 2026-10-04

Clears the two warnings the directory's scan raised for 1.1.0. Nothing changes on screen.

### Fixed

- Print: `break-inside: avoid` on callouts and embeds is gone. The scan counts it as css-multicolumn, which Obsidian 1.5.8 supports only partially.
- Size: `theme.css` is 110.9 KB instead of 118.9 KB, under the directory's size warning. Task states share one rule and set their glyph and tone as custom properties; the longer comments are shorter. The tests now check both.

## [1.1.0] - 2026-10-04

Takes up what the ten most downloaded community themes do well, where it fits Hanko: the Minimal set of task states and helper classes, image and plugin refinements, a second stage of focus, and a colour concept that leans harder on the Wada plates. Everything that appears on hover is desktop only; iOS keeps `:hover` after a tap, so touch devices keep their header and bars.

### Added

- Tasks: the Minimal set of task states, `[*]` star, `["]` quote, `[i]` info, `[I]` idea, `[b]` bookmark, `[l]` location, `[p]` pro, `[c]` con, `[k]` key, `[f]` urgent, `[w]` win, `[u]` up, `[d]` down, `[S]` amount, as line glyphs in ink. Four carry a role tone: pro green, urgent red (as a ring, unlike the filled `[!]`), star in the anchor tone, con in ink.
- Helper classes via `cssclasses`: `wide` (50 rem), `max` (full width), `table-wide`, `img-wide`, `wide-dataview`, `table-small`, `row-alt`, `img-grid` (also `img-grid-2`, `img-grid-4`).
- Callout modifiers `[!type|no-title]`, `|no-icon` and `|plain` (no card, only a line in the role colour).
- Images: captions from the alt text (switch, off by default; file names are never shown) and zoom while clicking and holding (switch to turn off).
- Embeds: a switch for seamless embeds without frame and title.
- Dataview: tables, lists and inline fields styled like Bases.
- Calendar plugin: days in ink, today as a ring in the anchor tone, dots in the anchor tone.
- Tasks plugin: dates, backlinks and tools small and grey, like source references.
- Kanban: lanes carry the Wada plate by position, like top-level folders. "Do not colour folders and lanes" turns both off.
- Focus, second stage: note header appears on hover, bars step back (tab bar and status bar to 28 percent), faded Markdown syntax in Live Preview, a mark on the active line. The first two are desktop only.
- Print and PDF export: white paper, ink links, no seal.
- Style Settings group "Content" (captions, zoom, seamless embeds) and the switch "Neutral surfaces".
- Test suite in `tests/`.

### Changed

- Colour: state surfaces (second surface, hover, text selection, row under the pointer, selected file, scrollbar) take a whisper of the plate of the mode instead of neutral grey: light Ecru and Vinaceous Cinnamon from No. 279, dark Artemesia Green and Turquoise Green from No. 293. "Neutral surfaces" restores grey.
- Colour: the "check" tone in light mode is Dark Tyrian Blue from plate No. 279 instead of Deep Lyons Blue. Affects recall and review callouts, `#evidence/contested`, `#status/waiting` and the bold option "Indigo". Dark mode keeps Salvia Blue.
- Keep the Rhythm: the light heatmap runs in the warm tones of plate No. 279 (Vinaceous Cinnamon, Ecru, Raw Sienna, Burnt Sienna) instead of the greens of No. 293, which belong to dark mode.

### Fixed

- Footnotes: the list label is "Sources" in the theme, as documented. A vault snippet can set another word.
- Empty tab: the hover line under actions is a border, not `text-decoration`.
- Seal: blend mode and opacity apply only to notes that carry the seal, not to every note's `::before`.
- Two stale comments in the CSS.

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

[Unreleased]: https://github.com/mdoroszewski/obsidian-hanko/compare/1.1.2...HEAD
[1.1.2]: https://github.com/mdoroszewski/obsidian-hanko/compare/1.1.1...1.1.2
[1.1.1]: https://github.com/mdoroszewski/obsidian-hanko/compare/1.1.0...1.1.1
[1.1.0]: https://github.com/mdoroszewski/obsidian-hanko/compare/1.0.1...1.1.0
[1.0.1]: https://github.com/mdoroszewski/obsidian-hanko/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/mdoroszewski/obsidian-hanko/releases/tag/1.0.0
