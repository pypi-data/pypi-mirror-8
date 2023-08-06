from otree.db import models
import otree.session.models
from save_the_change.mixins import SaveTheChange
from django_extensions.db.fields.json import JSONField
from otree.common_internal import get_models_module

class BaseGroup(SaveTheChange, models.Model):
    """
    Base class for all Groupes.
    """

    def __unicode__(self):
        return str(self.pk)

    def get_player_by_id(self, id_in_group):
        for p in self.get_players():
            if p.id_in_group == id_in_group:
                return p

    def get_player_by_role(self, role):
        for p in self.get_players():
            if p.role() == role:
                return p

    @classmethod
    def _create(cls, subsession):
        group = cls(
            subsession = subsession,
            session = subsession.session
        )
        # need to save it before you assign the player.group ForeignKey
        group.save()
        return group

    @property
    def _Constants(self):
        return get_models_module(self._meta.app_label).Constants


    class Meta:
        abstract = True