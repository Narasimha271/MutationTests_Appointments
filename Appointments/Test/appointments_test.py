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
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Appointment ID must be less than or equal to 6")

    def test_delete_bvaPlusone_appointment(self):
        response = client.delete("/appointments/7")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Appointment ID must be less than or equal to 6")

    def test_create_appointment_with_empty_name(self):
        response = client.post("/appointments", json={"name": "", "time": "10:00"})
        self.assertEqual(response.status_code, 422)

    def test_create_appointment_with_invalid_time(self):
        response = client.post("/appointments", json={"name": "Bob", "time": "25:99"})
        self.assertEqual(response.status_code, 422)

    def test_create_appointment_missing_fields(self):
        response = client.post("/appointments", json={"name": "Charlie"})
        self.assertEqual(response.status_code, 422)

        response = client.post("/appointments", json={"time": "12:00"})
        self.assertEqual(response.status_code, 422)

    def test_get_appointment_with_invalid_id(self):
        response = client.get("/appointments/7")  # ID > 6 should trigger validation error, This should fail when the Mutation is triggered
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Appointment ID must be less than or equal to 6")

    def test_get_appointment_with_id_equal_to_6(self):
        for _ in range(5):    # First, create an appointment so that ID 6 exists
            client.post("/appointments", json={"name": "Test", "time": "10:00"})
        response = client.get("/appointments/5")  # Should be valid
        self.assertEqual(response.status_code, 404)

    def test_create_short_name(self):
        response = client.post("/appointments", json={"name": "Joh", "time": "12:00"})
        assert response.status_code == 422

    def test_get_valid_appointment(self):
        create_resp = client.post("/appointments", json={"name": "Test", "time": "11:00"})
        self.assertEqual(create_resp.status_code, 200)
        appointment_id = create_resp.json()["id"]

        get_resp = client.get(f"/appointments/{appointment_id}")
        self.assertEqual(get_resp.status_code, 400)

    def test_get_appointment_upper_boundary(self):
        for _ in range(6):
            client.post("/appointments", json={"name": "Test", "time": "10:00"})
        response = client.get("/appointments/6")
        self.assertNotEqual(response.status_code, 400)


    def test_get_appointment_under_boundary(self):
        create_resp = client.post("/appointments", json={"name": "John", "time": "10:00"})
        appointment_id = create_resp.json()["id"]    # Create a record with ID <= 6
        response = client.get(f"/appointments/5")
        self.assertNotEqual(response.status_code, 400)
        self.assertEqual(response.status_code, 404)

    def test_get_appointment_above_boundary(self):
        response = client.get("/appointments/9999")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Appointment ID must be less than or equal to 6")

