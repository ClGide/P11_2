"""
Whenever we refer to clubs or competitions, we refer to dictionary
holding (possibly modified by user interaction) data about the clubs
or competitions from the JSON files. The keys of those dictionaries are
always strings while the values can be strings, integers, booleans and
even dictionaries.
"""


from flask import render_template, request, redirect, flash, url_for, Blueprint
# without the ., the below import statement won't work. Remember, the app is created in
# __init__.py.
from .utils import (load_clubs, search_club,
                    load_competitions, search_competition,
                    run_checks, update_all_competitions_taken_place_field,
                    record_changes)

COMPETITION_PATH = "competitions.json"
CLUB_PATH = "clubs.json"


bp = Blueprint('gudlft', __name__)


@bp.route('/')
def index(club_path=CLUB_PATH):
    clubs = load_clubs(club_path)
    return render_template('index.html',
                           clubs=clubs)


@bp.route("/back_to_summary/<email>")
def come_back_welcome_page(email,
                           competition_path=COMPETITION_PATH,
                           club_path=CLUB_PATH):
    """
    Loads the available competitions in welcome.html and the data about the
    club that used booking.html.
    """
    competitions = load_competitions(competition_path)
    club, clubs = search_club("email", email, club_path)
    return render_template('welcome.html',
                           club=club,
                           competitions=competitions)


@bp.route('/show_summary', methods=['POST'])
def show_summary(competition_path=COMPETITION_PATH, club_path=CLUB_PATH):
    """
    Loads the available competitions in welcome.html and the data about the
    club that just logged in through index.html. It handles the form in index.html.
    """
    club, clubs = search_club("email", request.form['email'], club_path)
    competitions = load_competitions(competition_path)
    if club:
        competitions = update_all_competitions_taken_place_field(
            competitions, competition_path
        )
        return render_template('welcome.html',
                               club=club,
                               clubs=clubs,
                               competitions=competitions)

    flash("we couldn't find your email in our database.")
    return render_template("index.html")


@bp.route(
    '/book/<competition_to_be_booked_name>/<club_making_reservation_name>'
)
def book(competition_to_be_booked_name,
         club_making_reservation_name,
         competition_path=COMPETITION_PATH, club_path=CLUB_PATH):
    """
    Shows the user for which competitions he can book places.

    A str repr of a dict and not a dict is sent through url_for (in welcome.html).
    In other words, the value passed to competition_to_be_booked_name isn't a dict
    but a str repr of a dict.
    """
    competition, competitions = search_competition(
        "name",
        competition_to_be_booked_name,
        competition_path
    )
    club, clubs = search_club("name", club_making_reservation_name, club_path)
    return render_template('booking.html',
                           club=club,
                           competition=competition)


@bp.route('/purchase_places', methods=['POST'])
def purchase_places(competition_path=COMPETITION_PATH, club_path=CLUB_PATH):
    """Handles the form in booking.html."""

    competition_to_be_booked_name = request.form['competition']
    competition, competitions = search_competition(
        "name",
        competition_to_be_booked_name,
        competition_path
    )
    club, clubs = search_club("name", request.form["club"], club_path)
    places_required = int(request.form['places'])

    failed_checks = run_checks(competition, club, places_required)
    if failed_checks:
        return failed_checks

    competitions, club = record_changes(competitions, competition, clubs, club,
                                        places_required,
                                        competition_path, club_path)
    flash('Great-booking complete!')
    return render_template('welcome.html',
                           club=club,
                           clubs=clubs,
                           competitions=competitions)


@bp.route("/points")
def points(club_path=CLUB_PATH):
    clubs_to_display = load_clubs(club_path)
    return render_template("points.html",
                           clubs=clubs_to_display)


@bp.route('/logout')
def logout():
    return redirect(url_for('gudlft.index'))
