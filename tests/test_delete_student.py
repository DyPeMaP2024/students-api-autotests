import allure
import pytest

from tests.conftest import valid_student_payload


@allure.feature("Students")
@allure.story("DELETE")
class TestDeleteStudent:
    @allure.title("Удаление существующего студента")
    def test_delete_student_ok(self, api_client):
        payload = valid_student_payload()
        create_resp = api_client.create_student(payload)
        student_id = create_resp.json()["student"]["id"]

        with allure.step("DELETE /student/{id}"):
            response = api_client.delete_student(student_id)

        with allure.step("Проверки"):
            assert response.status_code == 200
            assert response.json()["status"] == 1

        with allure.step("GET после удаления"):
            get_resp = api_client.get_student_by_id(student_id)
            assert get_resp.json()["status"] == 0

    @allure.title("Повторное удаление того же id")
    @pytest.mark.xfail(reason="BUG-004: второй delete тоже success")
    def test_delete_already_deleted(self, api_client):
        payload = valid_student_payload()
        sid = api_client.create_student(payload).json()["student"]["id"]

        with allure.step("Первый DELETE"):
            r1 = api_client.delete_student(sid)
            assert r1.json()["status"] == 1

        with allure.step("Второй DELETE"):
            r2 = api_client.delete_student(sid)
            assert r2.json()["status"] == 0

    @allure.title("Удаление несуществующего студента")
    @pytest.mark.xfail(reason="BUG-005: delete несуществующего id тоже success")
    def test_delete_not_found(self, api_client):
        with allure.step("DELETE random id"):
            response = api_client.delete_student(99999998)

        # тут api может вести себя по разному, проверяем что хотя бы не 500
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == 0 or "not found" in body.get("message", "").lower()
