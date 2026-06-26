# ✈️ AI Travel Planning System

An Advanced AI-powered **Travel Planning System** built on a **6-Agent LangGraph Pipeline** that delivers complete, real-time travel plans from a single natural language query.

The system integrates **Tavily MCP** for real-time web search, **Pinecone RAG** for verified destination knowledge retrieval, **OpenWeatherMap** for live weather data, and **Groq LLaMA 3.3 70B** for high-speed reasoning — all orchestrated by **LangGraph** in a sequential multi-agent pipeline.

Each Agent has a single focused responsibility and passes enriched context to the next stage. The result is a grounded, accurate **Travel Itinerary** built entirely from live data — not LLM memory alone. The system also maintains persistent session memory using **Supabase Cloud PostgreSQL** via LangGraph checkpointing, so context is preserved across queries.

---

## 🚀 Key Highlights

- 🤖 **Multi-Agent Orchestration** using **LangGraph**
- 🌐 **Real-Time Web Search** via **Tavily Remote MCP Server**
- 🔍 **Destination Knowledge Retrieval** via **Pinecone RAG**
- 🧠 **High-Speed Inference** using **Groq LLaMA 3.3 70B**
- 🌤️ **Live Weather & Forecast** via **OpenWeatherMap API**
- 🚆 **Smart Travel Mode Detection** — trains and buses for short trips, flights for international
- 💰 **Complete Budget Breakdown in INR** across budget, mid-range and luxury options
- 🐘 **Persistent Session Memory** via **Supabase Cloud PostgreSQL**
- 🖥️ **Interactive Web UI** built with **Streamlit**

---

## ⭐ Key Features

- **Real-Time Travel Intelligence** — integrates live APIs for flights, hotels and weather to provide up-to-date recommendations with source links
- **RAG-Powered Research** — retrieves verified destination knowledge from a **Pinecone** vector database instead of relying on LLM training data
- **MCP Integration** — connects to **Tavily's Remote MCP Server** for standardized real-time web search across Flight and Hotel agents
- **Smart Transport Detection** — automatically identifies trip type and suggests the most suitable transport: trains and buses for short domestic trips, flights for long-distance and international
- **Context-Aware Planning** — maintains session history using **Supabase PostgreSQL** so the system remembers previous queries
- **INR Budget Planning** — dedicated Budget Agent calculates complete trip costs in Indian Rupees across three scenarios
- **Scalable Architecture** — modular agent design makes it easy to add new agents like Visa Agent, Activity Agent or Currency Agent

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

Each agent receives the full output of all previous agents — building a richer, more accurate plan at every step.

---

## 🔹 Agent Details

### 🔬 Research Agent — Pinecone RAG
Queries the **Pinecone** vector database to retrieve verified destination knowledge including visa requirements for Indian citizens, best time to visit, local currency and money tips, cultural etiquette, local transportation options and safety guidelines. By grounding the LLM in retrieved facts rather than training data alone, the research brief is specific, accurate and up to date. The LLM synthesizes the retrieved chunks into a clean, structured research brief that feeds all subsequent agents.

---

### 🚆 Travel Agent — Tavily MCP
Automatically detects the trip type before searching. Short-distance domestic trips under 500km like Pune to Nashik get **trains, buses and cabs only** — the LLM is explicitly instructed not to suggest flights. Long-distance domestic trips get both trains and flights with a value-for-money comparison. International trips get airlines, flight durations from major Indian cities and fare ranges in INR. All results are sourced from **Tavily MCP** with real booking platform links.

---

### 🏨 Hotel Agent — Tavily MCP
Searches **Tavily MCP** for current hotel options at the destination across budget, mid-range and luxury categories. Returns hotel names, approximate prices per night in INR, best areas to stay and direct booking links from platforms like MakeMyTrip, Booking.com and Hotels.com. The LLM summarizes and ranks the options based on value and location.

---

### 🌤️ Weather Agent — OpenWeatherMap API
Fetches live current weather conditions and a 5-period short-term forecast directly from the **OpenWeatherMap API**. Captures temperature, feels-like temperature, humidity, wind speed and weather conditions. The LLM interprets the data and adds practical travel recommendations — clothing and packing tips, weather-appropriate activity suggestions and any weather warnings the traveler should be aware of.

---

### 💰 Budget Agent — Groq LLaMA 3.3 70B
Takes the travel and hotel information from previous agents and generates a complete trip cost breakdown in **INR**. Covers flights or ground transport, accommodation per night and total, daily food budget across budget and splurge options, local transportation, activities and sightseeing, shopping and miscellaneous, and travel insurance. Provides three total trip cost scenarios — budget, mid-range and luxury — with practical money-saving tips.

---

### 🗓️ Itinerary Agent — Groq LLaMA 3.3 70B
Acts as the final synthesis layer. Takes all outputs from the Research, Travel, Hotel, Weather and Budget agents and generates a comprehensive **day-by-day Travel Itinerary** with specific timings, hotel and transport recommendations, must-try local foods for each day, daily budget estimates in INR, visa and cultural reminders, and a list of useful apps and emergency contacts for the destination.

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

LinkedIn: https://www.linkedin.com/in/mandarborhade

GitHub: https://github.com/mandar7-star

🌐 Live Demo: https://ai-travel-planning-systems.streamlit.app

