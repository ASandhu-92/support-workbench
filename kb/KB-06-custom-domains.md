# KB-06 Custom domains

Custom domains are available on Pro and Team (KB-03).

1. Settings > Domains > Add domain, and type the domain (for example `www.example.com`).
2. At your DNS provider, add the record Buildbox shows:
   - a subdomain such as `www`: a **CNAME** to `edge.bbx.example`
   - the root domain (`example.com`): an **A** record to `192.0.2.10`
3. Wait for the status to turn **Verified**. DNS changes can take up to an hour to be seen.

After the domain is verified, Buildbox requests an HTTPS certificate automatically. This normally
takes up to 30 minutes. Until then the browser may warn "not secure"; that is expected in the first
30 minutes.

If the status stays **Pending** for more than 24 hours with the DNS record correct, check for a CAA
record at your DNS provider that blocks our certificate authority, and if there is none, contact
support with the domain name. That case needs an engineer.
