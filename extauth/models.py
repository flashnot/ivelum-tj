import re

from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from task.models import Worker


class ExtendedUserManager(BaseUserManager):
    """
    Manager for extended user model
    """
    def create_user(self, username, password=None):
        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class ExtendedUser(AbstractBaseUser):
    """
    Extend standart auth model with worker field
    """
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), 'Enter a valid username.', 'invalid')
        ]
    )
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    worker = models.ManyToManyField(Worker, blank=True, related_name='users');

    objects = ExtendedUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.username