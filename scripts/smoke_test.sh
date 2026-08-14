#!/usr/bin/env bash
set -euo pipefail

API_BASE="${API_BASE:-http://127.0.0.1:8000/api/v1}"
STAMP="$(date +%s)"
USERNAME="smoke${STAMP}"
EMAIL="smoke.${STAMP}@example.com"

curl -fsS "${API_BASE}/health" >/dev/null

REGISTER_RESPONSE="$(curl -fsS -X POST "${API_BASE}/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"${USERNAME}\",\"email\":\"${EMAIL}\",\"password\":\"strong-password\"}")"

TOKEN="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["access_token"])' <<< "${REGISTER_RESPONSE}")"

curl -fsS -X POST "${API_BASE}/glossary" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{"term":"payment","approved_translation":"भुगतान","source_language":"en","target_language":"hi","domain":"finance"}' >/dev/null

TRANSLATION_RESPONSE="$(curl -fsS -X POST "${API_BASE}/translate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{"source_text":"The payment has been processed successfully.","target_language":"hi","provider":"local"}')"

TRANSLATION_ID="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])' <<< "${TRANSLATION_RESPONSE}")"

curl -fsS -X POST "${API_BASE}/qa/review" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d "{\"source_text\":\"The payment has been processed successfully.\",\"translated_text\":\"[hi] The payment has been processed successfully.\",\"source_language\":\"en\",\"target_language\":\"hi\",\"translation_id\":${TRANSLATION_ID}}" >/dev/null

curl -fsS "${API_BASE}/analytics/summary" \
  -H "Authorization: Bearer ${TOKEN}" >/dev/null

echo "Smoke test passed"
