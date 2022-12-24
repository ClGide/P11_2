"""test_competition.json will have to be rewritten so that
on the 2023-03-27 10:00:00 so that tests depending on that value
stay relevant. E.g test_competition_took_place."""


import pytest

from Python_Testing.poc import create_app
from Python_Testing.poc.utils import (load_clubs, load_competitions,
                                      search_club, search_competition,
                                      update_all_competitions_taken_place_field,
                                      more_than_12_reserved_places,
                                      not_enough_points,
                                      no_more_available_places,
                                      competition_took_place,
                                      run_checks, record_changes)


COMPETITION_PATH = "./test_competitions.json"
CLUB_PATH = "./test_clubs.json"


@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def competitions():
    competitions = load_competitions(COMPETITION_PATH)
    return competitions


@pytest.fixture
def clubs():
    clubs = load_clubs(CLUB_PATH)
    return clubs


def test_load_clubs_good_keys(clubs):
    assert "name" in clubs[0].keys()
    assert "email" in clubs[0].keys()
    assert "points" in clubs[0].keys()
    assert "reserved_places" in clubs[0].keys()


def test_load_clubs_values_good_type(clubs):
    assert type(clubs[0]["name"]) == str
    assert type(clubs[0]["email"]) == str
    assert type(clubs[0]["points"]) == int
    assert type(clubs[0]["reserved_places"]) == dict


def test_load_competitions_good_keys(competitions):
    assert "name" in competitions[0].keys()
    assert "date" in competitions[0].keys()
    assert "number_of_places" in competitions[0].keys()


def test_load_competitions_values_good_type(competitions):
    assert type(competitions[0]["name"]) == str
    assert type(competitions[0]["date"]) == str
    assert type(competitions[0]["number_of_places"]) == int


def test_search_club_by_name_first_returned_value_correct():
    club, clubs = search_club("name", "Simply Lift", CLUB_PATH)
    assert club["name"] == "Simply Lift"
    assert club["email"] == "john@simplylift.co"


def test_search_club_by_email_first_returned_value_correct():
    club, clubs = search_club("email", "john@simplylift.co", CLUB_PATH)
    assert club["name"] == "Simply Lift"
    assert club["email"] == "john@simplylift.co"


def test_search_club_second_returned_value_correct():
    club, clubs = search_club("email", "john@simplylift.co", CLUB_PATH)
    assert type(clubs) == list
    assert type(clubs[0]) == dict
    assert len(clubs[0].keys()) == 4


def test_search_club_raise_error_wrong_field():
    with pytest.raises(ValueError) as excinfo:
        club, clubs = search_club("wrong_field", "john@simplylift.co", CLUB_PATH)

    assert "the value for the field arg isn't a valid one" in str(excinfo.value)


def test_search_club_wrong_value():
    club = search_club("name", "wrong_value", CLUB_PATH)
    assert club == []


def test_search_competition_by_name_first_returned_value_correct():
    competition, competitions = search_competition("name", "Spring Festival", COMPETITION_PATH)
    assert competition["name"] == "Spring Festival"
    assert competition["date"] == "2023-03-27 10:00:00"


def test_search_competition_by_date_first_returned_value_correct():
    competition, competitions = search_competition("date", "2023-03-27 10:00:00", COMPETITION_PATH)
    assert competition["name"] == "Spring Festival"
    assert competition["date"] == "2023-03-27 10:00:00"


def test_search_competition_second_returned_value_correct():
    competition, competitions = search_competition("name", "Spring Festival", COMPETITION_PATH)
    assert type(competitions) == list
    assert type(competitions[0]) == dict
    assert len(competitions[0].keys()) == 4


def test_search_competition_raise_error_wrong_field():
    with pytest.raises(ValueError) as excinfo:
        club, clubs = search_club("wrong_field", "Spring Festival", COMPETITION_PATH)

    assert "the value for the field arg isn't a valid one" in str(excinfo.value)


def test_search_competition_wrong_value():
    competition = search_competition("name", "wrong_value", COMPETITION_PATH)
    assert competition == []


@pytest.fixture
def tmp_competitions_path(tmp_path):
    d = tmp_path / "competitions"
    d.mkdir()
    p = d / "competitions.json"
    yield p


def test_update_all_competitions_taken_place_field(competitions, tmp_competitions_path):
    assert competitions[0]["taken_place"] is False
    assert competitions[1]["taken_place"] is False
    competitions = update_all_competitions_taken_place_field(competitions, tmp_competitions_path)
    assert competitions[0]["taken_place"] is False
    assert competitions[1]["taken_place"] is True


test_values = [
    (10, 2, None),
    (11, 4, "failed_check"),
    (0, 11, None),
    (9, 1, None),
]


@pytest.mark.parametrize("club_reserved_places, required_places, expected", test_values)
def test_more_than_12_reserved_places(app, club_reserved_places, required_places, expected):
    with app.test_request_context("/",
                                  method="GET"):
        assert more_than_12_reserved_places(club_reserved_places, required_places) == expected


test_values = [
    (10, 2, "failed_check"),
    (10, 10, None),
    (22, 32, None),
]


@pytest.mark.parametrize("required_places, club_number_of_points, expected", test_values)
def test_not_enough_points(app, required_places, club_number_of_points, expected):
    with app.test_request_context("/",
                                  method="GET"):
        assert not_enough_points(required_places, club_number_of_points) == expected


test_values = [
    (10, 2, "failed_check"),
    (10, 10, None),
    (22, 32, None),
]


@pytest.mark.parametrize("required_places, places_available, expected", test_values)
def test_no_more_available_places(app, required_places, places_available, expected):
    with app.test_request_context("/",
                                  method="GET"):
        assert not_enough_points(required_places, places_available,) == expected


def test_competition_took_place(app, competitions):
    with app.test_request_context("/",
                                  method="GET"):
        assert competition_took_place(competitions[0]) is None
        assert competition_took_place(competitions[2]) == "failed_check"


_competitions = competitions()
_clubs = clubs()

spring_festival = _competitions[0]
fall_classic = _competitions[1]
simply_lift = _clubs[0]
test_values = [
    # should fail because there are more than 12 places required
    (spring_festival, simply_lift, 13, 25, "failed_check"),
    (spring_festival, simply_lift, 14,  "failed_check"),
]


@pytest.mark.parametrize("competition, club, required_places, club_number_of_points, expected", test_values)
def test_run_checks(app, competition, club, required_places, club_number_of_points, expected):
    assert run_checks(competition, club, required_places, club_number_of_points) == expected
