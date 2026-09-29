# Drafts and routing, ticket by ticket

Every reply below is a draft for a human to review. Billing actions are proposals only; the command shown is what a person would run after checking.

## T-01: Out of credits already??

Tier 1, credits-and-usage, urgency normal. Outcome: **reply**. The customer is asking how and when Pro plan credits reset, which is explained in documentation.

Cites KB-02.

> Hi Rob,
> 
> Thanks for reaching out. Credits don't reset on the 1st of the month for everyone. They reset on your billing date, which is the day your subscription renews each month. So if your Pro plan started or renewed on, say, the 14th, that's when your 500 credits will refresh, not the 1st.
> 
> You can check your exact renewal date in Settings under Billing, or see your day-by-day usage in Settings > Usage to confirm when you used up your credits.
> 
> If you need more credits before then, you can also buy a credit pack of 200 for $10 at any time, and those never expire.
> 
> Let us know if anything looks off once you check your renewal date.
> 
> Buildbox Support

Note for the reviewer: No account data was looked up, so I couldn't confirm Rob's actual billing/renewal date; reply explains the general policy from KB-02. May want to check his account for exact renewal date if he follows up.

## T-02: custom domain

Tier 1, custom-domains, urgency low. Outcome: **reply**. Customer wants how-to instructions for connecting a custom domain and whether free plan supports it.

Cites KB-06, KB-03.

> Hi Nina, thanks for reaching out! Custom domains are available on our Pro and Team plans, so you'll need to upgrade from Free first. Once you're on Pro or Team, here's how to connect your domain:
> 
> 1. Go to Settings > Domains > Add domain, and enter your domain (like www.example.com).
> 2. At your registrar's DNS settings, add the record Buildbox shows you. For a subdomain like www, that's a CNAME record pointing to edge.bbx.example. For a root domain, it's an A record pointing to 192.0.2.10.
> 3. Wait for the status to show Verified. DNS changes can take up to an hour to show up.
> 
> After it's verified, Buildbox automatically sets up HTTPS, which usually takes up to 30 minutes. Your browser might show a "not secure" warning during that short window, which is normal.
> 
> Let us know if you run into any trouble along the way!
> 
> Buildbox Support

Note for the reviewer: Customer is on Free plan and needs to upgrade to Pro or Team before custom domains work; reply explains this along with the DNS setup steps from KB-06.

## T-03: Will Buildbox overwrite my GitHub edits?

Tier 1, github-sync, urgency normal. Outcome: **reply**. The customer is asking how GitHub sync handles conflicts between manual edits and AI generated changes, which is a documented behavior question.

Cites KB-07.

> Good news, your fix is safe. GitHub sync is two-way on the main branch, so the commit you pushed yesterday gets pulled into Buildbox within about a minute, if it hasn't already. Once it's in, any new AI generation you ask for builds on top of that code, including your fix.
> 
> The only time Buildbox holds back is if you edit the exact same file in Buildbox and on GitHub at the same moment. In that case it won't overwrite your GitHub commit, it just pauses syncing and marks the project as a conflict so you can choose which version to keep.
> 
> So as long as your fix was committed before you send the next prompt, you're good to go.
> 
> Buildbox Support

Note for the reviewer: Straightforward KB-07 question, no account data needed, no action required.

## T-04: Where do I put my Stripe key

Tier 1, environment-variables, urgency low. Outcome: **reply**. Customer is asking how to properly configure a Stripe secret key, which is a documented environment variables usage question.

Cites KB-08.

> Great question, and please don't paste your Stripe secret key into the prompt box. Prompts aren't the right place for private keys.
> 
> Instead, go to Settings > Environment and add your Stripe secret key there as a Production variable (use Stripe's test key in Preview). These values are encrypted and hidden after saving, and team members can't read them back later.
> 
> The AI can see the variable's name but never its actual value, so you can just ask it to "read the Stripe key from the environment variable STRIPE_SECRET_KEY" and it will wire things up correctly without the key itself ever being exposed.
> 
> One more thing: after adding or changing an environment variable, you'll need to deploy again for it to take effect on your live site.
> 
> Buildbox Support

Note for the reviewer: Standard question fully covered by KB-08; no account-specific action needed.

## T-05: adding a teammate

Tier 1, team-and-account, urgency low. Outcome: **reply**. The customer is asking how team seat pricing and permission roles work, which is documented product information.

Cites KB-09.

> Adding a 6th person to your Team workspace costs an extra $10 per month for that seat. This gets added to your next invoice, prorated for the rest of the current month.
> 
> To add them, go to Settings > Members > Invite and enter their email. The invite link stays valid for 7 days.
> 
> As for permissions, only the workspace Owner can delete the workspace. If you invite your contractor as an Admin or Member (not Owner), they will not be able to delete it. Admins can manage members and settings, while Members can build and deploy but not touch billing or deletion, so Member is likely the safer role for a contractor.
> 
> Let us know if you need help with anything else!
> 
> Buildbox Support

Note for the reviewer: Straightforward informational request about Team seat pricing and roles, fully covered by KB-09. No account data lookup or billing action needed.

## T-06: Getting my code out

Tier 1, data-and-backups, urgency low. Outcome: **reply**. The customer is asking how to export their project code and database data, which is a documented how-to question.

Cites KB-11.

> Hi Hana,
> 
> Yes, you can download everything easily.
> 
> For the code: open your project, go to the Project menu, then Export, and choose Download ZIP. This gives you the full source code, which you own and can host anywhere.
> 
> For the database: go to Project menu > Database > Export. This gives you one CSV file per table.
> 
> If it helps, you can also connect the project to GitHub sync so the code stays in a repository automatically, which can make handing off to your agency simpler.
> 
> Let us know if you run into any trouble with the downloads.
> 
> Buildbox Support

Note for the reviewer: Straightforward export question, fully covered by KB-11. No account-specific lookup was needed.

## T-07: Pro vs Team

Tier 1, plans-and-pricing, urgency low. Outcome: **reply**. The customer is asking about documented differences between Pro and Team plans to decide which to use.

Cites KB-03.

> Great question. The main difference between Pro and Team is seats. A Pro account has one seat, so only one person can log in to that account. Team comes with 5 seats included, so you and your cofounder could each have your own login within the same workspace.
> 
> Outside of that, Pro and Team give you the same things: unlimited projects, custom domains, and GitHub sync. Team just costs more ($50 vs $20 a month) and gives you a shared pool of 2,000 monthly credits instead of 500, plus slightly faster email support.
> 
> If you both need your own login and access, Team is the way to go. If one of you is fine sharing a single login, Pro would work and save you money.
> 
> Buildbox Support

Note for the reviewer: Straightforward plan comparison question, fully answered from KB-03. No account data needed.

## T-08: site says NOT SECURE

Tier 1, custom-domains, urgency normal. Outcome: **reply**. SSL certificates typically take some time to provision after a custom domain is verified, which documentation covers as expected behavior.

Cites KB-06.

> Nothing is broken on your end! Once a domain shows Verified, Buildbox automatically requests an HTTPS certificate for it, and that can take up to 30 minutes to finish. Until it's ready, browsers will show a Not Secure warning, which is expected during that window.
> 
> Since you added the domain about 10 minutes ago, just give it a little more time. Try loading the site again in 20 to 30 minutes and the warning should be gone.
> 
> If it's still showing Not Secure after 24 hours, let us know and we'll take a closer look.

Note for the reviewer: Straightforward KB-06 case; domain was verified only ~10 minutes ago, well within the normal 30-minute certificate issuance window. No action needed unless it persists past 24 hours.

## T-09: Deploy failed

Tier 1, deploys, urgency normal. Outcome: **reply**. The deploy is hitting the documented 10 minute build time limit likely due to AI image generation happening during build, which documentation can explain how to avoid.

Cites KB-05.

> Thanks for sending the log, that detail helps a lot.
> 
> That error means your build is taking longer than the 10 minute limit, and generating a lot of product photos during the build is a common cause of this.
> 
> The fix is to have those images uploaded as assets instead of generated at build time. You can ask the AI in your project to do this by prompting something like: "upload the product photos as static assets instead of generating them during build." You can also ask it to remove any unused packages, since that also helps reduce build time.
> 
> Once that change is made, try deploying again. Your app is still live on the last successful deploy, so nothing is down in the meantime.
> 
> Let us know if the build still fails after that and we will take a closer look.
> 
> Buildbox Support

Note for the reviewer: Straightforward KB-05 case (build time limit, likely caused by image generation at build time). No account data was needed or looked up.

## T-10: Do credits carry over

Tier 1, credits-and-usage, urgency low. Outcome: **reply**. The customer is asking a general documentation question about whether monthly credits and purchased credit packs expire or roll over.

Cites KB-02.

> Hi Zoe,
> 
> Great questions.
> 
> 1) Unused monthly credits do not carry over. Your 500 credits reset each month on your billing date, and whatever is left unused just resets rather than rolling forward.
> 
> 2) Credit packs are different. The 200 credits you buy in a pack never expire, and they are only used after your monthly credits run out. So if you have leftover monthly credits, the pack sits untouched until those are used up.
> 
> Let us know if you have any other questions!
> 
> Buildbox Support

Note for the reviewer: Straightforward factual question fully covered by KB-02; no account-specific data needed.

## T-11: SOC 2 report request

Tier 2, security-and-compliance, urgency normal. Outcome: **escalate-no-source**. The customer needs a human to provide SOC 2 certification status, share the audit report under NDA, and confirm data hosting location.

`escalate: no source`. Missing from the KB: The knowledge base has no information about SOC 2 or other compliance certifications, availability of audit reports under NDA, or the physical/cloud location where customer data is hosted. This is a security/compliance question that needs input from the security or compliance team, not something covered in product KB articles.

Note for the reviewer: Customer is doing a security review before a 40-seat rollout and is asking about SOC 2 Type II certification, NDA report access, and data hosting location. None of this is in the KB, please route to security/compliance team or whoever handles NDA and audit report requests.

## T-12: Nonprofit discount?

Tier 1, plans-and-pricing, urgency low. Outcome: **escalate-no-source**. Customer is asking whether a nonprofit or education discount exists for a paid plan.

`escalate: no source`. Missing from the KB: The knowledge base has no information about nonprofit or education discounts, or any discount programs beyond the standard Free/Pro/Team pricing in KB-03. I cannot confirm whether such a discount exists.

Note for the reviewer: Customer is asking about a nonprofit/education discount for the Team plan. Nothing in the KB covers this, so please check if there's an internal nonprofit discount policy before replying.

## T-13: Charged twice for credit pack

Tier 2, billing-charges, urgency high. Outcome: **propose-billing-action**. The customer was charged twice for a single credit pack purchase and only received credits for one, indicating a billing error that needs account investigation.

Cites KB-13.

> Hi Dana,
> 
> Thanks for flagging this, and sorry for the trouble. I can see two $10 charges for a credit pack posted just minutes apart, but only one pack's worth of 200 credits was applied to your account. That matches a duplicate charge, which we refund in full.
> 
> A teammate will confirm the refund for the extra charge shortly. Once it's issued, you'll get a confirmation email with the amount and date, and the refund should show on your statement within 5 to 10 business days depending on your bank.
> 
> Let us know if you have any other questions in the meantime.
> 
> Buildbox Support

Proposed billing action, **waiting for a human**: refund $10.00. Target found in account data: True. Reason: Two identical $10 credit pack charges posted minutes apart but only one 200-credit pack was granted; KB-13 treats duplicate charges as always refunded in full for the duplicate charge.

`python billing.py refund ch_****WSpd --reason "Two identical $10 credit pack charges posted minutes apart but only one 200-credit pack was granted; KB-13 treats duplicate charges as always refunded in full for the duplicate charge." --confirm --approved-by "<your name>"`

Note for the reviewer: Confirmed both charges are $10 credit packs, same timestamp window, unrefunded, and only 200 credits (one pack) were granted. Please verify which charge id is the duplicate before issuing the refund and confirm only one pack's credits were actually applied.

## T-14: payment failed email

Tier 2, billing-payment-failed, urgency high. Outcome: **reply**. The customer's Pro payment failed and they need billing help resolved before a client demo on Friday to avoid losing access to their projects.

Cites KB-14.

> Thanks for reaching out, and no need to worry right away. When a payment fails, we email you and automatically retry the card three times over the next 7 days. Your Pro plan stays active during this time, so nothing will be lost or paused yet.
> 
> To make sure everything is ready for your demo on Friday, the safest step is to update your card now rather than wait for the retries. Go to Settings > Billing > Manage billing and enter a working card there. The open invoice will be charged right away once you do, and your Pro plan will be fully confirmed.
> 
> If all the retries fail before you update the card, the account would move to the Free plan, and any projects over the Free limit would become read only until you upgrade again. Updating your card now avoids that entirely.
> 
> Let us know if you run into any trouble updating the card.
> 
> Buildbox Support

Note for the reviewer: Account shows the Pro subscription as 'incomplete' with the initial charge failed (card_declined) and invoice still open; customer needs to update payment method before Friday to avoid disruption. No refund/cancel action needed here.

## T-15: Refund please, forgot to cancel

Tier 2, billing-refunds, urgency normal. Outcome: **propose-billing-action**. The customer wants a refund for an unintended Pro plan renewal charge and to downgrade to the free plan.

Cites KB-13.

> Hi Priya,
> 
> Thanks for reaching out, and sorry for the mix-up with the renewal. Since your Pro plan just renewed and you've used very little since then, this qualifies for our refund policy. A teammate will confirm and process the refund on our side shortly. Once approved, the $20 charge will be refunded to your original card (usually showing within 5 to 10 business days), and your account will move to the Free plan, so you won't be charged again for Pro. You'll also get a confirmation email once the refund is issued.
> 
> If you have any projects or usage that go beyond the Free plan's limits, it's worth checking those before the switch happens.
> 
> Let us know if you have any other questions.
> 
> Buildbox Support

Proposed billing action, **waiting for a human**: refund $20.00. Target found in account data: True. Reason: Customer requested refund within 7 days of the subscription renewal charge per KB-13. Account data confirms the charge and that it is unrefunded, but credit usage since the charge is not shown in account data and should be checked to confirm the under-50-credit condition before approving.

`python billing.py refund ch_****UdgA --reason "Customer requested refund within 7 days of the subscription renewal charge per KB-13. Account data confirms the charge and that it is unrefunded, but credit usage since the charge is not shown in account data and should be checked to confirm the under-50-credit condition before approving." --confirm --approved-by "<your name>"`

Note for the reviewer: Please verify credit usage since the 2026-09-23 charge (not visible in account data) to confirm it's under 50 before approving the refund, per KB-13. If eligible, refunding this charge also cancels the plan and moves the account to Free per policy, so no separate cancel action is needed.

## T-16: Invoice with company details

Tier 2, billing-invoices, urgency normal. Outcome: **reply**. Customer needs their invoice reissued with company name and VAT number, which requires account admin action.

Cites KB-12.

> Hi Omar,
> 
> Thanks for reaching out. Past invoices can't be edited directly since they're tax documents, but since this one was issued within the last 90 days, we're able to issue a copy with Haddad Design Ltd and your VAT number added. A teammate will take care of this shortly and send the updated copy your way.
> 
> To make sure all your future invoices show these details automatically, please add your company name and VAT number in Settings > Billing > Manage billing, under "Billing information." That way you won't need to ask us again going forward.
> 
> Let us know if you need anything else.
> 
> Buildbox Support

Note for the reviewer: Customer's only invoice (in_****iWIV, $20 Pro subscription) is well within the 90-day window per KB-12, so a corrected copy with company name and VAT can be issued. Customer didn't provide the VAT number in the ticket, so please request it before reissuing.

## T-17: Where is my refund

Tier 2, billing-refunds, urgency normal. Outcome: **reply**. Customer wants confirmation on a previously promised refund that has not appeared on their card.

Cites KB-13.

> Hi Sofia,
> 
> Yes, your refund was sent. We can confirm the $10 for your credit pack was successfully refunded to your original card.
> 
> Refunds can take 5 to 10 business days to show up on your statement, depending on your bank, so if it has been less than that it should appear soon. If it still is not showing after 10 business days, let us know and we will look into it further.
> 
> Buildbox Support

Note for the reviewer: Account data confirms refund re_****spZS for charge ch_****UFy2 succeeded, full $10 already refunded. No action needed unless customer reports still missing after 10 business days.

## T-18: Weird charge after upgrading

Tier 2, billing-plan-changes, urgency normal. Outcome: **reply**. The customer needs an account specific explanation of a prorated charge and future billing after upgrading from Pro to Team.

Cites KB-15.

> Thanks for reaching out, and sorry for the confusion! What you saw is expected. When you upgrade from Pro to Team, Buildbox charges you right away for the new plan, but gives you credit for the unused time left on your old plan. That is why the amount was not a round $50: it was the Team price minus a credit for the Pro time you had not used yet, which comes out to an odd number rather than the full $50.
> 
> Going forward, you will not be charged twice. Your next regular charge will simply be the normal $50 Team plan renewal, once a month, nothing extra on top. If anything on your invoice still looks off, let us know and we will take a closer look.
> 
> Buildbox Support

Note for the reviewer: Verified the $30 charge matches proration math in the account data (-$20 unused Pro + $50 Team = $30), consistent with KB-15. No billing action needed; next renewal will be the standard $50/month Team charge.

## T-19: Cancel my subscription

Tier 2, billing-plan-changes, urgency normal. Outcome: **propose-billing-action**. Customer wants to cancel their Team subscription and asks about access timing, which requires account administration.

Cites KB-15.

> Hi Ana,
> 
> Thanks for letting us know. We will cancel your Team subscription so it does not renew again. A teammate will confirm this shortly.
> 
> You will not lose access right away. Cancelling stops the next charge, but you keep full Team access until the end of your current billing period, which gives you plenty of time to finish your migration. After that date your account moves to the Free plan, and nothing is deleted.
> 
> If you need more time beyond that, just let us know before the period ends.
> 
> Buildbox Support

Proposed billing action, **waiting for a human**: cancel $0.00. Target found in account data: True. Reason: Customer requested cancellation of Team subscription to stop future renewal; per KB-15 access continues until end of current billing period.

`python billing.py cancel sub_****vfuW --reason "Customer requested cancellation of Team subscription to stop future renewal; per KB-15 access continues until end of current billing period." --confirm --approved-by "<your name>"`

Note for the reviewer: Customer wants a couple weeks to migrate; current_period_end in account data is about a month out (sandbox dates), so timing should comfortably cover their need. Please confirm the cancellation in the billing system.

## T-20: change email on account

Tier 2, team-and-account, urgency normal. Outcome: **reply**. The customer needs account administration help to change their login and billing email while retaining their Pro plan.

Cites KB-10.

> Hi Jonas,
> 
> You can update this yourself and it will not affect your Pro plan. Go to Settings > Account > Email and enter your personal address. We will send a confirmation link to that new address, and once you click it, your login and billing email both switch over automatically.
> 
> Your Pro subscription and billing stay exactly as they are, just under the new email. No need to cancel or re-subscribe.
> 
> Let us know if you run into any trouble with the confirmation email.
> 
> Buildbox Support

Note for the reviewer: Straightforward email-change question fully covered by KB-10; no account action needed. Account is active Pro, no delinquency, so nothing else to flag.

## T-21: Owner left the company

Tier 2, team-and-account, urgency normal. Outcome: **reply**. The customer needs account administration support to transfer workspace ownership since the original owner is no longer accessible.

Cites KB-09.

> Thanks for reaching out, Grace. Since the workspace owner can no longer log in, our support team can transfer ownership to you.
> 
> To do this, we need to verify the request with a second Admin on your workspace, along with the billing email on file. Once you can confirm those, a teammate will process the ownership transfer for you.
> 
> Could you let us know who the second Admin is, or have them reach out to confirm as well? That will let us move forward quickly.
> 
> Buildbox Support

Note for the reviewer: Customer needs ownership transfer per KB-09 since prior owner cannot log in. Requires verification with a second Admin and the billing email on file before proceeding; please confirm those details with Grace before transferring ownership.

## T-22: $50 charge??

Tier 2, billing-charges, urgency normal. Outcome: **reply**. The customer was charged more than the expected plan price and needs an account specific billing review.

Cites KB-03, KB-15, KB-13.

> Hi Marco,
> 
> Thanks for reaching out. Looking at your account, you're currently on the Team plan, which is $50 a month, rather than Pro which is $20 a month. That's why the charge came through at $50.
> 
> If you meant to be on Pro instead, you can switch any time from Settings > Billing > Manage billing. Since this would be a downgrade from Team to Pro, it takes effect at the end of your current billing period and you'd keep Team access until then, with no partial refund for the difference.
> 
> If you'd rather switch right away and get a refund of this charge, that's possible since it's within 7 days of the charge, as long as you've used fewer than 50 credits since then. Just let us know and a teammate will check your usage and confirm.
> 
> Let us know how you'd like to proceed.
> 
> Buildbox Support

Note for the reviewer: Customer is on Team ($50/mo), charged correctly per account data, but may have intended Pro ($20). Charge is within 7 days so refund eligibility depends on credit usage since the charge, which I could not check - please verify usage under Settings > Usage if customer requests a refund/switch.

## T-23: All deploys stuck in Queued

Tier 3, deploys, urgency high. Outcome: **escalate-engineering**. Deploys are stuck in Queued for hours across multiple projects despite the status page showing normal operation, indicating a stuck job that needs engineering investigation.

Handoff note: [escalations/T-23.md](escalations/T-23.md)

## T-24: GitHub sync deleted my files

Tier 3, github-sync, urgency high. Outcome: **escalate-engineering**. A simple color change prompt caused Buildbox to delete an entire folder of files via GitHub sync and the repo is now stuck in a conflict state, indicating a bug that needs engineering investigation.

Handoff note: [escalations/T-24.md](escalations/T-24.md)

## T-25: SSL pending for 3 days

Tier 3, custom-domains, urgency high. Outcome: **escalate-engineering**. The customer verified DNS is correctly configured with no CAA blocking issue, yet the SSL certificate has been stuck in Pending for 3 days causing a live certificate error on their site.

Handoff note: [escalations/T-25.md](escalations/T-25.md)

## T-26: 500 error on every prompt + credits gone

Tier 3, editor-and-generation, urgency high. Outcome: **escalate-engineering**. The user is getting repeated 500 errors on prompt generation across browsers and projects while still being charged credits, indicating a bug that needs engineering investigation.

Handoff note: [escalations/T-26.md](escalations/T-26.md)

## T-27: database empty after redeploy

Tier 3, data-and-backups, urgency high. Outcome: **escalate-engineering**. The customer's live database lost all 1,200 rows after a redeploy, indicating a possible data loss bug that requires engineering investigation and is actively harming their business.

Handoff note: [escalations/T-27.md](escalations/T-27.md)

## T-28: Blank preview in Safari

Tier 3, editor-and-generation, urgency normal. Outcome: **escalate-engineering**. The preview crashes in Safari with an unhandled WebGPU API error even after standard troubleshooting, indicating a compatibility bug that needs engineering investigation.

Handoff note: [escalations/T-28.md](escalations/T-28.md)

## T-29: env vars not in production

Tier 3, environment-variables, urgency high. Outcome: **escalate-engineering**. The user correctly configured a Production-scoped environment variable and redeployed but it still is not available on the live site, indicating a bug affecting their production app.

Handoff note: [escalations/T-29.md](escalations/T-29.md)

## T-30: credits going down twice as fast

Tier 3, credits-and-usage, urgency high. Outcome: **escalate-engineering**. The customer reports that every generation is consistently consuming double the credits shown in the prompt since a recent update, which is a product bug causing ongoing credit loss.

Handoff note: [escalations/T-30.md](escalations/T-30.md)
