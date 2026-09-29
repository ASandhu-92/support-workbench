# Drafts and routing, ticket by ticket

Every reply below is a draft for a human to review. Billing actions are proposals only; the command shown is what a person would run after checking.

## T-01: Out of credits already??

Tier 1, credits-and-usage, urgency low. Outcome: **reply**. Customer on Pro ran out of credits mid-cycle and asks when credits reset, which is a documented question about credit allowances and renewal.

Cites KB-02, KB-03.

> Hi Rob,
> 
> Thanks for getting in touch. Credits don't reset on the 1st of the month. Monthly credits reset on your billing date, so your 500 Pro credits will come back on that date. Unused monthly credits don't roll over.
> 
> If you'd like more credits before then, you can buy a credit pack on your plan. A pack is 200 credits for $10. Pack credits never expire and are used only after your monthly credits run out.
> 
> You can see where your credits went under Settings > Usage, per day and per project. If you think you were charged credits for a generation that failed with an error, send us the project name and the time, and we'll look into it.
> 
> Buildbox Support

Note for the reviewer: No account data was looked up, so the billing date and usage are unverified. The reply does not state the customer's reset date.

## T-02: custom domain

Tier 1, custom-domains, urgency low. Outcome: **reply**. Customer on the free plan asks how to connect their own domain via DNS, which is a documented how-to question with no impact.

Cites KB-03, KB-06, KB-15.

> Hi Nina,
> 
> Thanks for asking. Custom domains are only available on the Pro and Team plans, so on Free your app can only use the bbx subdomain for now. Pro is $20 per month, and upgrading takes effect right away.
> 
> Once you're on Pro, here's how to connect your domain:
> 
> 1. Go to Settings > Domains > Add domain and type your domain (for example www.example.com).
> 2. At your registrar, add the record Buildbox shows. For a subdomain like www, that's a CNAME to edge.bbx.example. For a root domain like example.com, it's an A record to 192.0.2.10.
> 3. Wait for the status to turn Verified. DNS changes can take up to an hour.
> 
> After that, we set up HTTPS automatically, which usually takes up to 30 minutes. Your browser may say "not secure" until then, which is expected.
> 
> Best,
> Buildbox Support

Note for the reviewer: No account data was looked up. The plan is based on the customer's own report that they are on Free. The reply mentions the Pro upgrade only as the requirement for custom domains, and no upgrade is offered or proposed.

## T-03: Will Buildbox overwrite my GitHub edits?

Tier 1, github-sync, urgency normal. Outcome: **reply**. Customer asks how GitHub sync handles edits made directly on main versus AI changes in Buildbox, which is a documented how-to question, with some concern about losing work but no current loss.

Cites KB-07.

> Hi Tom,
> 
> Your fix should be safe. Commits pushed to main on GitHub are pulled into Buildbox within about a minute, so the AI will work on top of your fix once it has synced. Given you made the fix yesterday, it should already be in.
> 
> Buildbox also does not overwrite your GitHub commit. If the same file is edited in Buildbox and on GitHub at the same time, syncing stops and shows "Conflict". You are then asked to pick which version to keep, so nothing is lost without your say-so.
> 
> Before you send your next prompt, you may want to check that the fix appears in your Buildbox code view. If you see "Conflict" or "Unauthorized" in Settings > GitHub, choose the version with your fix, or reconnect if it shows Unauthorized.
> 
> Buildbox Support

Note for the reviewer: No account data was looked up; the answer relies only on KB-07. The customer's claim that they pushed to main yesterday is unverified.

## T-04: Where do I put my Stripe key

Tier 1, environment-variables, urgency low. Outcome: **reply**. Customer asks how to store a Stripe secret key safely, which is a how-to answered by documentation on environment variables (secrets should not be pasted into prompts).

Cites KB-08.

> Hi Ella,
> 
> Please don't paste your Stripe secret key into the prompt. There's a safer way.
> 
> 1. Go to Settings > Environment and add a variable named STRIPE_SECRET_KEY with your key as the value. Set its scope to Production. Values are encrypted and hidden after you save.
> 2. Add your Stripe test key as a Preview variable, so you can try payments safely in the preview.
> 3. In the prompt box, write: "read the Stripe key from the environment variable STRIPE_SECRET_KEY".
> 4. Deploy again after any change to a variable, so the live site picks it up.
> 
> The AI can see the variable name, so it can write the code, but it never sees the value.
> 
> Buildbox Support

Note for the reviewer: No account data needed for this question. Answer is based on KB-08.

## T-05: adding a teammate

Tier 1, team-and-account, urgency low. Outcome: **reply**. Customer asks how to add a sixth seat on Team, its cost, and how to restrict workspace deletion, which are documented how-to and permissions questions.

Cites KB-03, KB-09.

> Hi,
> 
> Thanks for reaching out. Your Team plan includes 5 seats, and each extra seat is $10 per month. A 6th person would be added to your next invoice, prorated for the rest of the month. Prices don't include sales tax or VAT where it applies.
> 
> To add them, go to Settings > Members > Invite and enter their email. The invite link is valid for 7 days.
> 
> On deleting the workspace: only the Owner can delete it (along with handling billing). Admins manage members and settings, and Members can build and deploy. So if you invite your contractor as a Member, they can build and deploy but can't delete the workspace.
> 
> Buildbox Support

Note for the reviewer: No account data was looked up. The answer comes from KB-03 and KB-09 only. KB-09 says the Owner role covers deleting the workspace, so the Member role limit on deletion is inferred from the role list.

## T-06: Getting my code out

Tier 1, data-and-backups, urgency low. Outcome: **reply**. Customer asks how to export their project code and database data for self-hosting, which is a how-to question documentation can answer.

Cites KB-11, KB-07.

> Hi Hana,
> 
> Yes, you can take everything with you. The code is yours to run anywhere.
> 
> Code: open your project, then go to the Project menu > Export > Download ZIP. You get the full source code.
> 
> Database: go to Project menu > Database > Export. You get one CSV file per table.
> 
> If your project is on a Pro or Team plan, you can also connect it to a GitHub repository (Settings > GitHub > Connect). Your agency could then pull the code from there, and it stays in sync with your project.
> 
> Let us know if anything looks off with the export.
> 
> Buildbox Support

Note for the reviewer: No account data was looked up, so the customer's plan is unknown. The GitHub option is only offered as available on Pro and Team.

## T-07: Pro vs Team

Tier 1, plans-and-pricing, urgency low. Outcome: **reply**. Customer asks a general question about the differences between Pro and Team plans and whether two people can share one Pro account, which documentation can answer.

Cites KB-03, KB-02, KB-09.

> Hi Leo,
> 
> Thanks for asking. Pro includes 1 seat, so for two of you working in Buildbox, Team is the plan built for that. Team includes 5 seats, and each of you would get your own login and role in a shared workspace.
> 
> Here is what differs:
> 
> Price: Pro is $20 per month, Team is $50 per month (before any sales tax or VAT).
> Credits: Pro has 500 per month. Team has 2,000 per month, shared by the whole workspace.
> Seats: 1 on Pro, 5 on Team (extra seats are $10 per month each).
> Support: Email on both, with a faster first response on Team.
> 
> Some things are the same on both: unlimited projects, custom domains, and GitHub sync.
> 
> If you would like to start on Pro and move up later, you can change plan at any time.
> 
> Buildbox Support

Note for the reviewer: Pricing question only, no account lookup needed. Reply is based on KB-03 seat limits; KB-15 covers upgrade proration if they ask.

## T-08: site says NOT SECURE

Tier 1, custom-domains, urgency normal. Outcome: **reply**. A newly verified custom domain showing Not Secure 10 minutes after adding it is most likely the SSL certificate still being issued, which is documented behavior, and the customer has not yet tried any fix.

Cites KB-06.

> Hi,
> 
> You haven't broken anything. Once a domain shows Verified, Buildbox requests the HTTPS certificate automatically. This normally takes up to 30 minutes, and until it's ready Chrome may show "Not secure". That's expected in the first 30 minutes.
> 
> You said you added the domain about 10 minutes ago, so it should be well within that window. Please check again in around 20 to 30 minutes, and the warning should be gone.
> 
> If it still shows "Not secure" after that, reply with your domain name and we'll take a closer look.
> 
> Buildbox Support

Note for the reviewer: No account data was looked up. The reply relies on the customer's report of timing and Verified status, which is unchecked.

## T-09: Deploy failed

Tier 1, deploys, urgency normal. Outcome: **reply**. The build hit the documented 10 minute limit, likely because images are generated during build, so this is a how-to question about moving that work out of the build step.

Cites KB-05.

> Hi Max,
> 
> Thanks for the details. That log line means your build took longer than the 10 minute limit. Since you mention the app generates product photos during the build, that is a likely cause. Here is what to try:
> 
> 1. Upload your product photos as files instead of generating them at build time.
> 2. Remove any packages the app no longer uses. You can ask the AI to "reduce build time by removing unused dependencies".
> 
> Then deploy again. A failed deploy never replaces your live site, so the previous version keeps running in the meantime.
> 
> If the build still fails after that, reply with your project name and the deploy id from Deploy history, and we will take a closer look.
> 
> Buildbox Support

Note for the reviewer: No account lookup was needed. The customer's guess about image generation is unverified, so the reply presents it as a likely cause.

## T-10: Do credits carry over

Tier 1, credits-and-usage, urgency low. Outcome: **reply**. Customer asks a general documented question about whether monthly credits roll over and whether purchased credit packs expire, with no account issue or impact.

Cites KB-02.

> Hi Zoe,
> 
> Thanks for getting in touch. Here are the answers to your two questions.
> 
> 1) No, unused monthly credits do not roll over. Your monthly credits reset on your billing date, so any leftovers from your 500 credits will not carry into next month.
> 
> 2) No, credit packs do not expire. A pack of 200 credits costs $10 and can be bought on any paid plan. Pack credits are only used after your monthly credits run out, so they stay available until you need them.
> 
> You can check your usage any time under Settings > Usage.
> 
> Buildbox Support

Note for the reviewer: No account lookup was needed. Answer comes directly from KB-02. Zoe says she is on 500 credits (Pro), which I did not verify.

## T-11: SOC 2 report request

Tier 1, security-and-compliance, urgency low. Outcome: **escalate-no-source**. Customer asks about SOC 2 Type II status, report access under NDA, and data hosting location, which are general security and compliance questions with no stated deadline or impact.

`escalate: no source`. Missing from the KB: The KB has nothing on SOC 2 or other security certifications, sharing compliance reports under NDA, or where customer data is hosted (region or cloud provider). Only KB-11 mentions daily database snapshots, with no location details.

Note for the reviewer: No account data was looked up and none is needed. Please route this to security/compliance for SOC 2 status, the NDA process for the report, and data hosting location, and reply to the customer (40-person rollout).

## T-12: Nonprofit discount?

Tier 1, plans-and-pricing, urgency low. Outcome: **escalate-no-source**. Customer asks whether a nonprofit or education discount exists for the Team plan, which is a pricing question documentation can answer.

`escalate: no source`. Missing from the KB: The knowledge base has no information on whether Buildbox offers nonprofit or education discounts, or how to apply for one. It only lists standard prices (KB-03).

Note for the reviewer: No KB article covers nonprofit or education discounts, so no reply was drafted. Please check with a support lead whether a discount exists and reply to the customer directly.

## T-13: Charged twice for credit pack

Tier 2, billing-charges, urgency normal. Outcome: **reply**. Customer was charged $10 twice for one credit pack and received only 200 credits, so someone must review the account and refund or correct the duplicate charge.

Cites KB-13.

> Hi Dana,
> 
> Thanks for writing, and sorry about the double charge. I checked your account and can see two $10 credit pack charges. One of them has already been refunded in full ($10). The other is the one you meant to buy, and it stays in place for your 200 credits.
> 
> Duplicate charges are refunded in full, and the refund goes back to your original card. It can take 5 to 10 business days to show on your statement, depending on your bank. You should also get a confirmation email with the refund amount and date.
> 
> If your bank still shows two charges after that time, reply here and we will look into it.
> 
> Buildbox Support

Note for the reviewer: Account data shows the duplicate charge (ch_...0TVaWSpd) was already refunded in full ($10, status succeeded) and the other charge is intact, so no new refund is proposed. Customer may be seeing the pending bank statement.

## T-14: payment failed email

Tier 2, billing-payment-failed, urgency normal. Outcome: **reply**. Customer received a failed Pro payment notice and worries about losing projects before a Friday client demo, which needs someone to review their account's payment status.

Cites KB-14, KB-15, KB-03, KB-11.

> Hi Liam,
> 
> Thanks for writing. I checked your account. The $20 payment for Pro on your account was declined ("Your card was declined"), so nothing was charged and the Pro plan never started. That means the retry and downgrade steps for failed renewals don't apply to you.
> 
> To get Pro before Friday, upgrade again from Free to Pro and use a card that works. It takes effect right away. Only your bank can tell you why the card was declined, so it's worth asking them too.
> 
> I can't see anything in your account that removes projects. The Free plan allows 3 projects, so I'd like a teammate to confirm how yours are affected. As a precaution, you can download your code any time from Project menu > Export > Download ZIP.
> 
> Buildbox Support

Note for the reviewer: Checked: subscription is incomplete_expired, the invoice is void (subscription_create), and the only charge failed with card_declined, so this is a failed first payment, not a renewal. Please confirm the state of the customer's projects if they have more than 3.

## T-15: Refund please, forgot to cancel

Tier 2, billing-refunds, urgency normal. Outcome: **propose-billing-action**. Customer was charged $20 for a Pro renewal they meant to cancel and wants a refund and a downgrade to free, which needs account review.

Cites KB-13, KB-15.

> Hi Priya,
> 
> Thanks for writing, and sorry for the surprise charge. I can see one $20 payment for your Pro plan, from the day you signed up (September 23). It's the first payment on the plan rather than a renewal.
> 
> Pro subscription charges can be refunded if you ask within 7 days of the charge and have used fewer than 50 credits since. If a refund goes ahead, your plan is cancelled and your account moves to Free, which is what you're asking for.
> 
> I can't confirm that you qualify yet. A teammate will check your credit usage and reply with the outcome. If a refund is approved, it goes back to your original card and can take 5 to 10 business days to show on your statement.
> 
> Buildbox Support

Proposed billing action, **waiting for a human**: refund $20.00. Reason: Customer asked for a refund of the $20 Pro subscription charge and to return to Free. The charge is within 7 days, but the credit condition is not shown in the data.

Check before approving (not in the account data): Fewer than 50 credits used since the charge

`python billing.py refund ch_****UdgA --reason "Customer asked for a refund of the $20 Pro subscription charge and to return to Free. The charge is within 7 days, but the credit condition is not shown in the data." --confirm --approved-by "<your name>"`

Note for the reviewer: Customer calls it a renewal, but the account shows only the initial subscription_create charge (paid, attempt 1) from 6 days ago, so the 7-day window looks met. Please check credit usage since the charge (under 50) before approving; the refund also cancels the plan.

## T-16: Invoice with company details

Tier 2, billing-invoices, urgency normal. Outcome: **reply**. Customer wants this month's Pro invoice reissued with their company name and VAT number, which needs someone to edit the invoice on their account.

Cites KB-12.

> Hi Omar,
> 
> Thanks for getting in touch. Invoices can't be edited once they're issued, because they are tax documents. But your Pro payment is from the last 90 days, so we can issue a copy with your company details added.
> 
> To do that, could you reply with your VAT number? You mentioned the company name as Haddad Design Ltd. Please also tell us if the address should appear on the copy, and what it should be.
> 
> For future invoices, you can add the company name, address and VAT number yourself. Go to Settings > Billing > Manage billing, then "Billing information". They will appear on all invoices from then on.
> 
> Once we have your VAT number, we'll get the copy sorted for you.
> 
> Buildbox Support

Note for the reviewer: Checked account data: one paid $20 Pro invoice from 2026-09-23, within the 90-day window, currently showing only Omar's name. VAT number still needed before a copy can be issued.

## T-17: Where is my refund

Tier 2, billing-refunds, urgency normal. Outcome: **reply**. Customer was told a $10 credit pack refund was issued but has not received it, so someone must check the refund status on their account.

Cites KB-13.

> Hi Sofia,
> 
> Thanks for checking in. I looked at your account, and the $10 refund for your credit pack (200 credits) shows as succeeded, so it has been sent back to your original card.
> 
> Refunds can take 5 to 10 business days to show on your statement, depending on your bank. If it has been longer than that, please contact your bank with the refund amount and date from our confirmation email, since they can see where the funds are on their side.
> 
> If it still hasn't appeared after that time, reply here and a teammate will look into it with you.
> 
> Buildbox Support

Note for the reviewer: Account data shows the $10 refund as succeeded, created 2026-09-23. The customer says support told her last week it was done, so the 5 to 10 business day window may not have passed. Please check the date before sending. I did not offer any new refund.

## T-18: Weird charge after upgrading

Tier 2, billing-charges, urgency normal. Outcome: **reply**. Customer upgraded from Pro to Team and was charged an unexpected amount (likely proration), and asks about next month's billing, which needs someone to review their account charges.

Cites KB-15, KB-03.

> Hi Ken,
> 
> Thanks for asking. The charge looks right to me. When you upgrade, you are charged right away for the rest of the current month at the new price, minus a credit for the unused part of your old plan. This is called proration.
> 
> On your account, the upgrade invoice was $30.00. It was $50.00 for the remaining time on Team, minus a $20.00 credit for the unused time on Pro.
> 
> You won't be charged twice. Your Team plan renews on 23 October 2026 at the regular $50 per month, plus any tax that applies where you are. There is no extra $50 on top of the $30.
> 
> If anything still looks off, reply and we'll take a closer look.
> 
> Buildbox Support

Note for the reviewer: Checked the account: the $30 invoice is a subscription_update with a -$20 Pro credit and a $50 Team line, and the next renewal is 2026-10-23 at $50. The customer did not ask for a refund, so no billing action is proposed.

## T-19: Cancel my subscription

Tier 2, billing-plan-changes, urgency normal. Outcome: **propose-billing-action**. Customer wants to cancel their Team subscription to avoid future charges and asks about access during a two-week migration, which needs account-level action.

Cites KB-15.

> Hi Ana,
> 
> Thanks for letting us know. We've passed your request to cancel the Team subscription to a teammate, who will confirm it shortly.
> 
> Cancelling stops the next renewal, so you won't be charged again. You don't lose access right away. You keep the Team plan until the end of the period you've already paid for, which runs to October 23, 2026 on our records. That should give you the couple of weeks you need to finish migrating. After that date your account moves to the Free plan.
> 
> If you'd like a copy of your code, you can download it any time from the Project menu under Export.
> 
> Buildbox Support

Proposed billing action, **waiting for a human**: cancel $0.00. Reason: Customer asked to cancel the Team subscription to stop future renewals. Per KB-15, cancelling keeps the plan until period end (2026-10-23) and is not a refund. No refund was requested.

`python billing.py cancel sub_****vfuW --reason "Customer asked to cancel the Team subscription to stop future renewals. Per KB-15, cancelling keeps the plan until period end (2026-10-23) and is not a refund. No refund was requested." --confirm --approved-by "<your name>"`

Note for the reviewer: Active Team subscription, period ends 2026-10-23, cancel_at_period_end is currently false. Cancel at period end, no refund requested or offered. I mentioned the ZIP export, which is in KB-11 but not cited, so please check that line or add the citation.

## T-20: change email on account

Tier 2, team-and-account, urgency normal. Outcome: **reply**. Customer wants their login and billing emails changed to a personal address while keeping their Pro plan, which is an account email change that needs staff to review the account.

Cites KB-10.

> Hi Jonas,
> 
> Good news: you can change this yourself, and your Pro plan stays as it is. The change only moves your login and billing email.
> 
> 1. Go to Settings > Account > Email.
> 2. Enter your new personal email address.
> 3. We send a confirmation link to that new address. Click it and the change happens.
> 
> Your billing email on the subscription changes at the same time, so receipts will go to the new address afterwards. Make sure you can open the new inbox before you start, because the link has to be clicked from there.
> 
> If anything goes wrong, reply here and we will help.
> 
> Buildbox Support

Note for the reviewer: Account shows an active Pro subscription. KB-10 says the email change also updates the billing email. The KB does not say explicitly that the plan is unaffected, but the subscription stays on the same account.

## T-21: Owner left the company

Tier 2, team-and-account, urgency normal. Outcome: **reply**. Admin needs workspace ownership transferred from a departed owner, which requires staff to verify and act on the account.

Cites KB-09.

> Hi Grace,
> 
> Sorry to hear about the trouble. Normally only the current Owner can make someone else the owner. Since the Owner can't log in, our support team can transfer ownership for you, but we need to verify the request first.
> 
> To do that, we need two things from you:
> 
> 1. A second Admin of your workspace to confirm the request. Please ask them to reply to us, or send us their name and the email they use in the workspace.
> 2. Confirmation of the billing email address on file for the subscription.
> 
> Once we have both, a teammate will check them and move ownership to you. We'll reply here as soon as that's done, so please don't expect the change until then.
> 
> Buildbox Support

Note for the reviewer: Account data shows an active Team subscription under grace.kim@example.com but not workspace members or roles. Verify Grace is an Admin, the second Admin's confirmation and the billing email before transferring ownership.

## T-22: $50 charge??

Tier 2, billing-charges, urgency normal. Outcome: **reply**. Customer was charged $50 instead of the expected $20 Pro price, so someone needs to review their account charges.

Cites KB-03, KB-15.

> Hi Marco,
> 
> Thanks for reaching out. I checked your account, and the $50 charge is for the Team plan, not Pro. Your subscription is Team at $50 per month, and the charge was a single payment of $50 for the first month. Pro is $20 per month, and Team is $50 per month with 2,000 shared credits and 5 seats.
> 
> If you meant to pick Pro, we can look at switching you. Just let me know what you'd like. Please note that a downgrade from Team to Pro takes effect at the end of the current billing period, with no partial refund. If you'd like to ask about a refund, tell us and a teammate will review it.
> 
> Buildbox Support

Note for the reviewer: Account shows an active Team subscription with one paid $50 charge, no duplicates. Customer did not ask for a refund, so none proposed; I only mentioned the option. Confirm which plan they intended.

## T-23: All deploys stuck in Queued

Tier 3, deploys, urgency high. Outcome: **escalate-engineering**. All deploys across four projects have been stuck in Queued for 3 hours with no incident on the status page, and the customer has a launch tomorrow morning, so an engineer needs to investigate now.

Handoff note: [escalations/T-23.md](escalations/T-23.md)

## T-24: GitHub sync deleted my files

Tier 3, github-sync, urgency high. Outcome: **escalate-engineering**. GitHub sync pushed an unrequested commit deleting 14 files including /api on main, and sync now shows Conflict after the customer's revert, so an engineer must investigate the data loss and sync state.

Handoff note: [escalations/T-24.md](escalations/T-24.md)

## T-25: SSL pending for 3 days

Tier 3, custom-domains, urgency normal. Outcome: **escalate-engineering**. Domain is verified with correct CNAME and no CAA record, yet the certificate has been stuck Pending for 3 days, so an engineer needs to investigate the provisioning.

Handoff note: [escalations/T-25.md](escalations/T-25.md)

## T-26: 500 error on every prompt + credits gone

Tier 3, editor-and-generation, urgency normal. Outcome: **escalate-engineering**. Every prompt returns a 500 error across two projects and browsers while credits are still deducted, which is a product fault needing engineering investigation.

Handoff note: [escalations/T-26.md](escalations/T-26.md)

## T-27: database empty after redeploy

Tier 3, data-and-backups, urgency high. Outcome: **escalate-engineering**. Live production database lost about 1,200 customer bookings after a redeploy, which is data loss affecting a real business now and needs an engineer to investigate and attempt recovery.

Handoff note: [escalations/T-27.md](escalations/T-27.md)

## T-28: Blank preview in Safari

Tier 3, editor-and-generation, urgency normal. Outcome: **escalate-engineering**. Preview pane is blank in Safari 19 with a navigator.gpu (WebGPU) TypeError, and the customer already tried a hard refresh and a private window, so an engineer needs to investigate.

Handoff note: [escalations/T-28.md](escalations/T-28.md)

## T-29: env vars not in production

Tier 3, environment-variables, urgency normal. Outcome: **escalate-engineering**. Production variable is set with the correct scope and redeployed twice, yet it is undefined on the live site while preview works, so the documented fix failed and an engineer must investigate.

Handoff note: [escalations/T-29.md](escalations/T-29.md)

## T-30: credits going down twice as fast

Tier 3, credits-and-usage, urgency normal. Outcome: **escalate-engineering**. Credits deducted are double the amount shown before each generation since Monday's update, which looks like a product bug needing engineering investigation.

Handoff note: [escalations/T-30.md](escalations/T-30.md)
