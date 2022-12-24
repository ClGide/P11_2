import pytest

from Python_Testing.poc import create_app
from Python_Testing.poc.server import show_summary, book, purchase_places, load_clubs, load_competitions


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
    competitions = load_competitions(COMPETITION_PATH)
    return competitions


@pytest.fixture
def clubs(client):
    clubs = load_clubs(CLUB_PATH)
    return clubs


def test_show_summary_show_points(app, client):
    with app.test_request_context("/show_summary", data={"email": "gide@gmail.com"}):
        template = show_summary(COMPETITION_PATH, CLUB_PATH)
    assert 'Points available' in template


def test_book(app, client):
    with app.test_request_context("/book"):
        template = book(
            club="club",
            competition="competition",
            competition_path=COMPETITION_PATH,
            club_path=CLUB_PATH
        )
    assert "Date" in template
    assert "Number of Places" in template


def test_purchase_places(app, client):
    with app.test_request_context("/purchase_places",
                                  method="POST"):
        template = purchase_places(COMPETITION_PATH, CLUB_PATH)
    assert "Points available" in template


# Is the below thing a functional test ?
def test_index(client):
    response = client.get("/")
    assert b'<input type="email" name="email" id=""/>' in response.data

