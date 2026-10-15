# FluffelNexus

FluffelNexus is a Python desktop project that brings together two personal-computing features:

- **Gesture control:** use a webcam and hand tracking to move the mouse, click, and scroll with hand gestures.
- **Daily briefing:** prepare a Telegram message with weather information and current news articles for a selected city and preferred news sources.

The project uses a PyQt6 desktop interface, MediaPipe/OpenCV for hand tracking, SQLite for settings, and external APIs for weather and news.

> **Status:** Work in progress / prototype. Some settings and scheduling behavior still need refinement; see [Known limitations](#known-limitations).

## Features

### Gesture control
- Detects hand landmarks with MediaPipe.
- Supports pointer movement, pinch-to-click, a second click gesture, and scrolling.
- Can be started and stopped from the desktop GUI.

### Daily briefing
- Lets the user enter a name and city.
- Offers a briefing-time selector, language selector, weather units, and selectable news sources.
- Stores settings in a local SQLite database.
- Builds a briefing with weather and news headlines and sends it through a Telegram bot.

## Project structure

```text
FluffelNexus/
├── main.py
├── gui.py
├── database.py
├── briefing_scheduler.py
├── requirements.txt
├── briefing/
│   ├── generator.py
│   ├── news.py
│   ├── weather.py
│   └── calander.py
├── vision/
│   └── gesture_control.py
└── db.db                 # Local SQLite database (should normally not be committed)
```

## Requirements

- Python 3.10 or a compatible version supported by the installed MediaPipe and PyQt6 releases
- A webcam for gesture control
- A graphical desktop session
- API credentials for the weather and news providers
- A Telegram bot and chat ID for sending briefings

Dependency compatibility can vary by operating system and Python version, particularly for MediaPipe, NumPy, and OpenCV.

## Setup

1. Clone the repository and enter its directory:

   ```bash
   git clone https://github.com/Flockemon24/FluffelNexus.git
   cd FluffelNexus
   ```

2. Create and activate a virtual environment:

   **Windows**
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   **Linux / macOS**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root. Add your own credentials:

   ```dotenv
   WEATHER_API_KEY=your_openweathermap_api_key
   NEWS_API_KEY=your_newsapi_key
   TELEGRAM_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   ```

   Never commit real API keys, bot tokens, or private chat IDs. Keep `.env` out of version control.

5. Start the application:

   ```bash
   python main.py
   ```

## Usage

### Gesture control
1. Launch FluffelNexus.
2. Select **Start Gesture Control**.
3. Allow camera access if prompted.
4. Use the supported hand gestures to control the pointer, click, or scroll.
5. Select the button again to stop the gesture-control process.

Gesture recognition and pointer control may need calibration for lighting, camera position, and hand size. The current implementation uses fixed distance thresholds.

### Daily briefing
1. Open **Show Settings**.
2. Enter a city and select the language, units, briefing time, and news sources.
3. Select **Save Settings**.
4. Select **Start daily Briefing Scheduler**.

**Important:** The current scheduler implementation runs the briefing every minute rather than at the selected time. Do not rely on the selected briefing time until this is fixed. A Telegram bot must also be configured correctly before sending can work.

## Configuration and data

- User settings are stored in the local SQLite database, `db.db`.
- API credentials are read from environment variables loaded from `.env`.
- Weather and news data depend on the availability, quotas, and terms of the respective external APIs.
- A network connection is required for online weather/news retrieval and Telegram delivery.

## Known limitations

- The scheduler process is not managed with a robust start/stop lifecycle, and repeated starts may create multiple processes.
- Settings are saved to SQLite, but the GUI does not currently load the saved values back into the form at startup.
- The weather request does not check HTTP errors or handle timeouts, and the briefing formats the temperature with a Celsius symbol even when imperial units are selected.
- News and weather failures are handled minimally; clearer error messages and logging are needed.
- The gesture-control preview window is disabled in the current code, and camera/MediaPipe resources should be cleaned up reliably on every exit path.
- Gesture actions use fixed thresholds and may trigger repeated clicks or scrolls in some situations.
- Dependency pins include overlapping OpenCV packages and should be tested as a compatible set on each target platform.
- The database file contains local user data and is better generated locally than tracked in Git.

## License

This project is Open-Source. Feel free to clone and use it wherever you want!
