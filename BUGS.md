# Bug-reports — Students API (93.77.188.34)

Дата проверки: 07.10.2025  
Окружение: тестовый стенд Петрович-ТЕХ, Swagger `/apidocs`

---

## BUG-001 — Разрешено создавать студентов с одинаковым email

| Поле | Значение |
|------|----------|
| **Severity** | Medium |
| **Endpoint** | `POST /student` |
| **Шаги** | 1. Создать студента с email `test@example.com`<br>2. Создать второго студента с тем же email |
| **Ожидание** | Второй запрос: `status=0`, сообщение об ошибке |
| **Факт** | Оба запроса возвращают `status=1`, создаются две записи |
| **Тест** | `test_duplicate_email_not_allowed` (xfail) |

---

## BUG-002 — Поле `status` в ответе PUT приходит строкой, не числом

| Поле | Значение |
|------|----------|
| **Severity** | Low |
| **Endpoint** | `PUT /student/{id}` |
| **Шаги** | Обновить студента с `"status": 0` |
| **Ожидание** | В `student.status` тип `integer` (как в GET и POST) |
| **Факт** | `"status": "0"` — строка |
| **Тест** | `test_update_status_field_type` (xfail) |

---

## BUG-003 — Некорректный `student_id` в path отдаёт HTML 404

| Поле | Значение |
|------|----------|
| **Severity** | Low |
| **Endpoint** | `GET /student/{student_id}` |
| **Шаги** | `GET /student/abc` |
| **Ожидание** | JSON с `status=0` и HTTP 200 (как для несуществующего id) |
| **Факт** | HTTP 404, `Content-Type: text/html` |
| **Тест** | `test_get_student_invalid_id_format` (xfail) |

---

## BUG-004 — Повторное удаление уже удалённого студента считается успехом

| Поле | Значение |
|------|----------|
| **Severity** | Medium |
| **Endpoint** | `DELETE /student/{id}` |
| **Шаги** | 1. DELETE существующего id<br>2. Повторить DELETE с тем же id |
| **Ожидание** | Второй ответ: `status=0`, student not found |
| **Факт** | `"message": "Student deleted successfully", "status": 1` |
| **Тест** | `test_delete_already_deleted` (xfail) |

---

## BUG-005 — DELETE несуществующего студента возвращает успех

| Поле | Значение |
|------|----------|
| **Severity** | Medium |
| **Endpoint** | `DELETE /student/{id}` |
| **Шаги** | `DELETE /student/99999998` (id точно нет в БД) |
| **Ожидание** | `status=0`, сообщение not found |
| **Факт** | `status=1`, `"Student deleted successfully"` |
| **Тест** | `test_delete_not_found` (xfail) |
