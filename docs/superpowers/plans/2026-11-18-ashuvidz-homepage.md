# AshuVidz Homepage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the single landing page with a three-page, two-language signpost (home, about, partners) in the channel's own visual identity, with no build step and no backend.

**Architecture:** Six hand-written HTML pages (French at `/`, `/moi/`, `/partenaires/`; English under `/en/`), one shared `assets/site.css`, self-hosted Anton and IBM Plex Mono, and a stdlib Python checker that fails on broken links, missing twins, broken hreflang, sitemap drift and French typography mistakes. nginx serves the repository root; a merge into `main` deploys.

**Tech Stack:** HTML5, CSS (no framework, no preprocessor), a single inline SVG data URI for grain, Python 3 standard library for the checker and its `unittest` suite. No JavaScript.

**Spec:** `docs/superpowers/specs/2026-11-18-ashuvidz-homepage-design.md`

## Global Constraints

- Palette tokens, exact: `--void:#0A0F1E`, `--ink:#05070F`, `--night:#141B2E`, `--paper:#F4EFE6`, `--muted:#8C97B0`, `--coral:#F2545B`. Coral is the only accent.
- Two composed typefaces: Anton for titles, IBM Plex Mono for labels. Body prose uses `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`. Poppins and Font Awesome are removed.
- Zero external requests: fonts self-hosted, no CDN, no icon font, no analytics, no JavaScript.
- French typography on every `lang="fr"` page: non-breaking space `U+00A0` before `:` and `;`, thin non-breaking space `U+202F` before `!` and `?`, typographic apostrophe `’`, accented capitals, thousands with `U+00A0`. No em dash `U+2014`, no en dash `U+2013`, no straight apostrophe `'`, no full stop at the end of a heading.
- Voice: `vous`, precise, patient, complicit. No swear word, no `TOP 5`, no schedule.
- No schedule, no live badge, no backend, no build step.
- Every page: `lang`, `<title>`, meta description, self canonical, `og:title`, `og:description`, `og:image`, `og:url`, exactly one `<h1>`.
- Never link a destination that does not answer. The forum, the wiki, AshuWorld, Reddit and the old recruitment Discord stay off the site.
- Deploy path: branch from `develop`, PR into `develop`, release `develop` to `main`. Never commit to `main` or `develop`.

## Review Focus

1. A page added or edited without its twin, or with a one-way `hreflang` link, must fail the check rather than ship. Pinned by `Tests/…broken-hreflang` in Task 1.
2. French copy containing a straight apostrophe, a normal space before `!`, or an em dash must fail before review. Pinned by `broken-typo` in Task 1.
3. A public page missing from `sitemap.xml`, or a sitemap entry with no page behind it, must fail. Pinned by `broken-sitemap` in Task 1.
4. On a 360px-wide screen the English strings are longer than the French ones, and the hero must not push the buttons under the footer or force a horizontal scroll. Verified by hand in Task 2 and Task 6.
5. Keyboard only: the skip link, the brand, the language switch and the three buttons must all show a visible coral focus ring over the plate. Verified by hand in Task 6.

---

## File Structure

| Path | Responsibility |
|---|---|
| `index.html` | French home: nav, hero, footer |
| `en/index.html` | English home, twin of the above |
| `moi/index.html` | French about |
| `en/about/index.html` | English about |
| `partenaires/index.html` | French partners |
| `en/partners/index.html` | English partners |
| `404.html` | one bilingual not-found page, `noindex` |
| `assets/site.css` | every style the six pages use |
| `assets/fonts/Anton-Regular.woff2` | copied from the brand kit |
| `assets/fonts/IBMPlexMono-Regular.woff2` | converted once from the brand TTF |
| `assets/fonts/OFL-Anton.txt`, `OFL-IBMPlexMono.txt` | licences that travel with the fonts |
| `assets/Ashuvidz_BG.webp`, `og-image.jpg` | kept unchanged |
| `scripts/check_site.py` | the checker, CLI `python3 scripts/check_site.py [ROOT]` |
| `tests/test_check_site.py` | `unittest` suite for the checker |
| `tests/fixtures/**` | one small site tree per rule, valid and broken |
| `sitemap.xml`, `robots.txt` | public URL list and crawler rules |
| `README.md`, `CHANGELOG.md` | how to preview and deploy; what changed |

Deleted by Task 2: `assets/fonts/poppins-*.woff2`, `assets/fonts/OFL.txt` (Poppins text), the Font Awesome `<link>`, and the whole inline `<style>` block of the old `index.html`.

---

### Task 1: The site checker

**Files:**
- Create: `scripts/check_site.py`, `tests/test_check_site.py`
- Create fixtures: `tests/fixtures/good/`, and one broken tree per rule

**Interfaces:**
- Produces: CLI `python3 scripts/check_site.py [ROOT]`, root defaults to the repository root. Prints one line per problem as `<path>: <RULE>: <message>` and exits `1`; prints nothing and exits `0` when clean.
- Rule IDs, used verbatim in tests: `LINK-INTERNAL`, `LINK-EMPTY`, `HEAD-REQUIRED`, `HREFLANG`, `PARITY`, `SITEMAP`, `FR-TYPO`, `EXTERNAL-REL`.

- [ ] **Step 1: Build the good fixture**

Create `tests/fixtures/good/` with `index.html`, `en/index.html`, `assets/site.css` (empty file is fine), and `sitemap.xml`. The French page carries `lang="fr"`, a self canonical `https://example.test/`, hreflang links to `fr`, `en` and `x-default`, the required og tags, one `<h1>`, a link to `/en/`, an internal image, and French text that passes `FR-TYPO`. The English page mirrors it at `https://example.test/en/` with `lang="en"` and its own canonical. The sitemap lists both URLs.

- [ ] **Step 2: Write the failing tests**

```python
class CheckSiteTest(unittest.TestCase):
    def run_check(self, name: str) -> subprocess.CompletedProcess:
        root = FIXTURES / name
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(root)],
            capture_output=True, text=True,
        )

    def test_good_tree_passes(self):        # exit 0, no output
    def test_internal_link_missing_file(self):   # LINK-INTERNAL
    def test_empty_href(self):                   # LINK-EMPTY
    def test_page_without_og_image(self):        # HEAD-REQUIRED
    def test_hreflang_not_reciprocal(self):      # HREFLANG
    def test_twins_link_different_hosts(self):   # PARITY
    def test_page_missing_from_sitemap(self):    # SITEMAP
    def test_straight_apostrophe_in_french(self):# FR-TYPO
    def test_blank_target_without_noopener(self):# EXTERNAL-REL
```

Each broken test asserts `returncode == 1` and that the rule ID appears in `stdout`. Copy the good tree, then break exactly one thing per tree.

- [ ] **Step 3: Run the suite and watch it fail**

Run: `python3 -m unittest discover -s tests -v`
Expected: FAIL, `check_site.py` does not exist yet.

- [ ] **Step 4: Implement `scripts/check_site.py`**

Standard library only: `html.parser`, `pathlib`, `re`, `sys`, `xml.etree.ElementTree`. Walk every `index.html` and `404.html` under the root. Rules, exactly:

- `LINK-INTERNAL`: for each `href`/`src` not starting with `http://`, `https://`, `mailto:`, `tel:`, `data:` or `#`, resolve against the page's directory; `/moi/` must resolve to `moi/index.html`. A missing file is a problem.
- `LINK-EMPTY`: `href` absent, `""`, or `#`.
- `HEAD-REQUIRED`: `lang`, `<title>`, `meta[name=description]`, `link[rel=canonical]`, `og:title`, `og:description`, `og:image`, `og:url`, and exactly one `<h1>`.
- `HREFLANG`: each page has `alternate` links for `fr`, `en`, `x-default`; the `en` link points at a page that links back, and `x-default` equals the `fr` URL. `canonical` equals the `alternate` link whose `hreflang` matches the page's own `lang`.
- `PARITY`: two pages joined by `hreflang` use the same set of outbound hosts and the same set of same-origin `src` paths.
- `SITEMAP`: parse `<loc>` values; every one maps to an existing page; every page except `404.html` appears exactly once.
- `FR-TYPO`: on `lang="fr"` pages only, across text nodes, outside `<script>` and `<style>`: `U+2013`, `U+2014`, `'` (`U+0027`), a `U+0020` immediately before `:` `;` `!` `?`, and a heading whose text ends with `.`.
- `EXTERNAL-REL`: every `<a>` with `target="_blank"` has `noopener` in `rel`; every link whose host is `instant-gaming.com`, `robertsspaceindustries.com` or `amzn.to` has `sponsored` in `rel`.

- [ ] **Step 5: Run the suite until green**

Run: `python3 -m unittest discover -s tests -v`
Expected: 9 tests, all PASS.

- [ ] **Step 6: Prove it on the real repository**

Run: `python3 scripts/check_site.py`
Expected today: problems listed for the old `index.html` (no twin, no hreflang, Poppins link), exit `1`. That is the baseline the next task fixes.

- [ ] **Step 7: Commit**

```bash
git add scripts tests
git commit -m "✨ feat: add a checker for links, twins, sitemap and French typography"
```

---

### Task 2: Fonts, stylesheet and the home pair

**Files:**
- Create: `assets/site.css`, `en/index.html`
- Modify: `index.html` (full replacement), `sitemap.xml`
- Create: `assets/fonts/Anton-Regular.woff2`, `assets/fonts/IBMPlexMono-Regular.woff2`, `assets/fonts/OFL-Anton.txt`, `assets/fonts/OFL-IBMPlexMono.txt`
- Delete: `assets/fonts/poppins-*.woff2`, `assets/fonts/OFL.txt`

**Interfaces:**
- Produces: the class contract every later page reuses. `site-header`, `site-header__inner`, `brand`, `site-nav`, `skip-link`, `lang-switch`, `hero`, `hero__plate`, `hero__veil`, `hero__copy`, `kicker`, `promise`, `lede`, `actions`, `btn`, `btn--primary`, `site-footer`, `site-footer__inner`.
- Produces: fonts at `assets/fonts/Anton-Regular.woff2` (weight 400), `assets/fonts/IBMPlexMono-Regular.woff2` (weight 400). Only these two files are loaded.

- [ ] **Step 1: Convert IBM Plex Mono to WOFF2**

```bash
python3 -m venv /tmp/fontvenv && /tmp/fontvenv/bin/pip -q install fonttools brotli
/tmp/fontvenv/bin/python -m fontTools.ttLib.woff2 compress \
  /home/vsynthese/projets/scripts/creator/brand/fonts/IBMPlexMono-Regular.ttf \
  -o assets/fonts/IBMPlexMono-Regular.woff2
cp /home/vsynthese/projets/scripts/creator/brand/fonts/Anton-Regular.woff2 assets/fonts/
rm -rf /tmp/fontvenv
```

Expected: `IBMPlexMono-Regular.woff2` exists and is smaller than the 136 KB TTF.

- [ ] **Step 2: Bring both licences and drop Poppins**

```bash
cp /home/vsynthese/projets/scripts/creator/brand/fonts/OFL.txt assets/fonts/OFL-IBMPlexMono.txt
curl -fsSL https://raw.githubusercontent.com/google/fonts/main/ofl/anton/OFL.txt -o assets/fonts/OFL-Anton.txt
git rm assets/fonts/poppins-400-latin.woff2 assets/fonts/poppins-400-latin-ext.woff2 \
       assets/fonts/poppins-600-latin.woff2 assets/fonts/poppins-600-latin-ext.woff2 \
       assets/fonts/OFL.txt
```

If the `curl` fails, copy the licence text out of the Anton TTF's `name` table with `fonttools` before deleting the venv, and say so in the commit body.

- [ ] **Step 3: Write `assets/site.css`**

Two `@font-face` blocks (`Anton`, `IBM Plex Mono`, `font-display: swap`, `local()` omitted). Then, in this order: tokens, reset, typography, skip link, header, nav, language switch, hero, buttons, footer, narrow-screen overrides, reduced motion.

Values that are decisions, not taste:

- `--max: 1120px`; horizontal padding `--gutter: clamp(1.25rem, 4vw, 2.75rem)`.
- Body: `background: var(--void); color: var(--paper); font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;`
- `.hero`: `min-height: 100svh; position: relative; display: grid; align-content: start;`
- `.hero__copy`: `padding-top: 24svh; max-width: 52%;` with a 900px override to `max-width: 100%; padding-top: 22svh;`
- `.hero__veil`, one rule: `linear-gradient(90deg, var(--void) 0%, rgba(10,15,30,.93) 34%, rgba(10,15,30,.35) 66%, rgba(10,15,30,.1) 100%)`, layered over `linear-gradient(180deg, rgba(10,15,30,.7), transparent 24%, rgba(10,15,30,.85))`.
- `.hero__plate`: `position:absolute; inset:0; background:url("Ashuvidz_BG.webp") center/cover no-repeat; filter: saturate(.85) brightness(.66);`
- `.promise` (Anton): `font-size: clamp(2.4rem, 5.2vw, 3.6rem); line-height: 1.06; text-transform: uppercase;` and `.promise em { color: var(--coral); font-style: normal; display: block; }`
- `.kicker` and nav labels (Plex Mono): `text-transform: uppercase; letter-spacing: .1em; font-size: .7rem; color: var(--muted);`
- `.btn`: pill, `padding: .65rem 1.15rem; border-radius: 999px; border: 1px solid rgba(244,239,230,.3);` and `.btn--primary { background: var(--coral); border-color: var(--coral); color: var(--void); }`
- Focus: `:focus-visible { outline: 3px solid var(--coral); outline-offset: 3px; }`
- Grain: `.hero::after` with the same inline SVG turbulence data URI used in the approved mock, `opacity:.35`.
- `@media (prefers-reduced-motion: reduce)`: no transition, no animation.
- One entrance animation: `.hero__copy { animation: rise .4s ease-out both }` from `opacity:0; translateY(8px)`.

- [ ] **Step 4: Write `index.html`**

Head, in this order: charset, viewport, title `AshuVidz, les MMO sans jargon`, meta description `Les MMO sans jargon, avec Ashu. Guild Wars 2, Star Citizen, et le direct sur Twitch.`, canonical `https://ashuvidz.com/`, `hreflang` fr/en/x-default, `og:*` with `og:image` `https://ashuvidz.com/assets/og-image.jpg`, `theme-color #0A0F1E`, favicon, apple-touch-icon, preload the plate and the Anton woff2, then `assets/site.css`. No `@font-face` in the page, no Font Awesome.

Body:

```
skip link
header.site-header
  a.brand  (img assets/Ashuvidz_Logo_trans.webp, alt AshuVidz, 44x44)
  nav.site-nav  Accueil (aria-current=page) · Moi · Partenaires
  p.lang-switch  FR (aria-current) · a[hreflang=en][lang=en] EN
main
  section.hero
    div.hero__plate (aria-hidden)
    div.hero__veil (aria-hidden)
    div.hero__copy
      p.kicker  DIRECT · MMO · DEPUIS 2012
      h1.promise  Les MMO,<em>sans jargon !</em>
      p.lede  Et vient jouer avec nous. Guild Wars 2 le plus souvent, Star Citizen quand il veut bien se lancer.
      div.actions  a.btn.btn--primary YouTube · a.btn Twitch · a.btn Discord
footer.site-footer
  a mailto ashuvidz@gmail.com · span © 2026 AshuVidz
```

All outbound links carry `target="_blank" rel="noopener noreferrer"`. YouTube, Twitch and Discord point at the verified URLs in the spec.

- [ ] **Step 5: Write `en/index.html`**

Same structure, twin head values (`https://ashuvidz.com/en/`, `lang="en"`, `og:locale en_GB`), nav `Home · About · Partners`, language switch back to `FR`, and: kicker `LIVE · MMO · SINCE 2012`, `h1` `MMOs,<em>no jargon!</em>`, lede `And come play with us. Guild Wars 2 most of the time, Star Citizen when it feels like launching.`, footer unchanged.

- [ ] **Step 6: Add both URLs to `sitemap.xml` with `lastmod 2026-11-18`**

- [ ] **Step 7: Run the checker**

Run: `python3 scripts/check_site.py`
Expected: clean, exit `0`.

- [ ] **Step 8: Look at it**

Run: `python3 -m http.server 8080`, then open `/` and `/en/` at 1440, 900 and 360 px wide. Confirm: no horizontal scroll, the buttons sit above the footer, the promise stays on two lines, the text stays readable over the plate at 900px.

- [ ] **Step 9: Commit**

```bash
git add assets index.html en sitemap.xml
git commit -m "✨ feat: rebuild the home page in the brand identity, in both languages"
```

---

### Task 3: The about pair

**Files:**
- Create: `moi/index.html`, `en/about/index.html`
- Modify: `sitemap.xml`

**Interfaces:**
- Consumes: the class contract from Task 2 plus `page`, `page__head`, `eyebrow`, `section`, `section__title`, `profile-group`, `profile-group h3`, `profile-list`, `note`, `contact-line`. Add those to `assets/site.css` in this task.

- [ ] **Step 1: Add the inner-page classes to `site.css`**

`page` is a centred column of `max-width: 46rem` with `padding-block: clamp(3rem, 8vw, 6rem)` on `void`; `section` separated by a 1px `rgba(244,239,230,.14)` rule; `profile-group h3` in Plex Mono, muted, uppercase; `profile-list` a loose list with 1rem row gap. No plate on this page.

- [ ] **Step 2: Write `moi/index.html`**

Nav with `Moi` marked `aria-current="page"`. Then:

- `h1` `Salut, moi c’est Ashu.`
- Three paragraphs in `vous`: the promise in his own words, the games (Guild Wars 2 most often, Star Citizen when it launches, live coding now and then), no fixed schedule and the announcement on Discord, and the closing line `Que vous débarquiez dans votre premier MMO ou que vous traîniez là depuis dix ans, la porte est la même.`
- `Où me trouver`, five groups: **Les chaînes** (YouTube, Twitch), **La communauté** (Discord), **Les réseaux annexes** (Instagram, TikTok, X) with one sentence saying these are Vyrtual Synthese, the character's accounts, **Le code et l’écriture** (GitHub, Medium, DEV), **Le jeu** (Steam, Exophase: omit both rows and the whole group until the creator supplies the URLs).
- `Liens partenaires`: Instant Gaming, Star Citizen referral, Amazon, each `rel="sponsored noopener noreferrer"`, under one sentence saying they support the channel.
- Footer, with the contact address and the copyright.

- [ ] **Step 3: Write `en/about/index.html`**

The same page in English, `About` marked, canonical `https://ashuvidz.com/en/about/`, `hreflang` back to `https://ashuvidz.com/moi/`.

- [ ] **Step 4: Add both URLs to `sitemap.xml`**

- [ ] **Step 5: Run the checker, look at the page, commit**

```bash
python3 scripts/check_site.py
git add moi en/about assets/site.css sitemap.xml
git commit -m "✨ feat: add the about page in both languages"
```

---

### Task 4: The partners pair

**Files:**
- Create: `partenaires/index.html`, `en/partners/index.html`
- Modify: `assets/site.css` (add `facts`, `fact`, `fact__value`, `fact__label`, `services`, `client-list`, `policy`), `sitemap.xml`

**Interfaces:**
- Consumes: Task 2 and Task 3 classes. `facts` is a `night` panel holding `fact` blocks; `fact__value` is Anton, `fact__label` Plex Mono.

- [ ] **Step 1: Write `partenaires/index.html`**

Corporate register, same nav, `Partenaires` marked. Sections:

1. `h1` `Travailler avec AshuVidz`, then one paragraph naming the two paid formats.
2. **Ce que je propose**: a promotion segment inside a video; a sponsored play session on Twitch, 1, 2 or 3 hours.
3. **Ce que ça touche**: the `night` panel with 22 900 abonnés, 800 vidéos, 5,22 M de vues cumulées, 97,7 % en France, 25 à 44 ans, and one line saying live and the 10 to 30 minute format carry the watch time. Under the panel, in Plex Mono: `relevé le 2 novembre 2026`. No 2018 figure anywhere.
4. **Ils m’ont fait confiance**: ArenaNet and NCSoft (Guild Wars 2, Blade & Soul), Pearl Abyss (lancement de Black Desert Online), Square Enix (lancement de Final Fantasy XIV). Names in type, no logos.
5. **Clés de jeu**: keys are accepted; a key does not reserve a broadcast slot; only a paid session does.
6. **Cadre**: no fixed schedule, no guaranteed volume, the date is announced on Discord.
7. **Tarifs**: on request.
8. **Contact**: the address, and what a first message should contain (game, target date, format, budget).

- [ ] **Step 2: Write `en/partners/index.html`**

The same seven sections in corporate English, same figures and the same date, canonical `https://ashuvidz.com/en/partners/`.

- [ ] **Step 3: Add both URLs, run the checker, look, commit**

```bash
python3 scripts/check_site.py
git add partenaires en/partners assets/site.css sitemap.xml
git commit -m "✨ feat: add the partners page in both languages"
```

---

### Task 5: The not-found page, the crawler files and the docs

**Files:**
- Modify: `404.html` (full replacement), `robots.txt`, `README.md`, `CHANGELOG.md`

**Interfaces:**
- Consumes: `site.css`, the header and footer markup.

- [ ] **Step 1: Rewrite `404.html`**

Same head as the others plus `meta[name=robots][content=noindex]` and `link[rel=canonical]` to `https://ashuvidz.com/404.html`. Body: the logo, `Page introuvable.` in Anton, one French line, one English line, and a single `Rentrer à l’accueil` / `Back home` link to `/`. No plate.

- [ ] **Step 2: Update `robots.txt`**

Keep the existing rules, add `Disallow: /scripts/`, `Disallow: /tests/`, `Disallow: /en/404.html`, and keep `Disallow: /docs/`.

- [ ] **Step 3: Update `README.md`**

Replace the "What is in here" table with the new paths, add `python3 scripts/check_site.py` to the quick start and to the update flow, and describe the two languages and the URL scheme. No new sections beyond what exists today.

- [ ] **Step 4: Update `CHANGELOG.md`**

Under `## [Unreleased]`, record: the three pages in two languages, the brand palette and type, Poppins and Font Awesome removed, the checker, and the removed cards (forum, wiki, Reddit, recruitment Discord, Star Citizen organisation).

- [ ] **Step 5: Run the checker and commit**

```bash
python3 scripts/check_site.py
python3 -m unittest discover -s tests
git add 404.html robots.txt README.md CHANGELOG.md
git commit -m "📝 docs: document the new site and the check"
```

---

### Task 6: The gate

- [ ] **Step 1: Full check**

```bash
python3 scripts/check_site.py && python3 -m unittest discover -s tests
```
Expected: both silent and `0`.

- [ ] **Step 2: Keyboard pass on `/` and `/moi/`**

Tab through: skip link appears first, then brand, then the language switch, then nav, then buttons. Every stop shows the coral outline. No trap.

- [ ] **Step 3: Width pass**

360, 768, 900, 1440 px on all six pages in both languages: no horizontal scroll, no text under the footer, buttons never clipped. Repeat with `prefers-reduced-motion` forced on.

- [ ] **Step 4: Weight check**

Run: `du -ch index.html assets/site.css assets/fonts/*.woff2 assets/Ashuvidz_BG.webp | tail -1`
Expected: under 200 KB.

- [ ] **Step 5: Hand over**

```bash
git fetch origin
git rebase origin/develop
git push origin feature/homepage-redesign
```
Open the pull request into `develop` with `github_create_pull_request`, body carrying the checker output and the weight figure.
