"""A host for canopy-based personal websites."""

import stripe
import web

app = web.application(__name__, automount=True, autotemplate=True)
host_name = app.cfg.get("host_name")
stripe.api_key = app.cfg.get("stripe_sk")


@app.control("")
class Home:
    """Homepage."""

    def get(self):
        return app.view.home(host_name)

    def post(self):
        return "coming soon"


@app.control("secret")
class StripeSecret:
    """Provide a Stripe secret for the registration client."""

    def get(self):
        intent = stripe.PaymentIntent.create(
            amount=100,
            currency="usd",
            metadata={"integration_check": "accept_a_payment"},
        )
        web.header("Content-Type", "application/json")
        return {"client_secret": intent.client_secret}


@app.control("register")
class Register:
    """Registration."""

    def post(self):
        username = web.tx.request.body._data["username"]
        passphrase = f"TODO-PW-FOR-{username}"  # canopy.initialize(username)
        # TODO insert into database
        web.header("Content-Type", "application/json")
        return {"passphrase": passphrase}
