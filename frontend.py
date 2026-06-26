import os
import streamlit as st
from datetime import datetime
from langchain_core.messages import HumanMessage
from main import app

st.set_page_config(page_title="AI Travel Planning System", page_icon="✈️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, .stApp { font-family: 'Inter', sans-serif; background: #FFFFFF; }
.hero-wrapper { position: relative; border-radius: 20px; overflow: hidden; margin-bottom: 2rem; min-height: 280px; }
.hero-content { position: relative; z-index: 2; min-height: 280px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 2.5rem 2rem; }
.hero-badge { background: rgba(37,99,235,0.15); border: 1px solid rgba(255,255,255,0.5); color: #ffffff !important; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; padding: 0.3rem 0.9rem; border-radius: 20px; margin-bottom: 0.9rem; display: inline-block; }
.hero-title { font-size: 2.6rem; font-weight: 700; color: #ffffff; margin: 0 0 0.6rem; line-height: 1.2; text-shadow: 0 2px 20px rgba(0,0,0,0.4); }
.hero-sub { color: #f0f0f0; font-size: 1rem; max-width: 600px; text-shadow: 0 2px 10px rgba(0,0,0,0.4); }
.input-label { color: #2563EB; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.5rem; }
div[data-testid="stButton"] > button { background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important; color: #ffffff !important; border: none !important; border-radius: 12px !important; padding: 0.85rem 2.5rem !important; font-size: 1.05rem !important; font-weight: 700 !important; width: 100% !important; box-shadow: 0 4px 14px rgba(37,99,235,0.25) !important; transition: all 0.3s ease !important; }
div[data-testid="stButton"] > button:hover { box-shadow: 0 6px 20px rgba(37,99,235,0.35) !important; transform: translateY(-2px) !important; }
.sec-head { display: flex; align-items: center; gap: 0.6rem; margin: 2rem 0 0.75rem; padding-bottom: 0.5rem; border-bottom: 1px solid #E5E5E5; }
.sec-head span { font-size: 1.15rem; font-weight: 600; color: #111111; }
.metric-row { display: flex; gap: 1rem; margin: 1.5rem 0; }
.metric-box { flex: 1; background: #F7F9FF; border: 1px solid #E5E5E5; border-radius: 12px; padding: 1rem 1.2rem; text-align: center; }
.metric-val { font-size: 1.8rem; font-weight: 700; color: #2563EB; }
.metric-lbl { font-size: 0.78rem; color: #6B7280; margin-top: 0.2rem; text-transform: uppercase; letter-spacing: 0.08em; }
.weather-card { background: linear-gradient(135deg, #EFF6FF 0%, #F0F9FF 100%); border: 1px solid #BFDBFE; border-radius: 14px; padding: 1.4rem 1.6rem; margin-bottom: 1rem; }
.weather-title { font-size: 0.78rem; font-weight: 600; color: #2563EB; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.8rem; }
.final-card { background: #FFFFFF; border: 1px solid #E5E5E5; border-left: 4px solid #2563EB; border-radius: 14px; padding: 1.8rem; line-height: 1.8; color: #1F2937; font-size: 0.95rem; }
.save-bar { background: #F7F9FF; border: 1px solid #E5E5E5; border-radius: 10px; padding: 0.85rem 1.2rem; color: #6B7280; font-size: 0.88rem; margin-top: 0.5rem; }
.save-bar code { color: #1D4ED8 !important; background: #EFF4FF !important; }
section[data-testid="stSidebar"] { background: #F1F5F9 !important; border-right: 1px solid #E2E8F0 !important; }
section[data-testid="stSidebar"] * { color: #1E293B !important; }
.sb-tech-chip { display: flex; align-items: center; gap: 0.55rem; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.45rem 0.75rem; margin-bottom: 0.4rem; font-size: 0.82rem; }
.agent-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 0.75rem 0.9rem; margin-bottom: 0.55rem; position: relative; overflow: hidden; }
.agent-card-accent { position: absolute; left: 0; top: 0; bottom: 0; width: 3px; border-radius: 12px 0 0 12px; }
.agent-card-inner { display: flex; align-items: center; gap: 0.65rem; padding-left: 0.4rem; }
.agent-icon-box { width: 36px; height: 36px; border-radius: 9px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; flex-shrink: 0; }
.agent-name { font-size: 0.88rem !important; font-weight: 600 !important; color: #1E293B !important; }
.agent-desc { font-size: 0.72rem !important; color: #64748B !important; margin-top: 0.1rem !important; }
.agent-step { font-size: 0.65rem !important; font-weight: 700 !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; }
.agent-badge { font-size: 0.62rem; font-weight: 600; padding: 0.18rem 0.5rem; border-radius: 20px; letter-spacing: 0.05em; flex-shrink: 0; }
.agent-connector { text-align: center; color: #94A3B8; font-size: 0.75rem; margin: -0.15rem 0; }
.stTextArea textarea { background: #FFFFFF !important; border: 1.5px solid #D5D5D5 !important; border-radius: 10px !important; color: #111111 !important; font-size: 0.95rem !important; resize: none !important; }
.stTextArea textarea:focus { border-color: #2563EB !important; box-shadow: 0 0 0 2px rgba(37,99,235,0.15) !important; }
.stTextInput input { background: #FFFFFF !important; border: 1.5px solid #D5D5D5 !important; border-radius: 8px !important; color: #111111 !important; }
.stMarkdown p, .stMarkdown li { color: #1F2937 !important; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #111111 !important; }
.stMarkdown a { color: #2563EB !important; text-decoration: none !important; }
#MainMenu, footer, header { visibility: hidden; }
div[data-testid="stDownloadButton"] > button { background: #FFFFFF !important; color: #111111 !important; border: 1.5px solid #D5D5D5 !important; border-radius: 10px !important; }

/* Style st.status headers */

</style>
""", unsafe_allow_html=True)


# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style="padding:0.5rem 0 0.2rem;">
        <div style="font-size:1.25rem;font-weight:700;color:#1E293B;">✈️ AI Travel Planner</div>
        <div style="font-size:0.78rem;color:#64748B;margin-top:0.2rem;">LangGraph · MCP · RAG</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#E2E8F0;margin:0.8rem 0;'>", unsafe_allow_html=True)

    thread_id = st.text_input("👤 Session ID", value="mandar_traveller",
                               help="Maintains your session memory via PostgreSQL")

    st.markdown("<hr style='border-color:#E2E8F0;margin:0.8rem 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.72rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#1E293B;margin-bottom:0.6rem;'>⚡ Powered By</div>", unsafe_allow_html=True)

    TECHS = [
        ("🔗", "LangGraph",       "Multi-agent orchestration"),
        ("🧠", "Groq · LLaMA 3.3","70B reasoning engine"),
        ("🔍", "Pinecone RAG",    "Destination knowledge base"),
        ("🌐", "Tavily MCP",      "Remote MCP server — web search"),
        ("🌤️","OpenWeatherMap",  "Live weather data"),
        ("🐘", "Supabase",        "Cloud PostgreSQL memory"),
    ]
    for icon, name, desc in TECHS:
        st.markdown(f"""
        <div class="sb-tech-chip">
            <span style="font-size:1rem;">{icon}</span>
            <span><strong>{name}</strong>
                  <span style="color:#64748B;font-size:0.72rem;"> — {desc}</span>
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#E2E8F0;margin:0.8rem 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.72rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#1E293B;margin-bottom:0.6rem;'>🤖 Agent Pipeline</div>", unsafe_allow_html=True)

    AGENTS = [
        {"step":"01","icon":"🔬","name":"Research Agent", "desc":"RAG · Visa · Culture",    "badge":"Pinecone RAG","accent":"#6366F1","bg":"rgba(99,102,241,0.15)","badge_bg":"rgba(99,102,241,0.2)","badge_color":"#A5B4FC","step_color":"#6366F1"},
        {"step":"02","icon":"🚆","name":"Travel Agent",   "desc":"Flight · Train · Bus · Routes", "badge":"Tavily MCP", "accent":"#3B82F6","bg":"rgba(59,130,246,0.15)","badge_bg":"rgba(59,130,246,0.2)","badge_color":"#93C5FD","step_color":"#3B82F6"},
        {"step":"03","icon":"🏨","name":"Hotel Agent",    "desc":"Prices · Ratings · Links","badge":"Tavily MCP", "accent":"#8B5CF6","bg":"rgba(139,92,246,0.15)","badge_bg":"rgba(139,92,246,0.2)","badge_color":"#C4B5FD","step_color":"#8B5CF6"},
        {"step":"04","icon":"🌤️","name":"Weather Agent", "desc":"Live temp · Forecast",    "badge":"OpenWeather","accent":"#06B6D4","bg":"rgba(6,182,212,0.15)", "badge_bg":"rgba(6,182,212,0.2)", "badge_color":"#67E8F9","step_color":"#06B6D4"},
        {"step":"05","icon":"💰","name":"Budget Agent",   "desc":"Cost · Breakdown · Tips", "badge":"LLaMA 3.3",  "accent":"#F59E0B","bg":"rgba(245,158,11,0.15)","badge_bg":"rgba(245,158,11,0.2)","badge_color":"#FCD34D","step_color":"#F59E0B"},
        {"step":"06","icon":"🗓️","name":"Itinerary Agent","desc":"Day-by-day · Full plan",  "badge":"LLaMA 3.3",  "accent":"#10B981","bg":"rgba(16,185,129,0.15)","badge_bg":"rgba(16,185,129,0.2)","badge_color":"#6EE7B7","step_color":"#10B981"},
    ]
    for i, ag in enumerate(AGENTS):
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-card-accent" style="background:{ag['accent']};"></div>
            <div class="agent-card-inner">
                <div class="agent-icon-box" style="background:{ag['bg']};">{ag['icon']}</div>
                <div style="flex:1;">
                    <div class="agent-step" style="color:{ag['step_color']};">STEP {ag['step']}</div>
                    <div class="agent-name">{ag['name']}</div>
                    <div class="agent-desc">{ag['desc']}</div>
                </div>
                <div class="agent-badge" style="background:{ag['badge_bg']};color:{ag['badge_color']};border:1px solid {ag['badge_color']}33;">{ag['badge']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if i < len(AGENTS) - 1:
            st.markdown("<div class='agent-connector'>▼</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#E2E8F0;margin:0.8rem 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.72rem;color:#64748B;text-align:center;'>LangGraph · MCP · RAG · Groq</div>", unsafe_allow_html=True)


# ── Hero ──
st.markdown("""
<div class="hero-wrapper">
    <img style="width:100%;height:100%;object-fit:cover;filter:brightness(0.55);position:absolute;inset:0;"
         src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1400&q=80"/>
    <div class="hero-content">
        <div class="hero-badge">✦ LangGraph · MCP · RAG · Multi-Agent</div>
        <div class="hero-title">✈️ AI Travel Planning System</div>
        <div class="hero-sub">Six specialized AI agents — researching destinations with RAG, finding flights and hotels via Tavily MCP, checking live weather, calculating budgets and building your complete day-by-day itinerary.</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Destination Cards ──
DESTINATIONS = [
    ("🇯🇵 Tokyo",   "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=300&q=70"),
    ("🇫🇷 Paris",   "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=300&q=70"),
    ("🇹🇭 Bangkok", "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=300&q=70"),
    ("🇮🇹 Rome",    "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=300&q=70"),
    ("🇦🇪 Dubai",   "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=300&q=70"),
]
cols = st.columns(5)
for col, (name, img_url) in zip(cols, DESTINATIONS):
    with col:
        st.markdown(f"""
        <div style="border-radius:10px;overflow:hidden;position:relative;height:90px;border:1px solid #E5E5E5;">
            <img src="{img_url}" style="width:100%;height:100%;object-fit:cover;filter:brightness(0.6);"/>
            <div style="position:absolute;bottom:8px;left:0;right:0;text-align:center;color:#fff;font-size:0.8rem;font-weight:600;text-shadow:0 2px 10px rgba(0,0,0,0.6);">{name}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Query Input ──
st.markdown("<div class='input-label'>🗺️ Describe your trip</div>", unsafe_allow_html=True)

if "user_query" not in st.session_state:
    st.session_state["user_query"] = ""

QUICK = ["7-day Japan under ₹2L", "Paris trip for 5 days", "Dubai weekend trip", "Bali backpacking 10 days"]
qcols = st.columns(len(QUICK))
for qc, label in zip(qcols, QUICK):
    with qc:
        if st.button(label, key=f"q_{label}"):
            st.session_state["user_query"] = label

user_query = st.text_area(
    "", value=st.session_state["user_query"],
    placeholder="e.g. Plan a complete 7-day Japan trip including flights, hotels and sightseeing under ₹2 lakhs",
    height=100, label_visibility="collapsed"
)
st.session_state["user_query"] = user_query
generate = st.button("🚀  Generate My Travel Plan", use_container_width=True)

AGENT_META = {
    "research_agent":  ("🔬", "Research Agent"),
    "flight_agent":    ("🚆",  "Travel Agent"),
    "hotel_agent":     ("🏨",  "Hotel Agent"),
    "weather_agent":   ("🌤️", "Weather Agent"),
    "budget_agent":    ("💰",  "Budget Agent"),
    "itinerary_agent": ("🗓️", "Itinerary Agent"),
}


# ── Main Generation ──
if generate:
    if not user_query.strip():
        st.warning("Please describe your trip first.")
    else:
        config    = {"configurable": {"thread_id": thread_id}}
        collected = {
            "research_results": "",
            "flight_results":   "",
            "hotel_results":    "",
            "weather_results":  "",
            "budget_results":   "",
            "itinerary":        "",
            "llm_calls":        0,
        }

        st.markdown("---")
        st.markdown("<div class='sec-head'><span>🤖 Agent Pipeline — Live</span></div>", unsafe_allow_html=True)

        for chunk in app.stream(
            {
                "messages":         [HumanMessage(content=user_query)],
                "user_query":       user_query,
                "research_results": "",
                "flight_results":   "",
                "hotel_results":    "",
                "weather_results":  "",
                "budget_results":   "",
                "itinerary":        "",
                "llm_calls":        0,
            },
            config=config,
            stream_mode="updates",
        ):
            for node_name, state_update in chunk.items():
                icon, label = AGENT_META.get(node_name, ("🔧", node_name))

                # Bold black title header
                st.markdown(
                    f"<div style='background:#F1F5F9;color:#111111;border:1.5px solid #E2E8F0;padding:12px 18px;"
                    f"border-radius:10px 10px 0 0;font-size:1.1rem;font-weight:800;"
                    f"letter-spacing:0.03em;margin-top:1rem;'>{icon} {label}</div>",
                    unsafe_allow_html=True
                )

                with st.container(border=True):
                    if node_name == "research_agent":
                        text = state_update.get("research_results", "")
                        collected["research_results"] = text
                        st.markdown(text or "_No research data._")
                    elif node_name == "flight_agent":
                        text = state_update.get("flight_results", "")
                        collected["flight_results"] = text
                        st.markdown(text or "_No travel data._")
                    elif node_name == "hotel_agent":
                        text = state_update.get("hotel_results", "")
                        collected["hotel_results"] = text
                        st.markdown(text or "_No hotel data._")
                    elif node_name == "weather_agent":
                        text = state_update.get("weather_results", "")
                        collected["weather_results"] = text
                        if text:
                            st.markdown(f"""
                            <div class="weather-card">
                                <div class="weather-title">🌤️ Live Weather Data</div>
                                <div style="color:#1F2937;font-size:0.9rem;line-height:1.7;white-space:pre-wrap;">{text.strip()}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    elif node_name == "budget_agent":
                        text = state_update.get("budget_results", "")
                        collected["budget_results"] = text
                        st.markdown(text or "_No budget data._")
                    elif node_name == "itinerary_agent":
                        text = state_update.get("itinerary", "")
                        collected["itinerary"] = text
                        st.markdown(text or "_No itinerary generated._")
                    collected["llm_calls"] = state_update.get("llm_calls", collected["llm_calls"])

        # ── Metrics ──
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box"><div class="metric-val">6</div><div class="metric-lbl">Agents Run</div></div>
            <div class="metric-box"><div class="metric-val">{collected['llm_calls']}</div><div class="metric-lbl">LLM Calls</div></div>
            <div class="metric-box"><div class="metric-val">✅</div><div class="metric-lbl">Status</div></div>
            <div class="metric-box"><div class="metric-val">🌤️</div><div class="metric-lbl">Live Weather</div></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Final Itinerary ──
        if collected["itinerary"]:
            st.markdown("<div class='sec-head'><span>🗓️ Your Complete Travel Itinerary</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='final-card'>{collected['itinerary']}</div>", unsafe_allow_html=True)

        # ── Save & Download ──
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename  = f"travel_plan_{timestamp}.md"
        save_dir  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "travel_plans")
        os.makedirs(save_dir, exist_ok=True)

        file_content = f"""# Travel Plan
**Query:** {user_query}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Session ID:** {thread_id}

---

## 🔬 Destination Research
{collected['research_results'] or 'N/A'}

---

## ✈️ Flight Information
{collected['flight_results'] or 'N/A'}

---

## 🏨 Hotel Information
{collected['hotel_results'] or 'N/A'}

---

## 🌤️ Weather Information
{collected['weather_results'] or 'N/A'}

---

## 💰 Budget Breakdown
{collected['budget_results'] or 'N/A'}

---

## 🗓️ Full Itinerary
{collected['itinerary'] or 'N/A'}

---
*Agents: Research → Flight → Hotel → Weather → Budget → Itinerary | LLM Calls: {collected['llm_calls']}*
"""
        with open(os.path.join(save_dir, filename), "w", encoding="utf-8") as f:
            f.write(file_content)

        dl_col, info_col = st.columns([1, 3])
        with dl_col:
            st.download_button("⬇️ Download Plan", data=file_content,
                               file_name=filename, mime="text/markdown",
                               use_container_width=True)
        with info_col:
            st.markdown(f"<div class='save-bar'>📁 Auto-saved → <code>travel_plans/{filename}</code></div>",
                        unsafe_allow_html=True)