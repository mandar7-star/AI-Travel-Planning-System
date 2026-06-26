# Run this ONCE locally to populate Pinecone with travel knowledge
# Command: python ingest_knowledge.py

import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

TRAVEL_KNOWLEDGE = [
    {"id":"japan_001","text":"Japan visa for Indian citizens: Tourist visa required. Apply at Japanese consulate with passport, photos, bank statements and itinerary. Processing takes 5-7 working days. Visa is free of charge.","destination":"Japan"},
    {"id":"japan_002","text":"Best time to visit Japan: March-May for cherry blossoms, October-November for autumn foliage. Avoid Golden Week (late April-early May) as it gets crowded and expensive.","destination":"Japan"},
    {"id":"japan_003","text":"Japan currency: Japanese Yen (JPY). 1 USD = approximately 150 JPY. Cash is widely used. Get yen from airport ATMs or 7-Eleven ATMs which accept international cards.","destination":"Japan"},
    {"id":"japan_004","text":"Japan transport: Buy JR Pass before arriving for unlimited Shinkansen bullet train travel. IC cards (Suica or Pasmo) work on all local trains and buses.","destination":"Japan"},
    {"id":"japan_005","text":"Japan culture tips: Remove shoes when entering homes and some restaurants. Bow as greeting. Tipping is not customary and considered rude. Speak softly on public transport.","destination":"Japan"},
    {"id":"paris_001","text":"Paris visa for Indian citizens: Schengen visa required. Apply at French consulate or VFS Global. Processing takes 15 working days. Need passport, travel insurance, hotel bookings, bank statements.","destination":"Paris"},
    {"id":"paris_002","text":"Best time to visit Paris: April-June and September-October for pleasant weather. July-August is peak season with higher prices. December is magical for Christmas markets.","destination":"Paris"},
    {"id":"paris_003","text":"Paris currency: Euro (EUR). 1 USD = approximately 0.92 EUR. Credit cards widely accepted. Use ATMs for better exchange rates, avoid airport currency counters.","destination":"Paris"},
    {"id":"paris_004","text":"Paris transport: Paris Visite pass covers unlimited Metro, RER and bus travel. Metro is fastest way around the city. Velib bike sharing great for short distances.","destination":"Paris"},
    {"id":"dubai_001","text":"Dubai visa for Indian citizens: Visa on arrival for 14 days. 30 or 90 day tourist visa available online through Emirates or Air Arabia websites. Visa on arrival fee is AED 100.","destination":"Dubai"},
    {"id":"dubai_002","text":"Best time to visit Dubai: November to April for pleasant weather 20-30 degrees C. May to October is extremely hot 40-45 degrees C. Dubai Shopping Festival is January-February.","destination":"Dubai"},
    {"id":"dubai_003","text":"Dubai currency: UAE Dirham (AED). 1 USD = approximately 3.67 AED. ATMs widely available. Tipping 10-15 percent customary in restaurants.","destination":"Dubai"},
    {"id":"dubai_004","text":"Dubai culture: Dress modestly in public. Alcohol only in licensed venues. Ramadan special rules — no eating or drinking in public during daytime. Friday is day of rest.","destination":"Dubai"},
    {"id":"bali_001","text":"Bali visa for Indian citizens: Visa on arrival for 30 days, extendable once for 30 more days. Cost is USD 35. Available at Ngurah Rai International Airport.","destination":"Bali"},
    {"id":"bali_002","text":"Best time to visit Bali: April-October dry season is ideal. November-March is wet season with heavy rainfall but lush green landscapes and fewer tourists.","destination":"Bali"},
    {"id":"bali_003","text":"Bali currency: Indonesian Rupiah (IDR). 1 USD = approximately 15,000 IDR. Always carry cash as many local warungs do not accept cards.","destination":"Bali"},
    {"id":"bangkok_001","text":"Bangkok visa for Indian citizens: Visa on arrival for 15 days, cost THB 2000. Or apply for 60-day tourist visa at Thai consulate with passport, photo, onward ticket, hotel booking.","destination":"Bangkok"},
    {"id":"bangkok_002","text":"Best time to visit Bangkok: November to February for cool dry weather. March-May is hot season. June-October is rainy season with occasional flooding.","destination":"Bangkok"},
    {"id":"bangkok_003","text":"Bangkok transport: BTS Skytrain and MRT Metro are best ways to avoid traffic. Use Grab app for taxis. Tuk-tuks for short distances. River ferries along Chao Phraya river.","destination":"Bangkok"},
    {"id":"general_001","text":"Travel insurance: Always buy comprehensive travel insurance covering medical emergencies, trip cancellation and baggage loss. Required for Schengen visa. Cost is typically 2-5 percent of total trip cost.","destination":"General"},
    {"id":"general_002","text":"Budget travel tips: Book flights 6-8 weeks in advance for best prices. Use Google Flights price tracking. Street food is safe and delicious in most Asian countries.","destination":"General"},
    {"id":"general_003","text":"Packing essentials: Universal power adapter, portable charger, copies of passport and visa, local SIM card, travel lock, first aid kit, microfiber towel.","destination":"General"},
]

def ingest():
    print("Connecting to Pinecone...")
    pc    = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index("travel-knowledge")
    print(f"Embedding {len(TRAVEL_KNOWLEDGE)} documents...")
    texts      = [doc["text"] for doc in TRAVEL_KNOWLEDGE]
    embeddings = pc.inference.embed(
        model="llama-text-embed-v2",
        inputs=texts,
        parameters={"input_type": "passage"}
    )
    vectors = []
    for i, doc in enumerate(TRAVEL_KNOWLEDGE):
        vectors.append({
            "id":       doc["id"],
            "values":   embeddings[i].values,
            "metadata": {"text": doc["text"], "destination": doc["destination"]}
        })
    index.upsert(vectors=vectors)
    print(f"✅ Successfully uploaded {len(vectors)} documents to Pinecone!")

if __name__ == "__main__":
    ingest()