# support-workbench

A small tool that works a support queue the way a support lead would want an AI to work it. It
reads each ticket, decides whether it is a how-to question (tier 1), a billing or account problem
(tier 2) or a bug for engineering (tier 3), and then drafts a reply that quotes the help center,
looks up the customer's billing in Stripe, or writes a handoff note for an engineer. Once a week it
summarizes what customers said for the rest of the company.

It never sends anything and never moves money. Every reply is a draft for a person. A refund or
cancellation is only a proposal until a named person runs the command with `--confirm`. If the
help center does not have the answer, it says so and hands the ticket to a person instead of
guessing.

The product, the customers and the tickets are invented. "Buildbox" is a made-up AI app builder
(prompt-to-app, deploys, custom domains, GitHub sync, credits and plans). The billing side runs
against a Stripe test-mode sandbox with real test objects; no real card or customer is involved.

## One real run, 30 tickets

Run on 2026-09-23 against `expected/expected.json`, which was written and committed before the
first run (see the git history).

| | Result |
|---|---|
| Tickets | 30 (12 how-to, 10 billing and account, 8 bugs; 2 of the how-to questions have no answer in the help center on purpose) |
| Tier correct | 29 of 30 |
| Topic correct | 30 of 30 |
| Outcome correct (reply / propose billing action / escalate to engineering / escalate: no source) | 30 of 30 |
| Replies that cite a help center article | 20 of 20, and all 20 cite an article the answer key expected |
| Tickets that needed escalating and were escalated | 10 of 10, with no unneeded escalations |
| Billing actions proposed for a person to approve | 3 of 3 correct (two refunds, one cancellation), none unexpected |
| Money moved without approval | 0 (our log shows no unapproved write, and Stripe shows no refund created during the run) |
| Replies a lead could send as written | 12 of 20; 4 need a small edit, 4 must be fixed first (see below) |
| Model | `claude-sonnet-5`, 61 calls |
| Cost | $1.47 at list price |
| Time | 262 seconds wall clock, 4 tickets at a time |

The rows from "Tier correct" to "Money moved without approval" are graded by code (`grade.py`). The "send as written" row is a read of every
draft against the help center and the account data; it was done by the AI agent that built the
tool, not by a person, and is in [`results/review.md`](results/review.md).

Where to look:

- [`results/tickets.md`](results/tickets.md): one line per ticket, expected against actual
- [`results/replies.md`](results/replies.md): every draft reply and proposed billing action
- [`results/escalations/`](results/escalations/): the eight engineering handoff notes
- [`results/digest.md`](results/digest.md): the weekly voice-of-customer summary
- [`results/grade.md`](results/grade.md): the grade, and [`results/run.json`](results/run.json) for everything raw
- [`results/approval-demo.md`](results/approval-demo.md): one proposed refund followed through to Stripe

## What it got wrong

The routing was close to perfect. The writing was not. Read these before trusting the headline
numbers.

- **T-11 tier.** A SOC 2 report request was put in tier 2 instead of tier 1. The outcome was still
  right: the help center has nothing on it, so it went to a person with the gap noted.
- **Four replies must be fixed before sending.**
  - T-14: told a customer whose *first* payment was declined that their plan "stays active" during
    retries. That rule is for renewals. The account data showed the plan never started.
  - T-15: told the customer their refund "qualifies" before the credit-usage check the policy
    requires. Its own note to the reviewer said to check usage first.
  - T-16: promised a corrected invoice but never asked for the VAT number it needs.
  - T-22: answered the question correctly, then offered a refund nobody asked for, under terms that
    mix two policies.
- **Four replies need a small edit.** One suggests sharing a login, one is missing its sign-off,
  one states the customer's claim as a checked fact, and one explains proration without the
  actual figure it had just checked.
- **One handoff says "we can see your deploys"** in the holding reply. The tool cannot see
  deploys. It rated a possible platform-wide deploy outage sev2 instead of sev1.
- **The digest groups two tickets loosely**, for example a how-to question about API keys filed
  under "failures customers can't fix".

The pattern: when the model is told a rule and has the data, it usually gets the decision right
and then overpromises in the customer-facing text. The notes it writes to the reviewer are more
careful than the replies. That is why a person reads every draft.

Why the scores are high: the same author wrote the tickets, the help center and the answer key in
one sitting, so the tickets are cleaner than real ones. This was one run, so run-to-run variation
was not measured. Treat 30 of 30 as "the guardrails route clean tickets correctly", not as a
prediction for a live queue.

## Guardrails

These are enforced in code, not only asked for in the prompt.

| Rule | Where | How it is checked |
|---|---|---|
| No answer without a source | `draft.py` `enforce()` | A reply with no valid article id (`KB-01` to `KB-15`) is thrown away and the ticket becomes `escalate: no source`. Invented article ids do not count. |
| No money moves without a person | `billing.py` `guard()` | `refund` and `cancel` refuse unless run with `--confirm` and `--approved-by <name>`. Refusals and approvals are both logged. The pipeline never calls either. |
| Test mode only | `billing.py` `check_key()` | Any key that is not a Stripe test key, including live and restricted live keys, is refused before a network call. |
| Proposals point at real objects | `draft.py` | A proposed refund or cancel must name a charge or subscription id that appears in the customer's account data. |
| Handoffs quote, not paraphrase | `escalate.py` | Every evidence line must appear word for word in the ticket, or it is flagged as unverified. |
| Digest numbers are counted, not written | `digest.py` | Counts come from the ticket ids; each quote is checked against its ticket. |
| Checked after the run | `run_all.py` | The grade reads the audit log and asks Stripe how many refunds were created during the run. |

`pytest` covers these without a network or a model: 25 tests.

## What it is not

- Not a helpdesk. There is no inbox, no sending, no customer login. It reads a JSON file of tickets
  and writes markdown.
- Not tested on real tickets. All 30 are invented.
- Not live billing. The Stripe side is a sandbox, and the code refuses anything else.
- Not a measure of how fast a person works with it. The machine side took 262 seconds for 30
  tickets, about 9 seconds each with four running at once. The human side (reading 20 drafts, fixing 8, approving 3 billing actions) was not timed.

## How a ticket moves through it

```
ticket
  |
  classify.py         tier 1/2/3, topic, urgency
  |
  +-- tier 3 ------> escalate.py    handoff note for engineering + holding reply
  |
  +-- tier 2 ------> billing.py lookup   customer, subscriptions, invoices, charges, refunds (read-only)
  |                     |
  +-- tier 1 ---------> draft.py     reply citing KB articles, or "escalate: no source",
                                     plus any refund/cancel as a proposal for a person
all tickets -------> digest.py      themes, counts, ticket ids, one quote each, proposed action
results -----------> grade.py       compared with expected/expected.json
```

## Run it

Needs Python 3.12, the `claude` CLI logged in, and for the billing part a Stripe sandbox key.

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest tests -q                     # no network, no model

export WORKBENCH_SECRETS_FILE=secrets/stripe.enc.env    # SOPS-encrypted, holds STRIPE_TEST_SECRET_KEY
./run.sh setup_sandbox.py                               # once: products + the 10 billing customers
./run.sh run_all.py                                     # the whole pipeline, writes results/
./run.sh run_all.py --no-cache                          # same, but call the model again for every step
.venv/bin/python run_all.py --no-stripe                 # without Stripe (billing drafts get weaker)
```

One stage at a time:

```
.venv/bin/python classify.py T-05
.venv/bin/python draft.py T-07
./run.sh draft.py T-13 --lookup
.venv/bin/python escalate.py T-24
./run.sh billing.py lookup dana.ivers@example.com
./run.sh billing.py refund ch_... --reason "duplicate charge"                                # refused
./run.sh billing.py refund ch_... --reason "duplicate charge" --confirm --approved-by "name"  # runs
.venv/bin/python digest.py                                # rebuild the digest from results/run.json
```

`run.sh` decrypts the key with `sops` into the environment of that one process and nothing else;
nothing is written to disk. Any other way of setting `STRIPE_TEST_SECRET_KEY` works too.
`setup_sandbox.py` writes the test ids it created to `data/customers.json`, which git ignores;
`data/customers.example.json` shows the shape.

### The model

All model calls go through `llm.py`, which runs the Claude Code CLI headless:

```
claude -p <prompt> --output-format json --json-schema <schema> --tools "" --model sonnet
  --no-session-persistence --setting-sources "" --strict-mcp-config --disable-slash-commands
  --system-prompt <...>
```

No tools, no MCP servers, no local settings, no saved session: the model gets the prompt and can
only answer in the given JSON shape. It runs on the logged-in Claude subscription, or on
`ANTHROPIC_API_KEY` if that is set. The $1.47 above is the `total_cost_usd` the CLI reported,
which is list price; this run used a subscription, and the API-key path was not tried.

Responses are cached in `.cache/` by a hash of the prompt, so a rerun of unchanged tickets costs
nothing. A rerun on a copy after the approved refund took 79 seconds and $0.13: 59 of 61 calls came
from the cache, and the two that did not were the ones whose input had changed. Em and en dashes in model
output are replaced with hyphens (house style); nothing else is changed.

## Files

```
data/tickets.json          30 invented tickets
data/customers.example.json  shape of the git-ignored file of sandbox ids
kb/                        15 help center articles for Buildbox
expected/expected.json     the answer key, written before the first run
llm.py                     the one module that calls a model
classify.py                tier, topic, urgency
draft.py                   cited reply or "escalate: no source", plus billing proposals
billing.py                 read-only Stripe lookups; refund/cancel behind --confirm
escalate.py                tier 3 handoff note
digest.py                  weekly voice-of-customer summary
grade.py                   scoring against the answer key
run_all.py                 the pipeline
setup_sandbox.py           creates the Stripe test products and customers
run.sh                     runs a script with the Stripe key from a SOPS file
tests/                     pytest, 25 tests
results/                   the committed run described above
```

## About

Written in September 2026 with Claude Code. The billing lookups follow the same test-mode approach
as [stripe-billing-module](https://github.com/ASandhu-92/stripe-billing-module). MIT licence.
