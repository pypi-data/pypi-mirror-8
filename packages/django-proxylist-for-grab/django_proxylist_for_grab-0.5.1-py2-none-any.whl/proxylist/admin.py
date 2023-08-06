# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib import admin
from django.http import Http404
from django import VERSION

if VERSION < (1, 5):
    from django.conf.urls.defaults import patterns, url
else:
    from django.conf.urls import patterns, url

from proxylist.models import Proxy, Mirror, ProxyCheckResult, Upload, ProxyList
from proxylist import defaults
try:
    from proxylist import tasks
except ImportError:
    pass


class ProxyAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'port', 'elapsed_time', 'country',
                    'anonymity_level', 'proxy_type', 'created',
                    'last_check', 'errors',)
    list_filter = ('anonymity_level', 'proxy_type', 'country',)
    search_fields = ('=hostname', '=port', 'country',)
    list_per_page = 25

    def changelist_view(self, request, extra_context=None):
        if defaults.PROXY_LIST_USE_CELERY:
            self.change_list_template = 'proxylist/admin/change_list_link.html'
            btn = defaults.ADMIN_BUTTONS
            cnx = dict(zip(btn, btn))
            if extra_context:
                extra_context.update(cnx)
            else:
                extra_context = cnx
        return super(ProxyAdmin, self).changelist_view(
            request, extra_context=extra_context)

    def _proxies_view(self, request, title, task):
        if Mirror.objects.all().count():
            task.delay()
            message = str(
                'Your request was added to queue. Click Back button in '
                'your browser and periodically refresh the page.'
            )
        else:
            message = 'No mirrors found. At first you should add it.'
        return render(
            request, 'proxylist/admin/proxylist.html', {
                'app_label': self.model._meta.app_label,
                'title': title,
                'message': message
            }
        )

    def clean_proxies(self, request):
        if 'Clean' not in defaults.ADMIN_BUTTONS:
            raise Http404
        return self._proxies_view(request, 'Clean proxies', tasks.CleanProxies)

    def check_proxies(self, request):
        if 'Check' not in defaults.ADMIN_BUTTONS:
            raise Http404
        return self._proxies_view(request, 'Check proxies', tasks.CheckProxies)

    def grab_proxies(self, request):
        if 'Grab' not in defaults.ADMIN_BUTTONS:
            raise Http404
        return self._proxies_view(request, 'Grab proxies', tasks.GrabProxies)

    def get_urls(self):
        urls = super(ProxyAdmin, self).get_urls()

        admin_urls = patterns(
            '',
            url(
                r'^clean_proxies/$',
                self.admin_site.admin_view(self.clean_proxies),
                name='admin_do_clean_proxies'
            ),
            url(
                r'^check_proxies/$',
                self.admin_site.admin_view(self.check_proxies),
                name='admin_do_check_proxies'
            ),
            url(
                r'^grab_proxies/$',
                self.admin_site.admin_view(self.grab_proxies),
                name='admin_do_grab_proxies'
            ),
        )
        return admin_urls + urls


class ProxyCheckResultAdmin(admin.ModelAdmin):
    list_filter = ('forwarded', 'mirror',)
    search_fields = ('=hostname', '=port', 'country',)
    list_display = (
        'proxy', 'forwarded', 'ip_reveal', 'hostname', 'real_ip_address',
        'check_start', 'check_end', 'response_start', 'response_end',
        'mirror', 'id',)
    list_per_page = 25
    ordering = ('-id',)

    def has_add_permission(self, request, obj=None):
        return False

    def __init__(self, model, admin_site):
        admin.ModelAdmin.__init__(self, model, admin_site)
        self.readonly_fields = [field.name for field in model._meta.fields]
        self.readonly_model = model


class MirrorAdmin(admin.ModelAdmin):
    list_display = ('url', 'output_type', 'id',)
    list_filter = ('output_type',)
    search_fields = ('url',)
    list_per_page = 25


class UploadAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'proxy_type', 'created', 'id',)
    list_filter = ('created', 'proxy_type')
    search_fields = ('file_name',)
    list_per_page = 25


class ProxyListAdmin(admin.ModelAdmin):
    list_display = ('url', 'update_period', 'next_check', 'created')


admin.site.register(ProxyList, ProxyListAdmin)
admin.site.register(Upload, UploadAdmin)
admin.site.register(Mirror, MirrorAdmin)
admin.site.register(Proxy, ProxyAdmin)

if defaults.PROXY_CHECK_RESULTS:
    admin.site.register(ProxyCheckResult, ProxyCheckResultAdmin)
