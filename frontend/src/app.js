let token = "";
let currentTranslation = null;

const get = (id) => document.getElementById(id);
const apiBase = () => get("apiBase").value.replace(/\/$/, "");

function show(data) {
  get("output").textContent = JSON.stringify(data, null, 2);
}

function setStatus(value) {
  get("status").textContent = value;
}

async function request(path, options = {}) {
  const headers = {
    ...(options.headers || {}),
  };
  if (!(options.body instanceof FormData)) {
    headers["Content-Type"] = headers["Content-Type"] || "application/json";
  }
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  const response = await fetch(`${apiBase()}${path}`, {
    ...options,
    headers,
  });
  const text = await response.text();
  const data = text ? JSON.parse(text) : {};
  if (!response.ok) {
    throw data;
  }
  return data;
}

get("healthBtn").addEventListener("click", async () => {
  const response = await fetch(`${apiBase()}/health`);
  const data = await response.json();
  setStatus(data.status);
  show(data);
});

get("registerBtn").addEventListener("click", async () => {
  const data = await request("/auth/register", {
    method: "POST",
    body: JSON.stringify({
      username: `${get("username").value}-${Date.now()}`,
      email: get("email").value.replace("@", `+${Date.now()}@`),
      password: get("password").value,
    }),
  });
  token = data.access_token;
  setStatus("Authenticated");
  show(data.user);
});

get("loginBtn").addEventListener("click", async () => {
  const form = new URLSearchParams();
  form.append("username", get("username").value);
  form.append("password", get("password").value);
  const data = await request("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: form,
  });
  token = data.access_token;
  setStatus("Authenticated");
  show(data.user);
});

get("glossaryBtn").addEventListener("click", async () => {
  const data = await request("/glossary", {
    method: "POST",
    body: JSON.stringify({
      term: get("glossaryTerm").value,
      approved_translation: get("approvedTranslation").value,
      source_language: "en",
      target_language: get("targetLanguage").value,
      domain: get("domain").value,
    }),
  });
  show(data);
});

get("translateBtn").addEventListener("click", async () => {
  const data = await request("/translate", {
    method: "POST",
    body: JSON.stringify({
      source_text: get("sourceText").value,
      target_language: get("targetLanguage").value,
      provider: get("provider").value,
    }),
  });
  currentTranslation = data;
  get("translatedText").value = data.translated_text;
  show(data);
});

get("qaBtn").addEventListener("click", async () => {
  const data = await request("/qa/review", {
    method: "POST",
    body: JSON.stringify({
      source_text: get("sourceText").value,
      translated_text: get("translatedText").value,
      source_language: currentTranslation?.source_language || "en",
      target_language: get("targetLanguage").value,
      translation_id: currentTranslation?.id,
    }),
  });
  show(data);
});

get("feedbackBtn").addEventListener("click", async () => {
  if (!currentTranslation) {
    show({ detail: "Translate text first" });
    return;
  }
  const data = await request(`/translations/${currentTranslation.id}/feedback`, {
    method: "POST",
    body: JSON.stringify({
      rating: 9,
      comment: "Approved from dashboard",
      status: "approved",
    }),
  });
  show(data);
});

get("documentBtn").addEventListener("click", async () => {
  const data = await request("/documents/ingest", {
    method: "POST",
    body: JSON.stringify({
      filename: "manual-input.txt",
      content_type: "text/plain",
      text: get("documentText").value,
    }),
  });
  show(data);
});

get("analyticsBtn").addEventListener("click", async () => {
  const data = await request("/analytics/summary");
  show(data);
});
