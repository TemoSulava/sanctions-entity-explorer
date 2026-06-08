def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_search_returns_ranked_results_with_full_shape(client):
    response = client.get("/api/search", params={"q": "al madar"})
    assert response.status_code == 200

    body = response.json()
    assert body["query"] == "al madar"
    assert isinstance(body["results"], list)
    assert body["results"]

    first = body["results"][0]
    expected_fields = {"id", "name", "type", "primary_country", "programs", "score", "matched_on"}
    assert set(first) == expected_fields
    assert 0.0 <= first["score"] <= 1.0
    assert first["matched_on"] in {"name", "alias"}
    assert isinstance(first["programs"], list)


def test_search_empty_query_is_200_with_no_results(client):
    response = client.get("/api/search", params={"q": "   "})
    assert response.status_code == 200
    assert response.json() == {"query": "   ", "results": []}


def test_search_rejects_out_of_bounds_limit(client):
    assert client.get("/api/search", params={"q": "al", "limit": 0}).status_code == 422
    assert client.get("/api/search", params={"q": "al", "limit": 26}).status_code == 422


def test_entity_returns_summary_shape(client):
    response = client.get("/api/entities/SDN-10001")
    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"id", "name", "type", "primary_country"}
    assert body["id"] == "SDN-10001"


def test_entity_missing_returns_404_detail(client):
    response = client.get("/api/entities/SDN-99999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Entity SDN-99999 not found"}


def test_graph_returns_render_ready_shape(client):
    response = client.get("/api/entities/SDN-10001/graph")
    assert response.status_code == 200

    body = response.json()
    assert set(body) == {"center", "nodes", "edges"}
    assert set(body["center"]) == {"id", "name", "type", "primary_country"}
    assert any(node["is_center"] for node in body["nodes"])
    assert set(body["nodes"][0]) == {"id", "name", "type", "is_center"}

    assert body["edges"]
    assert set(body["edges"][0]) == {"source", "target", "type", "note"}


def test_graph_missing_returns_404_detail(client):
    response = client.get("/api/entities/SDN-99999/graph")
    assert response.status_code == 404
    assert response.json() == {"detail": "Entity SDN-99999 not found"}


def test_cors_allows_frontend_origin(client):
    # The Vite dev origin must be echoed back, or the SPA is silently blocked.
    response = client.get("/api/health", headers={"Origin": "http://localhost:5173"})
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"
