import pytest
from meetliveinfo.client import HTTPClient
from meetliveinfo.models.agegroup import AgeGroupsResponse
from meetliveinfo.models.athlete import Athlete
from meetliveinfo.models.club import Club
from meetliveinfo.models.enums import Round
from meetliveinfo.models.events import EventsResponse
from meetliveinfo.models.globals import GlobalsResponse
from meetliveinfo.models.results import ResultsResponse


@pytest.fixture(scope="module")
def client():
    return HTTPClient(base_url="http://localhost:3001", language="us")


def test_get_agegroups(client: HTTPClient):
    agegroups = client.get_agegroups()
    assert isinstance(agegroups, AgeGroupsResponse)
    assert hasattr(agegroups, "agegroups")
    assert isinstance(agegroups.agegroups, (list, dict))


def test_get_athletes(client: HTTPClient):
    athletes = client.get_athletes()
    assert isinstance(athletes, list)
    if athletes:
        assert isinstance(athletes[0], Athlete)


def test_get_clubs(client: HTTPClient):
    clubs = client.get_clubs()
    assert isinstance(clubs, list)
    if clubs:
        assert isinstance(clubs[0], Club)


def test_get_events(client: HTTPClient):
    events = client.get_events()
    assert isinstance(events, EventsResponse)
    assert hasattr(events, "events")


def test_get_globals(client: HTTPClient):
    globals_info = client.get_globals()
    assert isinstance(globals_info, GlobalsResponse)
    assert hasattr(globals_info, "sessions")


def test_get_results_for_first_event(client: HTTPClient):
    events = client.get_events()
    for ev in events.events:
        if ev.round in (Round.BREAK, Round.MEDAL_CEREMONY):
            continue
        results = client.get_results_for_event(ev.number)
        assert isinstance(results, ResultsResponse)
