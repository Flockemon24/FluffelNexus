import sys
import subprocess
import sqlite3

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QListWidget,
    QListWidgetItem,
)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("FluffelNexus")
        self.resize(350, 200)

        self.gesture_control = False
        self.process = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        layout.addWidget(QLabel("Input Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(
            "e. g. John Doe"
        )
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Input City:"))
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText(
            "e. g. Berlin"
        )
        layout.addWidget(self.city_input)

        layout.addWidget(QLabel("Select Morning Briefing Time:"))
        self.briefing_time_selector = QComboBox()
        self.briefing_time_selector.addItems(["06:30", "07:00", "07:30", "08:00"])
        layout.addWidget(self.briefing_time_selector)

        layout.addWidget(QLabel("Select Language:"))
        self.language_selector = QComboBox()
        self.language_selector.addItems(["Deutsch", "English", "Français", "Español", "Italiano"])
        layout.addWidget(self.language_selector)

        layout.addWidget(QLabel("Select Weather Units:"))
        self.weather_units_selector = QComboBox()
        self.weather_units_selector.addItems(["Metric", "Imperial"])
        layout.addWidget(self.weather_units_selector)

        layout.addWidget(QLabel("Select News Sources:"))
        self.news_sources_selector = QListWidget()
        sources = [
            "spiegel.de",
            "tagesschau.de",
            "zeit.de",
            "welt.de",
            "faz.net",
            "sueddeutsche.de",
            "focus.de",
            "nytimes.com",
            "washingtonpost.com",
            "wsj.com",
            "apnews.com",
            "reuters.com",
            "cnn.com",
            "npr.org"
        ]
        for source in sources:
            item = QListWidgetItem(source)
            item.setFlags(
                item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
                | Qt.ItemFlag.ItemIsEnabled
            )
            item.setCheckState(
                Qt.CheckState.Unchecked
            )  # Standardmäßig nicht ausgewählt
            self.news_sources_selector.addItem(item)
        layout.addWidget(self.news_sources_selector)

        self.button = QPushButton("Save Settings")
        self.button.clicked.connect(self.on_save_settings_clicked)
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.button = QPushButton("Gesture Control starten")

        self.button.clicked.connect(self.on_button_clicked)

        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)

    def on_button_clicked(self):
        if not self.gesture_control:
            self.process = subprocess.Popen([sys.executable, "vision/gesture_control.py"])
            self.button.setText("Gesture Control running...\nClick to stop")
            self.gesture_control = True
        else:
            self.process.terminate()
            self.process.wait()
            self.button.setText("Gesture Control starten")
            self.gesture_control = False

    def on_save_settings_clicked(self):
        name = self.name_input.text()
        city = self.city_input.text()
        language = self.language_selector.currentText()
        weather_units = self.weather_units_selector.currentText()
        briefing_time = self.briefing_time_selector.currentText()

        selected_sources = []
        for index in range(self.news_sources_selector.count()):
            item = self.news_sources_selector.item(index)
            if item.checkState() == Qt.CheckState.Checked:
                selected_sources.append(item.text())

        print(f"Name: {name}")
        print(f"City: {city}")
        print(f"Language: {language}")
        print(f"Briefing Time: {briefing_time}")
        print(f"Weather Units: {weather_units}")
        print(f"Selected News Sources: {', '.join(selected_sources)}")

        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO user (name, city, briefing_time, language, news_sources, weather_units)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    city,
                    briefing_time,
                    language,
                    ",".join(selected_sources),
                    weather_units,
                ),
            )
            conn.commit()


app = QApplication(sys.argv)

app.setStyleSheet("""
    QWidget {
        background-color: #121212;
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }
    QPushButton {
      background-color: #1e88e5;
      border: none;
      border-radius: 5px;
      padding: 10px 20px;
      font-size: 14px;
      min-width: 200px; /* Verhindert, dass der Button beim Textwechsel springt */
    }
    QPushButton:hover {
        background-color: #1565c0;
    }
""")


def start_gui():
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
