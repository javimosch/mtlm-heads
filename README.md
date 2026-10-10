# mtlm-heads — the lane catalog

Certified decision lanes for [mtlm-router](https://github.com/javimosch/mtlm-router)
— the self-hosted 7M-param typed decision layer. Drop a `.lanepack` into the
appliance and the request type it covers is routed, calibrated, and abstains
honestly when it shouldn't guess.

Format: [SPEC.md](SPEC.md). Every pack ships its eval — you see the numbers
before you trust the lane.

## Catalog

| lane | version | classes | holdout | status |
|---|---|---|---|---|
| **clinc150** | 0.1.0 | 151 generic intents | 73.8% · OOS AUROC 0.842 | free, certified (`lanes/clinc150-0.1.0.lanepack.tar.gz`) |
| **helpdesk** | 0.1.0 | 5 IT routes + escalate | demo pack — no certified holdout | free (`lanes/helpdesk-0.1.0.lanepack.tar.gz`) |

## Custom lanes

A lane fitted on *your* taxonomy + *your* export (~50 labeled examples per
route for a working lane, full export + calibration for a certified point)
is the pilot offer — contact via the repo owner.
