import allure
import pytest


@allure.feature("Students")
@allure.story("GET")
class TestGetStudents:
    @allure.title("Получить список всех студентов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_students_list(self, api_client):
        with allure.step("Отправить GET /student"):
            response = api_client.get_all_students()

        with allure.step("Проверить код ответа 200"):
            assert response.status_code == 200

        with allure.step("Проверить структуру JSON"):
            body = response.json()
            assert body.get("status") == 1
            assert "students" in body
            assert isinstance(body["students"], list)

    @allure.title("Получить студента по существующему ID")
    def test_get_student_by_id(self, api_client, created_student):
        student_id, payload, _ = created_student

        with allure.step("GET /student/{id}"):
            response = api_client.get_student_by_id(student_id)

        with allure.step("Проверки"):
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == 1
            st = data["student"]
            assert st["id"] == student_id
            assert st["email"] == payload["email"]

    @allure.title("Запрос несуществующего студента")
    def test_get_student_not_found(self, api_client):
        fake_id = 99999999

        with allure.step("GET с большим id"):
            response = api_client.get_student_by_id(fake_id)

        with allure.step("Ожидаем status=0 в теле"):
            assert response.status_code == 200
            assert response.json()["status"] == 0
            assert "not found" in response.json()["message"].lower()

    @allure.title("Некорректный student_id в path")
    @pytest.mark.xfail(reason="сейчас 404 html вместо json — см BUG-003")
    def test_get_student_invalid_id_format(self, api_client):
        with allure.step("GET /student/abc"):
            response = api_client.get_student_by_id("abc")

        with allure.step("Должен быть json с ошибкой"):
            assert response.status_code == 200
            assert response.headers.get("content-type", "").startswith("application/json")
