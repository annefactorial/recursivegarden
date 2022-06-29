from django.db import models
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


class Focus(models.Model):
    card = models.ForeignKey('Card', on_delete=models.PROTECT)
    start = models.DateTimeField(default=timezone.now)
    duration = models.DurationField(null=True, blank=True)


class Card(models.Model):
    # ID
    uuid = models.UUIDField(default=uuid4, editable=False)

    # TIMESTAMPS
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(blank=True)

    # BODY DATA
    title = models.CharField(max_length=1023, blank=True)
    text = models.TextField(max_length=65535, blank=True)

    # FILE DATA
    file = models.FileField(
        max_length=255,
        blank=True,
        upload_to="files/")

    # META DATA
    type = models.CharField(max_length=1023, blank=True)
    votes = models.IntegerField(default=1)
    data = models.JSONField(null=True, blank=True)

    # RELATIONSHIP DATA
    src = models.URLField(max_length=1023, blank=True)

    author = models.ForeignKey(
        User,
        related_name="cards",
        on_delete=models.PROTECT)

    parent = models.ForeignKey(
        'self',
        related_name="children",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        help_text="If null, this is a top level card.")

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
        return self.title or str(self.text[255:])

    def get_absolute_url(self):
        return reverse('card_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_at']
