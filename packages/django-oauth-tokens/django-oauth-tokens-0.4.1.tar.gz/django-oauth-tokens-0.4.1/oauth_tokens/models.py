# -*- coding: utf-8 -*-
from datetime import datetime
import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models, transaction
from django.utils.importlib import import_module
from taggit.managers import TaggableManager
from tyoi.oauth2 import AccessTokenResponseError

from .exceptions import AccountLocked, LoginPasswordError


log = logging.getLogger('oauth_tokens')

HISTORY = getattr(settings, 'OAUTH_TOKENS_HISTORY', False)
PROVIDERS = [
    'vkontakte',
    'facebook',
    'twitter',
    'odnoklassniki',
]
PROVIDER_CHOICES = [((provider, provider.title())) for provider in PROVIDERS]
ACCESS_TOKENS_CLASSES = getattr(settings, 'OAUTH_TOKENS_CLASSES',
                                dict([(p, 'oauth_tokens.providers.%s.%sAccessToken' % (p, p.title()))
                                      for p in PROVIDERS])
                                )


class AccessTokenGettingError(Exception):
    pass


class AccessTokenRefreshingError(Exception):
    pass


class AccessTokenManager(models.Manager):

    '''
    Defautl manager for AccessToken for retrieving token
    '''

    def filter(self, *args, **kwargs):
        '''
        Optional filter by user's `tag`
        '''
        tag = kwargs.pop('tag', None)
        if tag:
            kwargs['user__in'] = UserCredentials.objects.filter(tags__name__in=[tag]).values_list('pk', flat=True)

        return super(AccessTokenManager, self).filter(*args, **kwargs)

    def filter_active_tokens_of_provider(self, provider, *args, **kwargs):
        return self.filter(provider=provider, expires__gt=datetime.now(), *args, **kwargs).order_by('?')

    def get_token(self, provider, tag=None):
        '''
        Returns access token instance. If tag argument provided or
        settings OAUTH_TOKENS_%s_USERNAME is not defined look up for credentials in DB
        '''
        token_class = self.get_token_class(provider)

        if tag is None and getattr(settings, 'OAUTH_TOKENS_%s_USERNAME' % provider.upper(), None):
            return token_class()

        qs_users = UserCredentials.objects.filter(provider=provider)
        if tag:
            qs_users = qs_users.filter(tags__name__in=[tag])

        try:
            user = qs_users[0]
        except IndexError:
            raise Exception("User with tag %s for provider %s does not exist" % (tag, provider))

        return self.get_token_by_user(token_class, user)

    def get_token_by_user(self, token_class, user):
        return token_class(username=user.username, password=user.password, additional=user.additional)

    def get_token_class(self, provider):

        if provider not in PROVIDERS:
            raise ValueError("Provider `%s` not in available providers list" % provider)

        try:
            path = ACCESS_TOKENS_CLASSES[provider].split('.')
            module = '.'.join(path[:-1])
            class_name = path[-1]
            token_class = getattr(import_module(module), path[-1])
        except ImportError:
            raise ImproperlyConfigured("Impossible to find access token class with path %s" %
                                       ACCESS_TOKENS_CLASSES[provider])

        return token_class

    def refresh(self, provider):
        '''
        Refresh tokens and save as new save it to database
        '''
        tokens = AccessToken.objects.filter(provider=provider).order_by('-id')

        access_tokens = []
        # TODO: remove limit for queryset, but handle behaviour with old accesstokens
        for token in tokens[:1]:
            token_class = self.get_token_class(provider)

            try:
                new_token = token_class().refresh(token)
            except AccessTokenResponseError:
                return self.fetch(provider)

            access_token = self.model(provider=provider, user=token.user)
            access_token.__dict__.update(new_token.__dict__)
            access_token.refresh_token = token.refresh_token
            access_token.save()
            access_tokens += [access_token]

        if len(access_tokens) == 0:
            raise AccessTokenRefreshingError("No tokens refreshed for provider %s" % provider)

        return access_tokens

    @transaction.commit_on_success
    def fetch(self, provider):
        '''
        Get new token and save it to database for all users in UserCredentials table.
        Сlean database before if OAUTH_TOKENS_HISTORY disabled
        '''
        token_class = self.get_token_class(provider)

        # walk through all users of current provider in UserCredentials table
        # or try to get user credentials from settings
        users = UserCredentials.objects.filter(provider=provider, active=True)
        if users.count() == 0:
            users = [None]

        access_tokens = []

        for user in users:

            try:
                token = self.get_token_by_user(token_class, user).get()
            except AccountLocked, e:
                log.error(u"Error '%s' while getting new token for provider %s and user %s" % (e, provider, user))
                continue
            except LoginPasswordError, e:
                log.error(u"Error '%s' while getting new token for provider %s and user %s" % (e, provider, user))
                user.active = False
                user.save()
                continue

            if not HISTORY:
                self.filter(provider=provider, user=user).delete()

            access_token = self.model(provider=provider, user=user)
            access_token.__dict__.update(token.__dict__)
            access_token.save()
            access_tokens += [access_token]

        if len(access_tokens) == 0:
            raise AccessTokenGettingError("No tokens for provider %s" % provider)

        return access_tokens


class AccessToken(models.Model):

    class Meta:
        verbose_name = 'Oauth access token'
        verbose_name_plural = 'Oauth access tokens'
        ordering = ('-granted',)
        get_latest_by = 'granted'

    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, db_index=True)
    granted = models.DateTimeField(auto_now=True)

    access_token = models.CharField(max_length=500)
    expires = models.DateTimeField(null=True, blank=True, db_index=True)
    token_type = models.CharField(max_length=200, null=True, blank=True)
    refresh_token = models.CharField(max_length=200, null=True, blank=True)
    scope = models.CharField(max_length=200, null=True, blank=True)

    user = models.ForeignKey('UserCredentials', null=True, blank=True)

    objects = AccessTokenManager()

    def __str__(self):
        return '#%s' % self.access_token


class UserCredentials(models.Model):

    name = models.CharField(max_length=100)
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    active = models.BooleanField()

    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    additional = models.CharField(max_length=100, blank=True)

    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.name
