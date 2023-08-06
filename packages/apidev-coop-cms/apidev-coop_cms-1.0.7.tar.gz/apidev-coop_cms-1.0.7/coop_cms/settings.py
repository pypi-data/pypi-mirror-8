# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from django.conf import settings as django_settings
from django.utils.importlib import import_module
import logging
logger = logging.getLogger("coop_cms")

COOP_CMS_NAVTREE_CLASS = 'coop_cms.NavTree'
DEPRECATED_COOP_CMS_NAVTREE_CLASS = getattr(django_settings, 'COOP_CMS_NAVTREE_CLASS', 'basic_cms.NavTree')

def get_navigable_content_types():
    ct_choices = []
    try:
        content_apps = django_settings.COOP_CMS_CONTENT_APPS
    except AttributeError:
        content_apps = []
        not_to_be_mapped = ('south', 'django_extensions', 'd2rq')
        for m in django_settings.INSTALLED_APPS:
            if(not m.startswith('django.') and m not in not_to_be_mapped):
                content_apps.append(m)
    apps_labels = [app.rsplit('.')[-1] for app in content_apps]
    navigable_content_types = ContentType.objects.filter(app_label__in=apps_labels).order_by('app_label')
    for ct in navigable_content_types:
        is_navnode = ((ct.model == 'navnode') and (ct.app_label == 'coop_cms'))
        if (not is_navnode) and 'get_absolute_url' in dir(ct.model_class()):
            ct_choices.append((ct.id, ct.app_label + u'.' + ct.model))
    return ct_choices

def get_navtree_class(defaut_class=None):
    if hasattr(get_navtree_class, '_cache_class'):
        return getattr(get_navtree_class, '_cache_class')
    else:
        full_class_name = COOP_CMS_NAVTREE_CLASS
        app_label, model_name = full_class_name.split('.')
        model_name = model_name.lower()
        ct = ContentType.objects.get(app_label=app_label, model=model_name)
        navtree_class = ct.model_class()
        setattr(get_navtree_class, '_cache_class', navtree_class)
        return navtree_class

def get_article_class():
    if hasattr(get_article_class, '_cache_class'):
        return getattr(get_article_class, '_cache_class')
    else:
        article_class = None
        full_class_name = getattr(django_settings, 'COOP_CMS_ARTICLE_CLASS', None)
        if not full_class_name and ('coop_cms.apps.basic_cms' in django_settings.INSTALLED_APPS):
            full_class_name = 'coop_cms.apps.basic_cms.models.Article'
        if full_class_name:
            module_name, class_name = full_class_name.rsplit('.', 1)
            module = import_module(module_name)
            article_class = getattr(module, class_name)
        else:
            raise Exception('No article class configured')

        setattr(get_article_class, '_cache_class', article_class)
        return article_class


def get_default_logo():
    return getattr(django_settings, 'COOP_CMS_DEFAULT_ARTICLE_LOGO', 'img/default-logo.png')

def get_article_form():
    try:
        full_class_name = getattr(django_settings, 'COOP_CMS_ARTICLE_FORM')
        module_name, class_name = full_class_name.rsplit('.', 1)
        module = import_module(module_name)
        article_form = getattr(module, class_name)

    except AttributeError:
        from coop_cms.forms import ArticleForm
        article_form = ArticleForm

    return article_form

def get_article_settings_form():
    try:
        full_class_name = getattr(django_settings, 'COOP_CMS_ARTICLE_SETTINGS_FORM')
        module_name, class_name = full_class_name.rsplit('.', 1)
        module = import_module(module_name)
        article_form = getattr(module, class_name)

    except AttributeError:
        from coop_cms.forms import ArticleSettingsForm
        article_form = ArticleSettingsForm

    return article_form

def get_new_article_form():
    try:
        full_class_name = getattr(django_settings, 'COOP_CMS_NEW_ARTICLE_FORM')
        module_name, class_name = full_class_name.rsplit('.', 1)
        module = import_module(module_name)
        article_form = getattr(module, class_name)

    except AttributeError:
        from coop_cms.forms import NewArticleForm
        article_form = NewArticleForm

    return article_form

def get_newsletter_templates(newsletter, user):
    try:
        return getattr(django_settings, 'COOP_CMS_NEWSLETTER_TEMPLATES')
    except AttributeError:
        return ()

def get_newsletter_form():
    try:
        full_class_name = getattr(django_settings, 'COOP_CMS_NEWSLETTER_FORM')
    except AttributeError:
        from coop_cms.forms import NewsletterForm
        newsletter_form = NewsletterForm
    else:
        module_name, class_name = full_class_name.rsplit('.', 1)
        module = import_module(module_name)
        newsletter_form = getattr(module, class_name)
    return newsletter_form

def get_article_templates(article, user):
    if hasattr(django_settings, 'COOP_CMS_ARTICLE_TEMPLATES'):
        coop_cms_article_templates = getattr(django_settings, 'COOP_CMS_ARTICLE_TEMPLATES')

        if type(coop_cms_article_templates) in (str, unicode):
            #COOP_CMS_ARTICLE_TEMPLATES is a string :
            # - a function name that will return a tuple
            # - a variable name taht contains a tuple

            #extract module and function/var names
            module_name, object_name = coop_cms_article_templates.rsplit('.', 1)
            module = import_module(module_name) #import module
            article_templates_object = getattr(module, object_name) #get the object
            if callable(article_templates_object):
                #function: call it
                article_templates = article_templates_object(article, user)
            else:
                #var: assign
                article_templates = article_templates_object
        else:
            #COOP_CMS_ARTICLE_TEMPLATES is directly a tuple, assign it
            article_templates = coop_cms_article_templates
    else:
        article_templates = None

    return article_templates

def _get_article_setting(article, setting_name, default_value):
    try:
        get_setting_name = getattr(django_settings, setting_name)
        try:
            module_name, fct_name = get_setting_name.rsplit('.', 1)
            module = import_module(module_name)
            get_setting = getattr(module, fct_name)
            if callable(get_setting):
                value = get_setting(article)
            else:
                value = get_setting
        except ValueError:
            value = get_setting_name

    except AttributeError:
        value = default_value
    return value

def get_article_logo_size(article):
    return _get_article_setting(article, 'COOP_CMS_ARTICLE_LOGO_SIZE', '48x48')

def get_article_logo_crop(article):
    return _get_article_setting(article, 'COOP_CMS_ARTICLE_LOGO_CROP', 'center')

def get_headline_image_size(article):
    return _get_article_setting(article, 'COOP_CMS_HEADLINE_IMAGE_SIZE', '900')

def get_headline_image_crop(article):
    return _get_article_setting(article, 'COOP_CMS_HEADLINE_IMAGE_CROP', None)

def get_max_image_width(image):
    return _get_article_setting(image, 'COOP_CMS_MAX_IMAGE_WIDTH', None)

def get_newsletter_item_classes():
    if hasattr(get_newsletter_item_classes, '_cache_class'):
        return getattr(get_newsletter_item_classes, '_cache_class')
    else:
        item_classes = []
        try:
            full_classes_names = getattr(django_settings, 'COOP_CMS_NEWSLETTER_ITEM_CLASSES')
        except AttributeError:
            item_classes = (get_article_class(),)
        else:
            item_classes = []
            for full_class_name in full_classes_names:
                module_name, class_name = full_class_name.rsplit('.', 1)
                module = import_module(module_name)
                item_classes.append(getattr(module, class_name))
            item_classes = tuple(item_classes)

        if not item_classes:
            raise Exception('No newsletter item classes configured')

        setattr(get_newsletter_item_classes, '_cache_class', item_classes)
        return item_classes
    
def get_newsletter_context_callbacks():
    if hasattr(get_newsletter_context_callbacks, '_cache_func'):
        return getattr(get_newsletter_context_callbacks, '_cache_func')
    else:
        try:
            callback_names = getattr(django_settings, 'COOP_CMS_NEWSLETTER_CONTEXT')
        except AttributeError:
            return ()
        else:
            callbacks = []
            for callback_name in callback_names:
                module_name, func_name = callback_name.rsplit('.', 1)
                module = import_module(module_name)
                callbacks.append(getattr(module, func_name))
            callbacks = tuple(callbacks)

        setattr(get_newsletter_context_callbacks, '_cache_func', callbacks)
        return callbacks

def is_localized():
    if ('localeurl' in django_settings.INSTALLED_APPS) and ('modeltranslation' in django_settings.INSTALLED_APPS):
        return True
    return False

def is_multilang():
    return len(django_settings.LANGUAGES)>1

def install_csrf_failure_view():
    dont_do_it = getattr(django_settings, 'COOP_CMS_DO_NOT_INSTALL_CSRF_FAILURE_VIEW', False)
    if not dont_do_it:
        setattr(django_settings, 'CSRF_FAILURE_VIEW', 'coop_cms.views.csrf_failure')

def cms_no_homepage():
    return getattr(django_settings, 'COOP_CMS_NO_HOMEPAGE', False)

def hide_media_library_menu():
    return getattr(django_settings, 'COOP_CMS_HIDE_MEDIA_LIBRARY_MENU', False)

def is_requestprovider_installed():
    is_installed = ('coop_cms.utils.RequestMiddleware' in django_settings.MIDDLEWARE_CLASSES)
    if not is_installed:
        logger.warn("You should add coop_cms.utils.RequestMiddleware to the MIDDLEWARE_CLASSES settings")
    return is_installed
    
def can_rewrite_url():
    return getattr(django_settings, 'COOP_CMS_CAN_EDIT_ARTICLE_SLUG', False)
    
def keep_deprecated_func_views_for_article():
    return getattr(django_settings, 'COOP_CMS_KEEP_DEPRECATED_ARTICLE_VIEWS', False)
    
def get_article_views():
    if keep_deprecated_func_views_for_article():
        raise Exception("coop_cms is configured with COOP_CMS_KEEP_DEPRECATED_ARTICLE_VIEWS=True")
    try:
        article_views = getattr(django_settings, 'COOP_CMS_ARTICLE_VIEWS')
    except AttributeError:
        from coop_cms.views import ArticleView, EditArticleView
        return {
            'article_view': ArticleView,
            'edit_article_view': EditArticleView,
        }
    else:
        expected_views = ('article_view', 'edit_article_view')
        imported_class_views = {}
        for view_name in expected_views:
            full_class_name = article_views[view_name]
            module_name, class_name = full_class_name.rsplit('.', 1)
            module = import_module(module_name)
            imported_class_views[view_name] = getattr(module, class_name)
        return imported_class_views
    return newsletter_form

def is_perm_middleware_installed():
    return 'coop_cms.middleware.PermissionsMiddleware' in django_settings.MIDDLEWARE_CLASSES
    
    if keep_deprecated_func_views_for_article():
        raise Exception("coop_cms is configured with COOP_CMS_KEEP_DEPRECATED_ARTICLE_VIEWS=True")
    try:
        article_views = getattr(django_settings, 'COOP_CMS_ARTICLE_VIEWS')
    except AttributeError:
        from coop_cms.views import ArticleView, EditArticleView
        return {
            'article_view': ArticleView,
            'edit_article_view': EditArticleView,
        }
    else:
        expected_views = ('article_view', 'edit_article_view')
        imported_class_views = {}
        for view_name in expected_views:
            full_class_name = article_views[view_name]
            module_name, class_name = full_class_name.rsplit('.', 1)
            module = import_module(module_name)
            imported_class_views[view_name] = getattr(module, class_name)
        return imported_class_views
    return newsletter_form

if is_localized():
    if django_settings.LANGUAGE_CODE[:2] != django_settings.LANGUAGES[0][0]:
        logger.warning(
            "coop_cms settings error: LANGUAGE_CODE ({0}) should be first in LANGUAGES (currently first is {1})".format(
                django_settings.LANGUAGE_CODE[:2], django_settings.LANGUAGES[0][0]
            )
        )