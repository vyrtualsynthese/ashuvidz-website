# ashuvidz-website

The static signpost of [ashuvidz.com](https://ashuvidz.com): hand-written HTML and CSS, no build
step, no framework. It sends visitors to the YouTube channel, Twitch and the Discord, and carries
two inner pages. Every page exists twice, in French and in English.

The site is served by the nginx chart in the homelab repository
(`cluster/helm/ashuvidz-website`, <https://github.com/vyrtualsynthese/homelab>), which clones the
`main` branch of this repository every 60 seconds. **A merge into `main` is a deployment.**

## Quick start

```sh
python3 -m http.server 8080
```

Open <http://localhost:8080>. Any static file server works; there is nothing to install or
compile.

Then check the tree before you trust it:

```sh
python3 scripts/check_site.py
python3 -m unittest discover -s tests
```

The checker needs nothing but the Python standard library. It reads every page and reports broken
internal links, empty `href`, missing head metadata, a broken French/English twin, hreflang that
does not point back, a page missing from the sitemap, French typography slips and external links
without the right `rel`. It prints one line per problem and exits non-zero when there is any.

## Update and deploy

1. Branch from `develop`, commit, open a pull request into `develop`.
2. Run `python3 scripts/check_site.py` and `python3 -m unittest discover -s tests`; both must be
   clean before you open the pull request.
3. When `develop` is ready, open the release pull request `develop` → `main` and merge it with
   **Create a merge commit**. A squash or rebase merge rewrites the commits and leaves `develop`
   with no shared history with `main`; the next release then conflicts instead of applying.
4. The pod picks up `main` within 60 seconds; hard-reload the page to see the change.

Never commit to `main` or `develop` directly. If the pod serves an old page, its git-sync
sidecar has not run yet or failed; check `kubectl logs` on the `ashuvidz` deployment.

## What is in here

| Path | Purpose |
|---|---|
| `index.html` | The French home page: the promise and the three destinations. |
| `moi/index.html` | The French about page: who is behind the channel, and every profile. |
| `partenaires/index.html` | The French partners page: paid formats, audience figures, clients. |
| `en/index.html`, `en/about/index.html`, `en/partners/index.html` | The same three pages in English. |
| `assets/site.css` | The one stylesheet: palette, type, header, hero, inner pages. |
| `assets/fonts/` | Anton and IBM Plex Mono as WOFF2, each with its SIL Open Font License. |
| `assets/` | Hero background, logo, social preview, favicon artwork. |
| `favicon.ico` | Browser tab icon, generated from the logo. |
| `scripts/check_site.py` | The pre-merge check described under Quick start. |
| `tests/` | The checker's own tests and their fixture trees. Not part of the site. |
| `robots.txt`, `sitemap.xml` | Crawler rules and the six-URL sitemap. |
| `404.html` | Not-found page, bilingual and `noindex`. The homelab chart must map it with `error_page` before nginx serves it. |

French is the default language and lives at the root: `/`, `/moi/`, `/partenaires/`. English is a
mirror under `/en/` with translated slugs: `/en/`, `/en/about/`, `/en/partners/`. Each page carries
a language switch, a canonical URL and three `hreflang` links that point at its twin and back.
Adding a page means writing both halves in the same commit, or the checker fails.

Because nginx serves the repository root, every file committed here is downloadable from the
site. `robots.txt` keeps crawlers out of the Markdown files, but it is not access control.

## Assets

The hero is a 1920×1080 WebP and the logo a 400×400 WebP, both already resized for display.
Keep new images in the same shape: WebP for photos and gradients, no unused source files in the
repository. `assets/og-image.jpg` is the 1200×630 social preview used by the Open Graph and
Twitter meta tags.

The two fonts are self-hosted from `assets/fonts/` as WOFF2, so no visitor request leaves for a
font CDN. Each has its SIL Open Font License next to it: `OFL-Anton.txt` and
`OFL-IBMPlexMono.txt`.
