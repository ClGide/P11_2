from locust import HttpUser, task


class gudlftUser(HttpUser):
    @task
    def test_index(self):
        self.client.get("/")



