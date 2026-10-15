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
    QSpacerItem,
    QSizePolicy
)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("FluffelNexus")
        
        # WINDOWSIZE
        self.setFixedSize(350, 550)

        self.gesture_control = False
        self.process = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 1. GESTURE CONTROL BUTTON
        self.gesture_button = QPushButton("Start Gesture Control")
        self.gesture_button.clicked.connect(self.on_button_clicked)
        main_layout.addWidget(self.gesture_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # 2. BUTTON TO HIDE/SHOW SETTINGS
        self.settings_toggle_button = QPushButton("⚙️ Show Settings")
        self.settings_toggle_button.setCheckable(True)
        self.settings_toggle_button.setChecked(False)
        self.settings_toggle_button.clicked.connect(self.toggle_settings)
        main_layout.addWidget(self.settings_toggle_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # 3. CONTAINER FOR SETTINGS
        self.settings_container = QWidget()
        settings_layout = QVBoxLayout(self.settings_container)
        settings_layout.setContentsMargins(0, 10, 0, 10)

        settings_layout.addWidget(QLabel("Input Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e. g. John Doe")
        settings_layout.addWidget(self.name_input)

        settings_layout.addWidget(QLabel("Input City:"))
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("e. g. Berlin")
        settings_layout.addWidget(self.city_input)

        settings_layout.addWidget(QLabel("Select Morning Briefing Time:"))
        self.briefing_time_selector = QComboBox()
        self.briefing_time_selector.addItems(["06:30", "07:00", "07:30", "08:00", "18:38"])
        settings_layout.addWidget(self.briefing_time_selector)

        settings_layout.addWidget(QLabel("Select News Language:"))
        self.language_selector = QComboBox()
        self.language_selector.addItems(["Deutsch", "English"])
        settings_layout.addWidget(self.language_selector)

        settings_layout.addWidget(QLabel("Select Weather Units:"))
        self.weather_units_selector = QComboBox()
        self.weather_units_selector.addItems(["Metric", "Imperial"])
        settings_layout.addWidget(self.weather_units_selector)

        settings_layout.addWidget(QLabel("Select News Sources:"))
        self.news_sources_selector = QListWidget()
        self.news_sources_selector.setMaximumHeight(100) 
        sources = [
            "spiegel.de", "tagesschau.de", "zeit.de", "welt.de", "faz.net",
            "sueddeutsche.de", "focus.de", "nytimes.com", "washingtonpost.com",
            "wsj.com", "apnews.com", "reuters.com", "cnn.com", "npr.org"
        ]
        for source in sources:
            item = QListWidgetItem(source)
            item.setFlags(
                item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
                | Qt.ItemFlag.ItemIsEnabled
            )
            item.setCheckState(Qt.CheckState.Unchecked)
            self.news_sources_selector.addItem(item)
        settings_layout.addWidget(self.news_sources_selector)

        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.on_save_settings_clicked)
        settings_layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.settings_container.setVisible(False)
        main_layout.addWidget(self.settings_container)

        self.briefing_button = QPushButton("Start daily Briefing Shudeler")
        self.briefing_button.setEnabled(False)
        self.briefing_button.setChecked(False)
        self.briefing_button.clicked.connect(self.start_briefing)
        main_layout.addWidget(self.briefing_button, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addStretch

    def toggle_settings(self, checked):
        if checked:
            self.settings_container.setVisible(True)
            self.settings_toggle_button.setText("⚙️ Hide Settings")
        else:
            self.settings_container.setVisible(False)
            self.settings_toggle_button.setText("⚙️ Show Settings")

    def on_button_clicked(self):
        if not self.gesture_control:
            self.process = subprocess.Popen([sys.executable, "vision/gesture_control.py"])
            self.gesture_button.setText("Gesture Control running...\nClick to stop")
            self.gesture_control = True
        else:
            self.process.terminate()
            self.process.wait()
            self.gesture_button.setText("Start Gesture Control")
            self.gesture_control = False

    def on_save_settings_clicked(self):
        self.name = self.name_input.text()
        self.city = self.city_input.text()
        self.language = self.language_selector.currentText()
        if self.language == "Deutsch":
            self.lang_code = "de"
        elif self.language == "English":    
            self.lang_code = "en"
        self.weather_units = self.weather_units_selector.currentText()
        self.briefing_time = self.briefing_time_selector.currentText()
        

        selected_sources = []
        for index in range(self.news_sources_selector.count()):
            item = self.news_sources_selector.item(index)
            if item.checkState() == Qt.CheckState.Checked:
                selected_sources.append(item.text())

        self.news_sources = ",".join(selected_sources)

        print(f"Name: {self.name}")
        print(f"City: {self.city}")
        print(f"Language: {self.language}")
        print(f"Language Code: {self.lang_code}")
        print(f"Briefing Time: {self.briefing_time}")
        print(f"Weather Units: {self.weather_units}")
        print(f"Selected News Sources: {', '.join(selected_sources)}")

        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO user (name, city, briefing_time, language, lang_code, news_sources, weather_units)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.name,
                    self.city,
                    self.briefing_time,
                    self.language,
                    self.lang_code,
                    self.news_sources,
                    self.weather_units,
                ),
            )
            conn.commit()
        self.briefing_button.setEnabled(True)

    def start_briefing(self):
        self.process = subprocess.Popen([
            sys.executable, 
            "briefing_scheduler.py", 
            str(self.briefing_time), 
            str(self.city),
            str(self.lang_code),
            str(self.news_sources),
            str(self.weather_units)
        ])
        print(f"Briefing shudeled for {self.briefing_time}")


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
      min-width: 200px;
    }
    QPushButton:hover {
        background-color: #1565c0;
    }
""")


def start_gui():
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    start_gui()
