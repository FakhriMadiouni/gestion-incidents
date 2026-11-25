def test_add_incident(client, incident_data):
    response = client.post("/incidents/nouveau", data=incident_data)
    assert response.status_code == 302  # redirection vers la liste
    page = client.get("/").get_data(as_text=True)
    assert "Projecteur en panne" in page


def test_list_incidents(client, incident_data):
    client.post("/incidents/nouveau", data=incident_data)
    client.post("/incidents/nouveau", data={**incident_data, "titre": "Wifi coupé"})
    page = client.get("/").get_data(as_text=True)
    assert "Projecteur en panne" in page
    assert "Wifi coupé" in page


def test_incident_detail(client, incident_data):
    client.post("/incidents/nouveau", data=incident_data)
    response = client.get("/incidents/1")
    assert response.status_code == 200
    assert "Salle B12" in response.get_data(as_text=True)


def test_change_status(client, incident_data):
    client.post("/incidents/nouveau", data=incident_data)
    client.post("/incidents/1/statut", data={"statut": "Résolu"})
    page = client.get("/incidents/1").get_data(as_text=True)
    assert "Résolu" in page


def test_delete_incident(client, incident_data):
    client.post("/incidents/nouveau", data=incident_data)
    client.post("/incidents/1/supprimer")
    assert client.get("/incidents/1").status_code == 404


def test_add_incident_missing_field(client):
    response = client.post("/incidents/nouveau", data={"titre": "", "priorite": "Faible"})
    assert response.status_code == 400
