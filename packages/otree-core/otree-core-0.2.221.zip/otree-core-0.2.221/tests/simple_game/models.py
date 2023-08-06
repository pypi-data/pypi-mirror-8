# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Currency, currency_range
import random
# </standard imports>

class Constants:
    name_in_url = 'simple_game'
    players_per_group = 1
    number_of_rounds = 1



author = 'Your name here'

doc = """
Description of this app.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'simple_game'


class Group(otree.models.BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 1

    def set_payoffs(self):
        for p in self.get_players():
            p.payoff = 0 # change to whatever the payoff should be


class Player(otree.models.BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>

    def other_player(self):
        """Returns other player in group. Only valid for 2-player groups."""
        return self.get_others_in_group()[0]

    # example field
    my_field = models.CurrencyField(
        doc="""
        Description of this field, for documentation
        """
    )

    add100_1 = models.PositiveIntegerField()
    add100_2 = models.PositiveIntegerField()


    def my_field_error_message(self, value):
        if not 0 <= value <= 10:
            return 'Value is not in allowed range'


    def role(self):
        # you can make this depend of self.id_in_group
        return ''
