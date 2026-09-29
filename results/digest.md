# Voice of customer, 2026-09-14 to 2026-09-22

**Two customers lost data this week (a live database emptied after a redeploy, and a GitHub sync commit that deleted 14 files), and both need engineering attention before anything else.**

Counts and ticket ids are computed from the tickets. The suggested changes are hypotheses from one week of tickets, not decisions.

| Theme | Kind | Tickets | Count | Owner | Suggested change (hypothesis) |
|---|---|---|---|---|---|
| Unexpected charges, refunds, cancellations and invoices | billing and account | T-13, T-14, T-15, T-16, T-17, T-18, T-19, T-22 | 8 | billing | We think a prorated-charge breakdown on the upgrade screen and a renewal reminder email a few days before charge would reduce the confusion and forgotten-cancel refunds seen in T-15, T-18 and T-22. Also test blocking a second credit pack purchase within a few minutes (T-13 rests on one ticket). |
| Setup questions: domains, GitHub, keys, export, failed builds | how-to question | T-02, T-03, T-04, T-06, T-08, T-09 | 6 | support/KB | We think inline hints at the moment of action would cut these tickets: a note that SSL can take time after a domain shows Verified, a warning on the GitHub connect screen about edits on main, and a secrets field prompt when a key is pasted into a prompt. Measure ticket volume on these six topics after shipping. |
| Plans, seats and account ownership | billing and account | T-05, T-07, T-20, T-21 | 4 | product | We believe a self-serve owner transfer and email change flow in account settings, plus a Pro vs Team comparison table on the pricing page, would remove these tickets. The owner transfer case (T-21) rests on one ticket. |
| Live site will not go live: stuck deploys, pending SSL, missing production variables | product defect | T-23, T-25, T-29 | 3 | engineering | We think a status page check that fails when deploys are queued longer than 15 minutes, plus an alert when a certificate stays Pending for over 1 hour, would surface these failures before customers write in. The env var case (T-29) rests on one ticket. |
| Editor errors and credits drained | product defect | T-26, T-28, T-30 | 3 | engineering | We believe automatically refunding credits for any generation that returns a 500 error, and showing the final credit cost before send, would remove the sense of being charged for failures. Test with the T-26 and T-30 accounts; the Safari blank preview (T-28) rests on one ticket and needs a fallback when WebGPU is missing. |
| Buildbox deleted customer data or files | product defect | T-24, T-27 | 2 | engineering | We believe a confirmation step and an automatic snapshot before any redeploy that touches the live database, and before any sync commit that deletes more than a few files, would prevent this kind of loss. Test it on these two cases first; each rests on one ticket. |
| Credit balance and reset questions | how-to question | T-01, T-10 | 2 | product | We believe showing the reset date, rollover rule and pack expiry next to the credit balance would answer both questions in product. This rests on two tickets, so treat it as a small test. |
| Security review and discount requests | request | T-11, T-12 | 2 | sales | We think a public trust page with SOC 2 status and data hosting location, and a decision on a nonprofit and education discount, would unblock these buyers. Each rests on one ticket, and a 40-seat rollout (T-11) is at stake. |

## In their words

- **Unexpected charges, refunds, cancellations and invoices** (T-18): "Please explain, this looks wrong."
- **Setup questions: domains, GitHub, keys, export, failed builds** (T-03): "I don't want to lose it."
- **Plans, seats and account ownership** (T-21): "The person who created our Team workspace left the company last month and nobody can log in as them."
- **Live site will not go live: stuck deploys, pending SSL, missing production variables** (T-23): "I have a launch tomorrow morning."
- **Editor errors and credits drained** (T-26): "I lost about 30 credits for nothing."
- **Buildbox deleted customer data or files** (T-27): "Please help urgently, this is our real business."
- **Credit balance and reset questions** (T-01): "It's only the 14th."
- **Security review and discount requests** (T-12): "Team would really help us but $50 a month is a lot for us."

## Knowledge base gaps

- T-11: The knowledge base has nothing on SOC 2 Type II certification status, sharing audit reports under NDA, or where customer data is hosted (region or cloud provider). KB-11 only covers backups and exports.
- T-12: The KB has no information about any nonprofit or education discount or program. It only lists standard prices (KB-03) and does not say whether discounts exist or how to apply for one.
