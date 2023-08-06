# -*- coding: utf-8 -*-
from otree.session import SessionType


def session_types():
    return [
        SessionType(
            name="simple_game",
            display_name="Simple Game",
            fixed_pay=0,
            num_demo_participants=1,
            num_bots=1,
            subsession_apps=['tests.simple_game'],
            doc=""""""
        ),
    ]


def show_on_demo_page(session_type_name):
    return True


demo_page_intro_text = """
<ul>
    <li><a href="https://github.com/oTree-org/otree" target="_blank">Source code</a> for the below games.</li>
    <li><a href="http://www.otree.org/" target="_blank">oTree homepage</a>.</li>
</ul>
<p>
Below are various games implemented with oTree. These games are all open source,
and you can modify them as you wish to create your own variations. Click one to learn more and play.
</p>
"""
