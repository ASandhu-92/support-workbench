"""Create the Buildbox products and the ten billing customers in a Stripe sandbox.

Test mode only (the same key check as billing.py). Idempotent: products are found by metadata key,
customers by email plus the workbench tag, and a customer that already exists is left alone.
Writes data/customers.json (git-ignored) with the test ids; data/customers.example.json shows its
shape with placeholders.

Test payment methods used: pm_card_visa (always succeeds) and pm_card_chargeCustomerFail (attaches,
then every charge is declined).
"""
import json

import stripe

import billing
from tickets import DATA

PRODUCTS = {
    # key: (name, plan label, cents, interval)
    "buildbox_pro": ("Buildbox Pro", "Pro", 2000, "month"),
    "buildbox_team": ("Buildbox Team", "Team", 5000, "month"),
    "buildbox_credits": ("Buildbox credit pack (200 credits)", "Credit pack", 1000, None),
}

# email: (name, ticket, scenario)
CUSTOMERS = {
    "dana.ivers@example.com": ("Dana Ivers", "T-13", "double_credit_pack"),
    "liam.novak@example.com": ("Liam Novak", "T-14", "pro_card_declined"),
    "priya.desai@example.com": ("Priya Desai", "T-15", "pro_paid"),
    "omar.haddad@example.com": ("Omar Haddad", "T-16", "pro_paid"),
    "sofia.lind@example.com": ("Sofia Lind", "T-17", "credit_pack_refunded"),
    "ken.muller@example.com": ("Ken Muller", "T-18", "pro_upgraded_to_team"),
    "ana.costa@example.com": ("Ana Costa", "T-19", "team_paid"),
    "jonas.berg@example.com": ("Jonas Berg", "T-20", "pro_paid"),
    "grace.kim@example.com": ("Grace Kim", "T-21", "team_paid"),
    "marco.rossi@example.com": ("Marco Rossi", "T-22", "team_paid"),
}


def ensure_product(key, name, plan, cents, interval):
    found = [p for p in stripe.Product.list(active=True, limit=100).auto_paging_iter()
             if billing.meta(p).get("key") == key]
    found.sort(key=lambda p: p.created)
    product = found[0] if found else stripe.Product.create(name=name, metadata={"key": key, **billing.TAG})
    for price in stripe.Price.list(product=product.id, active=True, limit=100).auto_paging_iter():
        if price.unit_amount == cents and (price.recurring.interval if price.recurring else None) == interval:
            return product.id, price.id
    kwargs = {"product": product.id, "unit_amount": cents, "currency": "usd",
              "nickname": plan, "metadata": {"plan": plan}}
    if interval:
        kwargs["recurring"] = {"interval": interval}
    return product.id, stripe.Price.create(**kwargs).id


def card(customer_id, test_pm):
    pm = stripe.PaymentMethod.attach(test_pm, customer=customer_id)
    stripe.Customer.modify(customer_id, invoice_settings={"default_payment_method": pm.id})
    return pm.id


def buy_pack(customer_id, pm, prices):
    return stripe.PaymentIntent.create(
        amount=PRODUCTS["buildbox_credits"][2], currency="usd", customer=customer_id,
        payment_method=pm, confirm=True, description=PRODUCTS["buildbox_credits"][0],
        automatic_payment_methods={"enabled": True, "allow_redirects": "never"},
        metadata={"price": prices["buildbox_credits"], **billing.TAG})


def subscribe(customer_id, price, **extra):
    return stripe.Subscription.create(customer=customer_id, items=[{"price": price}],
                                      metadata=billing.TAG, **extra)


def run_scenario(scenario, cid, prices):
    if scenario == "double_credit_pack":
        pm = card(cid, "pm_card_visa")
        buy_pack(cid, pm, prices)
        buy_pack(cid, pm, prices)
    elif scenario == "pro_card_declined":
        card(cid, "pm_card_chargeCustomerFail")
        subscribe(cid, prices["buildbox_pro"], payment_behavior="allow_incomplete")
    elif scenario == "credit_pack_refunded":
        pm = card(cid, "pm_card_visa")
        pi = buy_pack(cid, pm, prices)
        stripe.Refund.create(payment_intent=pi.id, metadata={"note": "sandbox setup", **billing.TAG})
    elif scenario == "pro_upgraded_to_team":
        card(cid, "pm_card_visa")
        sub = subscribe(cid, prices["buildbox_pro"])
        item = sub["items"].data[0]
        stripe.Subscription.modify(sub.id, items=[{"id": item.id, "price": prices["buildbox_team"]}],
                                   proration_behavior="always_invoice")
    elif scenario in ("pro_paid", "team_paid"):
        card(cid, "pm_card_visa")
        subscribe(cid, prices["buildbox_pro" if scenario == "pro_paid" else "buildbox_team"])
    else:
        raise ValueError(scenario)


def main():
    billing.configure()
    prices, products = {}, {}
    for key, spec in PRODUCTS.items():
        products[key], prices[key] = ensure_product(key, *spec)
        print(f"{key:18} {products[key]} {prices[key]}")
    out = {"products": {k: {"product": products[k], "price": prices[k]} for k in PRODUCTS}, "customers": {}}
    for email, (name, ticket, scenario) in CUSTOMERS.items():
        cust = billing.find_customer(email)
        if cust is None or billing.meta(cust).get("workbench") != billing.TAG["workbench"]:
            cust = stripe.Customer.create(email=email, name=name,
                                          metadata={"ticket": ticket, "scenario": scenario, **billing.TAG})
            run_scenario(scenario, cust.id, prices)
            state = "created"
        else:
            state = "exists"
        out["customers"][email] = {"customer": cust.id, "ticket": ticket, "scenario": scenario}
        print(f"{ticket} {email:26} {cust.id} {scenario} ({state})")
    (DATA / "customers.json").write_text(json.dumps(out, indent=2) + "\n")
    print("wrote data/customers.json")


if __name__ == "__main__":
    main()
