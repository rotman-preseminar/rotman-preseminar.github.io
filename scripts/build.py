#!/usr/bin/env python3
"""Build the data the website reads.

Reads data/site.yml, data/resources.yml and data/schedule/<year>.yml (one file per
academic year, e.g. data/schedule/2026-27.yml), scans sessions/ and resources/ for uploaded files, and writes:
  data/site.js       everything the page needs, in one file (a script, so the page
                     also works when index.html is opened straight from disk)
  schedule.ics       calendar feed students can subscribe to

Run locally before previewing:  python3 scripts/build.py && python3 -m http.server
On GitHub this runs automatically on every push (see .github/workflows/pages.yml).
Exits with a readable error if a YAML file has a mistake.
"""

import datetime as dt
import json
import re
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

ROOT = Path(__file__).resolve().parent.parent
TZ = ZoneInfo("America/Toronto")
IGNORED = {".gitkeep", ".DS_Store", "README.md", "Thumbs.db"}

SESSION_KEYS = {
    "id", "date", "speaker", "affiliation", "speaker_url", "paper", "paper_url", "slides_url",
    "coauthors", "presenter", "faculty", "preseminar", "seminar", "notes", "cancelled",
}

# Files in a session folder get a button label from their name. The first rule whose
# word appears anywhere in the name wins, so "Tuzel_discussion_v2.pdf" becomes "Slides".
FILE_LABELS = [
    (r"speaker", "Speaker slides"),
    (r"slides|discussion|presentation", "Slides"),
    (r"appendix", "Appendix"),
    (r"paper", "Paper"),
]

errors = []


class Loader(yaml.SafeLoader):
    """SafeLoader that keeps dates as text, so a bad date gets a friendly error below."""


Loader.yaml_implicit_resolvers = {
    k: [(tag, rx) for tag, rx in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def fail(msg):
    errors.append(msg)


def load_yaml(name):
    path = ROOT / "data" / name
    try:
        return yaml.load(path.read_text(encoding="utf-8"), Loader=Loader) or []
    except yaml.YAMLError as e:
        sys.exit(f"ERROR in data/{name}: the file is not valid YAML.\n{e}")


def pretty_name(stem):
    return re.sub(r"[-_]+", " ", stem).strip().capitalize()


def list_files(folder):
    if not folder.is_dir():
        return []
    return sorted(
        p for p in folder.rglob("*")
        if p.is_file() and p.name not in IGNORED and not p.name.startswith(".")
    )


def file_entry(path):
    stem = path.stem.lower()
    label = next((lbl for pat, lbl in FILE_LABELS if re.search(pat, stem)), pretty_name(path.stem))
    return {
        "label": label,
        "path": path.relative_to(ROOT).as_posix(),
        "ext": path.suffix.lstrip(".").lower(),
        "size": path.stat().st_size,
    }


def as_date(value, where):
    if isinstance(value, dt.date):
        return value
    try:
        return dt.date.fromisoformat(str(value))
    except ValueError:
        fail(f"{where}: '{value}' is not a date in YYYY-MM-DD format")
        return None


def build_sessions(site):
    files = sorted((ROOT / "data" / "schedule").glob("*.yml"))
    if not files:
        sys.exit("ERROR: no schedule found. Add a file like data/schedule/2026-27.yml.")

    defaults = site.get("defaults", {})
    sessions, seen = [], set()
    for f in files:
        year = f.stem
        raw = load_yaml(f"schedule/{f.name}")
        if not isinstance(raw, list):
            sys.exit(f"ERROR in data/schedule/{f.name}: expected a list of sessions (each starting with '- date:').")
        for i, s in enumerate(raw, 1):
            sessions.extend(parse_session(s, f"data/schedule/{f.name}, entry {i}", year, defaults, seen))

    # Folders under sessions/ that match no schedule entry are probably typos.
    folder = ROOT / "sessions"
    if folder.is_dir():
        for d in folder.iterdir():
            if d.is_dir() and d.name not in seen and list_files(d):
                fail(f"sessions/{d.name}/ has files but no schedule entry with that date or id")

    return sorted(sessions, key=lambda x: x["date"])


def parse_session(s, where, year, defaults, seen):
    """Validate one schedule entry; returns [session] or [] if it has errors."""
    if not isinstance(s, dict):
        fail(f"{where}: expected fields like 'date:' and 'speaker:'")
        return []
    unknown = set(s) - SESSION_KEYS
    if unknown:
        fail(f"{where}: unknown field(s) {', '.join(sorted(unknown))} (check spelling)")
    if "date" not in s or "speaker" not in s:
        fail(f"{where}: 'date' and 'speaker' are required")
        return []
    date = as_date(s["date"], where)
    if date is None:
        return []

    sid = str(s.get("id") or date.isoformat())
    if sid in seen:
        fail(f"{where}: two sessions share the id '{sid}'; give one of them an explicit 'id:'")
    seen.add(sid)

    pre = {**defaults.get("preseminar", {}), **(s.get("preseminar") or {})}
    pre_date = as_date(pre.get("date", date), where) or date
    pre["date"] = pre_date.isoformat()
    sem = {**defaults.get("seminar", {}), **(s.get("seminar") or {})}

    faculty = s.get("faculty") or []
    if isinstance(faculty, str):
        faculty = [faculty]

    return [{
        "id": sid,
        "year": year,
        "date": date.isoformat(),
        "speaker": str(s["speaker"]),
        "affiliation": s.get("affiliation"),
        "speaker_url": s.get("speaker_url"),
        "paper": s.get("paper"),
        "paper_url": s.get("paper_url"),
        "slides_url": s.get("slides_url"),
        "coauthors": s.get("coauthors"),
        "presenter": s.get("presenter"),
        "faculty": faculty,
        "preseminar": pre,
        "seminar": sem,
        "notes": s.get("notes"),
        "cancelled": bool(s.get("cancelled", False)),
        "files": [file_entry(p) for p in list_files(ROOT / "sessions" / sid)],
    }]


def build_resources():
    raw = load_yaml("resources.yml") or {}
    cats = raw.get("categories") or []
    items = raw.get("items") or []
    by_id = {c["id"]: {**c, "items": []} for c in cats}

    def category(cid):
        if cid not in by_id:
            by_id[cid] = {"id": cid, "title": pretty_name(cid), "description": "", "items": []}
        return by_id[cid]

    described = {}
    for i, it in enumerate(items, 1):
        where = f"data/resources.yml, item {i}"
        if "category" not in it or "title" not in it:
            fail(f"{where}: 'category' and 'title' are required")
            continue
        if bool(it.get("url")) == bool(it.get("file")):
            fail(f"{where}: give exactly one of 'url' (a link) or 'file' (a path under resources/)")
            continue
        if it.get("file"):
            path = ROOT / "resources" / it["category"] / it["file"]
            if not path.is_file():
                fail(f"{where}: file resources/{it['category']}/{it['file']} does not exist")
                continue
            described[path] = it
            continue
        category(it["category"])["items"].append({
            "title": it["title"], "url": it["url"],
            "description": it.get("description"), "added_by": it.get("added_by"),
        })

    # Uploaded files: resources/<category>/<file>
    for path in list_files(ROOT / "resources"):
        rel = path.relative_to(ROOT / "resources")
        if len(rel.parts) < 2:
            fail(f"resources/{rel}: put files inside a category folder, e.g. resources/general/")
            continue
        meta = described.get(path, {})
        entry = file_entry(path)
        category(rel.parts[0])["items"].append({
            "title": meta.get("title") or pretty_name(path.stem),
            "url": entry["path"],
            "ext": entry["ext"],
            "size": entry["size"],
            "description": meta.get("description"),
            "added_by": meta.get("added_by"),
        })

    return list(by_id.values())


def ics_escape(text):
    return str(text).replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def build_ics(site, sessions):
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//PhD Pre-Seminar//EN",
        "CALSCALE:GREGORIAN", f"X-WR-CALNAME:{ics_escape(site.get('title', 'Pre-Seminar'))}",
    ]
    for s in sessions:
        if s["cancelled"]:
            continue
        pre = s["preseminar"]
        try:
            h, m = map(int, str(pre.get("time", "09:30")).split(":"))
        except ValueError:
            continue
        start = dt.datetime.fromisoformat(pre["date"]).replace(hour=h, minute=m, tzinfo=TZ)
        end = start + dt.timedelta(minutes=int(pre.get("duration_minutes", 60)))
        fmt = lambda t: t.astimezone(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        desc = [f"Paper: {s['paper']}" if s["paper"] else "Paper: TBA",
                f"Presenter: {s['presenter'] or 'TBA'}"]
        lines += [
            "BEGIN:VEVENT", f"UID:preseminar-{s['id']}@preseminar",
            f"DTSTAMP:{stamp}", f"DTSTART:{fmt(start)}", f"DTEND:{fmt(end)}",
            f"SUMMARY:{ics_escape('Pre-seminar: ' + s['speaker'])}",
            f"LOCATION:{ics_escape(pre.get('room', 'TBA'))}",
            f"DESCRIPTION:{ics_escape(chr(10).join(desc))}",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


def main():
    site = load_yaml("site.yml") or {}
    sessions = build_sessions(site)
    resources = build_resources()
    if errors:
        print("The site was NOT built. Please fix the following:\n", file=sys.stderr)
        for e in errors:
            print("  - " + e, file=sys.stderr)
        sys.exit(1)

    out = {
        "site": site,
        "sessions": sessions,
        "resources": resources,
        "built": dt.datetime.now(TZ).isoformat(timespec="minutes"),
    }
    payload = json.dumps(out, indent=1, default=str)
    (ROOT / "data" / "site.js").write_text(f"window.SITE_DATA = {payload};\n", encoding="utf-8")
    (ROOT / "schedule.ics").write_text(build_ics(site, sessions), encoding="utf-8")
    print(f"Built: {len(sessions)} sessions, {sum(len(c['items']) for c in resources)} resources.")


if __name__ == "__main__":
    main()
