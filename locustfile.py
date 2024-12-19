from locust import HttpUser, task, between

class InventoryAPILoadTest(HttpUser):
    wait_time = between(1, 3)  # Shorter wait times for more aggressive testing

    @task(2)  # Weight of 2
    def list_products(self):
        self.client.get("/api/products/")

    @task(1)  # Weight of 1
    def create_product(self):
        payload = {
            "name": "New Product",
            "description": "A test product",
            "category": "Test",
            "price": 200.0,
            "sku": "TEST200"
        }
        self.client.post("/api/products/", json=payload)
