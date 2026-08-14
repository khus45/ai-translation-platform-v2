def auth_headers(client) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "reviewer",
            "email": "reviewer@example.com",
            "password": "strong-password",
        },
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_enterprise_translation_intelligence_flow(client) -> None:
    headers = auth_headers(client)

    glossary_response = client.post(
        "/api/v1/glossary",
        headers=headers,
        json={
            "term": "payment",
            "approved_translation": "भुगतान",
            "source_language": "en",
            "target_language": "hi",
            "domain": "finance",
        },
    )
    assert glossary_response.status_code == 201

    translation_response = client.post(
        "/api/v1/translate",
        headers=headers,
        json={
            "source_text": "The payment has been processed successfully.",
            "target_language": "hi",
            "provider": "local",
        },
    )
    assert translation_response.status_code == 200
    translation = translation_response.json()
    assert translation["domain"] == "finance"
    assert translation["retrieved_context"]

    qa_response = client.post(
        "/api/v1/qa/review",
        headers=headers,
        json={
            "source_text": translation["source_text"],
            "translated_text": translation["translated_text"],
            "source_language": translation["source_language"],
            "target_language": translation["target_language"],
            "translation_id": translation["id"],
        },
    )
    assert qa_response.status_code == 201
    qa_report = qa_response.json()
    assert qa_report["overall_score"] > 0
    assert qa_report["metrics"]["semantic_similarity"] >= 0

    feedback_response = client.post(
        f"/api/v1/translations/{translation['id']}/feedback",
        headers=headers,
        json={
            "rating": 9,
            "comment": "Good translation",
            "status": "approved",
        },
    )
    assert feedback_response.status_code == 201
    assert feedback_response.json()["approved"] is True

    memory_response = client.get("/api/v1/translation-memory", headers=headers)
    assert memory_response.status_code == 200
    assert len(memory_response.json()) >= 1

    document_response = client.post(
        "/api/v1/documents/ingest",
        headers=headers,
        json={
            "filename": "invoice.txt",
            "content_type": "text/plain",
            "text": "Payment invoice for customer order",
        },
    )
    assert document_response.status_code == 201
    assert document_response.json()["domain"] == "finance"

    analytics_response = client.get("/api/v1/analytics/summary", headers=headers)
    assert analytics_response.status_code == 200
    analytics = analytics_response.json()
    assert analytics["total_translations"] == 1
    assert analytics["total_reviews"] == 1
    assert analytics["human_approval_rate"] == 1.0
