import unittest
from fastapi.testclient import TestClient
from Services.main import app  # adjust if your path differs

client = TestClient(app)

def test_create_appointment():
    response = client.post("/appointments", json={"name": "Alice", "time": "10:00"})
    assert response.status_code == 200
    assert "id" in response.json()

def test_delete_nonexistent_appointment():
    response = client.delete("/appointments/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Appointment not found"

def test_delete_existing_appointment():
    create_resp = client.post("/appointments", json={"name": "Bob", "time": "15:30"})
    assert create_resp.status_code == 200
    appointment_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/appointments/{appointment_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["message"] == "Appointment cancelled"
    get_resp = client.get(f"/appointments/{appointment_id}")
    assert get_resp.status_code == 404

def test_create_appointment_with_empty_name():
    response = client.post("/appointments", json={"name": "", "time": "10:00"})
    assert response.status_code == 200 

def test_create_appointment_with_invalid_time():
    response = client.post("/appointments", json={"name": "Bob", "time": "25:99"})
    assert response.status_code == 200  

def test_create_appointment_missing_fields():
    response = client.post("/appointments", json={"name": "Charlie"})  
    assert response.status_code == 422  

    response = client.post("/appointments", json={"time": "12:00"})  
    assert response.status_code == 422
