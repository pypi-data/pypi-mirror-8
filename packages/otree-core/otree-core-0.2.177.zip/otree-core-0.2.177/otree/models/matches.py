from otree.db import models
import otree.sessionlib.models
from save_the_change.mixins import SaveTheChange
from otree.common import ModelWithCheckpointMixin
from django_extensions.db.fields.json import JSONField

class BaseMatch(SaveTheChange, ModelWithCheckpointMixin, models.Model):
    """
    Base class for all Matches.
    """

    _incomplete_checkpoints = JSONField()

    def __unicode__(self):
        return str(self.pk)

    def _is_ready_for_next_player(self):
        return len(self.player_set.all()) < self.players_per_match

    def get_player_by_index(self, index):
        for p in self.players:
            if p.index_among_players_in_match == index:
                return p

    def get_player_by_role(self, role):
        for p in self.players:
            if p.role() == role:
                return p

    def _CheckpointMixinClass(self):
        from otree.views.abstract import MatchCheckpointMixin
        return MatchCheckpointMixin

    @classmethod
    def _create(cls, treatment):
        match = cls(
            treatment = treatment,
            subsession = treatment.subsession,
            session = treatment.session
        )
        # need to save it before you assign the player.match ForeignKey
        match.save()
        return match

    class Meta:
        abstract = True