from django.apps import AppConfig


"""
The core app is the place where everything connects together.
This is the central routing hub, the main bus, the message queue.

Everything starts out here until it becomes specific enough to warrant another app.
"""


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.core'
