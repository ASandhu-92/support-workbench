# Drafts and routing, ticket by ticket

Every reply below is a draft for a human to review. Billing actions are proposals only; the command shown is what a person would run after checking.

## T-01: Out of credits already??

Tier 1, credits-and-usage, urgency low. Outcome: **reply**. Pro customer asks when credits refresh after running out mid-month, which is a documented question about credit limits and reset timing.

Cites KB-02, KB-03.

> Hi Rob,
> 
> Thanks for getting in touch. Monthly credits reset on your billing date, not on the 1st of the month. So your 500 Pro credits will refill on the date your plan renews. You can find that date under Settings > Billing > Manage billing.
> 
> Unused monthly credits don't roll over, so you start fresh each cycle.
> 
> If you'd like more credits before then, you can buy a credit pack on your paid plan. A pack is 200 credits for $10. Pack credits never expire, and they're used only after your monthly credits run out.
> 
> To see where your credits went, open Settings > Usage. It shows usage per day and per project. If you were charged credits for a generation that failed with an error, send us the project name and the time. That shouldn't happen and we'll look into it.
> 
> Buildbox Support

Note for the reviewer: No account data was looked up, so I did not check Rob's plan, billing date or credit usage. The reply gives the general reset rule and the pack option.

## T-02: custom domain

Tier 1, custom-domains, urgency low. Outcome: **reply**. Customer asks how to connect a custom domain to their app via DNS and mentions the free plan, which documentation on custom domains and plan limits can answer.

Cites KB-03, KB-06, KB-15.

> Hi Nina,
> 
> Thanks for asking. Custom domains are only available on the Pro and Team plans, so you would need to upgrade from Free first. Pro is $20 per month, and an upgrade takes effect right away.
> 
> Once you're on Pro, here's how to connect your domain:
> 
> 1. Go to Settings > Domains > Add domain and type your domain (for example www.example.com).
> 2. At your registrar, add the record Buildbox shows you. For a subdomain like www, that's a CNAME to edge.bbx.example. For the root domain, it's an A record to 192.0.2.10.
> 3. Wait for the status to turn Verified. DNS changes can take up to an hour.
> 
> After that, we request an HTTPS certificate automatically. This normally takes up to 30 minutes, and your browser may show "not secure" until it's done.
> 
> Buildbox Support

Note for the reviewer: No account lookup was done. The reply relies on the customer's own statement that they are on Free. Custom domains need Pro or Team per KB-03 and KB-06.

## T-03: Will Buildbox overwrite my GitHub edits?

Tier 1, github-sync, urgency normal. Outcome: **reply**. Customer asks how GitHub sync handles edits made directly on main versus AI changes in Buildbox, which is a documented how-to question, though they worry about losing work.

Cites KB-07.

> Hi Tom,
> 
> Your fix should be safe. Commits you push to main on GitHub are pulled into Buildbox within about a minute, so the AI will work on top of your fix once it has synced.
> 
> If the same file is edited in Buildbox and on GitHub at the same time, Buildbox does not overwrite your GitHub commit. It stops syncing, shows "Conflict", and asks you to pick which version to keep. Choose the GitHub version if you want to keep your fix.
> 
> Since you pushed yesterday, it should already be in Buildbox. It's worth a quick look at the code view to confirm before you send your next prompt.
> 
> Buildbox Support

Note for the reviewer: No account data was looked up; the answer relies only on KB-07. I did not verify that the customer's sync is connected or currently healthy.

## T-04: Where do I put my Stripe key

Tier 1, environment-variables, urgency low. Outcome: **reply**. Customer asks how to safely supply a Stripe secret key, which is a documented how-to answered by using environment variables rather than pasting it into the prompt.

Cites KB-08.

> Hi Ella,
> 
> Please don't paste your Stripe secret key into the prompt. There's a safer way.
> 
> 1. Go to Settings > Environment and add a variable named STRIPE_SECRET_KEY with your key as the value. Set its scope to Production.
> 2. Add your Stripe test key as a Preview variable, so you can try payments without real charges.
> 3. In the prompt box, ask the AI to "read the Stripe key from the environment variable STRIPE_SECRET_KEY".
> 
> The AI can see the variable name, so it can write the code, but it never sees the value. Saved values are encrypted and hidden. Changes take effect on your next deploy, so deploy again after adding or editing them.
> 
> Buildbox Support

## T-05: adding a teammate

Tier 1, team-and-account, urgency low. Outcome: **reply**. Customer asks how to add a sixth seat on the Team plan, its cost, and how to restrict workspace deletion via roles, all of which documentation covers.

Cites KB-03, KB-09.

> Hi Sam,
> 
> Thanks for getting in touch. Team includes 5 seats, so a 6th person is an extra seat at $10 per month. It is added to your next invoice, prorated for the rest of the month. Prices don't include sales tax or VAT where it applies.
> 
> To add them: go to Settings > Members > Invite and enter their email. The invite link is valid for 7 days.
> 
> On deleting the workspace: only the Owner can delete it (along with handling billing). Admins manage members and settings, and Members can build and deploy. If you invite your contractor as a Member, they won't be able to delete the workspace.
> 
> Buildbox Support

Note for the reviewer: No account data was looked up. The reply assumes Sam is on Team, as they reported. KB-09 says the Owner role covers deleting the workspace, so I inferred that Members can't delete it.

## T-06: Getting my code out

Tier 1, data-and-backups, urgency low. Outcome: **reply**. Customer asks how to export their project code and database data for self-hosting, which is a how-to question that documentation can answer.

Cites KB-11, KB-07.

> Hi Hana,
> 
> Yes, you can take everything with you. You own the code, and your agency can run it anywhere.
> 
> Code: open your project, then choose Project menu > Export > Download ZIP. This gives you the full source code.
> 
> Database: choose Project menu > Database > Export. You get one CSV file per table.
> 
> If your project is on a Pro or Team plan, you can also connect it to a GitHub repository (Settings > GitHub > Connect). Your code is then kept in that repository, which your agency can use directly.
> 
> Let us know if anything doesn't work as expected.
> 
> Buildbox Support

Note for the reviewer: No account lookup was done. The GitHub option is mentioned as a Pro/Team extra, and the customer's plan is unknown.

## T-07: Pro vs Team

Tier 1, plans-and-pricing, urgency low. Outcome: **reply**. Customer asks a general question about the differences between Pro and Team plans and whether two people can share one Pro account, which documentation can answer.

Cites KB-03, KB-02, KB-09.

> Hi Leo,
> 
> Thanks for asking. Pro includes 1 seat, so for two people working in the same workspace, Team is the plan built for that. Team includes 5 seats.
> 
> Here is what differs between the two:
> 
> 1. Price: Pro is $20 per month, Team is $50 per month (before any sales tax or VAT).
> 2. Seats: Pro has 1, Team has 5 included, with extra seats at $10 per month each.
> 3. Credits: Pro has 500 per month. Team has 2,000 per month, shared by everyone in the workspace.
> 4. Support: both get email support, and Team gets a faster first response.
> 
> Projects, deploys, custom domains and GitHub sync are the same on both. You can also change plan at any time, so you can start on one and switch later.
> 
> Buildbox Support

Note for the reviewer: No account lookup was done. The answer comes from the KB-03 plan table. The KB says Pro has 1 seat, and I did not suggest sharing a login.

## T-08: site says NOT SECURE

Tier 1, custom-domains, urgency normal. Outcome: **reply**. Domain was added only 10 minutes ago and is Verified, so the Not Secure warning is most likely the SSL certificate still being issued, which documentation covers, and the customer has not yet waited or tried any fix.

Cites KB-06.

> Hi Ivy,
> 
> You haven't broken anything. Once a domain shows Verified, Buildbox requests the HTTPS certificate automatically. That normally takes up to 30 minutes, and until it finishes the browser may show "not secure". You said you added the domain about 10 minutes ago, so this is what we'd expect at this stage.
> 
> Please check again in around 20 to 30 minutes, ideally after a hard refresh or in a private window. The warning should be gone by then.
> 
> If it still shows "not secure" after that, reply with your domain name and we'll look into it.
> 
> Buildbox Support

Note for the reviewer: No account data was looked up; the reply relies on the customer's report of timing and Verified status and on KB-06. The hard refresh or private window tip comes from KB-01, which is not cited.

## T-09: Deploy failed

Tier 1, deploys, urgency normal. Outcome: **reply**. The build hit the documented 10 minute limit, likely from generating many images at build time, so this is a how-to question that docs can answer (pre-generate or optimize assets).

Cites KB-05.

> Hi Max,
> 
> Thanks for sending the log line. "Build exceeded 10 minute limit" means the build took longer than 10 minutes. Your live site is not affected, because a failed deploy never replaces the version that is already running.
> 
> Here are two things to try:
> 
> 1. Upload your product photos instead of having them generated at build time. Large image assets are a common reason builds run long.
> 2. Ask the AI to "reduce build time by removing unused dependencies". You can also remove unused packages yourself.
> 
> After that, deploy again. If it still fails, reply with the project name and the deploy id from Deploy history, and we will take a closer look.
> 
> Buildbox Support

Note for the reviewer: No account lookup was needed. The reply follows the build time limit row in KB-05. The photo cause is the customer's own guess, so the reply frames it as a likely factor.

## T-10: Do credits carry over

Tier 1, credits-and-usage, urgency low. Outcome: **reply**. Customer asks a general documented question about whether unused monthly credits roll over and whether purchased credit packs expire.

Cites KB-02.

> Hi Zoe,
> 
> Thanks for asking. Here are the answers:
> 
> 1) No, unused monthly credits do not roll over. Your monthly credits reset on your billing date, so any leftovers from your 500 will not carry into next month.
> 
> 2) No, credit packs do not expire. A pack of 200 credits costs $10 and is a one-time purchase. Pack credits are only used after your monthly credits run out, so they stay available until you need them. Packs can be bought on any paid plan.
> 
> You can see your usage any time under Settings > Usage.
> 
> Buildbox Support

Note for the reviewer: Answered from KB-02 only. No account lookup was needed. The customer says she is on a 500-credit plan (Pro), which was not checked.

## T-11: SOC 2 report request

Tier 1, security-and-compliance, urgency low. Outcome: **escalate-no-source**. Customer asks about SOC 2 Type II status, obtaining the report under NDA, and data hosting location, which are general security and compliance questions with no stated deadline or impact.

`escalate: no source`. Missing from the KB: The knowledge base has nothing on SOC 2 Type II certification status, sharing audit reports under NDA, or where customer data is hosted (region or cloud provider). KB-11 only covers backups and exports.

Note for the reviewer: No billing data was needed. Please route to security/compliance for SOC 2 status, the NDA process and data hosting location, then reply to the customer (40-person rollout).

## T-12: Nonprofit discount?

Tier 1, plans-and-pricing, urgency low. Outcome: **escalate-no-source**. Customer asks whether a nonprofit or education discount exists for the Team plan, which is a general pricing question that documentation can answer.

`escalate: no source`. Missing from the KB: The KB has no information about any nonprofit or education discount or program. It only lists standard prices (KB-03) and does not say whether discounts exist or how to apply for one.

Note for the reviewer: The customer asked about a nonprofit/education discount and the KB is silent, so no draft was written. Please confirm with a support lead whether such a discount exists before replying. No account data was looked up.

## T-13: Charged twice for credit pack

Tier 2, billing-refunds, urgency normal. Outcome: **reply**. Customer was charged $10 twice for one credit pack but received only 200 credits, so someone needs to review the account and refund the duplicate charge.

Cites KB-13.

> Hi Dana,
> 
> Thanks for letting us know. I checked your account and see two $10 credit pack charges from the same morning. One of them has already been refunded in full ($10.00), and that refund shows as succeeded on our side. The other charge is the one that stays, and it matches the single 200 credit pack you received.
> 
> Refunds go back to your original card and usually show on your statement within 5 to 10 business days, depending on your bank. If your bank still shows both charges after that time, reply here and we will take another look.
> 
> Buildbox Support

Note for the reviewer: Account data shows the duplicate charge was already refunded ($10, succeeded) so no new action is proposed. Please confirm the customer's bank pending charge is not just the not-yet-posted refund.

## T-14: payment failed email

Tier 2, billing-payment-failed, urgency normal. Outcome: **reply**. Customer received a failed Pro payment notice and worries about losing projects before a Friday client demo, which needs a look at their account's payment status.

Cites KB-14, KB-15, KB-03, KB-11.

> Hi Liam,
> 
> Thanks for getting in touch. I checked your account. Your first Pro payment of $20 was declined by your card, so the Pro plan never started and nothing was taken from you. Because it was never an active plan, there is no downgrade happening and the automatic retries for renewals don't apply here. Only your bank can tell you why the card was declined.
> 
> To get Pro before Friday, start the upgrade again in Settings > Billing, using a different card or after checking with your bank. Pro takes effect straight away once the payment goes through.
> 
> In the meantime you are on the Free plan, which includes 3 projects. If you want a safe copy of anything, you can download your code any time from Project menu > Export > Download ZIP.
> 
> Buildbox Support

Note for the reviewer: Checked: the subscription is incomplete_expired, the invoice is void (subscription_create) and the charge failed with card_declined, so this is a failed first payment, not a renewal. The customer did not say how many projects they have; check that before confirming they are not affected by the Free limit of 3.

## T-15: Refund please, forgot to cancel

Tier 2, billing-refunds, urgency normal. Outcome: **propose-billing-action**. Customer was charged $20 for a Pro renewal they meant to cancel and wants a refund and a downgrade to free, which needs account-level review.

Cites KB-13, KB-15.

> Hi Priya,
> 
> Thanks for writing, and sorry about the surprise charge. I can see a $20 Pro payment on your account.
> 
> Pro charges can be refunded if you ask within 7 days of the charge and have used fewer than 50 credits since. If a refund goes ahead, your plan is cancelled and your account moves to Free, which is what you're asking for.
> 
> I've passed your request to a teammate. They will check your credit usage and reply to confirm whether the refund can go ahead. Refunds are approved by a person on our team, so nothing has been refunded or cancelled yet. If it is approved, it goes back to your original card and can take 5 to 10 business days to show on your statement.
> 
> Buildbox Support

Proposed billing action, **waiting for a human**: refund $20.00. Reason: Customer asked for a refund of the $20 Pro charge and a return to Free. Charge is within 7 days of today's date; refund under KB-13 also cancels the Pro plan.

Check before approving (not in the account data): Fewer than 50 credits used since the charge (usage not shown in account data)

`python billing.py refund ch_****UdgA --reason "Customer asked for a refund of the $20 Pro charge and a return to Free. Charge is within 7 days of today's date; refund under KB-13 also cancels the Pro plan." --confirm --approved-by "<your name>"`

The policy also cancels the plan. After the refund, run:

`python billing.py cancel sub_****5FrG --reason "Customer asked for a refund of the $20 Pro charge and a return to Free. Charge is within 7 days of today's date; refund under KB-13 also cancels the Pro plan." --confirm --approved-by "<your name>"`

Note for the reviewer: Customer calls it a renewal, but the only charge on file is the initial subscription creation charge. Please check credit usage since the charge (under 50 needed) in Settings > Usage before approving.

## T-16: Invoice with company details

Tier 2, billing-invoices, urgency normal. Outcome: **reply**. Customer wants this month's Pro invoice reissued with their company name and VAT number, which needs someone to edit it on their account.

Cites KB-12.

> Hi Omar,
> 
> Thanks for getting in touch. Invoices can't be edited once they're issued, but we can send you a copy with your company details added. Your Pro payment is recent, so it's within the 90 days we cover.
> 
> To set that up, could you please send us your VAT number? We have Haddad Design Ltd as the company name from your message. If you'd like an address on the invoice, please send that too.
> 
> To get your details onto future invoices, open Settings > Billing > Manage billing and add them under "Billing information".
> 
> Once we have your VAT number, a teammate will prepare the copy for you.
> 
> Buildbox Support

Note for the reviewer: Checked account data: the Pro invoice was created 2026-09-23, within the 90-day window, and shows only the customer's name. VAT number is still needed before issuing the copy.

## T-17: Where is my refund

Tier 2, billing-refunds, urgency normal. Outcome: **reply**. Customer was told a $10 credit pack refund was issued but has not received it, so someone must check the refund status on their account.

Cites KB-13.

> Hi Sofia,
> 
> Thanks for checking in. I looked at your account, and the $10 refund for your credit pack (200 credits) shows as succeeded, so it has been issued to your original card.
> 
> Refunds usually appear on your statement within 5 to 10 business days, depending on your bank, so it may simply not have shown up yet. We also send a confirmation email with the refund amount and date, so it's worth checking your inbox and spam folder for that.
> 
> If it still hasn't appeared after 10 business days, please reply and let us know. Your bank can also tell you whether it has received the refund.
> 
> Buildbox Support

Note for the reviewer: Account data shows the $10 refund as succeeded and the charge as fully refunded. The sandbox timestamps don't show how many business days have passed, so I could not check whether the 5 to 10 day window is over.

## T-18: Weird charge after upgrading

Tier 2, billing-charges, urgency normal. Outcome: **reply**. Customer upgraded from Pro to Team and was charged an unexpected amount (likely proration) and needs someone to review the account charge and explain next month's billing.

Cites KB-15, KB-03.

> Hi Ken,
> 
> Thanks for checking. The charge looks right. When you upgrade, you are charged right away for the rest of the current month at the new price, minus a credit for the unused part of your old plan. This is called proration.
> 
> On your account, the upgrade invoice was $30.00: $50.00 for the remaining time on Team, minus a $20.00 credit for the unused time on Pro. That is why it wasn't $50.
> 
> You won't be charged twice for the same period. Your Team plan is active and its next renewal is on 23 October 2026, at the regular $50 per month (plus any tax that applies).
> 
> If you still think something is off, reply and we'll take another look.
> 
> Buildbox Support

Note for the reviewer: Verified invoice: $30 = $50 Team minus $20 Pro credit, and the Team subscription is active and renews 2026-10-23 at $50. No refund was requested.

## T-19: Cancel my subscription

Tier 2, billing-plan-changes, urgency normal. Outcome: **propose-billing-action**. Customer wants to cancel their Team subscription and asks about access timing, which needs an agent to act on their account.

Cites KB-15.

> Hi Ana,
> 
> Thanks for letting us know. You won't lose access right away. Cancelling stops the next renewal, and you keep the Team plan until the end of the period you already paid for. Our records show that period ends on 2026-10-23, so you would have until then to finish migrating. After that, the account moves to Free and you won't be charged again.
> 
> A teammate will confirm the cancellation with you shortly. You can also do it yourself in Settings > Billing > Manage billing > Cancel plan.
> 
> Buildbox Support

Proposed billing action, **waiting for a human**: cancel $0.00. Reason: Customer asked to cancel the Team subscription to stop future renewals. Per KB-15, cancelling stops the next renewal and the plan stays active until period end (2026-10-23).

`python billing.py cancel sub_****vfuW --reason "Customer asked to cancel the Team subscription to stop future renewals. Per KB-15, cancelling stops the next renewal and the plan stays active until period end (2026-10-23)." --confirm --approved-by "<your name>"`

Note for the reviewer: Confirmed an active Team subscription with cancel_at_period_end false. Cancel at period end so access continues until 2026-10-23. Customer did not ask for a refund, so none was proposed.

## T-20: change email on account

Tier 2, team-and-account, urgency normal. Outcome: **reply**. Customer wants login and billing emails changed to a personal address while keeping their Pro plan, which is an email change that needs account-level review.

Cites KB-10.

> Hi Jonas,
> 
> Good news: you can change this yourself and your Pro plan stays as it is.
> 
> 1. Go to Settings > Account > Email.
> 2. Enter your personal email address.
> 3. We send a confirmation link to that new address. Click it and the change is made.
> 
> The billing email on your subscription changes at the same time, so both your login and billing emails move together. Your Pro plan is not affected, and your account data stays on the same account. Just make sure you can open the inbox of the new address, because the change only happens once you click the link.
> 
> If anything goes wrong, reply here and we will help.
> 
> Buildbox Support

Note for the reviewer: Account shows an active Pro subscription. KB-10 says the billing email changes with the login email. The KB does not say explicitly that the plan is unaffected, but the change is on the same account and subscription, so nothing suggests a plan change.

## T-21: Owner left the company

Tier 2, team-and-account, urgency normal. Outcome: **reply**. Admin needs workspace ownership transferred from a departed owner, which requires staff to verify and act on the account.

Cites KB-09.

> Hi Grace,
> 
> Sorry to hear that, and thanks for the details. Normally only the current Owner can make someone else the owner. Since the Owner has left and can't log in, our support team can transfer ownership for you.
> 
> To do that, we need to verify the request with a second Admin of your workspace and with the billing email we have on file. Could you please reply with:
> 
> 1. The name and email of another Admin in the workspace, so we can confirm with them.
> 2. The billing email address on the account, so we can check it matches what we have.
> 
> Once we have those, a teammate will verify the request and get the transfer moving.
> 
> Buildbox Support

Note for the reviewer: Account shows an active Team subscription under grace.kim@example.com. Per KB-09, verify with a second Admin and the billing email on file before transferring ownership. I can't see workspace members here, so confirm Grace is an Admin and find the second Admin.

## T-22: $50 charge??

Tier 2, billing-charges, urgency normal. Outcome: **reply**. Customer was charged $50 instead of the expected $20 Pro price and needs someone to review the charge on their account.

Cites KB-03, KB-15.

> Hi Marco,
> 
> Thanks for checking. I looked at your account, and the $50 charge on September 23 is for the Team plan, which is $50 per month. Your subscription is set up as Team, not Pro. Pro is $20 per month, so I can see why the amount looked unexpected.
> 
> If you meant to be on Pro, you can switch by downgrading from Team to Pro. A downgrade takes effect at the end of your current billing period, and there is no partial refund for the remaining time. Your Team features stay active until then.
> 
> If you'd like to move to Pro, just tell us and a teammate will help. If Team is fine, you don't need to do anything.
> 
> Buildbox Support

Note for the reviewer: Account shows an active Team subscription at $50 and a single paid $50 charge from subscription creation. Customer did not ask for a refund, so none is proposed.

## T-23: All deploys stuck in Queued

Tier 3, deploys, urgency high. Outcome: **escalate-engineering**. Deploys across four projects have been stuck in Queued for 3 hours with no incident on the status page, and the customer has a launch tomorrow morning, so an engineer needs to investigate.

Handoff note: [escalations/T-23.md](escalations/T-23.md)

## T-24: GitHub sync deleted my files

Tier 3, github-sync, urgency high. Outcome: **escalate-engineering**. A sync commit deleted 14 files including the /api folder from a button color prompt, and sync now shows Conflict after a revert, so an engineer must investigate the unexpected data loss.

Handoff note: [escalations/T-24.md](escalations/T-24.md)

## T-25: SSL pending for 3 days

Tier 3, custom-domains, urgency normal. Outcome: **escalate-engineering**. Domain is verified with correct CNAME and no CAA record, yet the certificate has been stuck Pending for 3 days, so an engineer needs to investigate the provisioning.

Handoff note: [escalations/T-25.md](escalations/T-25.md)

## T-26: 500 error on every prompt + credits gone

Tier 3, editor-and-generation, urgency normal. Outcome: **escalate-engineering**. Every prompt returns a 500 error across projects and browsers while credits are still being deducted, which is a product fault needing engineering investigation.

Handoff note: [escalations/T-26.md](escalations/T-26.md)

## T-27: database empty after redeploy

Tier 3, data-and-backups, urgency high. Outcome: **escalate-engineering**. Live database lost about 1,200 customer bookings after a redeploy, which is data loss affecting a real business now and needs an engineer to investigate and attempt recovery.

Handoff note: [escalations/T-27.md](escalations/T-27.md)

## T-28: Blank preview in Safari

Tier 3, editor-and-generation, urgency normal. Outcome: **escalate-engineering**. Preview renders blank in Safari 19 with a navigator.gpu WebGPU TypeError, and the documented fixes (hard refresh, private window) were already tried, so an engineer needs to investigate.

Handoff note: [escalations/T-28.md](escalations/T-28.md)

## T-29: env vars not in production

Tier 3, environment-variables, urgency normal. Outcome: **escalate-engineering**. Production-scoped MAPS_API_KEY is undefined on the live site after two redeploys while preview works, and the customer already checked the scope docs, so an engineer needs to investigate.

Handoff note: [escalations/T-29.md](escalations/T-29.md)

## T-30: credits going down twice as fast

Tier 3, credits-and-usage, urgency normal. Outcome: **escalate-engineering**. Customer is charged double the credits shown before each generation since Monday's update, which contradicts documented behavior and looks like a bug needing engineering investigation.

Handoff note: [escalations/T-30.md](escalations/T-30.md)
