# -*- encoding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class ProxylistConfig(AppConfig):
    name = 'proxylist'
    verbose_name = _('Proxies')
