# Voice of customer, 2026-09-14 to 2026-09-22

**A redeploy left one live database with zero rows out of about 1,200 bookings, and GitHub sync deleted a customer's /api folder, so data loss on deploy and sync is this week's top issue.**

Counts and ticket ids are computed from the tickets. The suggested changes are hypotheses from one week of tickets, not decisions.

| Theme | Kind | Tickets | Count | Owner | Suggested change (hypothesis) |
|---|---|---|---|---|---|
| Unexpected or duplicate charges, refunds and invoices | billing and account | T-13, T-18, T-22, T-14, T-15, T-16, T-17 | 7 | billing | We think a prorated price preview before confirming an upgrade, plus a disabled buy button after the first click on credit packs, would reduce the surprise charges in T-13, T-18 and T-22. Test it and compare charge disputes. |
| Setting up domains, deploys, GitHub, keys and exports | how-to question | T-02, T-08, T-09, T-03, T-04, T-06 | 6 | product | We think a status line next to Verified that says the certificate is still being issued, and roughly how long it takes, would stop worry like T-08. Test it and check whether domain how-to tickets fall. |
| Plan choice, seats, ownership and cancellation | billing and account | T-05, T-07, T-19, T-20, T-21 | 5 | product | Based mainly on T-21, we think letting an Admin request an owner transfer, with identity checks, would remove a manual support step. Test it with a short form and measure resolution time. |
| Live app lost data or config after deploy or sync | product defect | T-27, T-24, T-29 | 3 | engineering | We think an automatic snapshot of the production database, plus a confirmation that lists files a sync commit will delete, would prevent most of this loss. Test it by enabling both for a small set of projects and comparing restore requests. |
| Editor errors and credits charged wrongly | product defect | T-26, T-30, T-28 | 3 | engineering | We think automatically refunding credits whenever a generation fails with a server error would remove the sting of these failures. Test it on 500 errors first, then check whether T-30 double charging is the same bug. |
| Deploys and certificates stuck with no explanation | product defect | T-23, T-25 | 2 | engineering | We think a status page entry that flips automatically when deploy queue wait passes 15 minutes would cut support contacts like T-23. Test it for one month and compare ticket volume. |
| Credit balance and reset confusion | how-to question | T-01, T-10 | 2 | product | We think showing the next reset date and carry-over rule beside the credit balance, and on the zero-credits message, would answer these questions in the product. Test it with a small group and watch for repeat questions. This rests on two tickets. |
| Security review and discount requests | request | T-11, T-12 | 2 | sales | We think a public trust page with SOC 2 status, hosting region and an NDA report request form would help buyers like T-11. Separately, decide whether to offer a nonprofit discount as in T-12, which rests on one ticket. |

## In their words

- **Unexpected or duplicate charges, refunds and invoices** (T-18): "Please explain, this looks wrong."
- **Setting up domains, deploys, GitHub, keys and exports** (T-08): "Did I break something?"
- **Plan choice, seats, ownership and cancellation** (T-21): "The person who created our Team workspace left the company last month and nobody can log in as them."
- **Live app lost data or config after deploy or sync** (T-27): "We had about 1,200 customer bookings in there."
- **Editor errors and credits charged wrongly** (T-26): "And my credits went down each time, I lost about 30 credits for nothing."
- **Deploys and certificates stuck with no explanation** (T-23): "I have a launch tomorrow morning."
- **Credit balance and reset confusion** (T-01): "I'm on Pro and it says I have 0 credits left."
- **Security review and discount requests** (T-11): "Our security team is reviewing Buildbox before we roll it out to 40 people."

## Knowledge base gaps

- T-11: The KB has nothing on SOC 2 or other security certifications, sharing compliance reports under NDA, or where customer data is hosted (region or cloud provider). Only KB-11 mentions daily database snapshots, with no location details.
- T-12: The knowledge base has no information on whether Buildbox offers nonprofit or education discounts, or how to apply for one. It only lists standard prices (KB-03).
