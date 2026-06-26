# ✈️ AI Travel Planning System

An AI-powered travel planning system built on a **6-agent LangGraph pipeline** that combines **Tavily MCP**, **Pinecone RAG**, **OpenWeatherMap**, and **Groq LLaMA 3.3 70B** to deliver complete, real-time travel plans from a single query.

Six specialized agents run in sequence — each fetching real data from a different source and passing enriched context to the next — resulting in a grounded, accurate itinerary built from live information rather than LLM memory alone.

---

## 🚀 Key Highlights

- 🤖 **Multi-Agent Orchestration** using **LangGraph**
- 🌐 **Real-Time Web Search** via **Tavily Remote MCP Server**
- 🔍 **Destination Knowledge Retrieval** via **Pinecone RAG**
- 🧠 **High-Speed Inference** using **Groq LLaMA 3.3 70B**
- 🌤️ **Live Weather & Forecast** via **OpenWeatherMap API**
- 🚆 **Smart Travel Mode Detection** — trains and buses for short trips, flights for international
- 💰 **Budget Breakdown in INR** across budget, mid-range and luxury options
- 🐘 **Persistent Session Memory** via **Supabase Cloud PostgreSQL**
- 🖥️ **Interactive Web UI** built with **Streamlit**

---

## 🧠 System Architecture

```
User Query
    ↓
Research Agent  →  Pinecone RAG
    ↓
Travel Agent    →  Tavily MCP
    ↓
Hotel Agent     →  Tavily MCP
    ↓
Weather Agent   →  OpenWeatherMap API
    ↓
Budget Agent    →  Groq LLaMA 3.3 70B
    ↓
Itinerary Agent →  Groq LLaMA 3.3 70B
```

---

## 🔹 Agent Details

### 🔬 Research Agent — Pinecone RAG
Queries the **Pinecone** vector database to retrieve verified destination knowledge — visa requirements, best time to visit, local currency, cultural etiquette and safety tips. Grounds the LLM in real retrieved facts rather than training data alone.

---

### 🚆 Travel Agent — Tavily MCP
Detects trip type automatically. Short-distance domestic trips (under 500km) get **trains, buses and cabs only** — no flights. Long-distance domestic gets trains and flights. International gets flights with fare ranges in INR. All results come from **Tavily MCP** with real source links.

---

### 🏨 Hotel Agent — Tavily MCP
Searches **Tavily MCP** for current hotel options across budget, mid-range and luxury categories with prices in INR, best areas to stay, and direct booking links from platforms like MakeMyTrip and Booking.com.

---

### 🌤️ Weather Agent — OpenWeatherMap API
Fetches live current weather and a 5-period forecast from **OpenWeatherMap**. Includes temperature, humidity, wind speed and conditions. The LLM adds packing recommendations and weather-based activity tips.

---

### 💰 Budget Agent — Groq LLaMA 3.3 70B
Generates a complete trip cost breakdown in **INR** covering flights, accommodation, daily food, local transport, activities, shopping and travel insurance. Provides three total cost scenarios — budget, mid-range and luxury.

---

### 🗓️ Itinerary Agent — Groq LLaMA 3.3 70B
Synthesizes all previous agent outputs into a complete **day-by-day Travel Itinerary** with timings, hotel and transport recommendations, local food suggestions, daily budget in INR, visa and cultural reminders, and useful apps for the destination.

---

## 🏗️ Project Structure

```
AI_Travel_Planning_System/
├── main.py                  # LangGraph pipeline — 6 agents
├── frontend.py              # Streamlit web UI
├── tools.py                 # Tavily MCP, Pinecone RAG, Weather tools
├── ingest_knowledge.py      # Run once to populate Pinecone
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## ⚙️ Tech Stack

| Category | Technology |
|---|---|
| LLM | Groq — LLaMA 3.3 70B Versatile |
| Agent Orchestration | LangGraph |
| Framework | LangChain |
| MCP | Tavily Remote MCP Server |
| RAG | Pinecone Vector Database |
| Web Search | Tavily Search API |
| Weather | OpenWeatherMap API |
| Database | Supabase (Cloud PostgreSQL) |
| Frontend | Streamlit |

---

## 🔑 API Keys Required

| Service | Link |
|---|---|
| Groq | https://console.groq.com |
| Tavily | https://www.tavily.com |
| OpenWeatherMap | https://openweathermap.org/api |
| Pinecone | https://pinecone.io |
| Supabase | https://supabase.com |

---

## 🔐 Environment Variables

Create a `.env` file in the project root (see `.env.example`):

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENWEATHER_API_KEY=your_openweathermap_api_key
PINECONE_API_KEY=your_pinecone_api_key
DATABASE_URL=postgresql://username:password@host:5432/db_name
```

> ⚠️ Never commit your `.env` file. It is already in `.gitignore`.

---

## 🧪 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/mandar7-star/AI-Travel-Planning-System.git
cd AI-Travel-Planning-System
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Supabase

1. Create a free account at https://supabase.com
2. Create a new project
3. Go to **Connect → Session pooler** and copy the URI
4. Add it to your `.env` as `DATABASE_URL`

### 5. Set up Pinecone and populate knowledge base

1. Create a free account at https://pinecone.io
2. Create an index named `travel-knowledge` with model `llama-text-embed-v2`
3. Add your API key to `.env` as `PINECONE_API_KEY`
4. Run once to populate the knowledge base:

```bash
python ingest_knowledge.py
```

---

## ▶️ Run the Application

```bash
streamlit run frontend.py
```

---

## ☁️ Cloud Deployment (Streamlit Cloud)

1. Push your code to GitHub
2. Go to https://share.streamlit.io → **Create app**
3. Set **Main file path** to `frontend.py`
4. Go to **Advanced settings → Secrets** and paste:

```toml
GROQ_API_KEY = "your_key"
TAVILY_API_KEY = "your_key"
OPENWEATHER_API_KEY = "your_key"
PINECONE_API_KEY = "your_key"
DATABASE_URL = "your_supabase_pooler_url"
```

5. Click **Deploy**

---

## 💡 Example Queries

```
Plan a complete 7-day Japan trip under ₹2 lakhs including flights, hotels and sightseeing
```
```
5-day Paris trip for a couple with hotel recommendations
```
```
Pune to Nashik 2-day trip
```
```
Dubai weekend getaway from Mumbai
```

---

## 🖥️ UI Preview

### 🏠 Homepage
<img src="screenshots/home.png" width="800"/>

### 🤖 Agent Pipeline Live
<img src="screenshots/pipeline.png" width="800"/>

### 📊 Final Output
<img src="screenshots/result.png" width="800"/>

---

## 🎯 Use Cases

- Multi-Agent AI System Demonstration
- Real-Time RAG + MCP Integration Project
- Portfolio Project for AI/ML Roles
- Base for Building Production AI Travel Assistants

---

## 👨‍💻 Author

**Mandar Borhade**

Linkedin: https://www.linkedin.com/in/mandarborhade
GitHub: https://github.com/mandar7-star