# 🔥 BuildAgents

> **A CLI scaffolder that generates production-ready foundations for Agentic AI applications — opinionated, structured, and built for serious builders.**

---

## 📌 Overview

**BuildAgents** is a developer tool (CLI) that bootstraps an opinionated, production-ready project structure for Agentic AI applications in seconds. Inspired by tools like `create-react-app` and `cookiecutter`, it removes the boilerplate burden so you can focus on building your agent logic.

Under the hood, it:
- Copies a pre-baked template directory tree
- Substitutes `{{placeholders}}` with your actual project values
- Leaves you with a runnable FastAPI + LangGraph foundation — ready to wire up your agent

---

## 🚀 Quickstart

### 1. Install

```bash
pip install buildagents
# or if using uv:
uv add buildagents
```

### 2. Create a project

```bash
buildagents create my-agent-app
# With options:
buildagents create my-agent-app --author "John Doe" --description "My AI Agent"
```

### 3. Run it

```bash
cd my-agent-app
cp .env.example .env          # Add your OPENAI_API_KEY
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit: `http://localhost:8000/docs` → Swagger UI is live.

---

## 🛠️ CLI Commands

| Command | Description |
|---|---|
| `buildagents create <name>` | Scaffold a new agentic AI project |
| `buildagents add tool <name>` | Add a new tool to an existing project |
| `buildagents version` | Print the current CLI version |

### `create` Options

| Flag | Short | Default | Description |
|---|---|---|---|
| `--author` | `-a` | `"Your Name"` | Your name (used in README) |
| `--description` | `-d` | `"An Agentic AI Application"` | Project description |

### `add tool`

`buildagents add tool <name>`

Adds a new LangChain-compatible tool to your project's `app/tools/` directory.

**Example:**
```bash
buildagents add tool calculator
```
This will create `app/tools/calculator.py` with a basic tool stub.

---

## 🏗️ Architecture

### BuildAgents Tool Architecture

```
BuildAgents (CLI Tool)
│
├── pyproject.toml            ← Package metadata, entry point, dependencies
│
└── src/buildagents/
    ├── __init__.py           ← Version string (e.g. __version__ = "0.2.0")
    ├── __main__.py           ← Package entry point (python -m buildagents)
    ├── cli.py                ← Typer CLI app (commands: create, version)
    └── core/                 ← Internal engine
        ├── __init__.py
        ├── generator.py      ← Jinja2-powered scaffold engine
        └── templates/
            └── base/         ← The project template that gets scaffolded
```

**Flow:**

```
User runs CLI
    │
    ▼
cli.py (Typer)
    │   Parses: name, --author, --description
    ▼
core/generator.py → create_project()
    │   1. Validates target dir doesn't exist
    │   2. shutil.copytree(templates/base → ./<name>)
    │   3. Jinja2 Engine → walks all files and renders templates
    │      with PROJECT_NAME, AUTHOR, DESCRIPTION
    ▼
Scaffolded project on disk ✅
```

---

### Generated Project Architecture

When you run `buildagents create my-agent-app`, this is what gets created:

```
my-agent-app/
│
├── main.py                   ← FastAPI app entry point
├── requirements.txt          ← Python dependencies
├── .env.example              ← Environment variable template
├── Dockerfile                ← Production Docker image
├── docker-compose.yml        ← Local dev container stack
├── README.md                 ← Project-specific README
│
└── app/
    ├── __init__.py
    │
    ├── agent/
    │   └── base_agent.py     ← LangGraph agent stub (wire your graph here)
    │
    ├── api/
    │   └── v1/
    │       └── routes.py     ← FastAPI router — POST /api/v1/agent/run
    │
    ├── core/
    │   └── config.py         ← Pydantic Settings, reads from .env
    │
    └── utils/
        └── logger.py         ← Structured stdout logger
```

**Request flow in the generated app:**

```
HTTP POST /api/v1/agent/run
    │
    ▼
app/api/v1/routes.py
    │   FastAPI router receives request
    ▼
app/agent/base_agent.py → run_agent(query)
    │   Your LangGraph StateGraph logic lives here
    ▼
JSON response {"result": "..."}
```

---

## 📦 Dependencies

### CLI Tool (`buildagents`)

| Package | Purpose |
|---|---|
| `typer >= 0.12.0` | CLI framework (argument/option parsing, help text) |
| `jinja2 >= 3.1.0` | Templating engine (available for future template rendering) |

### Generated Project

| Package | Purpose |
|---|---|
| `fastapi >= 0.111.0` | Web framework for the agent API |
| `uvicorn[standard] >= 0.29.0` | ASGI server to run FastAPI |
| `langgraph >= 0.1.0` | Agent graph orchestration |
| `langchain-openai >= 0.1.0` | OpenAI LLM integration via LangChain |
| `pydantic-settings >= 2.0.0` | Settings management via `.env` |
| `python-dotenv >= 1.0.0` | Load `.env` into environment |

---

## ⚙️ Environment Variables

The generated project uses a `.env` file:

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | *(required)* | Your OpenAI API key |
| `DEBUG` | `false` | Enable debug mode |
| `LOG_LEVEL` | `INFO` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |

---

## 🐳 Docker

The generated project ships with Docker support out of the box.

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t my-agent-app .
docker run -p 8000:8000 --env-file .env my-agent-app
```

The container:
- Uses `python:3.11-slim` base image
- Exposes port `8000`
- Serves via `uvicorn main:app --host 0.0.0.0 --port 8000`

---

## 🔌 API Endpoints (Generated Project)

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/agent/run` | Run the agent pipeline |

### Example: Run the agent

```bash
curl -X POST "http://localhost:8000/api/v1/agent/run" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the capital of France?"}'
```

Response:
```json
{
  "result": "Agent received: What is the capital of France? — wire up LangGraph here."
}
```

---

## 🧩 Extending the Agent

The `base_agent.py` stub is where you wire in your LangGraph logic:

```python
# app/agent/base_agent.py
from langgraph.graph import StateGraph
from typing import TypedDict

class AgentState(TypedDict):
    query: str
    result: str

async def run_agent(query: str) -> str:
    graph = StateGraph(AgentState)
    # Define nodes, edges, and compile
    # ...
    compiled = graph.compile()
    output = compiled.invoke({"query": query})
    return output["result"]
```

---

## 🗺️ Roadmap

- [x] Add more templates (multi-agent, RAG, tool-use)
- [x] `--template` flag to choose different scaffolds
- [x] Interactive mode with prompts
- [x] Built-in `buildagents add tool` command to extend existing projects
- [x] PyPI publish pipeline

---

## 👥 Contributing

Contributions are welcome! To contribute:

```bash
git clone https://github.com/premsaivarmachekuri/BuildAgents.git
cd BuildAgents
uv sync         # Install all dependencies
uv run buildagents create test-project
```

---

## 📄 License

MIT — see [LICENSE](./LICENSE).

---

## 👤 Author

**Prem Sai Varma Chekuri** — [premsaivarma.chekuri@gmail.com](mailto:premsaivarma.chekuri@gmail.com)

[![GitHub](https://img.shields.io/badge/GitHub-BuildAgents-blue?logo=github)](https://github.com/premsaivarmachekuri/BuildAgents)
