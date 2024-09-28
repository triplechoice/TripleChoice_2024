import json
import os

import stripe


class StripePayment:
    def refund(self, instance):
        stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
        try:
            refund = None
            for payment_info in instance.payment_info['charges']['data']:
                if payment_info['id']:
                    refund = stripe.Refund.create(
                        charge=payment_info['id'],
                    )
            if refund is not None:
                instance.refund_info = json.loads(str(refund))
                instance.save()
            return True
        except Exception as e:
            print(e)
            return False
