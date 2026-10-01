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

## Commit messages

Commits follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```
type(scope): what the commit does, in the imperative

Why the change is needed and anything a reader cannot see in the
diff. Wrap lines at 72 characters.
```

- Types: `feat` (new styling or option), `fix` (something looks or works wrong), `docs`, `refactor` (same look, different CSS), `chore`.
- The scope names the part of Obsidian or the plugin, for example `file-explorer`, `links`, `home-tab`, `readwise`, `bases`, `settings`.
- One topic per commit.
- Every change people can see gets an entry in `CHANGELOG.md` under "Unreleased".

## Releases

1. Move the "Unreleased" entries in `CHANGELOG.md` under the new version.
2. Raise the version in `manifest.json` and commit both as `chore(release): 1.0.2`.
3. Tag that commit with the same number (`1.0.2`) and push the tag. The workflow creates a draft release with `manifest.json` and `theme.css`.
4. Paste the version's section from `CHANGELOG.md` into the release notes and publish the release.
