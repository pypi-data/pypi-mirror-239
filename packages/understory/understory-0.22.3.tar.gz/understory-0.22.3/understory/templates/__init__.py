import web
from web import tx

__all__ = ["tx", "admin_name", "admin_domain", "stripe_pk"]


understory = web.application("understory")

admin_name = understory.cfg["admin_name"]
admin_domain = understory.cfg["admin_domain"]
stripe_pk = understory.cfg["stripe_pk"]
