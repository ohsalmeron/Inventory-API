from locust import HttpUser, task, between

class InventoryAPILoadTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def list_products(self):
        # Test the /api/products/ endpoint
        response = self.client.get("/api/products/")
        if response.status_code == 200:
            print("Success:", response.json())
        else:
            print("Failed:", response.status_code, response.text)

