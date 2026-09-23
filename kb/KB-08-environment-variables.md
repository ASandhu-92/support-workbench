# KB-08 Environment variables and secrets

Store API keys and other private values in Settings > Environment, never in the code or in a
prompt.

- Each variable has a scope: **Preview**, **Production**, or both. The live site only sees
  Production values (KB-04).
- Values are encrypted at rest and are hidden after saving. Team members can replace a value but
  cannot read it back.
- The AI can see variable **names**, so it can write code that uses them, but never their values.
- A change to a variable takes effect on the next deploy. Deploy again after editing.
- For a payment provider key (for example a Stripe secret key), add it as a Production variable and
  ask the AI to "read the Stripe key from the environment variable STRIPE_SECRET_KEY". Use the
  provider's test key in Preview.
