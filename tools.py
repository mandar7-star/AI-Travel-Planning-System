import os
import asyncio
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv(override=True)

TAVILY_API_KEY      = os.getenv("TAVILY_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
PINECONE_API_KEY    = os.getenv("PINECONE_API_KEY")

llm = ChatGroq(model="llama-3.3-70b-versatile")

# ── Tavily MCP Client (Remote HTTP MCP Server) ──
mcp_client = MultiServerMCPClient(
    {
        "tavily": {
            "transport": "streamable_http",
            "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
        }
    }
)

_tavily_tool = None

async def _get_tavily_tool():
    global _tavily_tool
    if _tavily_tool is None:
        tools       = await mcp_client.get_tools()
        _tavily_tool = next((t for t in tools if t.name == "tavily_search"), None)
        if not _tavily_tool:
            raise RuntimeError("tavily_search tool not found")
    return _tavily_tool


def _parse_tavily_result(result) -> str:
    import json
    raw = ""
    if isinstance(result, str):
        raw = result
    elif isinstance(result, list):
        for item in result:
            if hasattr(item, "text") and item.text:
                raw += item.text
            elif isinstance(item, dict) and item.get("text"):
                raw += item["text"]
    elif isinstance(result, dict):
        raw = json.dumps(result)

    if not raw:
        return str(result)

    try:
        data    = json.loads(raw)
        results = data.get("results", [])
        if not results:
            return raw
        lines = []
        for i, item in enumerate(results[:5], 1):
            title   = item.get("title", "No title")
            url     = item.get("url", "")
            content = item.get("content", "").strip()
            snippet = content[:250] + ("..." if len(content) > 250 else "")
            lines.append(f"**{i}. [{title}]({url})**")
            if snippet:
                lines.append(snippet)
            lines.append(f"🔗 {url}\n")
        return "\n".join(lines)
    except Exception:
        return raw


async def tavily_search_async(query: str) -> str:
    tool   = await _get_tavily_tool()
    result = await tool.ainvoke({"query": query})
    return _parse_tavily_result(result)


def search_web(query: str) -> str:
    """Search web via Tavily MCP server."""
    return asyncio.run(tavily_search_async(query))


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
        results   = index.query(
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