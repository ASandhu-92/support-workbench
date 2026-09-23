# KB-14 Failed payments

If a card payment fails (expired card, insufficient funds, bank decline), we email the billing
address and retry the payment 3 times over the next 7 days.

- Your plan stays active during the retries.
- To fix it, update the card in Settings > Billing > **Manage billing**. The open invoice is paid
  with the new card right away.
- If all retries fail, the account moves to the Free plan. Nothing is deleted: projects over the
  Free limit become read-only, and custom domains stop serving until you upgrade again.
- The decline reason comes from your bank. We see a code such as "card declined" or "insufficient
  funds", but only your bank can tell you why it declined.
