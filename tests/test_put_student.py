import allure
import pytest


@allure.feature("Students")
@allure.story("PUT")
class TestPutStudent:
    @allure.title("Обновление данных студента")
    def test_update_student_ok(self, api_client, created_student):
        student_id, _, _ = created_student
        new_data = {
            "name": "Updated Name",
            "email": "updated_%s@test.local" % student_id,
            "gender": "female",
            "status": 0,
        }

        with allure.step("PUT /student/{id}"):
            response = api_client.update_student(student_id, new_data)

        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == 1
            assert data["student"]["name"] == new_data["name"]

        with allure.step("GET и сверка"):
            get_resp = api_client.get_student_by_id(student_id)
            st = get_resp.json()["student"]
            assert st["name"] == new_data["name"]
            assert st["status"] == 0

    @allure.title("Обновление несуществующего id")
    def test_update_not_found(self, api_client):
        body = {
            "name": "Nobody",
            "email": "nobody@test.local",
            "gender": "male",
            "status": 1,
        }

        with allure.step("PUT на несуществующий id"):
            response = api_client.update_student(987654321, body)

        assert response.json()["status"] == 0

    @allure.title("Неполное тело запроса")
    def test_update_incomplete_json(self, api_client, created_student):
        student_id, _, _ = created_student

        with allure.step("PUT только name"):
            response = api_client.update_student(student_id, {"name": "OnlyName"})

        assert response.json()["status"] == 0

    @allure.title("Тип поля status в ответе PUT при status=0")
    @pytest.mark.xfail(reason="BUG-002: status приходит строкой")
    def test_update_status_field_type(self, api_client, created_student):
        student_id, _, _ = created_student
        upd = {
            "name": "TypeCheck",
            "email": "typecheck_%s@test.local" % student_id,
            "gender": "male",
            "status": 0,
        }

        with allure.step("PUT status=0"):
            response = api_client.update_student(student_id, upd)

        st_status = response.json()["student"]["status"]
        with allure.step("status должен быть int"):
            assert isinstance(st_status, int)
