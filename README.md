# FluffelNexus

FluffelNexus is a Python desktop prototype combining webcam-based hand gesture control with a scheduled weather-and-news briefing delivered through Telegram.

## Features

- **Gesture control:** MediaPipe and OpenCV detect hand landmarks; PyAutoGUI translates supported gestures into pointer movement, clicks, and scrolling.
- **Daily briefing:** Fetches current weather and news, formats a message, and sends it to a configured Telegram chat.
- **Desktop GUI:** PyQt6 interface for settings, starting/stopping gesture control and managing the briefing scheduler.
- **Local settings:** SQLite persistence for the selected name, city, time, language, sources, and units.

> **Status:** Work in progress. The code has been improved for scheduling, API error handling, settings persistence, and subprocess cleanup, but it has not been verified on every supported operating system or hardware configuration.

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
└── db.db  # local settings database; normally keep out of Git
```

## Requirements

- Python version compatible with the installed PyQt6 and MediaPipe packages (Python 3.10–3.12 is a reasonable starting point; verify package wheels for your OS).
- Webcam and a graphical desktop session for gesture control.
- OpenWeatherMap API key for weather data.
- NewsAPI key for news articles.
- Telegram bot token and chat ID to deliver briefings.
- Internet access for external APIs and Telegram.

## Installation

Clone the repository:

```bash
git clone https://github.com/Flockemon24/FluffelNexus.git
cd FluffelNexus
```

Create and activate a virtual environment.

**Windows PowerShell**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a `.env` file in the repository root:

```dotenv
WEATHER_API_KEY=your_openweathermap_api_key
NEWS_API_KEY=your_newsapi_key
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

Use your own credentials. **Never commit real API keys, bot tokens, chat IDs, or other secrets.** Keep `.env` out of version control.

Start the desktop app:

```bash
python main.py
```

## Usage

### Gesture control

1. Click **Start Gesture Control** in the desktop app.
2. Allow camera access if requested.
3. Use the supported gestures:
   - **Index finger pointing:** move the pointer.
   - **Thumb + index pinch:** click once when the gesture begins.
   - **Thumb + middle-finger pinch:** double-click when the gesture begins.
   - **Index finger pointing down with other fingers folded:** scroll down.
4. Press **Q** in the camera preview to quit, or use the GUI button to stop the process.

Lighting, camera position, and gesture thresholds can affect detection. Test carefully before using gestures for actions where accidental clicks would be disruptive.

### Daily briefing

1. Open **Show Settings**.
2. Enter a name and city.
3. Select a daily time, language, weather units, and at least one news source.
4. Click **Save Settings**.
5. Click **Start Daily Briefing Scheduler**.

The scheduler runs once per day at the selected local time while its process is running. It does not send a message immediately on startup. Keep the application/scheduler running for the scheduled time to be reached. If settings change while the scheduler is running, save them and restart the scheduler.

## Configuration notes

- Settings are stored in `db.db` beside the application files.
- API credentials are read from environment variables loaded from `.env`.
- Weather units: `metric` (Celsius), `imperial` (Fahrenheit), or `standard` (Kelvin).
- News sources are sent as a comma-separated list of domains.
- The briefing may be incomplete if a provider is unavailable, credentials are missing, or API limits are reached.

## Known limitations

- Gesture recognition is based on fixed thresholds and may need calibration for different cameras and users.
- The scheduler runs as a separate process and needs to remain alive until the chosen time.
- The current database stores one active settings profile; multi-user profile management is not implemented.
- External API plans and availability may limit the number or freshness of news articles.
- Dependency compatibility, camera permissions, and desktop behavior still need testing on each target OS.
- Automated tests and continuous integration are not yet included.
- `calander.py` is currently an empty placeholder.

## Suggested next steps

- Add automated tests for settings storage, message formatting, and scheduler argument validation.
- Add application logging to a file and more visible scheduler status.
- Add configurable gesture thresholds and a pause/safety mode.
- Add a first-run setup wizard and configuration validation.
- Test installation from a clean virtual environment on Windows and Linux.
- Add a project license if you intend to accept contributions or distribute the software.

## Contributing

Bug reports and focused improvements are welcome. Do not include API credentials, personal information, or a populated local database in commits.

## License

This project is under MIT-License.
