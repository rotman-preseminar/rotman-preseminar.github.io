# Maintaining the site — quick reference

Live page: https://filippocavaleri.github.io/PreSeminar/

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

- Move the site to a GitHub organization so the address is `https://<org>.github.io/` (create it at https://github.com/account/organizations/new, Free plan).
- Make the repository private once GitHub Education is approved (apply from campus). Until then, uploaded papers and slides are publicly visible on GitHub.
