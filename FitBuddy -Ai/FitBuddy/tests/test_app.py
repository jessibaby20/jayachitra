import os
os.environ["GOOGLE_API_KEY"]=""
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db
init_db()
client=TestClient(app)
def test_health():
    r=client.get("/api/health"); assert r.status_code==200; assert r.json()["status"]=="ok"
def test_generate():
    p={"user_id":"TEST001","name":"Test User","age":20,"weight":60,"goal":"general wellness","intensity":"medium"}
    r=client.post("/api/generate-workout",json=p); assert r.status_code==200; assert "Day 1" in r.json()["workout_plan"]
def test_feedback():
    r=client.post("/api/feedback",json={"user_id":"TEST001","feedback":"Add more mobility work."})
    assert r.status_code==200; assert "UPDATED NOTES" in r.json()["updated_plan"]
