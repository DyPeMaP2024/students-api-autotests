import random
import string
import uuid

import allure
import pytest

from api.students_client import StudentsClient
from utils.logger_helper import setup_test_logger


@pytest.fixture(scope="session")
def api_client():
    return StudentsClient()


@pytest.fixture(autouse=True)
def test_log_attachment(request):
    logger, log_path = setup_test_logger(request.node.name)
    logger.info("start test: %s" % request.node.name)
    yield logger
    logger.info("finish test")
    if log_path and __import__("os").path.isfile(log_path):
        with open(log_path, "rb") as f:
            allure.attach(
                f.read(),
                name="request_log",
                attachment_type=allure.attachment_type.TEXT,
            )


def random_email():
    part = uuid.uuid4().hex[:8]
    return "auto_%s@test.local" % part


def valid_student_payload(email=None):
    if email is None:
        email = random_email()
    return {
        "name": "Autotest " + "".join(random.choices(string.ascii_letters, k=5)),
        "email": email,
        "phone_no": "+7999" + str(random.randint(1000000, 9999999)),
        "gender": random.choice(["male", "female"]),
        "status": 1,
    }


@pytest.fixture
def created_student(api_client):
    """Создаём студента и удаляем после теста если ещё жив."""
    payload = valid_student_payload()
    resp = api_client.create_student(payload)
    data = resp.json()
    student_id = data.get("student", {}).get("id")
    yield student_id, payload, resp
    if student_id:
        api_client.delete_student(student_id)
