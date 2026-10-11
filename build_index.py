#!/usr/bin/env python3
"""Regenerate index.json from lanes/*.lanepack.tar.gz — never edit by hand.

Each pack's manifest.json is authoritative; the index is a flattened projection
for consumers that browse/resolve/install lanes.

  python3 build_index.py
"""
import hashlib, json, os, tarfile, time

REPO = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.join(REPO, "lanes")
BASE_URL = "https://github.com/javimosch/mtlm-heads/raw/master/lanes"

floors_path = os.path.join(REPO, "floors.json")
floors = json.load(open(floors_path)) if os.path.exists(floors_path) else {}

entries = []
for fn in sorted(os.listdir(LANES)):
    if not fn.endswith(".lanepack.tar.gz"):
        continue
    path = os.path.join(LANES, fn)
    with tarfile.open(path) as t:
        man = json.loads(t.extractfile("manifest.json").read())
        ev = json.loads(t.extractfile("eval.json").read())
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    name_ver = fn[: -len(".lanepack.tar.gz")]
    # eval.json key names vary across emitters — normalize to index fields
    acc = ev.get("holdout_acc") or ev.get("in_scope_holdout_acc_trainonly") or ev.get("in_scope_acc_trainonly")
    oos = {k: ev[k] for k in ("oos_recall", "id_oos_recall", "far_oos_recall", "in_scope_false_oos",
                              "oos_leak_curve", "coverage_curve", "oos_eval_note") if k in ev}
    entries.append({
        "name": man["name"],
        "version": man["version"],
        "file": fn,
        "url": f"{BASE_URL}/{fn}",
        "sha256": sha,
        "head_sha256": man["head_sha256"],
        "classes": len(man["taxonomy"]),
        "taxonomy": man["taxonomy"],
        "status": man.get("status") or ev.get("status") or ("certified" if acc else "demo"),
        "holdout_acc": acc,
        "n_holdout": ev.get("n_holdout"),
        "oos": oos or None,
        "live_verified": bool(man.get("live_verified") or ev.get("live_verified")),
        "operating": floors.get(man["name"]),
        "conformal": ev.get("conformal"),
        "license": man["license"],
        "pricing": man.get("pricing", {"tier": "free"}),
        "provenance": man["provenance"],
        "runtime": man["runtime"],
        "published_at": man["created"],
    })

index = {
    "index_schema_version": "mtlm-index/1",
    "generated_at": int(time.time()),
    "artifacts_base": BASE_URL,
    "lanes": entries,
}
with open(os.path.join(REPO, "index.json"), "w") as f:
    json.dump(index, f, indent=2)
    f.write("\n")
print(json.dumps({"lanes": len(entries), "names": [e["name"] + "@" + e["version"] for e in entries]}))
