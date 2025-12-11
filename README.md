# Agentic Travel Planner — AI Travel Agent

**A modular, agentic travel planner that combines an LLM with tool plugins to produce detailed, real‑time travel plans and expense estimates.**

---

## Project Overview

This repository implements an *agentic* workflow built on top of language‑model bindings (Groq / OpenAI) and a small collection of tools (weather, currency, place search, expense calculator). The agent compiles tools into a `langgraph` state graph and exposes an HTTP API (FastAPI) and a lightweight Streamlit UI for interaction.

Key ideas

* Use an LLM that can be bound to external tools to gather live information.
* Provide one single function (`GraphBuilder`) that wires LLM + tools into a state graph.
* Tools are implemented as LangChain `@tool` callables and grouped into classes for reuse.
* Outputs can be saved to Markdown files for user-friendly travel plans.

---

## Repository Structure

```
├── agent/
│   └── agentic_workflow.py        # Builds the graph, binds LLM to tools
├── prompt_library/
│   └── system_prompt.py           # System prompt (travel agent instructions)
├── tools/
│   ├── weather_info_tool.py       # Weather tool wrapper
│   ├── currency_conversion_tool.py# Currency conversion wrapper
│   ├── expense_calculator_tool.py # Expense calculation helpers
│   └── place_search_tool.py       # Place/hospital/shopping search helpers
├── utils/
│   ├── config_loader.py           # YAML config loader
│   ├── model_loader.py            # Model selection and initialization
│   ├── weather_info.py            # Low-level weather API client
│   ├── currency_converter.py      # Low-level currency API client
│   ├── place_info_search.py       # Tavily search wrapper
│   └── save_to_document.py        # Export responses to Markdown
├── main.py                         # FastAPI server (POST /query)
├── app_streamlit.py                # Streamlit frontend
├── requirements.txt                # Python dependencies
└── README.md                       # <-- this file
```

---

## Features

* Runs a stateful `langgraph` agent that: accepts a user query, invokes the LLM, and routes to tool nodes when needed.
* Tooling includes:

  * Current weather and forecast (OpenWeatherMap)
  * Currency conversion (ExchangeRate‑API / AlphaVantage depending on tool)
  * Place searching (TavilySearch wrapper for attractions, hotels, restaurants, transport, nightlife, shopping, hospitals)
  * Expense calculation helpers (daily budgets, hostel cost, sum of items)
* Export output to nicely formatted Markdown files for offline viewing.
* FastAPI endpoint `POST /query` to query the agent programmatically.
* Streamlit UI for interactive usage.

---

## Requirements

* Python 3.10+
* A virtual environment is recommended.

Create environment and install:

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

`requirements.txt` should include (examples):

```
fastapi
uvicorn
streamlit
python-dotenv
langchain
langchain-groq
langchain-openai
langgraph
langchain-tavily
requests
pydantic
python-multipart
```

Adjust versions per your environment.

---

## Environment Variables

Create a `.env` file at project root with the following keys (example):

```
# LLM / provider
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# LangSmith (optional, used in agentic_workflow for tracing)
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_WORKSPACE_ID=your_langsmith_workspace_id

# External APIs used by tools
OPENWEATHER_API_KEY=your_openweathermap_api_key
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key
ALPHAVANTAGE_API_KEY=your_alpha_vantage_api_key   # optional if using AlphaVantage helper

# (Optional) other config keys referenced by utils/config/config.yaml
```

**Important:** Never commit `.env` to source control. Use a secrets manager for production.

---

## Configuration

The project uses a YAML config file at `config/config.yaml` (used by `utils.load_config`). Example minimal config:

```yaml
llm:
  groq:
    model_name: "deepseek-r1-distill-llama-70b"
openai_api_key: ""
```

Adjust model names and options to match your provider.

---

## How to Run

### Development (FastAPI)

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Endpoint: `POST /query`

**Example cURL:**

```bash
curl -X POST "http://127.0.0.1:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "Plan a 3-day trip to Paris for two people, budget-conscious."}'
```

The server will build the graph, draw a graph image (`graph.png`), invoke the agent, and return a `response` string in JSON.

### Streamlit UI

```bash
streamlit run app_streamlit.py
```

Open the Streamlit UI (default [http://localhost:8501](http://localhost:8501)) and enter a travel prompt. The UI posts to the FastAPI server and displays the returned Markdown.

---

## Code Highlights & How It Works

* **GraphBuilder** (`agent/agentic_workflow.py`) is the entrypoint for agent logic. It:

  1. Loads an LLM via `ModelLoader` (Groq or OpenAI)
  2. Instantiates tool wrappers (`WeatherInfoTool`, `CurrencyConversionTool`, `CalculatorTool`, `PlaceSearchTool`)
  3. Binds those tools to the LLM via `llm.bind_tools(...)`
  4. Builds a `langgraph.StateGraph` with an `agent` node and a `ToolNode`
  5. The graph's `agent_function` composes the `SYSTEM_PROMPT` plus user messages and calls the LLM with tools available

* **Tools** live under `tools/` and export LangChain `@tool` callables. Each tool class groups related tools (e.g., place search functions returned as a list).

* **ModelLoader** (`utils/model_loader.py`) picks the provider based on `model_provider` and pulls model configuration from `config/config.yaml`.

* **Utils** implement concrete API clients (`WeatherForecastTool`, `CurrencyConverter`, `TavilyPlaceSearchTool`) and helpers like `save_to_document` to persist Markdown output.

---

## Example: Adding a New Tool

1. Implement low-level client in `utils/` (e.g., `utils/rail_info.py`).
2. Add a wrapper class in `tools/rail_info_tool.py` that creates `@tool` callables and returns a list (similar to `PlaceSearchTool`).
3. In `agent/agentic_workflow.py`, instantiate your tool and add its tool list to `self.tools` so it gets bound to the LLM.

---

## Testing & Troubleshooting

* If LLM fails to load, verify `GROQ_API_KEY` or `OPENAI_API_KEY` and `config/config.yaml` are correct.
* If external API calls fail, check that corresponding environment variables are set and the APIs are reachable.
* Increase FastAPI timeout if agents take long to respond or simplify tools for quicker responses.

---

## Security & Production Notes

* Do not expose API keys in logs or committed files.
* For production: use a secrets manager, set environment variables in your deployment, and consider async-safe LLM clients and timeouts.
* Rate limits: Tools that call third‑party APIs may have rate limits — implement caching or a backoff strategy as needed.

---

## Contributing

Contributions are welcome! Please open issues or pull requests for bug fixes, additional tools, or documentation improvements. Suggested workflow:

1. Fork the repo
2. Create a feature branch
3. Add tests / update docs
4. Open a PR and describe the change
