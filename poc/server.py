import json

from flask import render_template, request, redirect, flash, url_for, Blueprint


def load_clubs(path):
    with open(path) as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions(path):
    with open(path) as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


bp = Blueprint('server', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


COMPETITION_PATH = "competitions.json"
CLUB_PATH = "clubs.json"


@bp.route('/showSummary', methods=['POST'])
def show_summary(competition_path, club_path):
    clubs = load_clubs(club_path)
    competitions = load_competitions(competition_path)
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html', club=club, competitions=competitions)


@bp.route('/book/<competition>/<club>')
def book(competition, club, competition_path, club_path):
    clubs = load_clubs(club_path)
    competitions = load_competitions(competition_path)
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@bp.route('/purchase_places', methods=['POST'])
def purchase_places(competition_path, club_path):
    competitions = load_competitions(competition_path)
    clubs = load_clubs(club_path)
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-places_required
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@bp.route('/logout')
def logout():
    return redirect(url_for('index'))
