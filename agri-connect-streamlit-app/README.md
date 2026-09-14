# AgriConnect Web Application

AgriConnect is an intuitive web application designed to empower farmers with market linkage, crop price discovery, shop rental planning, and direct buyer connections.

Built with clean **HTML5, CSS3, JavaScript (ES6+), JSON**, and a lightweight Python backend server.

## Features

- **Intuitive Farmer Interface**: Designed specifically for low cognitive load, high contrast, warm agricultural theme, and visual crop icons.
- **Voice Assistant**: Built-in speech recognition supporting Telugu, Hindi, English, Tamil, Kannada, Malayalam, Marathi, and Bengali, with auto-detection for local crop names (e.g. *టమాటా*, *mirchi*, *tamatar*).
- **Price Benchmarks & Quality Grades**: Dynamic price adjustments for Premium (+12%), Standard, and Value (-12%) grades.
- **Smart Net Earning Calculation**: Calculates true take-home earnings comparing **Shop Rentals** vs. **Direct Buyer Sales** after round-trip transport and stall costs.
- **Interactive Market Map**: Leaflet OpenStreetMap view with market locations, landmarks, and direct turn-by-turn Google Maps direction buttons.
- **Direct Buyer Linkage**: Filter buyers by crop, compare offers, and connect with 1-click confirmation.
- **Kisan AI Chatbot**: OpenAI-backed answers with a broad offline fallback for crop health, soil, markets, schemes, and selling questions.
- **Daily Market Freshness**: Market data is checked once per UTC day and reports its update date and source.
- **Regional Learning Videos**: The Market Map provides region-aware agricultural lesson searches for Kurnool, Warangal, Rajahmundry, Anantapur, Khammam, and other locations.

## Project Structure

```text
agri-connect-streamlit-app/
├── frontend/
│   ├── index.html        # Main semantic HTML5 interface
│   ├── style.css         # Agricultural theme & responsive layout
│   └── app.js            # Reactive application logic, calculations, voice & map
├── backend/
│   ├── server.py         # Lightweight Python static server and JSON API
│   └── config.json       # Host, port, and optional external API configuration
├── api/
│   ├── chat.py           # Secure Vercel chatbot endpoint
│   ├── data.py           # Daily market data endpoint
│   └── market_lookup.py  # Secure Vercel mandi lookup endpoint
├── db/
│   └── data.json         # Complete structured database (crops, markets, rentals, buyers)
├── legacy_streamlit/     # Archived original Streamlit Python files
├── server.py             # Root application launcher
├── app.py                # Alternate launcher entrypoint
└── README.md
```

## How to Run

No heavy third-party frameworks or build tools required. Start the application with Python:

```powershell
python server.py
```
*(or use your virtual environment: `.\.venv\Scripts\python.exe server.py`)*

The server will start and automatically open:
```
http://localhost:8000
```

## Deployment secrets

Never put API keys in `frontend/app.js`, browser local storage, or committed JSON. Configure these as environment variables in Vercel or the server host:

```text
OPENAI_API_KEY=...
GOOGLE_MAPS_API_KEY=...
MARKET_DATA_API_URL=https://your-provider.example/markets
```

`OPENAI_API_KEY` enables live Kisan AI and AI mandi lookup. Without it, the app uses its local agricultural knowledgebase. `MARKET_DATA_API_URL` is optional and should return a JSON object containing a `markets` array; the app checks it once per UTC day and falls back to `db/data.json` if it is unavailable. API keys are never returned by `/api/config`.