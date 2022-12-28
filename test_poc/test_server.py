import pytest

from Python_Testing.poc import create_app
import Python_Testing.poc.server as server

COMPETITION_PATH = "./test_competitions.json"
CLUB_PATH = "./test_clubs.json"


@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    return app


@pytest.fixture
def client(app):
    return app.test_client()


# maybe we won't use the below function
@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def competitions(client):
    competitions = server.load_competitions(COMPETITION_PATH)
    return competitions


@pytest.fixture
def clubs(client):
    clubs = server.load_clubs(CLUB_PATH)
    return clubs


def test_index_prompts_email(app):
    with app.test_request_context("/"):
        template = server.index(CLUB_PATH)
        assert '<input type="email" name="email" id="email"' in template


def test_show_summary_invalid_value(app):
    with app.test_request_context("/show_summary", data={"email": "doesnotexist@gmail.com"}):
        with pytest.raises(ValueError) as excinfo:
            template = server.show_summary(COMPETITION_PATH, CLUB_PATH)
        assert "there is no item matching the value you entered" in str(excinfo.value)


def test_show_summary_invalid_key(app):
    # should raise an Error because there's a typo in email.
    with app.test_request_context("/show_summary", data={"emaile": "admin@irontemple.com"}):
        with pytest.raises(KeyError) as excinfo:
            template = server.show_summary(COMPETITION_PATH, CLUB_PATH)
        assert "400 Bad Request" in str(excinfo.value)


def test_show_summary_show_points_all_clubs(app):
    with app.test_request_context("/show_summary", data={"email": "admin@irontemple.com"}):
        template = server.show_summary(COMPETITION_PATH, CLUB_PATH)
        assert "Simply Lift: 13" in template
        assert "Iron Temple: 2" in template
        assert "She Lifts: 12" in template


def test_book_show_correct_data(app):
    with app.test_request_context("/book"):
        template = server.book(
            "Spring Festival",
            "Simply Lift",
            COMPETITION_PATH, CLUB_PATH
        )
    assert "Booking for Spring Festival" in template
    assert "Places available: 25" in template


def test_book_enable_booking(app):
    with app.test_request_context("/book"):
        template = server.book(
            "Spring Festival",
            "Simply Lift",
            COMPETITION_PATH, CLUB_PATH
        )
    assert '<button type="submit">' in template
    assert '<input type="number"' in template


def test_purchase_places_invalid_competition_name(app):
    with app.test_request_context(
            "/purchase_places",
            method="POST",
            data={"competition": "non existent competition",
                  "club": "Simply Lift",
                  "places": 0}
    ):
        with pytest.raises(ValueError) as excinfo:
            template = server.purchase_places(COMPETITION_PATH, CLUB_PATH)
        assert "there is no item matching the value you entered" in str(excinfo.value)


def test_purchase_places_invalid_club_name(app):
    with app.test_request_context(
            "/purchase_places",
            method="POST",
            data={"competition": "Spring Festival",
                  "club": "non existent club",
                  "places": 0}
    ):
        with pytest.raises(ValueError) as excinfo:
            template = server.purchase_places(COMPETITION_PATH, CLUB_PATH)
        assert "there is no item matching the value you entered" in str(excinfo.value)


def test_purchase_places_club_correct_point_deduction(app, competitions, clubs):
    spring_festival = competitions[0]
    simply_lift = clubs[0]

    assert spring_festival["number_of_places"] == 25
    assert simply_lift["points"] == 13

    with app.test_request_context(
            "/purchase_places",
            method="POST",
            data={"competition": "Spring Festival",
                  "club": "Simply Lift",
                  "places": 12}
    ):
        server.purchase_places(COMPETITION_PATH, CLUB_PATH)


#    assert "Points available" in template
