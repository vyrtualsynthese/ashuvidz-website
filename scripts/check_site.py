#!/usr/bin/env python3
"""Check the site before a merge.

Usage: python3 scripts/check_site.py [ROOT]

ROOT defaults to the repository root. Prints one line per problem as
`<path>: <RULE>: <message>` and exits 1 when anything is wrong.

Rules: LINK-INTERNAL, LINK-EMPTY, HEAD-REQUIRED, HREFLANG, PARITY, SITEMAP,
FR-TYPO, EXTERNAL-REL. French typography follows brand/production-guide.md:
U+00A0 before `:` and `;`, U+202F before `!` and `?`, typographic apostrophe,
no em or en dash, no full stop at the end of a heading.
"""

from __future__ import annotations

import os
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "data:", "#")
IGNORED_DIRS = {".git", ".superpowers", "tests", "docs", "scripts"}
AFFILIATE_HOSTS = ("instant-gaming.com", "robertsspaceindustries.com", "amzn.to")
REQUIRED_META = ("og:title", "og:description", "og:image", "og:url")
TYPO_FIELDS = ("description", "og:title", "og:description", "og:image:alt", "twitter:title", "twitter:description")
HEADINGS = ("h1", "h2", "h3", "h4", "h5", "h6")


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.title = ""
        self.metas: dict[str, str] = {}
        self.links: list[dict[str, str]] = []
        self.anchors: list[dict[str, str]] = []
        self.sources: list[str] = []
        self.h1_count = 0
        self.texts: list[tuple[str | None, str]] = []
        self._in_title = False
        self._skip = 0
        self._heading: str | None = None

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang", "")
        elif tag == "title":
            self._in_title = True
        elif tag in ("script", "style"):
            self._skip += 1
        elif tag == "meta":
            key = a.get("property") or a.get("name")
            if key:
                self.metas[key] = a.get("content", "")
        elif tag == "link":
            self.links.append(a)
        elif tag == "a":
            self.anchors.append(a)
        elif tag in ("img", "script", "iframe", "source"):
            if a.get("src"):
                self.sources.append(a["src"])
        if tag in HEADINGS:
            self.h1_count += tag == "h1"
            self._heading = tag

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag in ("script", "style"):
            self._skip = max(0, self._skip - 1)
        elif tag in HEADINGS:
            self._heading = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data
            return
        if self._skip:
            return
        self.texts.append((self._heading, data))


class Page:
    def __init__(self, root: Path, path: Path) -> None:
        self.path = path
        self.rel = path.relative_to(root).as_posix()
        parser = PageParser()
        parser.feed(path.read_text(encoding="utf-8"))
        self.lang = parser.lang
        self.title = parser.title.strip()
        self.metas = parser.metas
        self.anchors = parser.anchors
        self.sources = parser.sources
        self.h1_count = parser.h1_count
        self.texts = parser.texts
        self.alternates: dict[str, str] = {
            link["hreflang"]: link.get("href", "")
            for link in parser.links
            if link.get("rel", "").lower() == "alternate" and link.get("hreflang")
        }
        self.canonical = next(
            (link.get("href", "") for link in parser.links if link.get("rel", "").lower() == "canonical"),
            "",
        )
        self.asset_links = [
            link.get("href", "")
            for link in parser.links
            if link.get("href")
            and not {"canonical", "alternate"} & set(link.get("rel", "").lower().split())
        ]


def check_links(page: Page, root: Path, problems: list[str]) -> None:
    targets = (
        list(page.anchors)
        + [{"href": s} for s in page.sources]
        + [{"href": s} for s in page.asset_links]
    )
    for anchor in targets:
        href = anchor.get("href", "")
        if href == "" or href == "#":
            problems.append(f"{page.rel}: LINK-EMPTY: a link with no destination")
            continue
        if href.startswith("//") or href.startswith(SKIP_SCHEMES):
            continue
        target = href.split("#", 1)[0].split("?", 1)[0]
        if target.startswith("/"):
            candidate = root / target.lstrip("/")
        else:
            candidate = page.path.parent / target
        if target.endswith("/") or target == "":
            candidate = candidate / "index.html"
        if not candidate.exists() and not (candidate / "index.html").exists():
            problems.append(f"{page.rel}: LINK-INTERNAL: {href} does not exist")


def check_head(page: Page, problems: list[str]) -> None:
    if not page.lang:
        problems.append(f"{page.rel}: HEAD-REQUIRED: missing lang")
    if not page.title:
        problems.append(f"{page.rel}: HEAD-REQUIRED: missing title")
    if not page.metas.get("description"):
        problems.append(f"{page.rel}: HEAD-REQUIRED: missing meta description")
    if not page.canonical:
        problems.append(f"{page.rel}: HEAD-REQUIRED: missing canonical")
    for key in REQUIRED_META:
        if not page.metas.get(key):
            problems.append(f"{page.rel}: HEAD-REQUIRED: missing {key}")
    if page.h1_count != 1:
        problems.append(f"{page.rel}: HEAD-REQUIRED: {page.h1_count} h1, expected 1")


def check_typo(page: Page, problems: list[str]) -> None:
    if not page.lang.startswith("fr"):
        return
    for heading, text in page.texts:
        if "\u2013" in text or "\u2014" in text:
            problems.append(f"{page.rel}: FR-TYPO: em or en dash")
        if "'" in text:
            problems.append(f"{page.rel}: FR-TYPO: straight apostrophe")
        if re.search(r" [;:!?]", text):
            problems.append(f"{page.rel}: FR-TYPO: plain space before punctuation")
        if re.search(r"\u00a0[!?]", text):
            problems.append(f"{page.rel}: FR-TYPO: non-breaking space before ! or ?, use U+202F")
        if heading and text.strip().endswith("."):
            problems.append(f"{page.rel}: FR-TYPO: full stop at the end of a heading")
    for field in TYPO_FIELDS:
        value = page.title if field == "title" else page.metas.get(field, "")
        if not value:
            continue
        if "'" in value:
            problems.append(f"{page.rel}: FR-TYPO: straight apostrophe in {field}")
        if "\u2013" in value or "\u2014" in value:
            problems.append(f"{page.rel}: FR-TYPO: em or en dash in {field}")
        if re.search(r" [;:!?]", value):
            problems.append(f"{page.rel}: FR-TYPO: plain space before punctuation in {field}")


def check_external_rel(page: Page, problems: list[str]) -> None:
    for anchor in page.anchors:
        href = anchor.get("href", "")
        rel = anchor.get("rel", "").split()
        if anchor.get("target") == "_blank" and "noopener" not in rel:
            problems.append(f"{page.rel}: EXTERNAL-REL: target=_blank without noopener in {href}")
        host = urlparse(href).hostname or ""
        if any(host == h or host.endswith("." + h) for h in AFFILIATE_HOSTS) and "sponsored" not in rel:
            problems.append(f"{page.rel}: EXTERNAL-REL: partner link without sponsored in {href}")


def check_hreflang(pages: list[Page], by_canonical: dict[str, Page], problems: list[str]) -> None:
    for page in pages:
        if page.rel.endswith("404.html"):
            continue
        alts = page.alternates
        own = primary_lang(page.lang)
        other = "en" if own == "fr" else "fr"
        for key in ("fr", "en", "x-default"):
            if key not in alts:
                problems.append(f"{page.rel}: HREFLANG: missing hreflang={key}")
        if "fr" in alts and alts.get("x-default") != alts["fr"]:
            problems.append(f"{page.rel}: HREFLANG: x-default is not the French URL")
        if page.canonical and alts.get(own) != page.canonical:
            problems.append(f"{page.rel}: HREFLANG: canonical is not the hreflang of its own language")
        twin, other = twin_of(page, by_canonical)
        if twin is None:
            problems.append(
                f"{page.rel}: HREFLANG: no {other} page behind {alts.get(other, 'its alternate')}"
            )
        elif twin.alternates.get(own) != page.canonical:
            problems.append(f"{page.rel}: HREFLANG: the twin does not point back")


def primary_lang(lang: str) -> str:
    return lang.split("-", 1)[0].lower()


def twin_of(page: Page, by_canonical: dict[str, Page]) -> tuple[Page | None, str]:
    own = primary_lang(page.lang)
    other = "en" if own == "fr" else "fr"
    twin = by_canonical.get(page.alternates.get(other, ""))
    if twin is None or twin is page or primary_lang(twin.lang) != other:
        return None, other
    return twin, other


def outbound_hosts(page: Page) -> set[str]:
    own = urlparse(page.canonical).hostname or ""
    hosts = set()
    for anchor in page.anchors:
        host = urlparse(anchor.get("href", "")).hostname or ""
        if host and host != own:
            hosts.add(host)
    return hosts


def check_parity(pages: list[Page], by_canonical: dict[str, Page], problems: list[str]) -> None:
    seen = set()
    for page in pages:
        if page.rel.endswith("404.html"):
            continue
        twin, _ = twin_of(page, by_canonical)
        if twin is None or (page.rel, twin.rel) in seen:
            continue
        seen.add((page.rel, twin.rel))
        seen.add((twin.rel, page.rel))
        if outbound_hosts(page) != outbound_hosts(twin):
            problems.append(f"{page.rel}: PARITY: the twin does not link the same outbound hosts")
        left = {s for s in page.sources if s.startswith("/")}
        right = {s for s in twin.sources if s.startswith("/")}
        if left != right:
            problems.append(f"{page.rel}: PARITY: the twin does not use the same assets")


def check_sitemap(root: Path, pages: list[Page], problems: list[str]) -> None:
    path = root / "sitemap.xml"
    if not path.exists():
        problems.append("sitemap.xml: SITEMAP: file is missing")
        return
    try:
        tree = ET.parse(path)
    except ET.ParseError as error:
        problems.append(f"sitemap.xml: SITEMAP: {error}")
        return
    locs = [el.text.strip() for el in tree.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc") if el.text]
    known = {
        page.canonical: page
        for page in pages
        if page.canonical and not page.rel.endswith("404.html")
    }
    for loc in locs:
        if loc not in known:
            problems.append(f"sitemap.xml: SITEMAP: {loc} has no page")
    for page in pages:
        if page.rel == "404.html":
            continue
        count = locs.count(page.canonical)
        if count != 1:
            problems.append(f"{page.rel}: SITEMAP: listed {count} times, expected 1")


def check_site(root: Path) -> list[str]:
    paths: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORED_DIRS)
        if "index.html" in filenames:
            paths.append(Path(dirpath) / "index.html")
    paths.sort()
    if (root / "404.html").exists():
        paths.append(root / "404.html")
    pages = [Page(root, path) for path in paths]
    by_canonical = {page.canonical: page for page in pages if page.canonical}
    problems: list[str] = []
    for page in pages:
        check_links(page, root, problems)
        check_head(page, problems)
        check_typo(page, problems)
        check_external_rel(page, problems)
    check_hreflang(pages, by_canonical, problems)
    check_parity(pages, by_canonical, problems)
    check_sitemap(root, pages, problems)
    return problems


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parent.parent
    problems = check_site(root)
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
