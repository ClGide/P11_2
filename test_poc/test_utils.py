"""Tests all functions written in poc/utils.py.

test_competition.json will have to be rewritten on
the 2023-03-27 10:00:00 so that tests depending on that value
stay relevant. E.g. test_competition_took_place supposes that
the competition Spring Festival is in the future. But that will
stop being the case on 2023-03-27."""

import json

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
    """Supplies an Application object."""
    app = create_app({"TESTING": True})
    return app


def test_load_clubs_good_keys(clubs):
    """Given the path to test_clubs.json, should return the well formatted
    data. That means that for any of the club, the following keys should be
    present: 'name', 'email', 'points' and 'reserved_places'."""
    assert "name" in clubs[0].keys()
    assert "email" in clubs[0].keys()
    assert "points" in clubs[0].keys()
    assert "reserved_places" in clubs[0].keys()


def test_load_clubs_values_good_type(clubs):
    """Given the path to test_clubs.json, should return the well formatted
    data. That means that the keys 'name' and 'email' should be strings, 'points'
    should be integer and 'reserved_places' should be a dictionary. ."""
    assert isinstance(clubs[0]["name"], str)
    assert isinstance(clubs[0]["email"], str)
    assert isinstance(clubs[0]["points"], int)
    assert isinstance(clubs[0]["reserved_places"], dict)


def test_load_competitions_good_keys(competitions):
    """Given the path to test_competitions.json, should return the well formatted
    data. That means that for any of the competitions, the following keys should be
    present: 'name', 'date', 'number_of_places'."""
    assert "name" in competitions[0].keys()
    assert "date" in competitions[0].keys()
    assert "number_of_places" in competitions[0].keys()


def test_load_competitions_values_good_type(competitions):
    """Given the path to test_competitions.json, should return the well formatted
    data. That means that the key 'name' should be a string, 'date'
    should be a string and 'number_of_places' should be an integer."""
    assert isinstance(competitions[0]["name"], str)
    assert isinstance(competitions[0]["date"], str)
    assert isinstance(competitions[0]["number_of_places"], int)


def test_search_club_by_name_returned_value_correct():
    """Given a key to search for (name), a value for that key (Simply Lift)
    and a path to test_clubs.json; should return the data about the sought club."""
    club, clubs = search_club("name", "Simply Lift", CLUB_PATH)
    assert club["name"] == "Simply Lift"
    assert club["email"] == "john@simplylift.co"


def test_search_club_by_email_returned_value_correct():
    """Given a key to search for (email), a value for that key (john@simplylift.co)
    and a path to test_clubs.json; should return the data about the sought club."""
    club, clubs = search_club("email", "john@simplylift.co", CLUB_PATH)
    assert club["name"] == "Simply Lift"
    assert club["email"] == "john@simplylift.co"


def test_search_club_returned_correct_format():
    """Given a key to search for (email), a value for that key (john@simplylift.co)
    and a path to test_clubs.json; should return correctly formatted data about
    the sought club."""
    club, clubs = search_club("email", "john@simplylift.co", CLUB_PATH)
    assert isinstance(clubs, list)
    assert isinstance(clubs[0], dict)
    assert len(clubs[0].keys()) == 4


def test_search_club_raise_error_wrong_field():
    """Given a non-existent key to search for, a value for that key (john@simplylift.co)
    and a path to test_clubs.json; should raise a KeyError."""
    with pytest.raises(KeyError) as excinfo:
        search_club("wrong_field", "john@simplylift.co", CLUB_PATH)
    assert "the field you used is not valid" in str(excinfo.value)


def test_search_club_wrong_value():
    """Given a key to search for (name), a non-existent value for that key
    and a path to test_clubs.json; should raise a ValueError."""
    with pytest.raises(ValueError) as excinfo:
        search_club("name", "wrong_value", CLUB_PATH)
    assert "there is no item matching the value you entered" in str(excinfo.value)


def test_search_competition_by_name_returned_value_correct():
    """Given a key to search for (name), a value for that key (Spring Festival) and a
     path to test_competitions.json; should return the data about the sought competition."""
    competition, competitions = search_competition("name",
                                                   "Spring Festival",
                                                   COMPETITION_PATH)
    assert competition["name"] == "Spring Festival"
    assert competition["date"] == "2023-03-27 10:00:00"


def test_search_competition_by_date_returned_value_correct():
    """Given a key to search for (date), a value for that key (2023-03-27 10:00:00)
    and a path to test_competitions.json; should return the data about the sought competition."""
    competition, competitions = search_competition("date",
                                                   "2023-03-27 10:00:00",
                                                   COMPETITION_PATH)
    assert competition["name"] == "Spring Festival"
    assert competition["date"] == "2023-03-27 10:00:00"


def test_search_competition_returned_correct_format():
    """Given a key to search for (name), a value for that key (Spring Festival)
    and a path to test_competitions.json; should return correctly formatted data about
    the sought competition."""
    competition, competitions = search_competition("name",
                                                   "Spring Festival",
                                                   COMPETITION_PATH)
    assert type(competitions) == list
    assert type(competitions[0]) == dict
    assert len(competitions[0].keys()) == 4


def test_search_competition_raise_error_wrong_field():
    """Given a non-existent key to search for, a value for that key (Spring Festival)
    and a path to test_competitions.json; should raise a KeyError."""
    with pytest.raises(KeyError) as excinfo:
        search_competition("wrong_field", "Spring Festival", COMPETITION_PATH)
    assert "the field you used is not valid" in str(excinfo.value)


def test_search_competition_wrong_value():
    """Given a key to search for (name), a non-existent value for that key
    and a path to test_competitions.json; should raise a ValueError."""
    with pytest.raises(ValueError) as excinfo:
        search_competition("name", "wrong_value", COMPETITION_PATH)
    assert "there is no item matching the value you entered" in str(excinfo.value)


@pytest.fixture
def tmp_competitions_path(tmp_path):
    """Supplies a temporary file for tests to write data to.

    Some functions tested below are designed to write to a file containing
    data on competitions. The goal is to allow multiple iteration of the same
    test to produce the same result. Thus, those tests read data from
    test_competitions.json but write to a temporary file."""
    directory = tmp_path / "competitions"
    directory.mkdir()
    path = directory / "competitions.json"
    yield path


@pytest.fixture
def tmp_clubs_path(tmp_path):
    """Supplies a temporary file for tests to write data to.

    Some functions tested below are designed to write to a file containing
    data on clubs. The goal is to allow multiple iteration of the same
    test to produce the same result. Thus, those tests read data from
    test_clubs.json but write to a temporary file."""
    directory = tmp_path / "clubs"
    directory.mkdir()
    path = directory / "clubs.json"
    yield path


def test_update_all_competitions_taken_place_field(competitions, tmp_competitions_path):
    """Given a competition whose 'date' key is in the past, the 'taken_place' key should
    be set to True."""

    spring_festival = competitions[0]
    fall_classic = competitions[1]
    assert spring_festival["taken_place"] is False
    assert fall_classic["taken_place"] is False
    update_all_competitions_taken_place_field(competitions, tmp_competitions_path)
    assert spring_festival["taken_place"] is False
    assert fall_classic["taken_place"] is True


test_values_more_than_12_places_reserved = [
    (10, 2, None),
    (11, 4, "failed_check"),
    (0, 11, None),
    (9, 1, None),
]


@pytest.mark.parametrize("club_reserved_places, required_places, expected",
                         test_values_more_than_12_places_reserved)
def test_more_than_12_reserved_places(app, club_reserved_places,
                                      required_places, expected):
    """The function should return the str 'failed_check' if the sum
     of already reserved places and required places is superior to 12."""
    with app.test_request_context("/",
                                  method="GET"):
        assert more_than_12_reserved_places(
            club_reserved_places, required_places
        ) == expected


test_values_not_enough_points = [
    (10, 2, "failed_check"),
    (10, 10, None),
    (22, 32, None),
]


@pytest.mark.parametrize("required_places, club_number_of_points, expected",
                         test_values_not_enough_points)
def test_not_enough_points(app, required_places,
                           club_number_of_points, expected):
    """The function should return the str 'failed_check' if the club tries to purchase
    more places than it has points."""
    with app.test_request_context("/",
                                  method="GET"):
        assert not_enough_points(required_places, club_number_of_points) == expected


test_values_no_more_available_places = [
    (10, 2, None),
    (10, 10, None),
    (22, 32, "failed_check"),
]


@pytest.mark.parametrize("required_places, places_available, expected",
                         test_values_no_more_available_places)
def test_no_more_available_places(app, required_places,
                                  places_available, expected):
    """The function should return the str 'failed_check' if the club
    tries to purchase places at a competition where there are no more available places."""
    with app.test_request_context("/",
                                  method="GET"):
        assert no_more_available_places(required_places, places_available) == expected


def test_competition_took_place(app, competitions):
    """The function should return the str 'failed_check' if the club
    tries to purchase places at a competition that already took place."""
    with app.test_request_context("/",
                                  method="GET"):
        assert competition_took_place(competitions[0]) is None
        assert competition_took_place(competitions[2]) == "failed_check"


COMPETITIONS = load_competitions(COMPETITION_PATH)
CLUBS = load_clubs(CLUB_PATH)

spring_festival = COMPETITIONS[0]
summer_plates = COMPETITIONS[2]
simply_lift = CLUBS[0]
iron_temple = CLUBS[1]
test_values_run_check = [
    # should fail because the club requires more than 12 places.
    (spring_festival, simply_lift, 13, "you required more than 12 places !"),
    # should fail because the club only have 2 points.
    (spring_festival, iron_temple, 3, "you do not have enough points!"),
    # should fail because there are only 2 places available at the competition.
    (summer_plates, simply_lift, 3, "there are no more places available !"),
    # should fail because the competition already took place
    (summer_plates, iron_temple, 1, "the competition already took place !"),
]


@pytest.mark.parametrize("competition, club, required_places, expected",
                         test_values_run_check)
def test_run_checks_failing(app, competition, club,
                            required_places, expected):
    """run_checks simply calls the above four tested functions. If one of them returns
     the str 'failed_check', run_checks should return it as well."""
    with app.test_request_context("/", method="GET"):
        assert expected in run_checks(competition, club, required_places)


def test_run_checks_passing(app):
    """run_checks simply calls the above four tested functions. If one of them returns
    the str 'failed_check', run_checks should return it as well. Otherwise, should return None."""
    # should pass because all conditions are met.
    with app.test_request_context("/", method="GET"):
        assert run_checks(spring_festival, iron_temple, 1) is None


def test_record_changes_club_correct_deduction(app,
                                               competitions, clubs,
                                               tmp_competitions_path, tmp_clubs_path):
    """Given correctly formatted data on all competitions and clubs, on the club that
    purchased the places and the competition to which it purchased them, the paths to the
    JSON files holding the data on the clubs and the competitions, should correctly update
    the data on the relevant club.
    """
    with app.test_request_context("/", method="POST"):
        assert clubs[0]["points"] == 13
        assert clubs[0]["reserved_places"]["Spring Festival"] == 6

        updated_competitions, updated_club = record_changes(
            competitions, competitions[0], clubs, clubs[0],
            10, tmp_competitions_path, tmp_clubs_path
        )

        # The club is simply_lift. Before their purchase, they had 13 points. They should now
        # have 3 points.
        assert updated_club["points"] == 3
        # The club had already purchased 6 places at this competition. Therefore, the total
        # number of purchased places should be 16. This doesn't respect the maximum of 12
        # places per club per competition constraint. But it's normal because the constraint
        # checks are done in run_checks. Thus, record_changes shouldn't be called if
        # run_checks wasn't called before to check the validity of the operation.
        assert updated_club["reserved_places"]["Spring Festival"] == 16

        # The data written to the file should be updated in the same way.
        with open(tmp_clubs_path, "r", encoding="utf-8") as to_be_updated_clubs:
            updated_clubs_in_file = json.load(to_be_updated_clubs)

        assert updated_clubs_in_file["clubs"][0]["points"] == 3
        assert updated_clubs_in_file["clubs"][0]["reserved_places"]["Spring Festival"] == 16


def test_record_changes_competition_correct_deduction(app,
                                                      competitions, clubs,
                                                      tmp_competitions_path, tmp_clubs_path):
    """Given correctly formatted data on all competitions and clubs, on the club that
    purchased the places and the competition to which it purchased them, the paths to the
    JSON files holding the data on the clubs and the competitions, should correctly update
    the data on the relevant competition.
    """
    with app.test_request_context("/", method="POST"):
        assert competitions[0]["number_of_places"] == 25

        updated_competitions, updated_club = record_changes(
            competitions, competitions[0], clubs, clubs[0],
            10, tmp_competitions_path, tmp_clubs_path
        )
        # The competition is spring_festival. Before the purchase, they had 25 places
        # available. Thus, after the purchase they should only have 15 places available.
        assert updated_competitions[0]["number_of_places"] == 15

        # The data written to the file should be updated in the same way.
        with open(tmp_competitions_path, "r", encoding="utf-8") as to_be_updated_competitions:
            updated_competitions_in_file = json.load(to_be_updated_competitions)

        assert updated_competitions_in_file["competitions"][0]["number_of_places"] == 15
