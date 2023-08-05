import hashlib
import os
import urllib
import urlparse
from decimal import Decimal
from os.path import dirname, join

import babel.numbers
from django import forms
from django.conf import settings
from django.template.defaultfilters import title
from django.utils.importlib import import_module
from easymoney import Money

from otree import constants


# R: Should not be needed
class _MoneyInput(forms.NumberInput):
     def _format_value(self, value):
         return str(Decimal(value))


def add_params_to_url(url, params):
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(url_parts)

def id_label_name(id, label):
    if label:
        return '{} (label: {})'.format(id, label)
    return '{}'.format(id)

def is_subsession_app(app_label):
    try:
        models_module = import_module('{}.models'.format(app_label))
    except ImportError:
        return False
    class_names = ['Player', 'Group', 'Subsession']
    return all(hasattr(models_module, ClassName) for ClassName in class_names)

def git_commit_timestamp():
    root_dir = dirname(settings.BASE_DIR)
    try:
        with open(join(root_dir, 'git_commit_timestamp'), 'r') as f:
            return f.read().strip()
    except IOError:
        return ''

def app_name_format(app_name):
    return title(app_name.replace("_", " "))

def url(cls, session_user, index=None):
    u = '/{}/{}/{}/{}/'.format(
        session_user.user_type_in_url,
        session_user.code,
        cls.get_name_in_url(),
        cls.__name__,
    )

    if index is not None:
        u += '{}/'.format(index)
    return u

def url_pattern(cls, is_sequence_url=False):
    p = r'(?P<{}>\w)/(?P<{}>[a-z]+)/{}/{}/'.format(
        constants.user_type,
        constants.session_user_code,
        cls.get_name_in_url(),
        cls.__name__,
    )
    if is_sequence_url:
        p += r'(?P<{}>\d+)/'.format(constants.index_in_pages,)
    p = r'^{}$'.format(p)
    return p

def directory_name(path):
    return os.path.basename(os.path.normpath(path))

def get_session_module():
    base_dir_name = directory_name(settings.BASE_DIR)
    module_name = getattr(settings, 'SESSION_MODULE',
                          '{}.session'.format(base_dir_name))
    return import_module(module_name)

def get_models_module(app_name):
    return import_module('{}.models'.format(app_name))

def flatten(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]

def _views_module(model_instance):
    return import_module('{}.views'.format(model_instance._meta.app_label))

def _players(self):
    if hasattr(self, '_players'):
        return self._players
    self._players = list(self.player_set.order_by('id_in_group'))
    return self._players

def _groups(self):
    if hasattr(self, '_groups'):
        return self._groups
    self._groups = list(self.group_set.all())
    return self._groups

def money_range(first, last, increment=Money(0.01)):
    assert last >= first
    assert increment >= 0
    values = []
    current_value = Money(first)
    while True:
        if current_value > last:
            return values
        values.append(current_value)
        current_value += increment

def expand_choice_tuples(choices):
    '''allows the programmer to define choices as a list of values rather than (value, display_value)'''
    if not choices:
        return
    # look at the first element
    first_choice = choices[0]
    if not isinstance(first_choice, (list, tuple)):
        choices = [(value, value) for value in choices]
    return choices

