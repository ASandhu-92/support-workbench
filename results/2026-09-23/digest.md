# Voice of customer, 2026-09-14 to 2026-09-22

**Billing and credit confusion drove the most tickets this week, but a production database wipe and a GitHub sync that deleted a customer's files are the most urgent risks to fix.**

| Theme | Tickets | Count | Owner | Proposed action |
|---|---|---|---|---|
| Billing and credit charges confuse customers (wrong amounts, double charges, refund status, resets) | T-01, T-10, T-13, T-14, T-15, T-16, T-17, T-18, T-19, T-22 | 10 | billing | Ship a single billing page showing current plan price, any proration math in plain language, credit balance, and exact reset/renewal date, so customers can answer these questions themselves instead of emailing support. |
| Deploys and environment variables fail in ways customers can't fix | T-04, T-09, T-23, T-29 | 4 | engineering | Raise the build time limit (or make it configurable) for image-heavy builds, fix Production-scoped environment variables so they actually reach the live build, and add a stuck-deploy timeout alert. |
| Custom domain and SSL setup feels broken or scary | T-02, T-08, T-25 | 3 | engineering | Replace the immediate 'Not Secure' state with a clear 'Certificate provisioning, usually done in X minutes' status, and auto-page engineering if issuance exceeds 30 minutes. |
| Generation and preview bugs waste credits and break the editor | T-26, T-28, T-30 | 3 | engineering | Stop deducting credits on any generation that returns a 500 error or fails, and add a feature-detection fallback so previews don't blank-screen on browsers without WebGPU support. |
| Team and account ownership changes have no clear self-serve path | T-05, T-20, T-21 | 3 | product | Let a verified Admin claim Owner role when the original owner is unreachable, and support self-serve login/billing email changes without disrupting the active plan. |
| Pricing tiers and compliance needs block growth and nonprofit customers | T-07, T-11, T-12 | 3 | sales | Publish a nonprofit/education discount and a self-serve NDA-gated SOC 2 report request on the pricing page, and clarify Pro vs Team seat limits so small teams don't have to ask support. |
| GitHub sync overwrites or deletes customer code without warning | T-03, T-24 | 2 | engineering | Require a diff preview and explicit confirmation before the AI pushes commits to main, and scope AI edits so unrelated files/folders can't be deleted by a single prompt. |
| Data loss and export fears around production databases | T-06, T-27 | 2 | engineering | Add automatic point-in-time backups of the production database taken before every redeploy, with a one-click restore, and make a full code+data export a standard self-serve action. |

## In their words

- **Billing and credit charges confuse customers (wrong amounts, double charges, refund status, resets)** (T-22): "I thought I was paying $20 for Pro. Why is it $50?"
- **Deploys and environment variables fail in ways customers can't fix** (T-23): "I have a launch tomorrow morning."
- **Custom domain and SSL setup feels broken or scary** (T-08): "Customers will see this!"
- **Generation and preview bugs waste credits and break the editor** (T-26): "I lost about 30 credits for nothing."
- **Team and account ownership changes have no clear self-serve path** (T-21): "nobody can log in as them."
- **Pricing tiers and compliance needs block growth and nonprofit customers** (T-12): "$50 a month is a lot for us."
- **GitHub sync overwrites or deletes customer code without warning** (T-24): "I did not ask for that, my prompt was to change a button color."
- **Data loss and export fears around production databases** (T-27): "this is our real business."

## Knowledge base gaps

- T-11: The knowledge base has no information about SOC 2 or other compliance certifications, availability of audit reports under NDA, or the physical/cloud location where customer data is hosted. This is a security/compliance question that needs input from the security or compliance team, not something covered in product KB articles.
- T-12: The knowledge base has no information about nonprofit or education discounts, or any discount programs beyond the standard Free/Pro/Team pricing in KB-03. I cannot confirm whether such a discount exists.
