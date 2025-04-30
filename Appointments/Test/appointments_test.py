import unittest
from fastapi.testclient import TestClient
from Services.main import app

client = TestClient(app)

class TestAppointments(unittest.TestCase):

    def test_create_appointment(self):
        response = client.post("/appointments", json={"name": "Alice", "time": "10:00"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())

    def test_delete_nonexistent_appointment(self):
        response = client.delete("/appointments/9999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Appointment not found")

    def test_delete_existing_appointment(self):
        create_resp = client.post("/appointments", json={"name": "Bob", "time": "15:30"})
        self.assertEqual(create_resp.status_code, 200)
        appointment_id = create_resp.json()["id"]

        delete_resp = client.delete(f"/appointments/{appointment_id}")
        self.assertEqual(delete_resp.status_code, 200)
        self.assertEqual(delete_resp.json()["message"], "Appointment cancelled")

        get_resp = client.get(f"/appointments/{appointment_id}")
        self.assertEqual(get_resp.status_code, 404)

    def test_create_appointment_with_empty_name(self):
        response = client.post("/appointments", json={"name": "", "time": "10:00"})
        self.assertEqual(response.status_code, 200)

    def test_create_appointment_with_invalid_time(self):
        response = client.post("/appointments", json={"name": "Bob", "time": "25:99"})
        self.assertEqual(response.status_code, 200)

    def test_create_appointment_missing_fields(self):
        response = client.post("/appointments", json={"name": "Charlie"})
        self.assertEqual(response.status_code, 422)

        response = client.post("/appointments", json={"time": "12:00"})
        self.assertEqual(response.status_code, 422)
