# A refund, from proposal to money moving

This is what happened to ticket T-13 (Dana, charged twice for one credit pack) after the graded
run. Stripe object ids are shortened to their last four characters.

## 1. The pipeline proposed it and stopped

The graded run drafted a reply citing KB-13 (duplicate charges are always refunded) and proposed
a $10 refund of one of the two charges. It did not issue it. The grade for that run shows
`unapproved billing writes: 0` and `stripe refunds created during run: 0`; the second number is
read back from Stripe, not from our own log.

## 2. A person runs the command, and it refuses twice

```
$ python billing.py refund ch_****WSpd --reason "duplicate credit pack charge (T-13)"
refused: refund on ch_****WSpd needs --confirm. Nothing was changed.
exit=2

$ python billing.py refund ch_****WSpd --reason "duplicate credit pack charge (T-13)" --confirm
refused: refund on ch_****WSpd needs --approved-by. Nothing was changed.
exit=2

$ python billing.py refund ch_****WSpd --reason "duplicate credit pack charge (T-13)" --confirm --approved-by "support lead"
{
  "refund": "re_****SrUa",
  "amount_usd": 10.0,
  "status": "succeeded"
}
exit=0
```

## 3. The audit log has all three attempts

```
{"at": "2026-09-23T07:28:23+00:00", "action": "refund", "target": "ch_****WSpd", "reason": "duplicate credit pack charge (T-13)", "approved_by": null, "executed": false, "refused": "missing --confirm"}
{"at": "2026-09-23T07:28:23+00:00", "action": "refund", "target": "ch_****WSpd", "reason": "duplicate credit pack charge (T-13)", "approved_by": null, "executed": false, "refused": "missing --approved-by"}
{"at": "2026-09-23T07:28:24+00:00", "action": "refund", "target": "ch_****WSpd", "reason": "duplicate credit pack charge (T-13)", "approved_by": "support lead", "executed": true, "stripe_id": "re_****SrUa", "amount_usd": 10.0, "status": "succeeded"}
```

The approver's name is also written onto the refund itself in Stripe (`metadata.approved_by`).

## 4. Running the ticket again does not refund twice

The pipeline was then run a second time on a copy of the repo, with the cache on. 59 of 61 model
calls came from the cache ($0.13 spent instead of $1.51, 79 seconds instead of 262). The two that
ran again were T-13's draft, because its account data had changed, and the digest, because
T-13's outcome had changed.

The new T-13 draft saw the refund in Stripe, proposed no action, and told the customer instead:

> Thanks for flagging this, and sorry for the confusion. We can see that two $10 charges did go
> through for the credit pack, most likely from that slow click. Good news: one of them was
> already refunded in full as a duplicate.
>
> The refund should appear on your statement within 5 to 10 business days, depending on your
> bank. [...]

On that second run the grader marks T-13 wrong (expected: propose a refund), because
`expected/expected.json` describes the account before the refund. That rerun is not the one
committed in this folder.

One detail a reviewer should notice: the model picked the older of the two identical charges as
"the duplicate". For identical charges that makes no difference to the customer, but a team may
want a rule (refund the later one) so the records read the same way every time.
