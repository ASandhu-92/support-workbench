# Review checklist for the 2026-09-29 run

The grader in `grade.md` checks routing: tier, topic, outcome, and whether a reply cites the
right article. It cannot tell whether a reply is right to send. This sheet is for a person to read
every draft, handoff and the digest against the help center (`kb/`) and the account data in
`run.json`, and mark it the way a support lead would before anything goes out.

The earlier read of the 2026-09-23 run, done by the AI agent that built the tool, is in
`2026-09-23/review.md`. This one is left blank for a person to fill in.

How to fill it in:

- **Verdict:** `send` (as written), `edit` (small change), `fix` (must change before sending), or
  `wrong` (the outcome itself is wrong, for example it should have escalated).
- **Edits:** what you changed, in a few words.
- **Serious errors:** anything that would mislead the customer, promise something the policy does
  not allow, or move money wrongly. Leave it empty if there are none.
- **Minutes:** how long the read and edit took you, to the nearest minute.

## Customer replies (18) - `replies.md`

| Ticket | Subject | Verdict | Edits | Serious errors | Minutes |
|---|---|---|---|---|---|
| T-01 | Out of credits already?? | | | | |
| T-02 | custom domain | | | | |
| T-03 | Will Buildbox overwrite my GitHub edits? | | | | |
| T-04 | Where do I put my Stripe key | | | | |
| T-05 | adding a teammate | | | | |
| T-06 | Getting my code out | | | | |
| T-07 | Pro vs Team | | | | |
| T-08 | site says NOT SECURE | | | | |
| T-09 | Deploy failed | | | | |
| T-10 | Do credits carry over | | | | |
| T-13 | Charged twice for credit pack | | | | |
| T-14 | payment failed email | | | | |
| T-16 | Invoice with company details | | | | |
| T-17 | Where is my refund | | | | |
| T-18 | Weird charge after upgrading | | | | |
| T-20 | change email on account | | | | |
| T-21 | Owner left the company | | | | |
| T-22 | $50 charge?? | | | | |

T-13: the sandbox refund from `2026-09-23/approval-demo.md` is still on this account, so the
draft proposes nothing. See the note in `grade.md`.

## Billing proposals (2) - `replies.md`

Read the reply and the proposed action. Would you approve the action as proposed?

| Ticket | Subject | Proposed | Verdict | Edits | Serious errors | Minutes |
|---|---|---|---|---|---|---|
| T-15 | Refund please, forgot to cancel | refund | | | | |
| T-19 | Cancel my subscription | cancel | | | | |

## No source in the help center (2) - `replies.md`

These go to a person with the gap noted. Check the note is accurate and the gap is real.

| Ticket | Subject | Verdict | Edits | Serious errors | Minutes |
|---|---|---|---|---|---|
| T-11 | SOC 2 report request | | | | |
| T-12 | Nonprofit discount? | | | | |

## Engineering handoffs (8) - `escalations/`

Check the severity, that the evidence lines are the customer's words, and that the holding reply
promises nothing the team cannot do.

| Ticket | Subject | Verdict | Edits | Serious errors | Minutes |
|---|---|---|---|---|---|
| T-23 | All deploys stuck in Queued | | | | |
| T-24 | GitHub sync deleted my files | | | | |
| T-25 | SSL pending for 3 days | | | | |
| T-26 | 500 error on every prompt + credits gone | | | | |
| T-27 | database empty after redeploy | | | | |
| T-28 | Blank preview in Safari | | | | |
| T-29 | env vars not in production | | | | |
| T-30 | credits going down twice as fast | | | | |

## Digest - `digest.md`

| Item | Verdict | Edits | Serious errors | Minutes |
|---|---|---|---|---|
| Headline | | | | |
| Themes and grouping | | | | |
| Suggested changes | | | | |
| Quotes | | | | |
| Knowledge base gaps | | | | |

## Held-out set (8) - `heldout/replies.md`

Written after the prompt changes and before any run on them (`expected/heldout.json` says what
each one tests). H-03 escalated for lack of a billing record where the answer key expected a reply
asking which email the customer paid with.

| Ticket | Subject | Outcome | Verdict | Edits | Serious errors | Minutes |
|---|---|---|---|---|---|---|
| H-01 | custom domain help | reply | | | | |
| H-02 | Pause my plan? | no source | | | | |
| H-03 | Charged twice | no source | | | | |
| H-04 | Re: double credit pack | reply | | | | |
| H-05 | another pack by mistake | reply | | | | |
| H-06 | payment failed again | reply | | | | |
| H-07 | Refund Team, go back to Free | refund proposed | | | | |
| H-08 | VAT number on invoices | reply | | | | |

## Totals

| | |
|---|---|
| Send as written | |
| Small edit | |
| Must fix | |
| Wrong outcome | |
| Total minutes | |
| Reviewed by, date | |
