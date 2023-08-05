
from otree.db import models
from ast import literal_eval

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class AuxiliaryModel(models.Model):
    player_content_type = models.ForeignKey(ContentType,
                                                 editable=False,
                                                 related_name = '%(app_label)s_%(class)s_player')
    player_object_id = models.PositiveIntegerField(editable=False)
    player = generic.GenericForeignKey('player_content_type',
                                            'player_object_id',
                                            )

    match_content_type = models.ForeignKey(ContentType,
                                           editable=False,
                                           related_name = '%(app_label)s_%(class)s_match')
    match_object_id = models.PositiveIntegerField(editable=False)
    match = generic.GenericForeignKey('match_content_type',
                                      'match_object_id',
                                      )

    class Meta:
        abstract = True


