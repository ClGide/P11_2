import json
import decorator

from Python_Testing.poc.utils import load_clubs, load_competitions


def rewrite_file_after_test(func):
    """Saves the content of test_clubs.json and test_competitions.json before
     the test call. After the test call, writes the content back to the file.
    The idea is that multiple test calls writing to those files behaves in the
    same way.

    I use the decorator package to preserve the decorated function signature.
    If the function signature is overwritten by the decorator (as is the case
    without the decorator package), pytest will throw an error. Also, the func is
    passed to the wrapper, which is unusual. But it's necessary for the decorator
    function to work properly."""
    def wrapper(func, *args, **kwargs):
        club_path = "./test_clubs.json"
        competition_path = "./test_competitions.json"
        clubs = load_clubs(club_path)
        competitions = load_competitions(competition_path)

        func(*args, **kwargs)

        with open(club_path, "w") as clubs_json_file:
            json.dump({"clubs": clubs},
                      clubs_json_file,
                      indent=4)
        with open(competition_path, "w") as competitions_json_file:
            json.dump({"competitions": competitions},
                      competitions_json_file,
                      indent=4)
    return decorator.decorator(wrapper, func)

