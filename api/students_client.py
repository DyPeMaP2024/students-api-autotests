import json
import logging

import requests

from config import BASE_URL, REQUEST_TIMEOUT


class StudentsClient:
    """Клиент для ручек /student"""

    def __init__(self, base_url=None):
        self.base_url = base_url or BASE_URL
        self.session = requests.Session()
        self.log = logging.getLogger("api.students")

    def _url(self, path):
        return self.base_url.rstrip("/") + path

    def _write_log(self, method, url, resp, body=None):
        msg = "%s %s -> %s\n" % (method, url, resp.status_code)
        try:
            msg += resp.text
        except Exception:
            pass
        self.log.info(msg)
        if body is not None:
            self.log.info("request body: %s" % json.dumps(body, ensure_ascii=False))

    def get_all_students(self):
        url = self._url("/student")
        resp = self.session.get(url, timeout=REQUEST_TIMEOUT)
        self._write_log("GET", url, resp)
        return resp

    def get_student_by_id(self, student_id):
        url = self._url("/student/%s" % student_id)
        resp = self.session.get(url, timeout=REQUEST_TIMEOUT)
        self._write_log("GET", url, resp)
        return resp

    def create_student(self, payload):
        url = self._url("/student")
        resp = self.session.post(
            url, json=payload, timeout=REQUEST_TIMEOUT
        )
        self._write_log("POST", url, resp, payload)
        return resp

    def update_student(self, student_id, payload):
        url = self._url("/student/%s" % student_id)
        resp = self.session.put(
            url, json=payload, timeout=REQUEST_TIMEOUT
        )
        self._write_log("PUT", url, resp, payload)
        return resp

    def delete_student(self, student_id):
        url = self._url("/student/%s" % student_id)
        resp = self.session.delete(url, timeout=10)  # тут другой таймаут, не заметил
        self._write_log("DELETE", url, resp)
        return resp
