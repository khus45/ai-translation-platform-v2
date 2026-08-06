def auth_headers(client) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "translator",
            "email": "translator@example.com",
            "password": "strong-password",
        },
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_translate_detect_history_detail_and_delete_flow(client) -> None:
    headers = auth_headers(client)

    translate_response = client.post(
        "/api/v1/translate",
        headers=headers,
        json={
            "source_text": "Hello world",
            "target_language": "hi",
            "provider": "local",
        },
    )
    assert translate_response.status_code == 200
    translation = translate_response.json()
    assert translation["translated_text"] == "नमस्ते दुनिया"
    assert translation["source_language"] == "en"
    assert translation["provider"] == "local"

    detect_response = client.post(
        "/api/v1/detect-language",
        headers=headers,
        json={"text": "नमस्ते दुनिया"},
    )
    assert detect_response.status_code == 200
    assert detect_response.json()["language"] == "hi"

    history_response = client.get("/api/v1/translations", headers=headers)
    assert history_response.status_code == 200
    assert len(history_response.json()) == 1

    detail_response = client.get(
        f"/api/v1/translations/{translation['id']}",
        headers=headers,
    )
    assert detail_response.status_code == 200
    assert detail_response.json()["id"] == translation["id"]

    delete_response = client.delete(
        f"/api/v1/translations/{translation['id']}",
        headers=headers,
    )
    assert delete_response.status_code == 204

    missing_response = client.get(
        f"/api/v1/translations/{translation['id']}",
        headers=headers,
    )
    assert missing_response.status_code == 404


def test_translation_routes_require_authentication(client) -> None:
    response = client.post(
        "/api/v1/translate",
        json={"source_text": "Hello", "target_language": "hi"},
    )

    assert response.status_code == 401


def test_auto_provider_falls_back_to_local_when_api_keys_are_missing(client) -> None:
    headers = auth_headers(client)

    response = client.post(
        "/api/v1/translate",
        headers=headers,
        json={
            "source_text": "Thank you",
            "target_language": "hi",
            "provider": "auto",
        },
    )

    assert response.status_code == 200
    assert response.json()["provider"] == "local"
    assert response.json()["translated_text"] == "धन्यवाद"
