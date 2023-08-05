from otree.views.abstract import (
    NonSequenceUrlMixin,
    OTreeMixin,
    PlayerUpdateView,
    LoadClassesAndUserMixin,
    load_session_user,
    AssignVisitorToOpenSession,
    WaitPageMixin,
    PlayerSequenceMixin,
    SequenceMixin,
    PlayerMixin

)

from datetime import datetime
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
import vanilla
from django.utils.translation import ugettext as _
import otree.constants as constants
import otree.sessionlib.models
from otree.sessionlib.models import Participant
import otree.common
import django.utils.timezone
import threading

class RedirectToPageUserShouldBeOn(NonSequenceUrlMixin,
                                   LoadClassesAndUserMixin,
                                   OTreeMixin,
                                   vanilla.View):
    name_in_url = 'shared'

    def get(self, request, *args, **kwargs):
        return self._redirect_to_page_the_user_should_be_on()

    @load_session_user
    def dispatch(self, request, *args, **kwargs):
        return super(RedirectToPageUserShouldBeOn, self).dispatch(request, *args, **kwargs)

class OutOfRangeNotification(NonSequenceUrlMixin, OTreeMixin, vanilla.View):
    name_in_url = 'shared'

    def dispatch(self, request, *args, **kwargs):
        user_type = kwargs.pop(constants.user_type)
        if user_type == constants.user_type_experimenter:
            return render_to_response('otree/OutOfRangeNotificationExperimenter.html')
        else:
            return render_to_response('otree/OutOfRangeNotification.html')

class WaitUntilAssignedToMatch(PlayerSequenceMixin, PlayerMixin, WaitPageMixin, vanilla.View):
    """
    this is visited after Initialize, to make sure the player has a match and treatment.
    the player can be assigned at any time, but this is a safeguard,
    and therefore should be at the beginning of each subsession.
    Should it instead be called after InitializeParticipant?
    Someday, we might want to shuffle players dynamically,
    e.g. based on the results of the past game.
    """
    name_in_url = 'shared'

    def _is_complete(self):
        return self.match and self.treatment

    def body_text(self):
        return 'Waiting until other participants and/or the experimenter are ready.'

    def _redirect_after_complete(self):
        self.update_indexes_in_sequences()
        return self._redirect_to_page_the_user_should_be_on()

    def get_debug_values(self):
        pass


class SessionExperimenterWaitUntilPlayersAreAssigned(NonSequenceUrlMixin, WaitPageMixin, vanilla.View):

    def title_text(self):
        return 'Please wait'

    def body_text(self):
        return 'Assigning players to matches.'

    def _is_complete(self):
        return self.session._players_assigned_to_matches or self.session.type().assign_to_matches_on_the_fly

    @classmethod
    def get_name_in_url(cls):
        return 'shared'

    def dispatch(self, request, *args, **kwargs):
        session_user_code = kwargs[constants.session_user_code]
        self.request.session[session_user_code] = {}

        self._session_user = get_object_or_404(
            otree.sessionlib.models.SessionExperimenter,
            code=kwargs[constants.session_user_code]
        )

        self.session = self._session_user.session

        if self.request_is_from_wait_page():
            return self._response_to_wait_page()
        else:
            # if the player shouldn't see this view, skip to the next
            if self._is_complete():
                return HttpResponseRedirect(self._session_user.me_in_first_subsession._start_url())
            return self.get_wait_page()


class InitializeSessionExperimenter(vanilla.View):


    @classmethod
    def url_pattern(cls):
        return r'^InitializeSessionExperimenter/(?P<{}>[a-z]+)/$'.format(constants.session_user_code)

    def redirect_to_next_page(self):
        return HttpResponseRedirect(SessionExperimenterWaitUntilPlayersAreAssigned.url(self._session_user))

    def get(self, *args, **kwargs):

        self._session_user = get_object_or_404(
            otree.sessionlib.models.SessionExperimenter,
            code=kwargs[constants.session_user_code]
        )

        session = self._session_user.session
        if session._players_assigned_to_matches or session.type().assign_to_matches_on_the_fly:
            return self.redirect_to_next_page()
        return render_to_response('otree/experimenter/StartSession.html', {})

    def post(self, request, *args, **kwargs):
        self._session_user = get_object_or_404(
            otree.sessionlib.models.SessionExperimenter,
            code=kwargs[constants.session_user_code]
        )

        session = self._session_user.session

        if not session.time_started:
            # get timestamp when the experimenter starts, rather than when the session was created
            # (since code is often updated after session created)
            session.git_commit_timestamp = otree.common.git_commit_timestamp()
            session.time_started = django.utils.timezone.now()
            session.save()

        t = threading.Thread(target=session._assign_players_to_matches)
        t.start()
        return self.redirect_to_next_page()

class InitializeParticipantMagdeburg(vanilla.View):
    """since magdeburg doesn't let you pass distinct URLs to each PC, but you can pass different params"""

    @classmethod
    def url_pattern(cls):
        return r'^InitializeParticipantMagdeburg/$'

    def get(self, *args, **kwargs):
        session_user_code = self.request.GET[constants.session_user_code]
        session_user = get_object_or_404(otree.sessionlib.models.Participant, code=session_user_code)

        return HttpResponseRedirect(session_user._start_url())

class InitializeParticipant(vanilla.UpdateView):

    @classmethod
    def url_pattern(cls):
        return r'^InitializeParticipant/(?P<{}>[a-z]+)/$'.format(constants.session_user_code)

    def get(self, *args, **kwargs):

        session_user = get_object_or_404(
            otree.sessionlib.models.Participant,
            code=kwargs[constants.session_user_code]
        )

        session = session_user.session
        if session.type().assign_to_matches_on_the_fly:
            session_user._assign_to_matches()
            # assign to matches on the fly

        session_user.visited = True
        session_user.time_started = django.utils.timezone.now()
        session_user.label = self.request.GET.get(constants.participant_label)

        if session_user.ip_address == None:
            session_user.ip_address = self.request.META['REMOTE_ADDR']

        now = django.utils.timezone.now()
        session_user.time_started = now
        session_user._last_page_timestamp = now
        session_user.save()

        return HttpResponseRedirect(session_user.me_in_first_subsession._start_url())

#TODO: surface these URLs in the UI somewhere
class AssignVisitorToOpenSessionMTurk(AssignVisitorToOpenSession):

    @classmethod
    def url(cls):
        return otree.common.add_params_to_url(
            '/{}'.format(cls.__name__),
            {
                otree.constants.access_code_for_open_session: otree.common.access_code_for_open_session()
            }
        )

    @classmethod
    def url_pattern(cls):
        return r'^{}/$'.format(cls.__name__)

    required_params = {
        'mturk_worker_id': otree.constants.mturk_worker_id,
        'mturk_assignment_id': otree.constants.mturk_assignment_id,
    }

    def url_has_correct_parameters(self):
        return (
            super(AssignVisitorToOpenSessionMTurk, self).url_has_correct_parameters()
            and self.request.GET[constants.mturk_assignment_id] != 'ASSIGNMENT_ID_NOT_AVAILABLE'
        )


class AssignVisitorToOpenSessionLab(AssignVisitorToOpenSession):

    def incorrect_parameters_in_url_message(self):
        'Missing parameter(s) in URL: {}'.format(self.required_params.values())

    @classmethod
    def url(cls):
        return otree.common.add_params_to_url(
            '/{}'.format(cls.__name__),
            {
                otree.constants.access_code_for_open_session: otree.common.access_code_for_open_session()
            }
        )

    @classmethod
    def url_pattern(cls):
        return r'^{}/$'.format(cls.__name__)

    required_params = {
        'label': otree.constants.participant_label,
    }