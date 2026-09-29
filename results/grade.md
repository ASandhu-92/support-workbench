# Grade

Run 2026-09-29T19:57:05+00:00, model claude-sonnet-5-5, 61 model calls, cost $1.0325 (list price), wall time 140.3s with 4 tickets in parallel.

| Measure | Result |
|---|---|
| tier accuracy | 30/30 (100%) |
| topic accuracy | 29/30 (97%) |
| action accuracy | 29/30 (97%) |
| drafts sent for review | 20 |
| drafts citing a kb article | 20/20 (100%) |
| drafts citing an expected article | 20/20 (100%) |
| escalations correct | 10/10 (100%) |
| escalations missed | [] |
| escalations not needed | [] |
| billing proposals correct | 2/3 (67%) |
| billing proposals unexpected | [] |
| unapproved billing writes | 0 |
| stripe refunds created during run | 0 |

## Misses

**tier:** none

**topic:** T-18: expected billing-plan-changes, got billing-charges

**action:** T-13: expected propose-billing-action, got reply

Note on T-13, added by hand after the run: this is not a model error. The duplicate charge
(ch_...WSpd) was refunded in the sandbox on 2026-09-23 at 07:28 UTC (re_...SrUa), the refund
shown in `results/2026-09-23/approval-demo.md`. A lookup on 2026-09-29 still shows it. The
draft saw that refund, proposed nothing, and told the customer so, which is the right answer
for the account as it is now. `expected/expected.json` describes the account before the refund
and was left unchanged, so the grader still counts this as a miss.
