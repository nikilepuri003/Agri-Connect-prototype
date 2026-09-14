# AgriConnect Web App

AgriConnect is a browser-based Python web application designed to empower farmers with market linkage and price discovery. The frontend uses HTML, CSS, and JavaScript, the backend exposes JSON endpoints, and the database layer contains the market data and pricing rules.

## Features

- **User-Friendly Interface**: The app features an attractive interface with crop images as icons, making navigation intuitive and engaging.
- **Multi-Crop Selling**: Farmers can input details for multiple crops, allowing for a comprehensive overview of their selling options.
- **Voice Input**: For farmers who may have difficulty typing, the app incorporates voice input functionality, enabling them to enter data using voice commands.
- **Google Maps Integration**: Users can view market locations and distances, helping them make informed decisions about where to sell their crops.
- **3D Agricultural Background**: The app is enhanced with a visually appealing 3D agricultural-themed background, creating an immersive experience.

## Run locally

Install dependencies and start the supported root launcher:

```bash
pip install -r requirements.txt
python app.py
```

The project is configured to open `http://localhost:8000` automatically when it starts. On Windows, you can use the project environment directly:

```powershell
.\.venv\Scripts\python.exe app.py
```

The root `app.py` is the supported launcher. The code is split into frontend, backend, and database layers.

   ## Included

   - Crop choices with visual icons and a low-reading-load workflow.
  - Browser microphone capture through the Web Speech API when supported by the browser.
   - Market map with local coordinates, distances, and recognizable landmarks.
  - Google Maps direction links without hard-coding an API key.
   - Direct buyer offers with quantity requirements and a connect action.
   - A warm, high-contrast farmer-facing theme.

  Voice input uses the browser Web Speech API. The map pins and landmark data are local demo data; replace `database/data.py` with live market data when a production source is available.

   ## Folder

   ```text
   frontend/
     index.html   Browser page structure
     style.css    Responsive visual design
     app.js       Browser interactions and API calls
   backend/
     server.py    Python HTTP server and JSON API
     config.py    Environment-based API-key access
     maps.py      Map helpers
   database/
     data.py      Demo markets, landmarks, crops, and buyer offers
   ```

## API keys

The app reads optional keys from environment variables or deployment secrets. Configure these values in your host:

```toml
GOOGLE_MAPS_API_KEY = "your-key"
GOOGLE_SPEECH_API_KEY = "your-key"
```

For environment-based hosts, use `GOOGLE_MAPS_API_KEY` and `GOOGLE_SPEECH_API_KEY` environment variables. Never commit real keys. The current Google Maps links work without a key, and browser voice input works without a server key when the browser supports Web Speech.

## Deploy

For a Python host such as Render, Railway, or a VM:

1. Push this project to a GitHub repository.
2. Start the service with `python app.py`.
3. Expose port `8000` (or use the host-provided `PORT` variable).

The previous Streamlit deployment is no longer the correct target for this HTML/JS/Python version. The included demo map links do not require an API key.