# PreSeminar

Website for the Rotman finance PhD pre-seminar (organizers: Nico Inostroza, Filippo Cavaleri).
Live: https://rotman-preseminar.github.io/ · Repo: rotman-preseminar/rotman-preseminar.github.io (public).

## Layout
Static, no framework. `index.html` + `assets/` (style.css, app.js). See `SITEMAP.md` for the file map,
`MAINTENANCE.md` for the upkeep steps.

- All visible prose (guidelines, headings) is hard-coded in `index.html` — no build needed.
- Data: `data/site.yml`, `data/schedule/<year>.yml` (one file per academic year), `data/resources.yml`.
- Files: `sessions/<date>/` (paper, discussion slides), `resources/<category>/`.
- `python3 scripts/build.py` → `data/site.js` + `schedule.ics`. Both are committed. Run after any
  change under `data/`, `sessions/`, `resources/`; the page reads site.js, so skipping it = no update.

## Publishing
GitHub Pages serves branch `main` directly (no Actions: the gh token lacks `workflow` scope).
`.github/workflows/pages.yml` exists locally but is git-ignored. Branch `local-history` = pre-publish
history; never push it. `EmailOrganization.pdf` is private — keep it out of git.

## Conventions
- Guidelines text comes from the organizers' email; keep their voice ("we expect", "we would like").
  No math symbols (write "up to 10 minutes"), no "&" in headings.
- Palette: U of T navy `--navy`, Rotman pink `--pink` for highlights only. White background, no dark mode.
- Schedule = compact table, one line per seminar. Keep it dense; no card layouts.
- Don't invent speakers, dates, papers or student names; ask.

## Status (Sep 2026)
12 speakers loaded for 2026–27 with websites; papers and presenters TBA until students sign up.
Moved to the `rotman-preseminar` org on 22 Sep 2026. The old personal URL was never shared, so it was
retired rather than redirected — `filippocavaleri.github.io/PreSeminar/` is dead and that is intended.
Pending: invite Nico as a second org owner (Settings → People → Invite → role Owner), enable the
auto-rebuild via `gh auth refresh -h github.com -s workflow`.
Dropped: making the repo private. Pages does not publish from private repos on a free org — that needs
GitHub Team, and the Education benefit only covers personal accounts. The site stays public; it is kept
out of search results by the `noindex` meta in `index.html` instead.
