from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.utils import timezone
from uuid import uuid4
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the provided email and password.
        """
        if not email:
            raise ValueError("The given email address must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model that uses email addresses instead of usernames, and
    name instead of first / last name fields.
    All other fields from the Django auth.User model are kept to
    ensure maximum compatibility with the built in management
    commands.
    """

    email = models.EmailField(blank=True, default="", unique=True)
    name = models.CharField(max_length=200, blank=True, default="")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name or self.email.split("@")[0]


class Card(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    parent = models.ForeignKey(
        'self',
        related_name="children",
        null=True, blank=True,
        on_delete=models.SET_NULL)

    uuid = models.UUIDField(
        unique=True,
        default=uuid4,
        editable=False,
        help_text='A universally unique identifier, allows referencing a card if no url is provided.')

    site = models.ForeignKey(
        Site,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='The domain name which this card will be viewable on.')

    url = models.CharField(
        max_length=1023,
        blank=True,
        help_text='If specified, allow viewing this card at this url for the above specified site. A url is a series of only lowercase letters, numbers, and slashes and ends with a slash.')

    title = models.CharField(
        max_length=1023,
        blank=True,
        help_text='A title for this card. If this card is used as the root card of a webpage, it will be used as the html page title.')
    description = models.TextField(
        max_length=8191,
        blank=True,
        help_text='A description of this card. If this card is used as the root card of a webpage, it will be used as the meta description text.')

    published = models.BooleanField(
        default=False,
        help_text='If true, this card will be publically viewable without required the viewer to be logged in. If false (default) this card will only be viewable by logged in users.')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    @property
    def content_type_template(self):
        return f"content_types/{self.content_type.model}.html"

    def __str__(self):
        return self.title or self.uuid

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class CardData(models.Model):
    '''
    Inherit from CardData to create a new content type of card with additional fields.
    '''

    cards = GenericRelation(Card)

    class Meta:
        abstract = True

    @property
    def card(self):
       return self.cards.first()


class HTMLContent(CardData):
    html_content = models.TextField()

    def __str__(self):
        return self.html_content[:255]


class MP4ImageViewer(CardData):
    small = models.FileField()
    medium = models.FileField()
    full = models.FileField()


class GoogleDoc(CardData):
    google_doc_title = models.CharField(max_length=1023)
    google_doc_url = models.CharField(max_length=1023)

    def __str__(self):
        return self.google_doc_title


class SiteSettings(CardData):
    site = models.OneToOneField(
        Site,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    background_color = models.CharField(max_length=255)


'''
class MarkdownContent(CardData):
    markdown_content = models.TextField()

    def __str__(self):
        return self.markdown_content[:255]


class CardStream(CardData):
    many to many to card
    like wagtail's StreamField

'''
    

"""
    # RELATIONSHIP DATA

    # The remote data for this card
    text = models.TextField(max_length=65535, blank=True)
    src = models.URLField(max_length=1023, blank=True)

    author = models.ForeignKey(
        User,
        related_name="cards",
        on_delete=models.PROTECT)

    # ORDERING DATA

    votes = models.IntegerField(default=1)
    root = models.ForeignKey(
        'self',
        related_name="descendants",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        help_text="If null, this is a top level card.")

    next = models.OneToOneField(
        'self',
        related_name='prev',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        help_text="The next card in this thread.")

    def __str__(self):
        return self.title or self.text[40:] or self.uuid

    def get_absolute_url(self):
        return reverse('card_detail', kwargs={'uuid': self.uuid})

    class Meta:
        ordering = ['-created_at']

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

    '''
    @property
    def root(self):
        return self.thread[0]

    @property
    def thread(self):
        return self.parent.children.order_by('order')
    '''


class FocusPeriod(CardData):
    card = models.ForeignKey('Card', on_delete=models.PROTECT)
    start = models.DateTimeField(default=timezone.now)
    duration = models.DurationField(null=True, blank=True)



class Compositor(CardType):
    '''
    Combines multiple cards onto a single page
    '''


"""
