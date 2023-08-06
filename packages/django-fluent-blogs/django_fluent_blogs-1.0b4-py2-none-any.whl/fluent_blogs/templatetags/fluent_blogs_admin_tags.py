from django.core.urlresolvers import reverse
from django.template import Library
from fluent_blogs.admin import EntryAdmin
from fluent_blogs.models import get_entry_model

register = Library()

@register.simple_tag()
def status_column(entry):
    return EntryAdmin.get_status_column(entry)


@register.simple_tag()
def actions_column(entry):
    return EntryAdmin.get_actions_column(entry)


@register.simple_tag()
def blog_entry_admin_change_url(entry):
    model = get_entry_model()
    return reverse('admin:{0}_{1}_change'.format(model._meta.app_label, model._meta.module_name), args=(entry.pk,))
