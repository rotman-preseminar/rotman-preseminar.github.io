# Maintaining the site — quick reference

Live page: https://rotman-preseminar.github.io/ · Map of the files: [SITEMAP.md](SITEMAP.md)

## Do I need to run the build?

- **No** — editing text in `index.html` (guidelines, headings, footer).
- **Yes** — anything in `data/` (schedule, resources, settings) or any file added to `sessions/` or `resources/`.
- The build is one line in Terminal:
  ```
  cd "/Users/filippo/Desktop/Filippo/5 Teaching/PreSeminar" && python3 scripts/build.py
  ```
- It prints an error naming the file and entry if something is wrong; fix and re-run.
- (This step disappears once the automatic rebuild is switched on: run `gh auth refresh -h github.com -s workflow` and ask Claude to enable it.)

## Publishing

- Commit and push in GitHub Desktop → live in about a minute.
- Ignore the `local-history` branch; never push it.
- `EmailOrganization.pdf` is deliberately kept off GitHub.

## Common tasks

- **Add a speaker / paper / presenter:** edit `data/schedule/2026-27.yml` → build → push.
  - Fields: `date`, `speaker`, then optional `affiliation`, `speaker_url`, `paper`, `paper_url`, `slides_url`, `presenter`, `faculty`, `notes`, `cancelled: true`.
  - Put titles with a colon in quotes.
- **Add the paper or the discussion slides:** drop the file in `sessions/<seminar date>/`, e.g. `sessions/2026-10-16/xx_paper.pdf` → build → push.
  - Any file name containing *paper* → **Paper** button; *slides* / *discussion* → **Slides** button; anything else gets a button with its own name.
  - The folder name must match the date in the schedule exactly.
- **Add a resource:** drop a file in `resources/<category>/`, or add a link under `items:` in `data/resources.yml` → build → push.
- **Edit the guidelines:** edit the text between `<li>` and `</li>` in `index.html` (section `<!-- GUIDELINES -->`) → push. Write `&` as `&amp;`.
- **Change the time, room, organizers or the banner:** `data/site.yml` → build → push.
- **New academic year:** create `data/schedule/2027-28.yml` → build → push. Earlier years stay online under their own tab.

## Preview before pushing

- Build, then double-click `index.html` and refresh the browser.

## Still to do

- Invite Nico as a second **owner** of the `rotman-preseminar` organization, so the site does not depend
  on one account: org page → Settings → People → Invite member → then set his role to Owner.

## Notes

- The site moved to the `rotman-preseminar` organization on 22 September 2026.
- The repository is public, and this is now a settled decision: GitHub Pages does not publish from a
  private repository on the free organization plan. Uploaded papers and slides are therefore visible to
  anyone with the link — only post what the speaker is happy to share. The page asks search engines not
  to index it, but that is not the same as privacy.
