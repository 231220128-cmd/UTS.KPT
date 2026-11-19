from locust import HttpUser, task, between

class BookStoreUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(3)
    def read_books(self):
        self.client.get("/books/", name="GET /books")

    @task(1)
    def create_transaction(self):
        # Sesuaikan book_id dengan ID buku yang tersedia dan stoknya cukup.
        self.client.post(
            "/transactions/",
            json={"book_id": 1, "quantity": 1},
            name="POST /transactions",
        )
