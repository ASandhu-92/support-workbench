# support-workbench

A small tool that works a support queue the way a support lead would want an AI to work it. It
reads each ticket, decides whether it is a how-to question (tier 1), a billing or account problem
(tier 2) or a bug for engineering (tier 3), and then drafts a reply that quotes the help center,
looks up the customer's billing in Stripe, or writes a handoff note for an engineer. Once a week it
summarizes what customers said for the rest of the company.

It never sends anything and never moves money. Every reply is a draft for a person. A refund or
cancellation is only a proposal until a person runs the command with `--confirm` and their name. If the
help center does not have the answer, it says so and hands the ticket to a person instead of
guessing.

**Start here:** the table below, then [`results/review.md`](results/review.md) (the checklist a
person fills in for every draft) and [`results/replies.md`](results/replies.md).

The product, the customers and the tickets are invented. "Buildbox" is a made-up AI app builder
(prompt-to-app, deploys, custom domains, GitHub sync, credits and plans). The billing side runs
against a Stripe test-mode sandbox with real test objects; no real card or customer is involved.

## Two runs, 30 tickets, and 8 held-out tickets

The answer key `expected/expected.json` was written and committed before the first run, and
`expected/heldout.json` before any run on the held-out tickets (see the git history). The first run
found problems in the replies (below). The prompts and guardrails were changed, and the same 30
tickets were run again from scratch, with no cache. The 8 held-out tickets were written after those
changes, to test things the first 30 did not. Both sets were run again, from scratch, after
one more fix (H-07 and T-15 below); the numbers are from those runs.

| | 2026-09-23, first run | 2026-09-29, after the fixes | 2026-09-29, held-out |
|---|---|---|---|
| Tickets | 30 | 30 | 8 |
| Tier correct | 29 of 30 | 30 of 30 | 8 of 8 |
| Topic correct | 30 of 30 | 28 of 30 (T-13, T-18) | 7 of 8 |
| Outcome correct (reply / propose billing action / escalate to engineering / escalate: no source) | 30 of 30 | 29 of 30 (T-13, see below) | 7 of 8 |
| Replies that cite an article the answer key expected | 20 of 20 | 20 of 20 | 6 of 6 |
| Tickets that needed escalating and were escalated | 10 of 10 | 10 of 10 | 1 of 1, plus one not needed (H-03) |
| Billing actions proposed for a person to approve | 3 of 3 | 2 of 3 (T-13) | 1 of 1 |
| Money moved without approval | 0 | 0 | 0 |
| Replies a lead could send as written | 12 of 20, read by the AI agent | not read yet | not read yet |
| Model | `claude-sonnet-5`, 61 calls | `claude-sonnet-5-5`, 61 calls | `claude-sonnet-5-5`, 17 calls |
| Cost at list price | $1.47 | $1.03 | $0.27 |
| Time, 4 tickets at a time | 262 s | 131 s | 48 s |

The 30 tickets are the same in both runs. The tickets are split 12 how-to, 10 billing and account
and 8 bugs, and 2 of the how-to questions have no answer in the help center on purpose. The
held-out tickets test instructions hidden in a ticket, a request the policy does not cover, a
customer with no billing record, billing that changed since the first run, a claim the account data
does not support, a refund whose policy condition is not in the account data, and a self-serve task.

Every row down to "Money moved without approval" is graded by code (`grade.py`). "Money moved
without approval" is checked twice: our audit log shows no unapproved write, and Stripe shows no
refund created during the run. The "send as written" row needs a person. For the first run it was
done by the AI agent that built the tool, not by a person
([`results/2026-09-23/review.md`](results/2026-09-23/review.md)). For the new runs it has not been
done yet; [`results/review.md`](results/review.md) is the blank checklist for it.

Where to look:

- [`results/tickets.md`](results/tickets.md): one line per ticket, expected against actual
- [`results/replies.md`](results/replies.md): every draft reply and proposed billing action
- [`results/escalations/`](results/escalations/): the eight engineering handoff notes
- [`results/digest.md`](results/digest.md): the weekly voice-of-customer summary
- [`results/grade.md`](results/grade.md): the grade, and [`results/run.json`](results/run.json) for everything raw
- [`results/heldout/`](results/heldout/): the same files for the held-out run
- [`results/2026-09-23/`](results/2026-09-23/): the first run, its review, and
  [`approval-demo.md`](results/2026-09-23/approval-demo.md), one proposed refund followed through to Stripe

## What it got wrong

### First run

The routing was close to perfect. The writing was not.

- **T-11 tier.** A SOC 2 report request was put in tier 2 instead of tier 1. The outcome was still
  right: the help center has nothing on it, so it went to a person with the gap noted.
- **Four replies had to be fixed before sending.**
  - T-14: told a customer whose *first* payment was declined that their plan "stays active" during
    retries. That rule is for renewals. The account data showed the plan never started.
  - T-15: told the customer their refund "qualifies" before the credit-usage check the policy
    requires. Its own note to the reviewer said to check usage first.
  - T-16: promised a corrected invoice but never asked for the VAT number it needs.
  - T-22: answered the question correctly, then offered a refund nobody asked for, under terms that
    mix two policies.
- **Four replies needed a small edit.** One suggests sharing a login, one is missing its sign-off,
  one states the customer's claim as a checked fact, and one explains proration without the
  actual figure it had just checked.
- **One handoff said "we can see your deploys"** in the holding reply. The tool cannot see
  deploys. It rated a possible platform-wide deploy outage sev2 instead of sev1.
- **The digest grouped two tickets loosely**, for example a how-to question about API keys filed
  under "failures customers can't fix".

The pattern: when the model is told a rule and has the data, it usually gets the decision right
and then overpromises in the customer-facing text. The notes it writes to the reviewer are more
careful than the replies.

What changed after it: prompt rules for each of the four failures and the small-edit patterns; a
severity rubric; holding replies that claim "we can see" are flagged; a billing proposal with an
unknown target goes to manual review; a policy condition the account data cannot show blocks
approval (next section); the digest labels each theme's kind and marks suggested changes as
hypotheses. Whether the replies are now right to send is what the checklist is for. The grader
cannot tell.

### Second run and held-out

- **T-13 outcome and topic.** Not a model error. The duplicate charge was refunded in the sandbox during the
  approval demo on 2026-09-23 and is still refunded. The draft saw that, proposed nothing and told
  the customer, and filed it under refunds. The answer key describes the account before the refund
  and was left as it was, so the grader counts two misses. Note in [`results/grade.md`](results/grade.md).
- **T-18 topic.** A charge after an upgrade was filed as `billing-charges` instead of
  `billing-plan-changes`. The reply was still the expected one.
- **H-03.** A customer with no billing record said they were charged twice. The answer key
  expected a reply asking which email they paid with. The tool sent it to a person instead, with
  that question in its note. Safe, but slower for the customer.
- **H-07 and T-15, a subscription refund without the cancel.** KB-13 says a refunded Pro or Team
  charge also cancels the plan. The replies told the customer that, but the proposal only carried
  the refund command, so an approver following it would refund and leave the plan running. A
  refund proposal can now carry the subscription to cancel (`also_cancel_subscription_id`), checked
  like any other target, and the draft prints both commands. Both sets were run again after this
  change, and H-07 and T-15 now show both commands.

Why the scores are high: the same author wrote the tickets, the help center and both answer keys,
so the tickets are cleaner than real ones. The held-out set is small (8) and was written after the
author had seen the first run's mistakes. Each set was run once per version, so run-to-run
variation was not measured. Treat the numbers as "the guardrails route clean tickets correctly",
not as a prediction for a live queue.

## Guardrails

These are enforced in code, not only asked for in the prompt.

| Rule | Where | How it is checked |
|---|---|---|
| No answer without a source | `draft.py` `enforce()` | A reply with no valid article id (`KB-01` to `KB-15`) is thrown away and the ticket becomes `escalate: no source`. Invented article ids do not count. |
| No money moves without a person | `billing.py` `guard()` | `refund` and `cancel` refuse unless run with `--confirm` and `--approved-by <name>`. Refusals, approvals and writes that fail at Stripe are all logged. A refund amount of 0 or less is refused. The pipeline never calls either. |
| Test mode only | `billing.py` `check_key()` | Any key that is not a Stripe test key, including live and restricted live keys, is refused before a network call. |
| Proposals point at real objects | `draft.py` | A proposed refund or cancel must name, exactly, a charge or subscription id of the right type from the customer's account data. Anything else puts the ticket in `manual review`: the proposal is marked blocked and no command is offered. |
| A refund that cancels the plan says so | `draft.py` | When the policy says a refund also cancels the plan, the proposal names the subscription too. It must be one of the customer's subscriptions, and only a refund can carry it; otherwise the ticket goes to manual review. The approver gets a refund command and a cancel command. |
| Unchecked conditions block approval | `draft.py` | The model must list every policy condition the account data does not show (for example credits used since the charge) in `unverified_conditions`. A proposal with any listed is not ready for approval, and the conditions are printed above the command. |
| Handoffs quote, not paraphrase | `escalate.py` | Every evidence line must appear word for word in the ticket, or it is flagged as unverified. |
| Digest numbers are counted, not written | `digest.py` | Counts come from the ticket ids; each quote is checked against its ticket. |
| Checked after the run | `run_all.py` | The grade reads the audit log and asks Stripe how many refunds were created during the run. |

`--confirm` and `--approved-by` are an acknowledgement, not authentication. The tool records the
name it is given and cannot check who typed it. In a real team this would sit behind a login.

`pytest` covers these without a network or a model: 46 tests. CI runs them on Python 3.12 and
3.13, with the versions pinned in `constraints.txt`.

## What it is not

- Not a helpdesk. There is no inbox, no sending, no customer login. It reads a JSON file of tickets
  and writes markdown.
- Not tested on real tickets. All 38 are invented.
- Not live billing. The Stripe side is a sandbox, and the code refuses anything else.
- Not a measure of how fast a person works with it. The machine side of the second run took 131
  seconds for 30 tickets, about 4 seconds each with four running at once. The human side has not
  been timed yet; the checklist has a minutes column for it.

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
.venv/bin/pip install -r requirements.txt -c constraints.txt   # optional: the versions CI uses
.venv/bin/python -m pytest tests -q                     # no network, no model

export WORKBENCH_SECRETS_FILE=secrets/stripe.enc.env    # SOPS-encrypted, holds STRIPE_TEST_SECRET_KEY
./run.sh setup_sandbox.py                               # once: products + the 10 billing customers
./run.sh run_all.py                                     # the whole pipeline, writes results/
./run.sh run_all.py --no-cache                          # same, but call the model again for every step
./run.sh run_all.py --set heldout                       # the 8 held-out tickets, writes results/heldout/
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
`ANTHROPIC_API_KEY` if that is set. The costs above are the `total_cost_usd` the CLI reported,
which is list price; every run used a subscription, and the API-key path was not tried.

Responses are cached in `.cache/` by a hash of the prompt, so a rerun of unchanged tickets costs
nothing. A rerun on a copy after the approved refund took 79 seconds and $0.13: 59 of 61 calls came
from the cache, and the two that did not were the ones whose input had changed. Em and en dashes in model
output are replaced with hyphens (house style); nothing else is changed.

## Files

```
data/tickets.json          30 invented tickets
data/heldout.json          8 held-out tickets, written after the first run's fixes
data/customers.example.json  shape of the git-ignored file of sandbox ids
kb/                        15 help center articles for Buildbox
expected/expected.json     the answer key, written before the first run
expected/heldout.json      the held-out answer key, written before any run on them
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
tests/                     pytest, 46 tests
constraints.txt            the package versions CI tests with
.github/workflows/         CI: the offline tests on Python 3.12 and 3.13
results/                   the second run; heldout/ and 2026-09-23/ hold the other two
```

## About

Written in September 2026 with Claude Code. The billing lookups follow the same test-mode approach
as [stripe-billing-module](https://github.com/ASandhu-92/stripe-billing-module). MIT licence.
