# Reading the drafts as a support lead would

The grader in `grade.md` checks routing: tier, topic, outcome, and whether a reply cites the right
article. It cannot tell whether a reply is actually right to send. So every draft and handoff in
this run was also read by hand against the KB and the account data, and marked the way a lead
would mark it before it goes out.

This read was done by the AI agent that built the tool, not by a person. It is a second opinion,
not a sign-off.

## Customer replies (20)

| Verdict | Count | Tickets |
|---|---|---|
| Send as written | 12 | T-01, T-02, T-03, T-04, T-05, T-06, T-09, T-10, T-17, T-19, T-20, T-21 |
| Small edit | 4 | T-07, T-08, T-13, T-18 |
| Must fix before sending | 4 | T-14, T-15, T-16, T-22 |

### Must fix

- **T-14 (payment failed).** The reply says "Your Pro plan stays active" while the card is
  retried. That is the KB-14 rule for a failed *renewal*. The account data shows something else:
  the subscription is `incomplete` because the *first* payment was declined, so the plan never
  started. The model had the right data and applied the wrong rule.
- **T-15 (refund, forgot to cancel).** The reply tells the customer "this qualifies for our refund
  policy". KB-13 also requires fewer than 50 credits used since the charge, and usage is not in the
  account data. The model knew this (its note to the reviewer says to check usage first) but the
  customer-facing text promises it anyway.
- **T-16 (invoice with VAT number).** The reply promises a corrected invoice copy "shortly" but
  never asks for the VAT number, which the customer did not give. The note to the reviewer spots
  this; the reply does not.
- **T-22 ($50 charge).** The customer asked why the charge was $50. The reply explains it
  correctly (they are on Team) and then offers a refund if they "switch right away". KB-13's
  subscription refund moves the account to Free, not to Pro, so the offer mixes two policies. It
  also offers money nobody asked for.

### Small edit

- **T-07.** Suggests two cofounders could share one Pro login to save money. The KB does not say
  that is allowed, and a lead would not suggest it.
- **T-08.** Missing the "Buildbox Support" sign-off the prompt asks for.
- **T-13.** Says "only one pack's worth of 200 credits was applied to your account". That is the
  customer's claim; the account data has no credit balance in it.
- **T-18.** Checked the proration math ($50 Team, minus $20 unused Pro, is $30) in its note, but the
  reply only says "an odd number". Saying "$30" would answer the ticket better.

## Engineering handoffs (8)

Every evidence line in all eight notes was found word for word in its ticket (the code checks
this). The notes are usable. Two things a lead would change:

- **T-23 (all deploys queued).** The holding reply to the customer says "We can see your deploys
  ... have been queued far longer than expected". Nobody looked; the tool has no access to deploy
  status. It should say "you've told us" rather than "we can see".
- **T-23 severity.** Marked sev2 (one customer blocked). Four projects stuck with a green status
  page could be a platform-wide queue problem. The note does ask engineering whether it is wider,
  but sev1 until proven otherwise is the safer call.

## Weekly digest

The counts and ticket ids are computed by code, and every quote was verified against its ticket.
The grouping is the model's, and two groupings are weak:

- T-04 (where to put a Stripe key, answered from the KB) sits under "Deploys and environment
  variables fail in ways customers can't fix". It was a how-to question, not a failure.
- T-01 and T-10 (how credits reset) are folded into the billing theme with double charges and
  refunds, which makes billing look bigger than it is.

The proposed product actions are reasonable starting points, not validated decisions. "Raise the
build time limit" rests on one ticket that the KB already answers.
