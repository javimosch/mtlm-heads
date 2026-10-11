# Lane pricing & licensing

The runtime, trunk, and tools are open source (mtlm-router, machin-anvil).
What is licensed are **lane packs** — calibrated decision heads plus their
eval evidence and provenance. You are not buying a weight file; you are
buying the certification around it: taxonomy design, leak-free eval,
conformal operating point, and recalibration support.

## Tiers

| tier | what's in the pack | license | price |
|---|---|---|---|
| **free / demo** | head + eval report, honestly labeled (incl. weak lanes) | Apache-2.0 | €0 |
| **free / certified** | head + holdout eval + conformal qhat + full provenance | Apache-2.0 | €0 |
| **commercial lane** | certified pack + commercial-use license + 12mo recalibration window | commercial (per-domain) | per agreement |
| **custom lane** | head trained on *your* exported route examples — your distribution, your taxonomy, your exclusivity | work-for-hire | per agreement |

## What "commercial lane" means concretely

- License grants production use of that lane's head within the licensed
  domain, on your own infrastructure — no egress, no per-call metering.
- Recalibration window: monitor drift (`tools/monitor.py`), and when the
  conformal operating point needs refitting we recalibrate against a fresh
  labeled split — the guarantee tracks your traffic, not the training set.
- A lane pack's `manifest.json` carries `pricing.tier` and `license`;
  `index.json` projects them so installers and buyers see terms before fetch.

## What stays private, always

- Client-fitted heads and client-derived corpora live in the private
  `mtlm-data` repo — never published, never resold, never folded into a
  public lane.
- A commercial lane built for one client is exclusive to that client.
- Public demo lanes exist so the format and the honesty bar are inspectable
  before anyone pays for anything — including lanes that *fail* certification
  (`eq_tone` ships its 51.4% eval openly; that is the point of the catalog).

## Why free certified lanes exist

They are the proof, not the product: `clinc150` demonstrates the format,
the verification tooling (`lane_verify.py`), and what a certified eval looks
like — on public data where the numbers can be checked by anyone.
