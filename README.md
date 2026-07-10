# 🍳 Recipe Preparation Agent
**RAG-based AI cooking assistant powered by IBM watsonx.ai (Granite)**

> Input your available ingredients → get tailored recipes, step-by-step instructions,
> smart substitutions, dietary adjustments, and cooking tips — all powered by
> IBM Granite running on IBM Cloud Lite.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Recipe Agent System                         │
│                                                                  │
│  User Browser                                                    │
│  ┌──────────────┐    HTTP/JSON    ┌──────────────────────────┐   │
│  │  Chat UI     │ ─────────────► │  FastAPI Backend          │   │
│  │  (HTML/CSS/  │ ◄────────────  │  /api/chat                │   │
│  │   Vanilla JS)│                │  /api/recipes             │   │
│  └──────────────┘                └──────────┬───────────────┘   │
│                                             │                    │
│                              ┌──────────────▼───────────────┐   │
│                              │    Core Agent Logic           │   │
│                              │  • Ingredient Parser          │   │
│                              │  • Diet Preference Detector   │   │
│                              └──────────┬────────────────────┘   │
│                                         │                        │
│                       ┌─────────────────▼──────────────────┐    │
│                       │         RAG Pipeline                │    │
│                       │  ┌────────────────────────────┐    │    │
│                       │  │  Recipe Corpus (JSON)       │    │    │
│                       │  │  20 recipes across 10 cats  │    │    │
│                       │  └────────────┬───────────────┘    │    │
│                       │               │ encode              │    │
│                       │  ┌────────────▼───────────────┐    │    │
│                       │  │  sentence-transformers      │    │    │
│                       │  │  (all-MiniLM-L6-v2)         │    │    │
│                       │  └────────────┬───────────────┘    │    │
│                       │               │ vectors             │    │
│                       │  ┌────────────▼───────────────┐    │    │
│                       │  │  FAISS Index (cosine sim)   │    │    │
│                       │  │  Top-K retrieval            │    │    │
│                       │  └────────────────────────────┘    │    │
│                       └─────────────────┬──────────────────┘    │
│                                         │ top-3 recipes          │
│                       ┌─────────────────▼──────────────────┐    │
│                       │    IBM watsonx.ai (Granite)         │    │
│                       │    ibm/granite-13b-instruct-v2      │    │
│                       │    IBM Cloud Lite (free tier)       │    │
│                       └────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | IBM Granite 13B Instruct v2 (via IBM watsonx.ai) |
| Cloud | IBM Cloud Lite (free tier) |
| Embeddings | `sentence-transformers` – `all-MiniLM-L6-v2` (local) |
| Vector Store | FAISS (CPU, in-process) |
| Backend | FastAPI + Uvicorn |
| Frontend | Vanilla HTML / CSS / JavaScript |
| Recipe Corpus | 20 hand-crafted recipes (JSON) |

---

## Prerequisites

- Python **3.10+**
- An **IBM Cloud** account (free Lite tier): https://cloud.ibm.com/registration
- An **IBM watsonx.ai** project

---

## Setup

### 1. Clone / navigate to the project

```bash
cd "Recipe Agent"
```

### 2. Create a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure IBM watsonx.ai credentials

```bash
cp .env.example .env
```

Edit `.env` and fill in your IBM Cloud details:

```env
WATSONX_API_KEY=your_ibm_cloud_api_key_here
WATSONX_PROJECT_ID=your_watsonx_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
GRANITE_MODEL_ID=ibm/granite-13b-instruct-v2
```

#### Where to get these values:

| Value | Where to find it |
|-------|-----------------|
| `WATSONX_API_KEY` | IBM Cloud → Manage → Access (IAM) → API Keys |
| `WATSONX_PROJECT_ID` | watsonx.ai → Your project → Manage → General → Project ID |
| `WATSONX_URL` | Use `https://us-south.ml.cloud.ibm.com` for Dallas region |

> **Note:** The app works without credentials too — it uses a structured
> fallback response mode. Configure IBM credentials for full Granite AI responses.

### 5. Run the agent

```bash
python main.py
```

Open your browser at **http://localhost:8000**

---

## API Reference

### `POST /api/chat`

Chat with the agent.

**Request body:**
```json
{
  "message": "I have eggs, pasta, garlic and olive oil",
  "history": [
    {"role": "user", "content": "I'm vegetarian"},
    {"role": "assistant", "content": "..."}
  ]
}
```

**Response:**
```json
{
  "reply": "Based on your ingredients, here are my suggestions...",
  "recipes": [ { "id": "R001", "name": "Classic Spaghetti Aglio e Olio", ... } ],
  "ingredients": ["eggs", "pasta", "garlic", "olive oil"],
  "diet_prefs": ["vegetarian"]
}
```

### `GET /api/recipes`

Browse all recipes. Optional query params:
- `?search=pasta` — semantic search
- `?diet=vegan` — filter by diet
- `?category=soup` — filter by category

### `GET /health`

Returns `{"status": "ok", "model": "ibm/granite-13b-instruct-v2"}`

---

## Project Structure

```
Recipe Agent/
├── main.py                         # Entry point (uvicorn launcher)
├── requirements.txt
├── .env.example                    # Credentials template
├── recipe_agent/
│   ├── core/
│   │   ├── config.py               # Settings from .env
│   │   ├── agent.py                # Main agent orchestration
│   │   ├── embeddings.py           # FAISS index + retrieval
│   │   └── llm.py                  # IBM Granite wrapper
│   ├── api/
│   │   └── app.py                  # FastAPI app + endpoints
│   ├── data/
│   │   └── recipes.json            # 20 recipe knowledge base
│   ├── templates/
│   │   └── index.html              # Chat UI
│   └── static/
│       ├── css/style.css
│       └── js/app.js
```

---

## Features

- **RAG-powered suggestions** — FAISS semantic search over 20 recipe corpus
- **IBM Granite LLM** — personalised instructions, substitutions and tips
- **Diet detection** — auto-detects vegan / vegetarian / keto / gluten-free etc.
- **Ingredient parsing** — extracts ingredients from natural language
- **Multi-turn chat** — maintains conversation context (last 4 turns)
- **Recipe cards** — click any recipe in the sidebar for full details
- **Substitution table** — per-recipe ingredient swap suggestions
- **Fallback mode** — works without IBM credentials for local demos
- **Food waste focus** — recipes matched to what you already have

---

## Sample Conversations

```
User: I have eggs, pasta, garlic, olive oil and parsley
Agent: Here are your best options: Classic Spaghetti Aglio e Olio ...

User: I'm vegan and have chickpeas, tomatoes, garlic and ginger
Agent: Perfect for Chana Masala! Here's how to make it with your ingredients...

User: Can I substitute fresh garlic?
Agent: Absolutely — use 1/2 tsp garlic powder per clove needed...
```

---

## IBM Cloud Lite Setup Guide

1. Register at https://cloud.ibm.com/registration (free, no credit card needed for Lite)
2. Create a **watsonx.ai** service instance
3. Create a new **Project** in watsonx.ai
4. Generate an **API Key** under IAM → API Keys
5. Copy Project ID from Project → Manage → General
6. Set values in `.env`

---

*Built with IBM watsonx.ai (Granite) — reducing food waste, one recipe at a time.*
https://drive.google.com/file/d/1EZql3OZjOU87dFtQK-NZkuQd88Cycy4n/view?usp=sharing
