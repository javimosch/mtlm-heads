#!/usr/bin/env python3
"""Regenerate the README catalog table from index.json + catalog_notes.json.

The table between <!-- lanes:start --> and <!-- lanes:end --> in README.md is a
generated projection — never hand-edit it. Mechanical fields come from
index.json (itself generated from pack manifests); curated per-pack copy comes
from catalog_notes.json.

  python3 render_readme.py          # rewrite README.md in place
  python3 render_readme.py --check  # exit 1 if README is stale (regen-diff gate)
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
README = os.path.join(REPO, "README.md")
START = "<!-- lanes:start -->"
END = "<!-- lanes:end -->"


def render_table():
    idx = json.load(open(os.path.join(REPO, "index.json")))
    notes = json.load(open(os.path.join(REPO, "catalog_notes.json")))
    rows = ["| lane | version | classes | holdout | status |",
            "|---|---|---|---|---|"]
    # curated order: certified/demo lanes first in catalog order, then
    # superseded/yanked history rows last (kept visible — the catalog's
    # honesty is showing its deprecated packs too)
    live = [e for e in idx["lanes"]
            if not e.get("yanked") and not e.get("superseded_by")]
    old = [e for e in idx["lanes"]
           if e.get("yanked") or e.get("superseded_by")]
    order = ["civic", "clinc150", "banking77", "civic_fr", "helpdesk", "eq_tone"]
    live.sort(key=lambda e: (order.index(e["name"])
                             if e["name"] in order else 99, e["name"]))
    old.sort(key=lambda e: e["name"])

    missing_notes = []
    for e in live + old:
        key = f"{e['name']}@{e['version']}"
        n = notes.get(key, {})
        if not n:
            missing_notes.append(key)
        desc = n.get("desc", f"{e['classes']} labels")
        hold = n.get("holdout")
        if not hold:
            acc = e.get("holdout_acc")
            hold = f"{acc*100:.1f}%" if isinstance(acc, (int, float)) else "—"
        tier = e.get("status") or "free"
        if tier not in ("free", "demo", "certified"):
            tier = f"free, {tier}"
        elif tier != "free":
            tier = f"free, {tier}"
        name = e["name"] if not (e.get("yanked") or e.get("superseded_by")) \
            else f"{e['name']} (old)"
        bold = "**" + name + "**" if not (e.get("yanked") or e.get("superseded_by")) else name
        rows.append(
            f"| {bold} | {e['version']} | {desc} | {hold} | "
            f"{tier} (`lanes/{e['file']}`) |")
    return "\n".join(rows), missing_notes


def main():
    table, missing = render_table()
    if missing:
        print("warn: no catalog_notes.json entry for: " + ", ".join(missing),
              file=sys.stderr)
    src = open(README).read()
    if START not in src or END not in src:
        print(f"README.md lacks {START} … {END} markers", file=sys.stderr)
        sys.exit(2)
    before = src[:src.index(START) + len(START)]
    after = src[src.index(END):]
    new = before + "\n" + table + "\n\n" + after
    if "--check" in sys.argv:
        if new != src:
            print("README.md catalog table is stale — run render_readme.py")
            sys.exit(1)
        print("README.md catalog table is current")
        return
    open(README, "w").write(new)
    print("wrote README.md catalog table")


if __name__ == "__main__":
    main()
