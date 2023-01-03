"""Tests all functions written in poc/server.py."""


import pytest

from Python_Testing.poc import create_app
import Python_Testing.poc.server as server

COMPETITION_PATH = "./test_competitions.json"
CLUB_PATH = "./test_clubs.json"


@pytest.fixture
def app():
    """Supplies an Application object."""
    app = create_app({"TESTING": True})
    return app


@pytest.fixture
def competitions():
    """returns the content of test_poc/test_competitions.json"""
    competitions = server.load_competitions(COMPETITION_PATH)
    return competitions


@pytest.fixture
def clubs():
    """returns the content of test_poc/test_clubs.json"""
    clubs = server.load_clubs(CLUB_PATH)
    return clubs


def test_index_prompts_email(app):
    """Given the path to the JSON file holding data on the clubs, should return
    a str containing HTML code. The HTML code should contain a prompt for the email."""
    with app.test_request_context("/"):
        template = server.index(CLUB_PATH)
        assert '<input type="email" name="email" id="email"' in template


def test_come_back_welcome_page_correct_club(app):
    """
    Given the email of the user that was about to book some places,
    returns the HTML code for the welcome page. This code should contain
    data about the correct club.
    """
    email = "john@simplylift.co"
    with app.test_request_context("back_to_summary/"):
        template = server.come_back_welcome_page(email,
                                                 COMPETITION_PATH,
                                                 CLUB_PATH)
        assert "john@simplylift.co" in template
        assert "admin@irontemple.com" not in template
        assert "kate@shelifts.co.uk" not in template


def test_come_back_welcome_page_correct_competitions(app):
    """
    Given the email of the user that was about to book some places,
    returns the HTML code for the welcome page. This code should contain
    data about all the competitions.
    """
    email = "john@simplylift.co"
    with app.test_request_context("back_to_summary/"):
        template = server.come_back_welcome_page(email,
                                                 COMPETITION_PATH,
                                                 CLUB_PATH)
        assert "Spring Festival" in template
        assert "Fall Classic" in template
        assert "Summer plates" in template


def test_show_summary_invalid_value(app):
    """Given the path to the JSON files holding data on competitions and clubs, should raise a
    ValueError because the email passed by the user doesn't exist."""
    with app.test_request_context("/show_summary", data={"email": "doesnotexist@gmail.com"}):
        with pytest.raises(ValueError) as excinfo:
            server.show_summary(COMPETITION_PATH, CLUB_PATH)
        assert "there is no item matching the value you entered" in str(excinfo.value)


def test_show_summary_show_points_all_clubs(app):
    """Given the path to the JSON file holding data on competitions and clubs, should return
    a str containing HTML code. The HTML code should contain the right number of points for
    each club."""
    with app.test_request_context("/show_summary", data={"email": "admin@irontemple.com"}):
        template = server.show_summary(COMPETITION_PATH, CLUB_PATH)
    assert "Simply Lift: 13" in template
    assert "Iron Temple: 2" in template
    assert "She Lifts: 12" in template


def test_show_summary_invalid_key(app):
    """Given the path to the JSON files holding data on the clubs, should raise an KeyError
     because there's a typo in email."""
    with app.test_request_context("/show_summary", data={"emaile": "admin@irontemple.com"}):
        with pytest.raises(KeyError) as excinfo:
            server.show_summary(COMPETITION_PATH, CLUB_PATH)
        assert "400 Bad Request" in str(excinfo.value)


def test_book_show_correct_data(app):
    """Given the name of a competition, the name of a club and a path to the JSON files
     holding data on clubs and competitions, should display the correct amount of available
     points for the competition."""
    with app.test_request_context("/book"):
        template = server.book(
            "Spring Festival",
            "Simply Lift",
            COMPETITION_PATH, CLUB_PATH
        )
    assert "Places available: 25" in template


def test_purchase_places_invalid_competition_name(app):
    """Given the path to the JSON files holding data on clubs and competitions, should
     raise a ValueError because the competition given by the user doesn't exist."""
    with app.test_request_context(
            "/purchase_places",
            method="POST",
            data={"competition": "non existent competition",
                  "club": "Simply Lift",
                  "places": 0}
    ):
        with pytest.raises(ValueError) as excinfo:
            server.purchase_places(COMPETITION_PATH, CLUB_PATH)
        assert "there is no item matching the value you entered" in str(excinfo.value)


def test_purchase_places_invalid_club_name(app):
    """Given the path to the JSON files holding data on clubs and competitions, should
     raise a ValueError because the club given by the user doesn't exist."""
    with app.test_request_context(
            "/purchase_places",
            method="POST",
            data={"competition": "Spring Festival",
                  "club": "non existent club",
                  "places": 0}
    ):
        with pytest.raises(ValueError) as excinfo:
            server.purchase_places(COMPETITION_PATH, CLUB_PATH)
        assert "there is no item matching the value you entered" in str(excinfo.value)


def test_points_display_correct_number_of_points(app):
    """Given the path to the JSON file holding data on clubs, should return a str
     containing HTML code for a page displaying the number of points of each club."""
    with app.test_request_context("/points"):
        template = server.points(CLUB_PATH)
    assert "Simply Lift: 13" in template
    assert "Iron Temple: 2" in template
    assert "She Lifts: 12" in template
