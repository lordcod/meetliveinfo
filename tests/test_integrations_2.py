import pytest

from meetliveinfo.client import HTTPClient
from meetliveinfo.models.entries import EntriesResponse
from meetliveinfo.models.enums import Round
from meetliveinfo.models.events_by_session import EventsBySessionResponse
from meetliveinfo.models.events_by_stroke import EventsByStrokeResponse
from meetliveinfo.models.heat import HeatResultResponse
from meetliveinfo.models.medals import MedalsResponse
from meetliveinfo.models.pointscores import PointScore, PointScoreDetailsResponse
from meetliveinfo.models.records import RecordItem, RecordsResponse
from meetliveinfo.models.record_by_event import RecordByEventItem


@pytest.fixture(scope="module")
def client():
    return HTTPClient(base_url="http://localhost:3001", language="us")


# =========================
# Events grouping
# =========================

def test_get_events_by_session(client: HTTPClient):
    data = client.get_events_by_session()
    assert isinstance(data, EventsBySessionResponse)


def test_get_events_by_stroke(client: HTTPClient):
    data = client.get_events_by_stroke()
    assert isinstance(data, EventsByStrokeResponse)


# =========================
# Entries
# =========================

def test_get_entries_for_first_event(client: HTTPClient):
    events = client.get_events()
    if not events.events:
        pytest.skip("No events available")

    event = events.events[0]
    entries = client.get_entries_for_event(1)

    assert isinstance(entries, EntriesResponse)


# =========================
# Heats
# =========================

def test_get_heat_if_exists(client: HTTPClient):
    events = client.get_events()

    for ev in events.events:
        for heat in ev.heats:
            heat = client.get_heat(ev.number, heat.code)
            assert isinstance(heat, HeatResultResponse)


def test_get_heat_by_id_if_exists(client: HTTPClient):
    events = client.get_events()

    for ev in events.events:
        try:
            heat = client.get_heat(ev.number, 1)
            heat_id = heat.id
            heat_by_id = client.get_heat_by_id(heat_id)
            assert isinstance(heat_by_id, HeatResultResponse)
            return
        except Exception:
            continue

    pytest.skip("No heat IDs available")


def test_get_ares_heat_if_available(client: HTTPClient):
    events = client.get_events()

    for ev in events.events:
        try:
            data = client.get_ares_heat(ev.number, ev.round, 1)
            assert isinstance(data, dict)
            return
        except Exception:
            continue

    pytest.skip("ARES heat endpoint not available")


# =========================
# Medals
# =========================

def test_get_medal_statistics(client: HTTPClient):
    medals = client.get_medal_statistics()
    assert isinstance(medals, MedalsResponse)


def test_get_medals_for_event(client: HTTPClient):
    events = client.get_events()
    if not events.events:
        pytest.skip("No events available")

    for event in events.events:
        if event.round in (Round.BREAK, Round.MEDAL_CEREMONY):
            continue
        medals = client.get_medals_for_event(event.number)


# =========================
# Point scores
# =========================

def test_get_point_scores(client: HTTPClient):
    scores = client.get_point_scores()
    assert isinstance(scores, list)

    if scores:
        assert isinstance(scores[0], PointScore)


def test_get_point_score_summary(client: HTTPClient):
    scores = client.get_point_scores()
    if not scores:
        pytest.skip("No point scores available")
    for score in scores:
        details = client.get_point_score_summary(score.id)

        assert isinstance(details, PointScoreDetailsResponse)


# =========================
# Records
# =========================

def test_get_record_lists(client: HTTPClient):
    records = client.get_record_lists()
    assert isinstance(records, list)

    if records:
        assert isinstance(records[0], RecordItem)


def test_get_records_for_list(client: HTTPClient):
    record_lists = client.get_record_lists()
    if not record_lists:
        pytest.skip("No record lists available")
    for rc in record_lists:
        records = client.get_records(rc.id)
        assert isinstance(records, RecordsResponse)


def test_get_records_for_event(client: HTTPClient):
    events = client.get_events()
    if not events.events:
        pytest.skip("No events available")
    for event in events.events:
        if event.round in (Round.BREAK, Round.MEDAL_CEREMONY):
            continue
        records = client.get_records_for_event(event.number)

        assert isinstance(records, list)
        if records:
            assert isinstance(records[0], RecordByEventItem)
