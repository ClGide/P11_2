import pytest
from OCRProject11 import create_app
from OCRProject11.server import load_clubs, load_competitions
from OCRProject11.server import show_summary, book, purchase_places


COMPETITION_PATH = "../Tests_OCRProject11/test_competitions.json"
CLUB_PATH = "../Tests_OCRProject11/test_clubs.json"


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
    competitions = load_competitions("../OCRProject11/clubs.json")
    return competitions


@pytest.fixture
def clubs(client):
    clubs = load_clubs("../OCRProject11/competitions.json")
    return clubs


def test_load_clubs_good_format(client):
    clubs = load_clubs("../OCRProject11/clubs.json")
    assert "name" in clubs[0].keys()
    assert "email" in clubs[0].keys()
    assert "points" in clubs[0].keys()


def test_load_competitions_good_format(client):
    competitions = load_competitions("../OCRProject11/competitions.json")
    assert "name" in competitions[0].keys()
    assert "date" in competitions[0].keys()
    assert "number_of_places" in competitions[0].keys()


def test_show_summary_show_points(app, client):
    with app.test_request_context("/showSummary", data={"email": "gide@gmail.com"}):
        template = show_summary(COMPETITION_PATH, CLUB_PATH)
    print(type(template))
    print(template)
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


