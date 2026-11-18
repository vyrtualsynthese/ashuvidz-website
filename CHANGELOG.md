# Changelog

All notable changes to this repository are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Three pages in two languages, six URLs: the home page at `/`, the about page at `/moi/`, the
  partners page at `/partenaires/`, and their English twins at `/en/`, `/en/about/` and
  `/en/partners/`. Each page carries a language switch, a canonical URL and reciprocal `hreflang`
  links.
- `assets/site.css`, one stylesheet for every page: the brand palette (void, night, paper, coral),
  Anton for headlines, IBM Plex Mono for labels and system fonts for prose. No build step.
- `scripts/check_site.py` and `tests/`, a standard-library checker that fails on broken internal
  links, empty `href`, missing head metadata, a missing or non-reciprocal language twin, a page
  absent from the sitemap, French typography slips and external links without the right `rel`.
- The partners page: the two paid formats, the audience figures measured on 2 November 2026, the
  client list (ArenaNet and NCSoft, Pearl Abyss, Square Enix), the game-key policy and rates on
  request. The page is built for the corporate reader, not for the audience.
- Repository scaffolding: this changelog, a README describing the local preview and the deployment
  path, and a `develop` integration branch. The homelab nginx pod still deploys `main`.
- `favicon.ico`, `assets/apple-touch-icon.png` and `assets/og-image.jpg` (1200×630). The page
  referenced `favicon.ico` but the file had never been committed, so every visit logged a 404, and
  the social preview pointed at a WebP that some platforms do not accept.
- Poppins is self-hosted from `assets/fonts/` (weights 400 and 600, Latin and Latin Extended),
  replacing a `font-family` declaration that named a font the browser never loaded and silently
  fell back to the system sans-serif.
- `robots.txt`, `sitemap.xml` and `404.html`. The not-found page still needs an `error_page`
  directive in the homelab chart before nginx serves it.
- Canonical URL, `theme-color`, `og:site_name`, `og:locale` and Open Graph image dimensions.

### Changed

- The home page is a signpost again: one promise, three destinations (YouTube first, then Twitch
  and Discord). The recruitment, forum, wiki and Reddit blocks are gone.
- The visual identity follows `creator/brand/visual-identity.md`: void and night grounds, paper
  text, one coral accent, Anton headlines and IBM Plex Mono labels, with the plate graded toward
  coral on the home page only.
- The hero background is delivered at 1920×1080 instead of 2560×1440, and the logo at 400×400
  instead of 800×800. The page now transfers about 80 KB of images where it used to transfer
  580 KB.
- Section titles are `<h2>` headings inside `<main>`, the social rows are labelled `<nav>`
  landmarks, and a skip link reaches the content from the keyboard.
- Icon-only links carry accessible names; decorative icons are hidden from screen readers.
- Focus outlines are visible, and the entrance animations turn off under
  `prefers-reduced-motion`.
- The index is no longer one file with an inline `<style>` block: markup and styles are split, and
  the shared header and footer are repeated per page because there is no build step.
- The footer copyright year is 2026.

### Fixed

- Every link that opens in a new tab now sends `rel="noopener noreferrer"`; none did before.
- The Amazon partner link pointed at `amzn.tu`, a domain that does not resolve, so the affiliate
  link was dead. It is `amzn.to` again.

### Removed

- Poppins and Font Awesome. Anton and IBM Plex Mono replace them, and the icons were decoration
  that the copy did not need.
- The forum link, which answers 404, and the recruitment Discord card, which promised a slot the
  channel cannot fill.
- The Reddit rows, unmaintained for years.
- The "Wiki Communautaire" card. `wiki.ashuvidz.com` was retired on 2026-11-18 and answers 404.
- The "Organisation Star Citizen" recruitment card, which linked to `#` and never had a
  destination. Add it back with a real URL when there is one.
- The unused `Ashuvidz_BG.jpg` and `Ashuvidz_Logo_trans.png` sources, the two
  `*:Zone.Identifier` files, and the tracked `.idea/` project files. Git history keeps them.

## [1.0.0] - 2025-08-12

### Added

- The landing page: hero with the logo and channel buttons, the community, recruitment and partner
  cards, the social rows, and the contact footer.
