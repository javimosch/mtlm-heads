# mtlm-heads — the lane catalog

Certified decision lanes for [mtlm-router](https://github.com/javimosch/mtlm-router)
— the self-hosted 7M-param typed decision layer. Drop a `.lanepack` into the
appliance and the request type it covers is routed, calibrated, and abstains
honestly when it shouldn't guess.

Format: [SPEC.md](SPEC.md). Every pack ships its eval — you see the numbers
before you trust the lane.

## Catalog

<!-- lanes:start -->
| lane | version | classes | holdout | status |
|---|---|---|---|---|
| **civic** | 0.2.1 | 13 routes + explicit `oos` class — OOS recall 96.8%, live-verified | 86.6% | free, demo (`lanes/civic-0.2.1.lanepack.tar.gz`) |
| **clinc150** | 0.1.4 | 150 generic intents + `oos` — hard-negative retrain | 73.8% · OOS AUROC 0.842 | free, certified (`lanes/clinc150-0.1.4.lanepack.tar.gz`) |
| **banking77** | 0.1.0 | 50 banking intents + `oos` | 73.3% in-scope · **84.4%** ID-OOS recall · 70.2% OOD-OOS · leak 1.6%/cov 58% @ conf 0.7 | free, certified (`lanes/banking77-0.1.0.lanepack.tar.gz`) |
| **banking77** | 0.1.1 | 50 banking intents + `oos` — ships eval_sample.jsonl for lane_repro | 73.3% in-scope · **84.4%** ID-OOS recall · repro: `lane_repro <pack>` replays embedded 200-row sample | free, certified (`lanes/banking77-0.1.1.lanepack.tar.gz`) |
| **civic_fr** | 0.1.1 | 11 FR routes + `oos` — OOS recall 90.9%, live-verified | template corpus; natural phrasings abstain (honest) | free, demo (`lanes/civic_fr-0.1.1.lanepack.tar.gz`) |
| **civic_fr** | 0.2.1 | 12 labels | 98.8% | free, demo (`lanes/civic_fr-0.2.1.lanepack.tar.gz`) |
| **helpdesk** | 0.2.0 | 6 IT routes + `oos` | demo — OOS recall 0.90 on hand-written negatives, live-verified + parity-checked | free, demo (`lanes/helpdesk-0.2.0.lanepack.tar.gz`) |
| **eq_tone** | 0.2.0 | 5 tone classes + `oos` — hard-negative retrain | ~50% in-scope (weak but honest, see note) · **87.9%** OOS recall on non-tone text · triage-only: floor conf≥0.9 (~5.6% auto) | free, demo (`lanes/eq_tone-0.2.0.lanepack.tar.gz`) |
| **pii** | 0.1.0 | PII + off-platform handoff flags (email/phone/IBAN/card/SSN/handoff) — obfuscation-resistant | 85.8% in-scope · 95.7% OOS · 90% natural | free, certified (`lanes/pii-0.1.0.lanepack.tar.gz`) |
| civic (old) | 0.1.0 | 13 civic defect routes (FixMyStreet) | **96.8%** on 941-row holdout · conformal α=.05 → 93.7% auto @ 0.79% err | free, certified (`lanes/civic-0.1.0.lanepack.tar.gz`) |
| civic_fr (old) | 0.1.0 | 11 FR routes + `oos` — template corpus (superseded by 0.1.1 retrain) | 100.0% | free, demo (`lanes/civic_fr-0.1.0.lanepack.tar.gz`) |
| civic_fr (old) | 0.2.0 | +110 natural phrasings; fixes confident-oos on natural text (v3w); qhat 0.746 @ alpha=0.02; trade-off: weaker in-dist oos recall | 98.8% | free, demo (`lanes/civic_fr-0.2.0.lanepack.tar.gz`) |
| clinc150 (old) | 0.1.2 | 150 generic intents + `oos` (superseded — labels.txt dropped 3 classes) | 73.8% | free, certified (`lanes/clinc150-0.1.2.lanepack.tar.gz`) |
| clinc150 (old) | 0.1.3 | 150 generic intents + `oos` (superseded by 0.1.4 hard-negative retrain) | 73.8% | free, certified (`lanes/clinc150-0.1.3.lanepack.tar.gz`) |
| eq_tone (old) | 0.1.1 | 5 tone classes, no `oos` (superseded by 0.2.0 hard-negative retrain) | 51.4% | free, demo (`lanes/eq_tone-0.1.1.lanepack.tar.gz`) |
| helpdesk (old) | 0.1.1 | 5 IT routes + escalate | demo pack — no certified holdout | free, demo (`lanes/helpdesk-0.1.1.lanepack.tar.gz`) |

<!-- lanes:end -->

`eq_tone` is published deliberately: a generic-vocab public dataset gives a weak
lane (cf. clinc150's stronger 73.8%), and its honest conformal numbers show *why*
calibrated abstention and domain-fitted heads matter. Certified lanes keep a
higher bar.

`clinc150` 0.1.2 replaces 0.1.x — same weights (sha256 `2110652d…338ec`), the
0.1.0 `labels.txt` dropped 3 of 151 classes. Found by `lane_verify.py`.

## Verify a pack

`lanes/SHA256SUMS.txt` pins every tarball. With mtlm-router checked out:

```sh
curl -LO https://github.com/javimosch/mtlm-heads/raw/master/lanes/eq_tone-0.1.1.lanepack.tar.gz
python3 tools/lane_verify.py eq_tone-0.1.1.lanepack.tar.gz --sums lanes/SHA256SUMS.txt
```

`lane_verify.py` checks the tarball checksum, head↔manifest sha256, manifest
schema, labels↔taxonomy agreement, the head's embedded class count, and the
certified-claim gate. Exit 0 = verified.

## Install a lane

`index.json` (generated, never hand-edited) is the machine-readable registry —
name, version, url, sha256s, taxonomy, status, holdout metrics, conformal
points per pack. One command resolves, downloads, verifies and installs:

```sh
python3 tools/lane_install.py eq_tone --appliance ./mtlm-router-v0.5.0-linux-amd64 --apply
# verifies shas, writes models/, patches start.sh env — restart and it's live
python3 tools/lane_install.py --appliance . --list      # what's installed
python3 tools/lane_install.py --appliance . --uninstall eq_tone
```

## Pricing & licensing

[PRICING.md](PRICING.md) — free demo/certified lanes are Apache-2.0; commercial
and custom lanes ship the same pack format under a commercial license with a
recalibration window. Every pack's `manifest.json` (and `index.json`) carries
`pricing.tier` + `license` — terms visible before download.

## Custom lanes

A lane fitted on *your* taxonomy + *your* export (~50 labeled examples per
route for a working lane, full export + calibration for a certified point)
is the pilot offer — contact via the repo owner. Client-fitted heads and
client-derived corpora stay private, always.
