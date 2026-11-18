# ashuvidz-website

The static landing page of [ashuvidz.com](https://ashuvidz.com): one HTML file and its images,
no build step, no framework. It links to the YouTube and Twitch channels, the community Discord
and forum, the recruitment Discord and the partner links.

The site is served by the nginx chart in the homelab repository
(`cluster/helm/ashuvidz-website`, <https://github.com/vyrtualsynthese/homelab>), which clones the
`main` branch of this repository every 60 seconds. **A merge into `main` is a deployment.**

## Quick start

```sh
python3 -m http.server 8080
```

Open <http://localhost:8080>. Any static file server works; there is nothing to install or
compile.

## Update and deploy

1. Branch from `develop`, commit, open a pull request into `develop`.
2. When `develop` is ready, open the release pull request `develop` → `main`.
3. The pod picks up `main` within 60 seconds; hard-reload the page to see the change.

Never commit to `main` or `develop` directly. If the pod serves an old page, its git-sync
sidecar has not run yet or failed; check `kubectl logs` on the `ashuvidz` deployment.

## What is in here

| Path | Purpose |
|---|---|
| `index.html` | The whole page: markup, styles and text. |
| `assets/` | Hero background, logo, social preview image, favicon artwork and the self-hosted Poppins font. |
| `favicon.ico` | Browser tab icon, generated from the logo. |
| `robots.txt`, `sitemap.xml` | Crawler rules and the one-URL sitemap. |
| `404.html` | Not-found page. The homelab chart must map it with `error_page` before nginx serves it. |

Because nginx serves the repository root, every file committed here is downloadable from the
site. `robots.txt` keeps crawlers out of the Markdown files, but it is not access control.

## Assets

The hero is a 1920×1080 WebP and the logo a 400×400 WebP, both already resized for display.
Keep new images in the same shape: WebP for photos and gradients, no unused source files in the
repository. `assets/og-image.jpg` is the 1200×630 social preview used by the Open Graph and
Twitter meta tags.

The Poppins font is self-hosted from `assets/fonts/`, two weights and two character subsets,
so no visitor request leaves for a font CDN. Its SIL Open Font License sits next to the files in
`assets/fonts/OFL.txt`.
