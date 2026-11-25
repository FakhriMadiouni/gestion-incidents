import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    # Chaque test utilise une base SQLite temporaire et vide
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    return app.test_client()


@pytest.fixture
def incident_data():
    return {
        "titre": "Projecteur en panne",
        "description": "Le projecteur ne s'allume plus",
        "lieu": "Salle B12",
        "priorite": "Élevée",
    }
