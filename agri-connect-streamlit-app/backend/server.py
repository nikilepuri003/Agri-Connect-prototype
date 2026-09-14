#!/usr/bin/env python3
"""
AgriConnect Backend Server
Provides static file serving, REST APIs, OpenAI dynamic market lookup, and Kisan AI chatbot.
"""

from __future__ import annotations

import json
import mimetypes
import os
import sys
import urllib.parse
import urllib.request
import urllib.error
from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
DB_DIR = BASE_DIR / "db"
DATA_JSON_PATH = DB_DIR / "data.json"
CONFIG_JSON_PATH = Path(__file__).resolve().parent / "config.json"


def load_config() -> dict:
    if CONFIG_JSON_PATH.exists():
        try:
            with open(CONFIG_JSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not read config.json: {e}", file=sys.stderr)
    return {"port": 8000, "host": "localhost"}


def load_data() -> dict:
    if DATA_JSON_PATH.exists():
        with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


# Regional Mandi Knowledgebase for dynamic discovery when OpenAI key is not configured
REGIONAL_MANDI_HUBS = {
    "kurnool": [
        {"market": "Kurnool APMC Market Yard", "location": "Kurnool", "latitude": 15.8281, "longitude": 78.0373, "prices": {"Tomato": 23, "Chilli": 114, "Rice": 33, "Cotton": 74, "Wheat": 32}, "distance": 8, "landmarks": "Bellary Road · Near APMC Complex"},
        {"market": "Nandyal Rythu Bazar", "location": "Nandyal", "latitude": 15.4786, "longitude": 78.4836, "prices": {"Tomato": 25, "Chilli": 116, "Rice": 34, "Cotton": 72, "Wheat": 30}, "distance": 52, "landmarks": "Near Bus Station · Clock Tower"},
        {"market": "Adoni Cotton Market", "location": "Adoni", "latitude": 15.6322, "longitude": 77.2728, "prices": {"Tomato": 22, "Chilli": 110, "Rice": 32, "Cotton": 76, "Wheat": 31}, "distance": 68, "landmarks": "Cotton Market Yard · Alur Road"}
    ],
    "warangal": [
        {"market": "Enumamula Grain & Chilli Market", "location": "Warangal", "latitude": 17.9689, "longitude": 79.5941, "prices": {"Tomato": 24, "Chilli": 122, "Rice": 36, "Cotton": 75, "Wheat": 33}, "distance": 6, "landmarks": "Asia's 2nd Largest Market · Enumamula"},
        {"market": "Jangaon Market Yard", "location": "Jangaon", "latitude": 17.7219, "longitude": 79.1636, "prices": {"Tomato": 23, "Chilli": 115, "Rice": 35, "Cotton": 72, "Wheat": 31}, "distance": 48, "landmarks": "Station Road · Rythu Sangham"},
        {"market": "Mahabubabad Vegetable Mandi", "location": "Mahabubabad", "latitude": 17.5985, "longitude": 80.0044, "prices": {"Tomato": 26, "Chilli": 118, "Rice": 34, "Cotton": 71, "Wheat": 30}, "distance": 65, "landmarks": "Near Railway Overbridge · Main Road"}
    ],
    "rajahmundry": [
        {"market": "Rajahmundry Central Mandi", "location": "Rajahmundry", "latitude": 17.0005, "longitude": 81.8040, "prices": {"Tomato": 26, "Chilli": 112, "Rice": 38, "Cotton": 69, "Wheat": 32}, "distance": 7, "landmarks": "Kotipalli Bus Stand · Godavari Bund"},
        {"market": "Kakinada Port Wholesale Market", "location": "Kakinada", "latitude": 16.9891, "longitude": 82.2475, "prices": {"Tomato": 27, "Chilli": 115, "Rice": 37, "Cotton": 68, "Wheat": 33}, "distance": 45, "landmarks": "Main Road Market · Near D-Boat Yard"},
        {"market": "Eluru Agriculture Market", "location": "Eluru", "latitude": 16.7107, "longitude": 81.0952, "prices": {"Tomato": 24, "Chilli": 109, "Rice": 36, "Cotton": 70, "Wheat": 31}, "distance": 58, "landmarks": "Powerpet Railway Station · Market Gate"}
    ],
    "anantapur": [
        {"market": "Anantapur Agricultural Market", "location": "Anantapur", "latitude": 14.6819, "longitude": 77.6006, "prices": {"Tomato": 21, "Chilli": 108, "Rice": 32, "Cotton": 73, "Wheat": 33}, "distance": 9, "landmarks": "Clock Tower · Gooty Road"},
        {"market": "Dharmavaram Silk & Vegetable Yard", "location": "Dharmavaram", "latitude": 14.4137, "longitude": 77.7126, "prices": {"Tomato": 23, "Chilli": 110, "Rice": 33, "Cotton": 71, "Wheat": 32}, "distance": 42, "landmarks": "Station Road · APMC Complex"},
        {"market": "Hindupur Wholesale Mandi", "location": "Hindupur", "latitude": 13.8290, "longitude": 77.4930, "prices": {"Tomato": 25, "Chilli": 112, "Rice": 34, "Cotton": 70, "Wheat": 34}, "distance": 75, "landmarks": "Border Checkpost Road · Market Yard"}
    ],
    "khammam": [
        {"market": "Khammam Chilli & Grain Market Yard", "location": "Khammam", "latitude": 17.2473, "longitude": 80.1514, "prices": {"Tomato": 24, "Chilli": 124, "Rice": 35, "Cotton": 74, "Wheat": 31}, "distance": 6, "landmarks": "Wyra Road · Mirchi Yard"},
        {"market": "Madhira Grain Market", "location": "Madhira", "latitude": 16.9200, "longitude": 80.3700, "prices": {"Tomato": 23, "Chilli": 118, "Rice": 36, "Cotton": 72, "Wheat": 30}, "distance": 38, "landmarks": "Railway Gate Road · Rythu Samiti"},
        {"market": "Kothagudem APMC Mandi", "location": "Kothagudem", "latitude": 17.5500, "longitude": 80.6200, "prices": {"Tomato": 26, "Chilli": 120, "Rice": 34, "Cotton": 70, "Wheat": 32}, "distance": 62, "landmarks": "Bus Stand · Singareni Gate"}
    ]
}


def query_openai_chat(api_key: str, message: str, history: list) -> str:
    """Call OpenAI Chat Completions API with an agricultural system prompt."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    system_prompt = (
        "You are Kisan AI (AgriConnect AI), a warm, deeply knowledgeable agricultural expert and advisor "
        "dedicated to Indian farmers. Answer questions about crop health, pest and disease remedies, "
        "fertilizer and nutrient guidance, real-time market selling strategies, APMC mandi procedures, "
        "and government schemes (e.g. PM-KISAN, PMFBY). "
        "If the user asks in Telugu, Hindi, or another regional language, respond respectfully in that language. "
        "Keep your advice clear, step-by-step, actionable, and formatted nicely in bullet points."
    )

    messages = [{"role": "system", "content": system_prompt}]
    # Add previous turn history (up to last 6 messages)
    for turn in history[-6:]:
        if isinstance(turn, dict) and "role" in turn and "content" in turn:
            messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": message})

    payload = json.dumps({
        "model": "gpt-4o-mini",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=12) as response:
        result = json.loads(response.read().decode("utf-8"))
        return result["choices"][0]["message"]["content"]


def query_openai_markets(api_key: str, location: str, crop: str) -> list[dict]:
    """Ask OpenAI for realistic nearby APMC mandis and benchmark prices in JSON format."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    prompt = (
        f"Generate a strict JSON array of 3 realistic nearby APMC agricultural markets/mandis for a farmer located in or near '{location}', India, selling '{crop}'. "
        f"For each market, return an object with: "
        f"'market' (e.g. 'Town APMC Market Yard'), "
        f"'location' (city/town name), "
        f"'latitude' (approximate float), "
        f"'longitude' (approximate float), "
        f"'prices' (an object with estimated current prices in ₹/kg for Tomato, Chilli, Rice, Cotton, Wheat), "
        f"'distance' (estimated driving distance in km from {location} as integer), "
        f"'landmarks' (prominent local landmark string). "
        f"Output ONLY valid JSON, no surrounding markdown or explanation."
    )

    payload = json.dumps({
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=12) as response:
        result = json.loads(response.read().decode("utf-8"))
        text = result["choices"][0]["message"]["content"].strip()
        if text.startswith("```"):
            text = text.strip("`")
            if text.startswith("json"):
                text = text[4:].strip()
        return json.loads(text)


def offline_agricultural_expert(message: str) -> str:
    """Intelligent rule-based fallback expert when OpenAI API key is unavailable."""
    msg = message.lower()

    if any(w in msg in msg for w in ["టమాటా", "tomato", "tamatar"]):
        if any(w in msg for w in ["pest", "disease", "పురుగు", "తెగులు", "leaf", "rot"]):
            return (
                "🍅 **Tomato Health & Pest Advisory**:\n"
                "• **Early/Late Blight**: Spray Mancozeb 75% WP @ 2.5g/L water or Copper Oxychloride @ 3g/L.\n"
                "• **Fruit Borer**: Set up Pheromone traps (5 traps/acre). For chemical control, spray Emamectin Benzoate 5% SG @ 4g/10L water.\n"
                "• **Leaf Curl (Whitefly transmitted)**: Spray Neem oil 10,000 ppm @ 2ml/L water or Imidacloprid 17.8 SL @ 0.3ml/L.\n"
                "• **Tip**: Ensure proper staking and avoid overhead irrigation to prevent fungal spread."
            )
        return (
            "🍅 **Tomato Market & Crop Guidance**:\n"
            "• Current quality tomato prices in local APMCs range from ₹22 to ₹28/kg.\n"
            "• **Grading Advice**: Sort tomatoes into Class A (firm, uniform red) to fetch up to 12% premium in wholesale yards.\n"
            "• **Storage**: Keep harvested crates under shade at 15–20°C with ventilation to avoid softening."
        )

    if any(w in msg for w in ["మిర్చి", "chilli", "mirchi"]):
        return (
            "🌶️ **Chilli (Mirchi) Protection & Selling Strategy**:\n"
            "• **Thrips / Black Thrips Management**: Use Blue sticky traps (25–30/acre). Spray Fipronil 5% SC @ 2ml/L or Spinetoram 11.7 SC @ 1ml/L.\n"
            "• **Dieback / Anthracnose**: Spray Azoxystrobin 23% SC @ 1ml/L or Difenoconazole @ 0.5ml/L at first sight of spots.\n"
            "• **Market Note**: Guntur & Warangal are primary trading hubs. Clean, moisture-controlled dried red chillies currently benchmark between ₹105–₹125/kg."
        )

    if any(w in msg for w in ["rice", "paddy", "బియ్యం", "వరి"]):
        return (
            "🌾 **Paddy / Rice Cultivation Tips**:\n"
            "• **Blast Disease (Aggi Tegulu)**: Spray Tricyclazole 75% WP @ 0.6g/L water.\n"
            "• **Stem Borer**: Apply Chlorantraniliprole 0.4% G (Ferterra) @ 4kg/acre with sand at 15–20 days after transplanting.\n"
            "• **Selling Benchmark**: Standard grade paddy benchmarks at ₹32–₹36/kg in nearby coastal Andhra & Telangana grain yards."
        )

    if any(w in msg for w in ["cotton", "పత్తి", "kapas"]):
        return (
            "☁️ **Cotton Care & Fair Pricing**:\n"
            "• **Pink Bollworm**: Install Pheromone traps. Spray Profenofos 50% EC @ 2ml/L or Emamectin Benzoate.\n"
            "• **Harvesting**: Pick clean bolls in dry afternoon hours to maintain low moisture (under 8%) for top grade pricing.\n"
            "• **Benchmark**: Current APMC rates range from ₹68–₹74/kg."
        )

    if any(w in msg for w in ["pm kisan", "scheme", "subsidy", "పథకం", "సబ్సిడీ"]):
        return (
            "🏛️ **Farmer Welfare & Government Schemes**:\n"
            "• **PM-KISAN**: ₹6,000/year in 3 equal installments directly to bank accounts via DBT. Check status on `pmkisan.gov.in`.\n"
            "• **e-NAM Portal**: National Agriculture Market lets you trade produce across state lines online without middleman cuts.\n"
            "• **Rythu Bharosa / Subsidized Seeds**: Contact your local Rythu Bharosa Kendra (RBK) or Mandal Agricultural Officer (MAO)."
        )

    # General fallback
    return (
        "🌾 **Namaste! I am your Kisan AI Assistant**.\n\n"
        "I can help you with:\n"
        "• **Pest & Disease Solutions**: Natural and certified remedies for tomato, chilli, rice, cotton, and wheat.\n"
        "• **Market Price Optimization**: Comparing local stall rents vs. direct buyer earnings.\n"
        "• **Fertilizer & Soil Advice**: Balanced NPK, zinc, and micronutrient schedules.\n"
        "• **Government Schemes**: PM-KISAN, e-NAM, and crop insurance guidance.\n\n"
        "*(Feel free to speak or type in English, Telugu, or Hindi!)*"
    )


class AgriConnectHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def do_GET(self) -> None:
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path == "/api/data":
            self.send_json_response(load_data())
            return

        if path == "/api/config":
            cfg = load_config()
            safe_cfg = {
                "google_maps_api_key": cfg.get("google_maps_api_key", ""),
                "has_openai_key": bool(cfg.get("openai_api_key") or os.getenv("OPENAI_API_KEY")),
                "app_name": "AgriConnect",
                "version": "2.1.0"
            }
            self.send_json_response(safe_cfg)
            return

        if path == "/api/health":
            self.send_json_response({"status": "ok", "app": "AgriConnect", "version": "2.1.0"})
            return

        if path in ("", "/"):
            self.path = "/index.html"

        return super().do_GET()

    def do_POST(self) -> None:
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        content_len = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"

        try:
            body = json.loads(post_data)
        except Exception:
            body = {}

        cfg = load_config()
        configured_key = body.get("apiKey") or cfg.get("openai_api_key") or os.getenv("OPENAI_API_KEY", "")

        # Endpoint 1: AI Chatbot (/api/chat)
        if path == "/api/chat":
            user_msg = body.get("message", "").strip()
            history = body.get("history", [])

            if not user_msg:
                self.send_json_response({"error": "Message is required"}, status=HTTPStatus.BAD_REQUEST)
                return

            reply = ""
            source = "kisan_ai_offline"

            if configured_key:
                try:
                    reply = query_openai_chat(configured_key, user_msg, history)
                    source = "openai"
                except Exception as e:
                    print(f"OpenAI Chat API notice: {e}. Using offline agricultural expert.")
                    reply = offline_agricultural_expert(user_msg)
            else:
                reply = offline_agricultural_expert(user_msg)

            self.send_json_response({"reply": reply, "source": source})
            return

        # Endpoint 2: Dynamic Market Discovery (/api/market-lookup)
        if path == "/api/market-lookup":
            location = body.get("location", "").strip()
            crop = body.get("crop", "Tomato").strip()

            if not location:
                self.send_json_response({"error": "Location is required"}, status=HTTPStatus.BAD_REQUEST)
                return

            markets = []
            source = "kisan_spatial_engine"

            if configured_key:
                try:
                    markets = query_openai_markets(configured_key, location, crop)
                    source = "openai"
                except Exception as e:
                    print(f"OpenAI Market API notice: {e}. Falling back to spatial database.")

            if not markets:
                # Spatial matching from regional hubs
                loc_lower = location.lower()
                matched_hub = None
                for hub_name, hub_markets in REGIONAL_MANDI_HUBS.items():
                    if hub_name in loc_lower:
                        matched_hub = hub_markets
                        break

                if matched_hub:
                    markets = matched_hub
                else:
                    # Dynamically generate realistic local mandis for the entered town
                    capitalized = location.title()
                    markets = [
                        {
                            "market": f"{capitalized} APMC Main Mandi",
                            "location": capitalized,
                            "latitude": 16.3 + (hash(location) % 100) / 200.0,
                            "longitude": 80.4 + (hash(location) % 100) / 200.0,
                            "prices": {"Tomato": 24, "Chilli": 110, "Rice": 33, "Cotton": 70, "Wheat": 31},
                            "distance": 6,
                            "landmarks": f"{capitalized} Rythu Bazar · Near Main Bus Depot"
                        },
                        {
                            "market": f"{capitalized} Regional Farmers Yard",
                            "location": f"{capitalized} Rural",
                            "latitude": 16.35 + (hash(location) % 100) / 200.0,
                            "longitude": 80.45 + (hash(location) % 100) / 200.0,
                            "prices": {"Tomato": 25, "Chilli": 112, "Rice": 35, "Cotton": 72, "Wheat": 32},
                            "distance": 22,
                            "landmarks": "Highway Junction · Market Complex"
                        }
                    ]

            # Generate rentals for any newly discovered markets
            rentals = []
            for m in markets:
                rentals.append({
                    "market": m["market"],
                    "shop": f"{m['location']} Stall #{hash(m['market']) % 20 + 1}",
                    "daily_rent": 280 + (hash(m['market']) % 250),
                    "security_deposit": 700 + (hash(m['market']) % 800),
                    "landmark": m.get("landmarks", "Main Yard Lane")
                })

            self.send_json_response({"markets": markets, "rentals": rentals, "source": source})
            return

        self.send_json_response({"error": "Endpoint not found"}, status=HTTPStatus.NOT_FOUND)

    def send_json_response(self, data: dict | list, status: int = HTTPStatus.OK) -> None:
        payload = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def log_message(self, format: str, *args) -> None:
        sys.stdout.write(f"[AgriConnect Server] {self.address_string()} - {args[0]} - {args[1]}\n")
        sys.stdout.flush()


def run_server(host: str = "localhost", port: int = 8000, open_browser: bool = False) -> None:
    server_address = (host, port)
    httpd = HTTPServer(server_address, AgriConnectHandler)
    url = f"http://{host}:{port}"
    print("=" * 60)
    print(">> AgriConnect Web App Server is running!")
    print(f"   URL: {url}")
    print(f"   Frontend files: {FRONTEND_DIR}")
    print(f"   Database file:  {DATA_JSON_PATH}")
    print("   Press Ctrl+C to stop the server.")
    print("=" * 60)

    if open_browser:
        import webbrowser
        webbrowser.open(url)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping AgriConnect server...")
        httpd.server_close()
        print("Server stopped cleanly.")


if __name__ == "__main__":
    config = load_config()
    server_host = config.get("host", "localhost")
    server_port = int(config.get("port", 8000))
    run_server(host=server_host, port=server_port, open_browser=False)
