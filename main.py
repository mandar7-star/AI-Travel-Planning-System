import os
import operator
import psycopg
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, SystemMessage
from langchain_groq import ChatGroq
from tools import (
    search_web,
    get_current_weather,
    get_forecast,
    search_destination_knowledge,
    extract_destination
)

load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")
llm          = ChatGroq(model="llama-3.3-70b-versatile")


# ── State ──
class TravelState(TypedDict):
    messages:         Annotated[list[AnyMessage], operator.add]
    user_query:       str
    research_results: str
    flight_results:   str
    hotel_results:    str
    weather_results:  str
    budget_results:   str
    itinerary:        str
    llm_calls:        int


# ── Agent 1: Research Agent (RAG + Pinecone) ──
def research_agent(state: TravelState):
    print("\nINSIDE RESEARCH AGENT\n")
    query       = state["user_query"]
    destination = extract_destination(query)
    rag_data    = search_destination_knowledge(destination)

    prompt = f"""
    You are a travel research expert.
    User Query: {query}
    Destination: {destination}
    {"Retrieved Knowledge from Database:\n" + rag_data if rag_data else ""}

    Provide a detailed research brief:
    1. Visa requirements for Indian citizens
    2. Best time to visit
    3. Local currency and money tips
    4. Cultural tips and etiquette
    5. Local transportation options
    6. Safety tips
    """
    response = llm.invoke([
        SystemMessage(content="You are an expert travel researcher. Be specific and practical."),
        HumanMessage(content=prompt)
    ])
    return {
        "research_results": response.content,
        "messages":         [AIMessage(content="Research completed")],
        "llm_calls":        state.get("llm_calls", 0) + 1
    }


# ── Agent 2: Travel Agent (Tavily MCP + LLM) ──

# Known international countries — if destination matches, it's international
INTERNATIONAL_KEYWORDS = [
    "japan", "france", "paris", "dubai", "uae", "thailand", "bangkok",
    "bali", "indonesia", "singapore", "malaysia", "usa", "america",
    "uk", "london", "australia", "canada", "germany", "italy", "rome",
    "spain", "china", "nepal", "sri lanka", "maldives", "europe"
]

def detect_trip_type(query: str) -> str:
    """Detect trip type without relying on LLM classification."""
    q_lower = query.lower()

    # Check for international keywords
    for kw in INTERNATIONAL_KEYWORDS:
        if kw in q_lower:
            return "INTERNATIONAL"

    # If query contains two Indian cities it's domestic
    # Ask LLM only to estimate distance in km
    distance_response = llm.invoke(
        f"What is the approximate road distance in kilometers between the two places mentioned in this query?\n"
        f"Return ONLY a number. If only one place mentioned or it is international return 9999.\n"
        f"Query: {query}"
    ).content.strip()

    try:
        distance = int(''.join(filter(str.isdigit, distance_response.split('.')[0])))
    except Exception:
        distance = 9999

    print(f"Estimated distance: {distance} km")

    if distance <= 500:
        return "DOMESTIC_SHORT"
    elif distance <= 9000:
        return "DOMESTIC_LONG"
    else:
        return "INTERNATIONAL"


def travel_agent(state: TravelState):
    print("\nINSIDE TRAVEL AGENT\n")
    query     = state["user_query"]
    trip_type = detect_trip_type(query)
    print(f"Trip type: {trip_type}")

    if trip_type == "DOMESTIC_SHORT":
        search_data = search_web(f"train bus cab options {query}")
        system_msg  = (
            "You are a local India transport expert. "
            "Suggest ONLY ground transport — trains, buses, shared cabs, auto, private taxi. "
            "NEVER mention flights for short distances under 500km. "
            "All prices in INR."
        )
        prompt_body = f"""
        User Query: {query}
        This is a SHORT DISTANCE trip under 500km. Do NOT suggest flights.

        Search Results:
        {search_data}

        Provide ONLY ground transport:
        1. Train options — train names, duration, fare in INR, book on IRCTC (irctc.co.in)
        2. Bus options — operator names, duration, fare in INR, book on RedBus (redbus.in)
        3. Cab/taxi — estimated fare in INR (Ola, Uber, local)
        4. Best recommended option with reason
        5. Booking links
        """

    elif trip_type == "DOMESTIC_LONG":
        search_data = search_web(f"train flight options {query} India 2025")
        system_msg  = (
            "You are a domestic India travel expert. "
            "Suggest trains and flights. All prices in INR."
        )
        prompt_body = f"""
        User Query: {query}
        This is a LONG DISTANCE domestic trip.

        Search Results:
        {search_data}

        Provide:
        1. Train options — names, duration, fare in INR (sleeper/3AC/2AC)
        2. Flight options — airlines, duration, fare in INR
        3. Which is best value for money and why
        4. Booking platforms — IRCTC, MakeMyTrip, Ixigo with links
        """

    else:
        destination = extract_destination(query)
        search_data = search_web(f"flights to {destination} from India price 2025")
        system_msg  = (
            "You are an international flight expert. "
            "All prices in INR."
        )
        prompt_body = f"""
        User Query: {query}
        This is an INTERNATIONAL trip.

        Search Results:
        {search_data}

        Provide:
        1. Best airlines flying from India to {destination}
        2. Flight duration from Mumbai, Delhi, Bangalore
        3. Economy and business fares in INR
        4. Best time to book
        5. Booking platforms with links
        """

    response = llm.invoke([
        SystemMessage(content=system_msg),
        HumanMessage(content=prompt_body)
    ])
    return {
        "flight_results": response.content,
        "messages":       [AIMessage(content="Travel options researched")],
        "llm_calls":      state.get("llm_calls", 0) + 1
    }


# ── Agent 3: Hotel Agent (Tavily MCP + LLM) ──
def hotel_agent(state: TravelState):
    print("\nINSIDE HOTEL AGENT\n")
    query       = state["user_query"]
    destination = extract_destination(query)
    search_data = search_web(f"best hotels in {destination} prices ratings booking 2025")

    response = llm.invoke([
        SystemMessage(content="You are an expert accommodation advisor. Use search results to recommend hotels with source links. Always show prices in Indian Rupees (INR)."),
        HumanMessage(content=f"""
        User Query: {query}
        Destination: {destination}

        Web Search Results:
        {search_data}

        Provide:
        1. Top budget hotels with prices per night in INR
        2. Top mid-range hotels with prices per night in INR
        3. Top luxury hotels with prices per night in INR
        4. Best areas to stay in {destination}
        5. Booking tips and platforms with source links
        """)
    ])
    return {
        "hotel_results": response.content,
        "messages":      [AIMessage(content="Hotel research completed")],
        "llm_calls":     state.get("llm_calls", 0) + 1
    }


# ── Agent 4: Weather Agent (OpenWeatherMap + LLM) ──
def weather_agent(state: TravelState):
    print("\nINSIDE WEATHER AGENT\n")
    destination = extract_destination(state["user_query"])

    try:
        country_code = llm.invoke(
            f"What is the 2-letter ISO country code for {destination}? Return ONLY the 2-letter code."
        ).content.strip().upper()
        city_query = f"{destination},{country_code}" if len(country_code) == 2 and country_code.isalpha() else destination
    except Exception:
        city_query = destination

    # Try with country code first, fallback to destination name only
    weather_data = get_current_weather(city_query)
    if "unavailable" in weather_data.lower():
        weather_data = get_current_weather(destination)

    forecast_data = get_forecast(city_query)
    if "unavailable" in forecast_data.lower():
        forecast_data = get_forecast(destination)

    response = llm.invoke([
        SystemMessage(content="You are a travel weather advisor."),
        HumanMessage(content=f"""
        Destination: {destination}
        Current Weather: {weather_data}
        Forecast: {forecast_data}

        Provide:
        1. Summary of current conditions
        2. What to expect during the trip
        3. Recommended clothing and packing list
        4. Weather-based activity suggestions
        5. Any weather warnings or precautions
        """)
    ])
    return {
        "weather_results": f"**Live Weather:**\n{weather_data}\n\n**Forecast:**\n{forecast_data}\n\n**Weather Advisory:**\n{response.content}",
        "messages":        [AIMessage(content="Weather data fetched")],
        "llm_calls":       state.get("llm_calls", 0) + 1
    }


# ── Agent 5: Budget Agent (LLM) ──
def budget_agent(state: TravelState):
    print("\nINSIDE BUDGET AGENT\n")
    response = llm.invoke([
        SystemMessage(content="You are an expert travel budget planner. Always provide ALL costs in Indian Rupees (INR ₹). Give realistic cost breakdowns."),
        HumanMessage(content=f"""
        User Query: {state['user_query']}
        Flight Info: {state['flight_results']}
        Hotel Info: {state['hotel_results']}

        Provide complete budget breakdown in INR (₹):
        1. Flight costs in ₹
        2. Accommodation costs per night and total in ₹
        3. Daily food budget in ₹ (budget / mid-range / splurge)
        4. Local transportation costs in ₹
        5. Activities and sightseeing costs in ₹
        6. Shopping and miscellaneous in ₹
        7. Travel insurance estimate in ₹
        8. Total trip cost in ₹ (budget / mid-range / luxury options)
        9. Money-saving tips
        """)
    ])
    return {
        "budget_results": response.content,
        "messages":       [AIMessage(content="Budget calculated")],
        "llm_calls":      state.get("llm_calls", 0) + 1
    }


# ── Agent 6: Itinerary Agent (LLM — synthesizes all) ──
def itinerary_agent(state: TravelState):
    print("\nINSIDE ITINERARY AGENT\n")
    response = llm.invoke([
        SystemMessage(content="You are an expert travel planner. Create a comprehensive day-by-day itinerary. Show all costs in Indian Rupees (INR ₹)."),
        HumanMessage(content=f"""
        User Query: {state['user_query']}
        Research: {state['research_results']}
        Flights: {state['flight_results']}
        Hotels: {state['hotel_results']}
        Weather: {state['weather_results']}
        Budget: {state['budget_results']}

        Create:
        1. Complete day-by-day itinerary with timings
        2. Hotel recommendation with reason
        3. Flight recommendation
        4. Must-try local foods each day
        5. Daily budget estimate in ₹
        6. Important reminders (visa, currency, culture)
        7. Useful apps and emergency contacts
        """)
    ])
    return {
        "itinerary": response.content,
        "messages":  [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


# ── LangGraph Pipeline ──
graph = StateGraph(TravelState)
graph.add_node("research_agent",  research_agent)
graph.add_node("flight_agent",    travel_agent)
graph.add_node("hotel_agent",     hotel_agent)
graph.add_node("weather_agent",   weather_agent)
graph.add_node("budget_agent",    budget_agent)
graph.add_node("itinerary_agent", itinerary_agent)

graph.add_edge(START,             "research_agent")
graph.add_edge("research_agent",  "flight_agent")
graph.add_edge("flight_agent",    "hotel_agent")
graph.add_edge("hotel_agent",     "weather_agent")
graph.add_edge("weather_agent",   "budget_agent")
graph.add_edge("budget_agent",    "itinerary_agent")
graph.add_edge("itinerary_agent", END)

# ── PostgreSQL Checkpointing (Supabase) ──
_conn        = psycopg.connect(DATABASE_URL, autocommit=True)
checkpointer = PostgresSaver(_conn)
try:
    checkpointer.setup()
except Exception:
    pass

app = graph.compile(checkpointer=checkpointer)