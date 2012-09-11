from __future__ import absolute_import

from django.core.urlresolvers import reverse
from django.template import Library
from django.utils.translation import ugettext as _

from haystack.forms import SearchForm

from ..models import RecentSearch
from ..conf.settings import RECENT_COUNT

register = Library()


@register.inclusion_tag('search_results_subtemplate.html', takes_context=True)
def search_form(context):
    context.update({
        'form': SearchForm(initial={'q': context.get('query_string', {}).get('q'), 'source': 'sidebar'}),
        'request': context['request'],
        'STATIC_URL': context['STATIC_URL'],
        'form_action': reverse('search'),
        'form_title': _(u'Search'),
        'submit_label': _(u'Search'),
        'submit_icon_famfam': 'zoom',
    })
    return ''


@register.inclusion_tag('generic_subtemplate.html', takes_context=True)
def recent_searches_template(context):
    recent_searches = RecentSearch.objects.get_for_user(user=context['user'])
    context.update({
        'request': context['request'],
        'STATIC_URL': context['STATIC_URL'],
        'side_bar': True,
        'title': _(u'recent searches (maximum of %d)') % RECENT_COUNT,
        'paragraphs': [
            u'<a href="%(url)s"><span class="famfam active famfam-%(icon)s"></span>%(text)s</a>' % {
                'text': recent_search,
                'url': recent_search.get_absolute_url(),
                'icon': 'zoom_in' if recent_search.is_advanced() else 'zoom',
            } for recent_search in recent_searches
        ]
    })
    return context