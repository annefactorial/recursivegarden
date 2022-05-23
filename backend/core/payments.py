from contextlib import contextmanager
from django.conf import settings

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


stripe.Charge.create(
    
)

charge = stripe.Charge.create(
    amount=2000,
    currency="usd",
    description="My First Test Charge (created for API docs at https://www.stripe.com/docs/api)",
    source="tok_visa", # obtained with Stripe.js
    # Generate uuidv4
    idempotency_key='EYBj2DzWbgo32hYr'
)

def get_balance():
    return balance = stripe.Balance.retrieve()
    return {
        "object": "balance",
        "available": [
            {
                "amount": 0,
                "currency": "usd",
                "source_types": {
                    "card": 0
                }
            }
        ],
        "livemode": false,
        "pending": [
            {
                "amount": 0,
                "currency": "usd",
                "source_types": {
                    "card": 0
                }
            }
        ]
    }


@contextmanager
def handle_stripe_error():
    try:
        yield
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        print('Status is: %s' % e.http_status)
        print('Code is: %s' % e.code)
        # param is '' in this case
        print('Param is: %s' % e.param)
        print('Message is: %s' % e.user_message)
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        pass
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        pass
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        pass
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        pass
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        pass
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        pass
