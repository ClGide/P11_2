from locust import HttpUser, task


class gudlftUser(HttpUser):
    @task
    def index(self):
        self.client.get("/")

    @task
    def welcome_page(self):
        self.client.get("/back_to_summary", {"email": "john@simplylift.co"})

    @task(5)
    # the 5 above means this method 5 times more prone to be called than the others.
    # the on_start below means that this method is always going to be called before the other.
    def show_summary(self):
        self.client.post("/show_summary", {"email": "john@simplylift.co"})

    @task(5)
    def book(self):
        self.client.get("/book", {
            "competition_to_be_booked_name": "Fall Classic",
            "club_making_reservation_name": "admin@irontemple.com"
        })

    @task(5)
    def purchase_places(self):
        self.client.post("/purchase_places", {
            "competition": "Fall Classic",
            "club": "She Lifts",
            "places": 10
        })

    @task
    def points(self):
        self.client.get("/points")
