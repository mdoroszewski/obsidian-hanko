# Contributing to Hanko

Thanks for helping. Hanko is small on purpose, so the rules are short.

## Reporting a problem

Open an [issue](https://github.com/mdoroszewski/obsidian-hanko/issues) with:

- your Obsidian version and platform (desktop or mobile, light or dark mode),
- which plugins are involved, if any,
- a screenshot and, if you can, the smallest note that shows the problem.

## Suggesting a change

Open an issue first if the change is bigger than a fix, so we can agree on it before you spend time.

Pull requests are welcome. Please keep them to one topic and describe what changes on screen, ideally with a before and after screenshot in light and dark mode.

## Rules for the CSS

- Everything stays in `theme.css`. No network requests: images and icons are embedded as `data:` URLs.
- No `!important` and no `:has()`. Keep selectors simple and prefer Obsidian's CSS variables over new selectors.
- Every text and background pair reaches at least 4.5:1 in light and dark mode.
- Colours come from Sanzo Wada's *A Dictionary of Color Combinations*. Raw Sienna is the anchor colour and comes first in every plate.
- Settings for Style Settings are written in English. Class names and tags you type in notes are English too (`seal`, `focus`, `daily-page`, `#evidence/…`, `#status/…`).

## Releases

The version in `manifest.json` and the Git tag are the same number (for example `1.0.1`). Pushing the tag creates a draft release with `manifest.json` and `theme.css`.
