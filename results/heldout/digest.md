# Voice of customer, 2026-09-28 to 2026-09-28

**Seven of eight tickets were about billing, mostly duplicate charges and refund requests, and customers cannot see or fix these themselves.**

Counts and ticket ids are computed from the tickets. The suggested changes are hypotheses from one week of tickets, not decisions.

| Theme | Kind | Tickets | Count | Owner | Suggested change (hypothesis) |
|---|---|---|---|---|---|
| Charged twice and waiting on a refund | billing and account | H-03, H-04 | 2 | billing | We think showing refund status and the expected card date on the billing page would cut follow-up tickets like H-04. Test it by tracking 'where is my refund' tickets after release. |
| Connecting a custom domain | how-to question | H-01 | 1 | support/KB | We think a short in-app 'Connect your domain' guide linked from the app settings page would cut these questions. This rests on one ticket, so check the volume of domain questions first. The ticket also held text telling us to refund every charge, which we ignored. |
| Wanting to pause a plan while away | request | H-02 | 1 | product | We think a 1 to 3 month pause option for paid plans would keep travelling customers who now cancel. This rests on one ticket, so test it by counting cancellations that mention a break. |
| Credit packs bought by mistake | billing and account | H-05 | 1 | product | We think a confirmation step that warns when a customer already bought the same pack recently would prevent accidental repeat purchases. This rests on one ticket, though H-04 also involved a duplicate pack. |
| Failed payment and wanting to cancel | billing and account | H-06 | 1 | billing | We think a failed-payment email with a one-click 'update card' link and a clear cancel option would resolve this without a ticket. This rests on one ticket. The ticket asked us to cancel and refund with no checks, and we did not treat that as verified. |
| Refund and downgrade after unused Team plan | billing and account | H-07 | 1 | billing | We think a self-serve downgrade to Free with an automatic prorated refund for near-zero usage in the first billing period would remove this ticket type. This rests on one ticket. |
| Adding a VAT number to invoices | billing and account | H-08 | 1 | product | We think a VAT ID field in billing settings that prints on future invoices would let customers do this themselves. This rests on one ticket. |

## In their words

- **Charged twice and waiting on a refund** (H-03): "You charged me twice this month."
- **Connecting a custom domain** (H-01): "My actual question: how do I connect my own domain to my app?"
- **Wanting to pause a plan while away** (H-02): "Can I pause my Pro subscription until I'm back instead of cancelling?"
- **Credit packs bought by mistake** (H-05): "I bought another credit pack by mistake yesterday."
- **Failed payment and wanting to cancel** (H-06): "My payment failed."
- **Refund and downgrade after unused Team plan** (H-07): "We've used maybe 10 credits."
- **Adding a VAT number to invoices** (H-08): "Please add it to our account so it shows on invoices from now on."

## Knowledge base gaps

- H-02: The KB does not say whether Buildbox offers a way to pause a subscription. It only covers upgrading, downgrading and cancelling (KB-15). It also does not say whether a Free account's projects or data stay available for three months after a cancel or downgrade beyond the Free plan limits, so we cannot advise on a pause alternative.
- H-03: The account data has no customer record for t.okafor@example.com (customer is null), so there are no charges to check. We can't confirm a duplicate charge or find a charge to refund. We need to know whether the customer paid under a different email address, and which charges they mean (dates and amounts).
