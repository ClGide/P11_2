from Python_Testing.test_poc.decorators import rewrite_file_after_test
from Python_Testing.poc.utils import record_changes, load_clubs, load_competitions


competitions = load_competitions("./test_competitions.json")
clubs = load_clubs("./test_clubs.json")
spring_festival = competitions[0]
simply_lift = clubs[0]


def call_record_changes(*args, **kwargs):
    record_changes(*args, **kwargs)


call_record_changes(competitions, spring_festival, clubs, simply_lift,
                    10, "./test_competitions.json", "./test_clubs.json")




