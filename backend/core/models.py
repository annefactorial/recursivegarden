from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from pathlib import Path
from django.db import models
from django.urls import reverse
from django.utils import timezone
from uuid import uuid4

import toml
from django.template.loader import render_to_string
from django.conf import settings
import glob


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    stripe_customer_id = models.CharField(max_length=255, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    # Make the admin work, but permissions are just either
    # normal user or admins who have full permissions
    @property
    def is_staff(self):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def full_name(self):
        return self.display_name


class Topic(models.Model):
    '''
    A topic is a discord channel, where if you are in that channel and you create new cards, it adds them to that channel
    Cards can belong to multiple channels
    Maybe only top level cards, or cards that are first in their series, can belong to a topic? the other cards assume to inherit their prev's topics?
    '''
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    uuid = models.UUIDField(default=uuid4, editable=False)
    title = models.CharField(max_length=1023, blank=True)
    slug = models.SlugField(max_length=1023, blank=True)

    def __str__(self):
        return self.title or self.uuid

    def get_absolute_url(self):
        return reverse('tag_detail', kwargs={'slug': self.slug})


class Card(models.Model):
    '''
    To make: Card Explorer
    '''
    '''
    A piece of content that can be referenced in a template by id or searches for a list

    A card is not a store of html, that is a template. A card has data that can be accessed in the template using curlies, including text content
    '''
    # Universally unique id in case this card is referenced externally
    uuid = models.UUIDField(default=uuid4, editable=False)

    topics = models.ManyToManyField(Topic, blank=True, related_name='cards')

    # Ascend up and down
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.SET_NULL)

    # Move forward and backward (but this should be time, or order?)
    order = models.IntegerField(default=0)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="cards",
        null=True,
        blank=True,
        on_delete=models.SET_NULL)

    title = models.CharField(max_length=1023, blank=True)

    file = models.FileField(
        max_length=255,
        null=True, blank=True,
        upload_to="cards/%Y/%m/")

    # The contents of the card are at an external url
    src = models.URLField(max_length=1023, blank=True)

    # Raw card contents
    text = models.TextField(max_length=65535, blank=True)

    # Sort by ranking
    gravity = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['order']

        '''
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prev_or_parent_not_both",
                check=(
                    models.Q(
                        prev__isnull=False,
                        parent__isnull=True,
                    ) | models.Q(
                        prev__isnull=True,
                        parent__isnull=False,
                    ) | models.Q(
                        prev__isnull=True,
                        parent__isnull=True,
                    )
                ))
        ]
        '''

    @property
    def root(self):
        return self.thread[0]

    @property
    def thread(self):
        return self.parent.children.order_by('order')

    def __str__(self):
        return self.title or self.text[40:] or self.uuid

    def get_absolute_url(self):
        return reverse('card_detail', kwargs={'uuid': self.uuid})


class MoneyAccount(models.Model):
    """
    The Accounting Equation:

    Assets = Liabilities + Owners Equity
    """

    uuid = models.UUIDField(default=uuid4, editable=False)
    type = models.CharField(max_length=40, choices=(
        ('assets', 'Assets'),
        ('liability', 'Liability'),
        ('equity', 'Owner\'s Equity'),
    ))
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE)

    description = models.TextField(max_length=8191, blank=True)


class MoneyFlow(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    stripe_charge_id = models.CharField(max_length=255, blank=True)

    outflowing_from = models.ForeignKey(MoneyAccount, related_name='outflows', on_delete=models.PROTECT)
    inflowing_to = models.ForeignKey(MoneyAccount, related_name='inflows', on_delete=models.PROTECT)

    amount = models.PositiveIntegerField()
    currency = models.CharField(
        max_length=5,
        choices=(('USD', 'USD'), ('BTC', 'BTC'), ('ETH', 'ETH'))
    )

    description = models.TextField(max_length=1023, blank=True)


class Product(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    stripe_product_id = models.CharField(max_length=255, blank=True)

    title = models.CharField(max_length=1023)
    slug = models.SlugField(max_length=1023)
    file = models.FileField(max_length=255, null=True, blank=True, upload_to="products/%Y/%m/")

    def create_stripe_product(self):
        return stripe.Product.create()


class ProductPurchase(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='purchases',
        on_delete=models.PROTECT)

    money_flow = models.ForeignKey(
        MoneyFlow,
        related_name='flows',
        on_delete=models.PROTECT)


class ProductUnlock(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="unlocks",
        on_delete=models.PROTECT)

    product = models.ForeignKey(
        Product,
        related_name='unlocks',
        on_delete=models.PROTECT)
