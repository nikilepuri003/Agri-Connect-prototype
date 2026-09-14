# AgriConnect Streamlit App

AgriConnect is an innovative Streamlit application designed to empower farmers by providing them with essential tools for market linkage and price discovery. This application allows farmers to easily compare market prices, find potential buyers, and manage their crop sales efficiently.

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
streamlit run app.py
```

The project is configured to open `http://localhost:8501` automatically when it starts. On Windows, you can use the project environment directly:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

The app is also self-contained in `farmer_hub/`; the root `app.py` is the supported launcher.

   ## Included

   - Crop choices with visual icons and a low-reading-load workflow.
   - Browser microphone capture with language selection for English, Hindi, Telugu, Tamil, Kannada, Malayalam, Marathi, Bengali, and other languages.
   - Market map with local coordinates, distances, and recognizable landmarks.
   - Google Maps direction links without hard-coding an API key.
   - Direct buyer offers with quantity requirements and a connect action.
   - A warm, high-contrast farmer-facing theme.

   Voice transcription uses Google Speech Recognition through `SpeechRecognition`, so it needs internet access. The map pins and landmark data are local demo data; replace `farmer_hub/data.py` with live market data when a production source is available.

   ## Folder

   ```text
   farmer_hub/
     data.py      Demo markets, landmarks, crops, and buyer offers
     maps.py      Map display and Google Maps links
     voice.py     Browser audio capture and multilingual transcription
     ui.py        Farmer workflow and theme
   ```

## Deploy

For Streamlit Community Cloud:

1. Push this project to a GitHub repository.
2. In Streamlit Community Cloud, choose **Deploy an app**.
3. Select the repository, branch, and `app.py` as the main file.
4. Deploy.

The cloud service installs `requirements.txt` automatically. No API key is required for the included demo maps; voice transcription requires internet access.