const projects = [
  {
    title: "Advo-AI",
    type: "GenAI",
    highlight: "AI legal practice workspace with OCR, RAG, drafting, and case-aware chat.",
    details:
      "Built an India-first AI workspace for advocates to manage clients, cases, hearings, legal research, drafting, and structured case analysis.",
    impact: "Case-aware retrieval with user, case, client, and document metadata.",
    stack: ["FastAPI", "React", "Qdrant", "OpenAI", "ABBYY OCR", "Supabase"],
    link: "https://github.com/Khus45/Advo-AI",
  },
  {
    title: "Enterprise AI Translation Intelligence Platform",
    type: "Backend",
    highlight: "Production-style translation QA platform with RAG, agents, feedback, and analytics.",
    details:
      "Designed a FastAPI backend that translates text, retrieves glossary context, runs multi-agent QA, stores reviewer feedback, and exposes analytics.",
    impact: "Auth, RBAC, provider pattern, tests, Docker Compose, and monitoring surfaces.",
    stack: ["FastAPI", "SQLAlchemy", "JWT", "OpenAI", "Gemini", "Docker"],
    link: "https://github.com/Khus45/ai-translation-platform-v2",
  },
  {
    title: "Marketing Analytics",
    type: "Analytics",
    highlight: "Agentic analytics app for safe SQL, segmentation, leads, and campaign drafts.",
    details:
      "Created a Streamlit analytics workflow that routes questions to BI, segmentation, product, and email-writing agents.",
    impact: "Read-only SQL safety, KMeans customer groups, Plotly charts, CSV exports, and tests.",
    stack: ["Streamlit", "Python", "SQLite", "Pandas", "scikit-learn", "Plotly"],
    link: "https://github.com/Khus45/Marketing-analytics",
  },
  {
    title: "Text-to-SQL",
    type: "Analytics",
    highlight: "Natural-language SQL assistant for uploaded CSV datasets.",
    details:
      "Built during internship to ingest CSV files, normalize columns, extract schema, generate SQLite queries, and show results in a clean table.",
    impact: "Made dataset querying easier for non-technical users.",
    stack: ["Streamlit", "LangChain", "OpenAI", "SQLite", "Pandas", "SQLAlchemy"],
    link: "https://github.com/Khus45/text-to-sql",
  },
  {
    title: "Ai-data-analyst",
    type: "Analytics",
    highlight: "AI data analyst prototype for EDA, charts, and business insights.",
    details:
      "Built a CSV analysis assistant that cleans data, previews metrics, routes questions, and generates visual insight views.",
    impact: "Shows practical analytics UX with Python, Plotly, and LLM-assisted reasoning.",
    stack: ["Streamlit", "Python", "Pandas", "Plotly", "LLMs"],
    link: "https://github.com/Khus45/Ai-data-analyst",
  },
  {
    title: "generative_ai_agent",
    type: "GenAI",
    highlight: "Agent demo exploring LLM workflows and data analysis assistance.",
    details:
      "Created a supporting GenAI prototype focused on prompt orchestration, dataset questions, and automated insight generation.",
    impact: "Useful foundation for agent routing and Streamlit AI interfaces.",
    stack: ["Python", "Streamlit", "LangChain", "OpenAI"],
    link: "https://github.com/Khus45/generative_ai_agent",
  },
];

const skills = [
  {
    title: "AI Engineering",
    items: ["RAG", "Agentic AI", "LangChain", "LangGraph", "OpenAI", "Gemini", "Embeddings"],
  },
  {
    title: "Backend",
    items: ["FastAPI", "Pydantic", "SQLAlchemy", "Alembic", "JWT", "RBAC", "REST APIs"],
  },
  {
    title: "Data",
    items: ["SQL", "Snowflake", "Power BI", "EDA", "ETL", "Data Validation", "Feature Engineering"],
  },
  {
    title: "Platforms",
    items: ["PostgreSQL", "Qdrant", "Pinecone", "Docker", "GitHub Actions", "Supabase", "N8N"],
  },
];

const answers = [
  {
    label: "About",
    title: "Tell me about yourself",
    body:
      "I am Khushi Sinha, a data analyst and GenAI-focused developer with experience in SQL, Python, enterprise operations, and LLM applications. At Capgemini, I work on the IKEA FOOD - Infor M3 project, where I support ERP data operations, documentation workflows, H5 scripts, widget customization, and Snowflake SQL logic. Alongside that, I build AI systems such as Advo-AI, an enterprise translation QA platform, and marketing analytics agents.",
  },
  {
    label: "Hire Me",
    title: "Why should we hire you?",
    body:
      "You should hire me because I combine business-facing operations experience with practical GenAI engineering. I can understand support workflows, clean and analyze data, write SQL, build dashboards, and also create AI applications with FastAPI, Streamlit, RAG, agents, vector search, and tests.",
  },
  {
    label: "Strongest",
    title: "What is your strongest project?",
    body:
      "My strongest project is Advo-AI because it shows full-stack AI product thinking. It includes legal case workflows, scanned document processing with OCR, chunking, embeddings, Qdrant retrieval, case-aware chat, drafting, research surfaces, and scoped user data.",
  },
  {
    label: "Challenge",
    title: "What was a technical challenge?",
    body:
      "A major challenge was grounding AI responses in the correct context. In Advo-AI, legal documents belong to different clients, cases, and advocates, so retrieval cannot mix data. I solved this by indexing chunks with metadata and filtering retrieval by authenticated user, case, client, and document IDs.",
  },
];

const timeline = [
  {
    period: "Dec 2024 - Present",
    title: "Associate Data Analyst, Capgemini",
    text: "Infor M3 ERP operations, support workflows, documentation, H5 scripts, widgets, Snowflake SQL, and dashboard automation logic.",
  },
  {
    period: "Feb 2024 - Aug 2024",
    title: "Software Developer Intern, Verma Consultancy",
    text: "Built Text-to-SQL workflows with Streamlit, CSV ingestion, SQLite, LangChain, OpenAI, and result downloads.",
  },
  {
    period: "Jul 2024",
    title: "B.E. Information Science and Engineering",
    text: "Graduated from CMR Institute of Technology, Bengaluru.",
  },
];

const filters = ["All", "GenAI", "Analytics", "Backend"];
let activeFilter = "All";
let activeAnswer = 0;

const byId = (id) => document.getElementById(id);

function renderFilters() {
  byId("filters").innerHTML = filters
    .map(
      (filter) => `
        <button class="filter-button ${filter === activeFilter ? "is-active" : ""}" data-filter="${filter}" type="button">
          ${filter}
        </button>
      `,
    )
    .join("");
}

function renderProjects() {
  const visibleProjects =
    activeFilter === "All" ? projects : projects.filter((project) => project.type === activeFilter);

  byId("projectGrid").innerHTML = visibleProjects
    .map(
      (project) => `
        <article class="project-card tilt-card">
          <div class="project-orbit" aria-hidden="true">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <div class="project-topline">
            <span>${project.type}</span>
            <a href="${project.link}" target="_blank" rel="noreferrer" aria-label="Open ${project.title} on GitHub">GitHub</a>
          </div>
          <h3>${project.title}</h3>
          <p class="project-highlight">${project.highlight}</p>
          <p>${project.details}</p>
          <p class="impact">${project.impact}</p>
          <div class="stack-list">
            ${project.stack.map((item) => `<span>${item}</span>`).join("")}
          </div>
        </article>
      `,
    )
    .join("");
}

function renderSkills() {
  byId("skillGroups").innerHTML = skills
    .map(
      (group) => `
        <article class="skill-card tilt-card">
          <h3>${group.title}</h3>
          <div>
            ${group.items.map((item) => `<span>${item}</span>`).join("")}
          </div>
        </article>
      `,
    )
    .join("");
}

function renderAnswers() {
  byId("answerTabs").innerHTML = answers
    .map(
      (answer, index) => `
        <button
          class="answer-tab ${index === activeAnswer ? "is-active" : ""}"
          type="button"
          role="tab"
          aria-selected="${index === activeAnswer}"
          data-answer="${index}"
        >
          ${answer.label}
        </button>
      `,
    )
    .join("");

  const answer = answers[activeAnswer];
  byId("answerCard").innerHTML = `
    <div>
      <h3>${answer.title}</h3>
      <button class="copy-button" type="button" data-copy="${activeAnswer}">Copy</button>
    </div>
    <p>${answer.body}</p>
  `;
}

function renderTimeline() {
  byId("timeline").innerHTML = timeline
    .map(
      (item) => `
        <article class="timeline-item tilt-card">
          <span>${item.period}</span>
          <h3>${item.title}</h3>
          <p>${item.text}</p>
        </article>
      `,
    )
    .join("");
}

document.addEventListener("click", async (event) => {
  const filterButton = event.target.closest("[data-filter]");
  if (filterButton) {
    activeFilter = filterButton.dataset.filter;
    renderFilters();
    renderProjects();
  }

  const answerButton = event.target.closest("[data-answer]");
  if (answerButton) {
    activeAnswer = Number(answerButton.dataset.answer);
    renderAnswers();
  }

  const copyButton = event.target.closest("[data-copy]");
  if (copyButton) {
    await navigator.clipboard.writeText(answers[Number(copyButton.dataset.copy)].body);
    copyButton.textContent = "Copied";
    setTimeout(() => {
      copyButton.textContent = "Copy";
    }, 1400);
  }
});

document.addEventListener("pointermove", (event) => {
  const card = event.target.closest(".tilt-card");
  if (!card) {
    return;
  }

  const rect = card.getBoundingClientRect();
  const x = (event.clientX - rect.left) / rect.width - 0.5;
  const y = (event.clientY - rect.top) / rect.height - 0.5;
  card.style.setProperty("--tilt-x", `${(-y * 7).toFixed(2)}deg`);
  card.style.setProperty("--tilt-y", `${(x * 8).toFixed(2)}deg`);
  card.style.setProperty("--glow-x", `${((x + 0.5) * 100).toFixed(1)}%`);
  card.style.setProperty("--glow-y", `${((y + 0.5) * 100).toFixed(1)}%`);
});

document.addEventListener("pointerout", (event) => {
  const card = event.target.closest(".tilt-card");
  if (!card || card.contains(event.relatedTarget)) {
    return;
  }

  card.style.removeProperty("--tilt-x");
  card.style.removeProperty("--tilt-y");
  card.style.removeProperty("--glow-x");
  card.style.removeProperty("--glow-y");
});

renderFilters();
renderProjects();
renderSkills();
renderAnswers();
renderTimeline();
