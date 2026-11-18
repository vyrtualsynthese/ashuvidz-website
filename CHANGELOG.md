# Changelog

All notable changes to this repository are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

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

- The hero background is delivered at 1920×1080 instead of 2560×1440, and the logo at 400×400
  instead of 800×800. The page now transfers about 80 KB of images where it used to transfer
  580 KB.
- Font Awesome is pinned to 6.7.2 with a Subresource Integrity hash.
- Section titles are `<h2>` headings inside `<main>`, the social rows are labelled `<nav>`
  landmarks, and a skip link reaches the content from the keyboard.
- Icon-only links carry accessible names; decorative icons are hidden from screen readers.
- Focus outlines are visible, and the entrance animations turn off under
  `prefers-reduced-motion`.
- The footer copyright year is 2026.

### Fixed

- All 23 links that open in a new tab send `rel="noopener noreferrer"`.
- The Amazon partner link pointed at `amzn.tu`, a domain that does not resolve, so the affiliate
  link was dead. It is `amzn.to` again.

### Removed

- The "Wiki Communautaire" card. `wiki.ashuvidz.com` was retired on 2026-11-18 and answers 404.
- The "Organisation Star Citizen" recruitment card, which linked to `#` and never had a
  destination. Add it back with a real URL when there is one.
- The unused `Ashuvidz_BG.jpg` and `Ashuvidz_Logo_trans.png` sources, the two
  `*:Zone.Identifier` files, and the tracked `.idea/` project files. Git history keeps them.

## [1.0.0] - 2025-08-12

### Added

- The landing page: hero with the logo and channel buttons, the community, recruitment and partner
  cards, the social rows, and the contact footer.
