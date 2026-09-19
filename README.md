# Finance PhD Pre-Seminar — website

A single-page site for the Rotman finance PhD pre-seminar: schedule, guidelines, papers,
discussion slides, and resources. It is shared by link only and marked `noindex`, so search
engines are asked not to list it.

**For day-to-day upkeep, see [MAINTENANCE.md](MAINTENANCE.md).** This file explains the whole setup.

Everything on the page comes from three text files and two folders.

| To change…                         | Edit                        |
|------------------------------------|-----------------------------|
| Speakers, dates, papers, presenters| `data/schedule/<year>.yml`  |
| Resource categories and links      | `data/resources.yml`        |
| Title, organizers, default time/room, banner | `data/site.yml`   |
| Papers and slides for a session    | upload to `sessions/<date>/`|
| Files for students                 | upload to `resources/<category>/` |
| Guidelines text                    | `index.html` (Guidelines section) |

Every change you commit on GitHub republishes the site within about a minute.

## Common tasks (all from the GitHub website, no software needed)

### Add or update a session
1. Open this year's file in `data/schedule/` (e.g. `2026-27.yml`) and click the pencil icon.
2. Copy an existing entry and edit it. Minimal entry:
   ```yaml
   - date: 2026-11-13
     speaker: Jane Doe
     affiliation: Some University
     paper: "Title of the Paper"
     presenter: Student Name
   ```
   Optional fields: `speaker_url`, `paper_url`, `slides_url`, `coauthors`, `faculty: [Name, Name]`,
   `preseminar: {date: 2026-11-12, time: "09:30", room: "Rotman 4-xxx"}`,
   `seminar: {time: "14:00", room: "..."}`, `notes`, `cancelled: true`.
   Put titles containing a colon in quotes.
3. Commit.

### Upload the paper or discussion slides
1. Go to the `sessions/` folder → **Add file → Upload files**.
2. Put the file in a folder named after the session date. To make that folder, type
   `sessions/2026-11-13/` before the file name in the upload screen, or upload to an existing folder.
3. Keep the file name as it is: any name containing "slides", "discussion" or "presentation"
   gets the **Slides** button, and any name containing "paper" gets the **Paper** button.
   Any other file gets a button with its own name. To link instead of
   uploading (e.g. a Dropbox link), use `paper_url:` / `slides_url:` in the schedule.

### Start a new academic year
Create `data/schedule/2027-28.yml` (copy last year's file and replace the entries). The site
opens on the year of the next session; earlier years stay available as tabs above the table,
with all their papers and slides. Session folders are named by date, so they never clash.

### Share a resource
- **A file:** upload it to `resources/<category>/` (e.g. `resources/examples/`). It appears
  automatically, titled after the file name. For a nicer title or description, add an item
  with `file:` in `data/resources.yml`.
- **A link:** add an item with `url:` in `data/resources.yml`.
- **A new category:** create a new folder under `resources/`, and optionally describe it under
  `categories:` in `data/resources.yml`.

### If the site does not update
Open the **Actions** tab. A red ✗ means a file has a mistake; click it and the
"Build data" step says which file and entry to fix (e.g. a misspelled field or a bad date).

## Preview locally (optional)

```bash
python3 scripts/build.py      # needs PyYAML
```
then double-click `index.html`.

## How it works

`scripts/build.py` reads the YAML files, scans `sessions/` and `resources/`, checks for mistakes,
and writes `data/site.js` (read by the page) and `schedule.ics` (the calendar feed).
`.github/workflows/pages.yml` runs it on every push and publishes to GitHub Pages.
`index.html` + `assets/` are static, with no frameworks. Fonts are loaded from Google Fonts.

## Access for other faculty

Repository **Settings → Collaborators → Add people**, using their GitHub username.
Collaborators can edit files and upload materials. Only the owner can change settings.
