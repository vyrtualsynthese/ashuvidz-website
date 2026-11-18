# AshuVidz.com: the homepage, the about page and the partners page

Design approved in conversation on 2026-11-18. Supersedes the single-page landing site of
`index.html`.

## Intent

The site is a signpost, not a guide. Someone who has just heard the name should be one click away
from the three rooms where the channel actually lives: YouTube, Twitch, Discord. Two other readers
get their own page: a partner who wants to work with the channel, and someone who wants to know who
is behind it.

Why now: the current page is a drawer of link cards with a row of eight icons. Its visual language
(`#f97316` orange, Poppins, rounded cards, Font Awesome) is not the brand in
`creator/brand/visual-identity.md`, and the brand file records the site as "out of scope, rebuilt
from scratch by the creator". Two of its cards point at retired destinations.

## Who reads it

| Reader | Arrives from | Wants | One action |
|---|---|---|---|
| Viewer, French, 25 to 44 | a video description, a Twitch panel, Discord, a search for the name | to watch or to join | click YouTube, Twitch or Discord |
| Partner, French or English | a press kit, a referral, a search | to know who watches and what is for sale | send an email |
| Curious | anywhere | to know who Ashu is | read, then follow |

## Goals

- One click from the homepage to the three destinations, YouTube first.
- Look like the channel: Anton, void navy, one coral accent, no icon soup.
- French by default, a complete English twin of every page.
- A partners page a studio can take seriously, in both languages.
- Nothing dead on the page: no placeholder, no link to a retired service.

## Non-goals

- No guides, blog, wiki or forum content on this site.
- No stream schedule, no live indicator, no countdown (there is no fixed schedule).
- No newsletter, shop, donation widget, comment system, or analytics beyond the host's.
- No backend of any kind at this time.
- No build step (see Approaches).
- Not an index of every account the creator owns.

## Anti-goals

- A page that reads like a bought template.
- Audience claims the numbers do not support. 2018 is never a benchmark.
- Any link that 404s, including a "coming soon" card.
- English that reads like machine translation.

## Constraints

Platform:

- nginx clones `main` every 60 seconds. A merge is a deployment.
- Static files only. JavaScript is allowed in the page, there is no server to talk to.
- The repository root is served, so `docs/` and `*.md` stay excluded in `robots.txt`.
- `404.html` still needs the chart's `error_page` before nginx serves it.

Brand (`creator/brand/visual-identity.md`, `voice.md`, `production-guide.md`):

| Token | Hex | Role |
|---|---|---|
| void | `#0A0F1E` | ground |
| ink | `#05070F` | shadow, vignette |
| night | `#141B2E` | panels if any |
| paper | `#F4EFE6` | text, rules |
| muted | `#8C97B0` | secondary labels |
| coral | `#F2545B` | the only accent |

- Two composed typefaces: **Anton** (titles) and **IBM Plex Mono** (labels). Long prose is rendered
  by the platform's own typeface, so the body uses a system stack and downloads nothing.
- Contrasts already verified: paper/void 16.7:1, muted/night 5.9:1, coral/void 5.6:1. Coral is for
  large text and marks only.
- French typography: non-breaking space before `:` `;`, thin non-breaking space (`U+202F`) before
  `!` `?`, typographic apostrophe `’`, accented capitals, no em dash, no en dash, no full stop in a
  title or a label, thousands separated by a non-breaking space.
- Voice: `vous`, precise and patient and complicit, humour only at the creator's own expense,
  no `TOP 5`, no schedule, no swear word.
- The promise is locked: « Les MMO, sans jargon ! Et vient jouer avec nous ! »

## Approaches

| | How | Trade |
|---|---|---|
| **A (chosen)** | Six hand-written pages (three in French, three in English), one shared `assets/site.css`, a stdlib link check, no build | Nav, footer and copy are written twice; the check guards the drift. Real URL per language, no JavaScript needed, no toolchain |
| B | One file per page, both languages inside, switched by a script | Both languages downloaded by everyone; the English page cannot rank on its own URL; breaks without JavaScript |
| C | Templates plus a build, generated pages committed | One source for the layout; adds a toolchain and a "did you rebuild" failure mode to a repo whose virtue is that it has none |

A was chosen for the size of the thing: three pages, small markup, and the check is cheaper than a
build. The trigger to revisit: a fourth page pair, or content edited often, or a third language.

## Site map

| French | English | Page |
|---|---|---|
| `/` | `/en/` | signpost |
| `/moi` | `/en/about` | who is behind the channel |
| `/partenaires` | `/en/partners` | partners |
| `404.html` | same file | one bilingual not-found page, `noindex` |

- Every page carries `<link rel="alternate" hreflang="fr">`, `hreflang="en"`, `hreflang="x-default"`
  on the French URL, and a self-referencing `canonical`.
- The header holds two language links, each pointing at the twin of the current page, with
  `aria-current` on the active one and `lang` set to the target language.
- `sitemap.xml` lists all six URLs.

## The visual system

The chosen screen (mock "titre respiré", Verre finish): a full-bleed plate, graded by a left-to-right
veil so the text sits on a dark field and the plate stays visible on the right, running out of frame.

- **Hero:** `100svh`. Navigation bar at the top, the text block at 24% from the top in the left 52%,
  buttons under the text, a thin footer line underneath the viewport.
- **Veil:** `linear-gradient(90deg, void 0%, void 93% 34%, transparent 100%)` plus a top and bottom
  gradient. The brand rule holds: darken only behind the text, never the whole frame.
- **The promise:** Anton, `clamp(2.4rem, 5.2vw, 3.6rem)`, line-height 1.06, "sans jargon !" in coral
  on its own line. Air above (kicker 22px away), below (description 24px), and before the buttons
  (34px).
- **Buttons:** pills. YouTube is coral filled with void text; Twitch and Discord are paper on a 1px
  paper border at 30% opacity. No icons.
- **Grain:** one inline SVG turbulence data URI at low opacity. No image request.
- **The Verre finish resolved without a card:** a translucent bottom rail on narrow screens and the
  graded veil on wide ones. No floating panel, because a panel concentrates the text again.
- **The plate:** `assets/Ashuvidz_BG.webp` is the channel's own art (navy field, dotted topography,
  the A monogram), and the approved mock used it. It keeps its place, graded toward coral so the
  orange tail of its gradient reads as the accent. `assets/og-image.jpg` stays as it is: it is the
  same art at 1200×630 and already legible at thumbnail size. Recutting it with the promise set in
  Anton would need the image toolchain from the creator repository, and that is not work for this
  plan. No new photograph or illustration is needed, and no generative image is used.
- **Ground per page:** the plate belongs to the home page only. `/moi` and `/en/about` sit on `void`
  and are type-led. `/partenaires` and `/en/partners` sit on `void` with one `night` panel holding
  the audience numbers. All four share the same nav, footer and type scale.
- **Motion:** one entrance, 400ms, opacity plus 8px rise for the text block. Everything off under
  `prefers-reduced-motion`.
- **Breakpoints:** 900px (text block full width, plate behind with a vertical veil), 600px (nav
  collapses to the page names, buttons stack full width, footer stacks).
- **No external request at all:** Anton and Plex Mono self-hosted from `assets/fonts/`, no CDN, no
  Font Awesome. Poppins is removed.

Page weight target: under 200 KB total including the plate, LCP the title or the plate.

## Pages

### Home

Fixed French strings:

- Kicker: `DIRECT · MMO · DEPUIS 2012`
- Title: `Les MMO,` / `sans jargon !` (coral on the second line)
- Subtitle: `Et vient jouer avec nous.`
- Description: `Guild Wars 2 le plus souvent, Star Citizen quand il veut bien se lancer.`
- Buttons: `YouTube`, `Twitch`, `Discord`
- Footer: `ashuvidz@gmail.com`, `© 2026 AshuVidz`

Fixed English strings:

- Kicker: `LIVE · MMO · SINCE 2012`, title `MMOs,` / `no jargon!`, subtitle `And come play with us.`
- Description: `Guild Wars 2 most of the time, Star Citizen when it feels like launching.`
- Footer: the same address, the same copyright line.

The footer carries the email and the copyright only. The forum answered `404` on 2026-11-18 and is
being repaired; it joins the footer the day it answers, as does AshuWorld. A footer with two honest
items beats one with a dead link, and the rule is the same on every page.


### Moi / About

- Opening: `Salut, moi c’est Ashu.` then three short paragraphs built from
  `creator/brand/copy/youtube-about.md`: the promise in his own words, the games, no fixed schedule,
  announced on Discord, and "que vous débarquiez dans votre premier MMO ou que vous traîniez là
  depuis dix ans, la porte est la même".
- `Où me trouver`, grouped: **Les chaînes** (YouTube, Twitch), **La communauté** (Discord; the forum
  joins the group when it answers again), **Les réseaux annexes** (Instagram, TikTok, X) under one
  line saying these are Vyrtual Synthese, the persona's accounts, **Le code et l’écriture** (GitHub,
  Medium, DEV), **Le jeu** (Steam, Exophase).
- `Liens partenaires`: Instant Gaming, Star Citizen referral, Amazon, each `rel="sponsored noopener"`,
  with one sentence saying they support the channel.
- Contact: the email address.
- No portrait photograph until the creator supplies one. The page is type-led.

### Partenaires / Partners

Corporate register, in both languages, same facts.

1. **Ce que je propose**: a promotion segment inside a video; a sponsored play session on Twitch for
   1, 2 or 3 hours.
2. **Ce que ça touche**: measured audience, with the date of the snapshot (`relevé le 2 novembre
   2026`). 22 900 subscribers, 800 videos, 5.22 M lifetime views, 97.7% France, 25 to 44, live and
   the 10 to 30 minute band carry the watch time. No 2018 figure, no claim that a platform converts.
3. **Ils m’ont fait confiance**: ArenaNet and NCSoft (Guild Wars 2, Blade & Soul), Pearl Abyss
   (Black Desert Online launch), Square Enix (Final Fantasy XIV launch). Set in type, no logos:
   press-kit assets only, and the brand forbids anything else.
4. **Clés de jeu**: keys are accepted. A key does not reserve a slot; only a paid session does.
5. **Cadre**: no fixed schedule, no guaranteed volume, content announced on Discord.
6. **Tarifs**: on request.
7. **Contact**: the email address, plus what to put in a first message (game, target date, format,
   budget).

## Outbound links

Nothing on this site links out on trust. Every address below was requested on 2026-11-18 and the
answer recorded. The two that cannot be verified yet are not on the page.

| Destination | URL | State |
|---|---|---|
| YouTube | `https://www.youtube.com/ashuvidz` | 200 |
| Twitch | `https://www.twitch.tv/ashuvidz` | 200 |
| Discord | `https://discord.gg/rzW36hah5x` | valid, never expires, guild AshuDashi (AshuVidz), #annonces |
| Instagram | `https://www.instagram.com/vyrtualsynthese/` | 200 |
| TikTok | `https://www.tiktok.com/@ashuvidz` | 200 |
| X | `https://x.com/vyrtualsynthese` | 200 |
| GitHub | `https://github.com/vyrtualsynthese` | 200 |
| Medium | `https://medium.com/@vyrtualsynthese` | 403 to a scripted request, the profile page answers in a browser |
| DEV | `https://dev.to/vyrtualsynthese` | 200 |
| Instant Gaming | `https://www.instant-gaming.com/?igr=ashuvidz` | 200, redirects to `/fr/` |
| Star Citizen referral | `https://robertsspaceindustries.com/enlist?referral=STAR-4G67-3JHH` | 200 |
| Amazon | `https://amzn.to/40agkE6` | 202, resolves to `tag=ashuvidz-20` |
| Steam, Exophase | unknown | the profile handles are not derivable; the rows appear once the creator gives them |
| Forum | `https://forum.ashuvidz.com/` | 404, being repaired |
| Wiki | `https://wiki.ashuvidz.com/` | 404, retired |
| Reddit | `https://www.reddit.com/r/AshuvidzCommunity/` | not maintained, dropped |
| Recruitment Discord | `https://discord.gg/4NEa9eBBbS` | expired, dropped |

`https://discord.gg/PR5JYUVma` (the invite in `brand/copy/youtube-about.md`) reaches the same guild
but expires on 2026-11-28, so the site uses the permanent one.

The check verifies internal links only. An outbound address is verified by request when it is added,
and again when a page is edited around it; a failure means the row comes off the page, not that it
stays and apologises.

## The check

`scripts/check_site.py`, Python standard library only, run before every pull request:

- every internal `href` and `src` resolves to a file
- no `href="#"`, no empty `href`
- every page has `lang`, `<title>`, meta description, canonical, `og:title`, `og:description`,
  `og:image`, and exactly one `<h1>`
- every page's hreflang pair is reciprocal and its canonical points at itself
- the two languages of a pair link to the same outbound hosts and use the same assets
- `sitemap.xml` lists every public page and nothing else
- exit code 1 with a readable list

## Accessibility and performance

- Skip link, visible focus ring on the coral, landmarks, `aria-current`, `alt` on the logo,
  `lang` on both languages.
- Keyboard order follows the visual order. The language switch is reachable first, after the logo.
- No external requests, no icon font, `font-display: swap`, fixed image dimensions, `100svh`.
- Targets on mobile: Lighthouse performance 95 or better, accessibility 100.

## Deployment

Branch from `develop`, pull request, release `develop` to `main`, the pod picks it up within 60
seconds. Local preview: `python3 -m http.server 8080`. The check runs before the PR and its output is
in the PR body.

Two things sit outside this repository and outside this plan:

- `404.html` is only served once the nginx chart adds `error_page 404 /404.html`, which is a change
  in `homelab` (`cluster/helm/ashuvidz-website`). It becomes a task on the homelab board. The site
  ships the bilingual page; whether nginx serves it does not hold this work.
- The Twitch panels and the YouTube description point at `ashuvidz.com`. Repointing them at
  `/moi` and `/partenaires` is a separate pass in the creator repository, after the pages exist.

## Calls made here, not by the partner

| Call | Reason |
|---|---|
| Poppins removed, prose in the system stack | the brand says the site's prose uses no third typeface |
| Font Awesome removed, buttons are text | no external request, and the brand allows no icon set |
| No portrait on the about page for now | a photo is the creator's to choose, and a stock one would be worse than none |
| Persona accounts under "réseaux annexes" | the brand keeps Vyrtual Synthese off the channel's surfaces, but a visitor must be able to find them |
| Client names in type, not logos | rights, and the brand allows press-kit assets only |
| Affiliate links on the about page, not the home | they serve neither reader of the homepage |
| No live badge anywhere | needs an API call and a public key, and no schedule means it would rot |
| Rates on request | a published rate card goes stale and anchors the negotiation |
| One bilingual 404 | nginx maps a single file, and a second one buys nothing |
| The existing plate is kept, graded toward coral | it is the channel's own art, the approved mock used it, and a new one would be invented art |
| The plate stays on the home page | the about page is type-led by design, and the partners page must read corporate |
| The permanent Discord invite | the one in the brand copy expires on 2026-11-28 |
| The forum, Reddit, the wiki and AshuWorld stay off the site | all four answer 404 or are unmaintained today; each returns the day it answers |
| The nginx `error_page` change is not in this plan | it belongs to the homelab chart, and its absence does not block the pages |

## Left to the builder

- The CSS architecture inside the single stylesheet, the spacing scale and the exact breakpoints.
- The English wording beyond the fixed strings above.
- The paragraphs of the about page and the partners page, within the voice rules.
- The implementation of the check and the wording of its messages.
