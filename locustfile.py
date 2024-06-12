import random
import secrets

from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def post_dog(self):
        response = self.client.post("/dogs", json={
            "name": secrets.token_hex(20),
            "breed": f"Mixed {secrets.token_hex(20)}",
            "age": random.randint(1, 20)
        })

        self.response_data = response.json()
        id = self.response_data['id']

        self.client.get("/dogs", params={"id": id}, name="/dogs?id=[id]")
