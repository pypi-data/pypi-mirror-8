#-*- coding: utf-8 -*-

from django import forms
from coop_cms.apps.rss_sync import models, widgets
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

#These 2 admin forms makes possible to add custom widgets for the id field

class RssSourceAdminForm(forms.ModelForm):
    url = forms.CharField(widget=widgets.AdminCollectRssWidget)
    class Meta:
        model = models.RssSource
        
    class Media:
        css = {
            'all': (settings.STATIC_URL+'css/rss_sync/admin-cust.css',),
        }
        
        
class RssItemAdminForm(forms.ModelForm):
    id = forms.IntegerField(widget=widgets.AdminCreateArticleWidget, label=u'Id')
    class Meta:
        model = models.RssItem
