import allure
import pytest

from tests.conftest import random_email, valid_student_payload


@allure.feature("Students")
@allure.story("POST")
class TestPostStudent:
    @allure.title("Успешное создание студента")
    def test_create_student_ok(self, api_client):
        payload = valid_student_payload()

        with allure.step("POST /student с валидным телом"):
            response = api_client.create_student(payload)

        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == 1
            assert data["message"] == "Student created successfully"
            student = data["student"]
            assert student["name"] == payload["name"]
            assert student["email"] == payload["email"]

        with allure.step("Удалить созданного студента"):
            sid = student["id"]
            del_resp = api_client.delete_student(sid)
            assert del_resp.json()["status"] == 1

    @allure.title("Создание с пустым JSON")
    def test_create_empty_body(self, api_client):
        with allure.step("POST {}"):
            response = api_client.create_student({})

        with allure.step("Ожидаем отказ"):
            assert response.status_code == 200
            assert response.json()["status"] == 0

    @allure.title("Неверный gender")
    def test_create_wrong_gender(self, api_client):
        payload = valid_student_payload()
        payload["gender"] = "other"

        with allure.step("POST с gender=other"):
            response = api_client.create_student(payload)

        assert response.json()["status"] == 0

    @allure.title("Неверный status")
    def test_create_wrong_status(self, api_client):
        payload = valid_student_payload()
        payload["status"] = 5

        with allure.step("POST status=5"):
            response = api_client.create_student(payload)

        body = response.json()
        assert body["status"] == 0
        assert "status" in body["message"].lower()

    @allure.title("Дубликат email — документируем поведение API")
    @pytest.mark.xfail(reason="BUG-001: дубликаты email разрешены")
    def test_duplicate_email_not_allowed(self, api_client):
        email = random_email()
        p1 = valid_student_payload(email=email)
        p2 = valid_student_payload(email=email)

        with allure.step("Первое создание"):
            r1 = api_client.create_student(p1)
            id1 = r1.json()["student"]["id"]

        with allure.step("Второе с тем же email"):
            r2 = api_client.create_student(p2)
            try:
                assert r2.json()["status"] == 0
            finally:
                api_client.delete_student(id1)
                if r2.json().get("status") == 1:
                    api_client.delete_student(r2.json()["student"]["id"])
