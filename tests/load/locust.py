import logging
import random
from uuid import uuid4

from locust import task, between
from locust.contrib.fasthttp import FastHttpUser

# Настройки тестирования
TEST_USERNAME = "test_user"
TEST_PASSWORD = "Test_password123!"
TEST_EMAIL = "test@example.com"
BASE_URL = "http://localhost:8000"  # или адрес вашего сервера


class QuickStartUser(FastHttpUser):
    wait_time = between(0.5, 2.5)

    def on_start(self):
        """Выполняется при старте каждого виртуального пользователя"""
        # Регистрируем нового пользователя
        username = f"{TEST_USERNAME}_{uuid4().hex[:8]}"
        email = f"{uuid4().hex[:8]}{TEST_EMAIL}"

        try:
            response = self.client.post(
                "/users/",
                json={
                    "username": username,
                    "email": email,
                    "password": TEST_PASSWORD,
                    "role": "USER"
                }
            )

            # Получаем токен для аутентификации
            auth_response = self.client.post(
                "/auth/token",
                data={
                    "username": username,
                    "password": TEST_PASSWORD
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            self.token = auth_response.json()["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}

        except Exception as e:
            logging.error(f"Failed to register/authenticate user: {e}")
            self.token = None
            self.headers = None

    @task(3)
    def health_check(self):
        """Тестируем простой эндпоинт без БД"""
        self.client.get("/health", headers=self.headers)

    @task(2)
    def get_current_user(self):
        """Тестируем эндпоинт с простым запросом к БД"""
        if self.token:
            self.client.get("/auth/me", headers=self.headers)

    @task(5)
    def tasks_workflow(self):
        """Полный цикл работы с задачами (CRUD)"""
        if not self.token:
            return

        # Создаем задачу
        task_title = f"Task {uuid4().hex[:6]}"
        create_response = self.client.post(
            "/tasks/",
            json={"title": task_title},
            headers=self.headers
        )

        if create_response.status_code == 201:
            task_id = create_response.json()["id"]

            # Получаем список задач
            self.client.get("/tasks/", headers=self.headers)

            # Получаем конкретную задачу
            self.client.get(f"/tasks/{task_id}", headers=self.headers)

            # Обновляем задачу
            self.client.patch(
                f"/tasks/{task_id}",
                json={"title": f"Updated {task_title}", "is_done": False},
                headers=self.headers
            )

            # Удаляем задачу (не всегда, чтобы имитировать разное поведение)
            if random.random() > 0.7:  # 30% chance to delete
                self.client.delete(f"/tasks/{task_id}", headers=self.headers)

    @task(1)
    def refresh_token(self):
        """Тестируем обновление токена"""
        if self.token:
            auth_response = self.client.post(
                "/auth/token",
                data={
                    "username": TEST_USERNAME,
                    "password": TEST_PASSWORD
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            self.token = auth_response.json()["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
