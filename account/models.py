from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.models import BaseModel


class HumanResources(AbstractUser):
    username_validator = ASCIIUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=128,
        unique=True,
        help_text=_('Required. 128 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=128)
    last_name = models.CharField(_('last name'), max_length=128)

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'user'


class Skill(models.Model):
    title = models.CharField(max_length=64, verbose_name=_('name'), unique=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('skill')
        verbose_name_plural = _('skills')
        db_table = 'skill'


class Project(models.Model):
    title = models.CharField(max_length=64, verbose_name=_('name'), unique=True)
    link = models.URLField(verbose_name=_('link'), default='')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')
        db_table = 'project'


class JobSeeker(BaseModel):
    first_name = models.CharField(_('first name'), max_length=128)
    last_name = models.CharField(_('last name'), max_length=128)
    email = models.EmailField(_('email address'), unique=True)
    phone_regex = RegexValidator(regex=r'^(\+98|0)?9\d{9}$',
                                 message="Phone number must be entered in the format: '+989123456789/09123456789'.")
    phone_number = models.CharField(verbose_name=_('phone number'), validators=[phone_regex], max_length=13, blank=True)
    skills = models.ManyToManyField(Skill, verbose_name=_('skill'))
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=_('project'))

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
