import os
import json
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv(override=True)

TAVILY_API_KEY      = os.getenv("TAVILY_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
PINECONE_API_KEY    = os.getenv("PINECONE_API_KEY")

llm = ChatGroq(model="llama-3.3-70b-versatile")


# ── Tavily Search (Direct API — same data as MCP) ──
def search_web(query: str, max_results: int = 5) -> str:
    """Search web via Tavily API."""
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            headers={"Content-Type": "application/json"},
            json={
                "api_key":     TAVILY_API_KEY,
                "query":       query,
                "max_results": max_results
            },
            timeout=15
        )
        results = response.json().get("results", [])
        if not results:
            return "No results found."
        lines = []
        for i, item in enumerate(results, 1):
            title   = item.get("title", "No title")
            url     = item.get("url", "")
            content = item.get("content", "").strip()
            snippet = content[:250] + ("..." if len(content) > 250 else "")
            lines.append(f"**{i}. [{title}]({url})**")
            if snippet:
                lines.append(snippet)
            lines.append(f"🔗 {url}\n")
        return "\n".join(lines)
    except Exception as e:
        return f"Search unavailable: {str(e)}"


# ── OpenWeatherMap Direct API ──
def get_current_weather(city: str) -> str:
    """Get live weather from OpenWeatherMap."""
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"},
            timeout=10
        )
        data = response.json()
        if response.status_code != 200:
            return f"Weather unavailable: {data.get('message', 'Unknown error')}"
        return (
            f"📍 City: {data['name']}\n"
            f"🌡️ Temperature: {data['main']['temp']}°C "
            f"(Feels like {data['main']['feels_like']}°C)\n"
            f"💧 Humidity: {data['main']['humidity']}%\n"
            f"🌤️ Condition: {data['weather'][0]['description'].title()}\n"
            f"💨 Wind Speed: {data['wind']['speed']} m/s"
        )
    except Exception as e:
        return f"Weather unavailable: {str(e)}"


def get_forecast(city: str) -> str:
    """Get 5-period forecast from OpenWeatherMap."""
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params={"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"},
            timeout=10
        )
        data = response.json()
        if response.status_code != 200:
            return f"Forecast unavailable: {data.get('message', 'Unknown error')}"
        lines = [f"📍 5-Period Forecast for {city}:"]
        for item in data["list"][:5]:
            lines.append(
                f"  • {item['dt_txt']} — "
                f"{item['main']['temp']}°C, "
                f"{item['weather'][0]['description'].title()}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Forecast unavailable: {str(e)}"


# ── Pinecone RAG ──
def search_destination_knowledge(destination: str) -> str:
    """Search Pinecone vector DB for destination travel knowledge."""
    try:
        from pinecone import Pinecone
        pc    = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index("travel-knowledge")

        embedding = pc.inference.embed(
            model="llama-text-embed-v2",
            inputs=[f"Travel information about {destination}"],
            parameters={"input_type": "query"}
        )
        results = index.query(
            vector=embedding[0].values,
            top_k=5,
            include_metadata=True
        )
        knowledge = [
            match.metadata.get("text", "")
            for match in results.matches
            if match.score > 0.3 and match.metadata.get("text")
        ]
        return "\n\n".join(knowledge) if knowledge else ""
    except Exception:
        return ""


# ── Utility ──
def extract_destination(query: str) -> str:
    prompt = (
        f"Extract only the destination city or country name from this travel query. "
        f"Return ONLY the city or country name, nothing else.\n\nQuery: {query}"
    )
    return llm.invoke(prompt).content.strip()