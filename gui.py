"""PyQt6 desktop interface."""
from pathlib import Path
import subprocess, sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QComboBox, QLabel, QLineEdit, QListWidget, QListWidgetItem, QMainWindow, QPushButton, QVBoxLayout, QWidget
from database import load_settings, save_settings

BASE = Path(__file__).resolve().parent
SOURCES = ["spiegel.de","tagesschau.de","zeit.de","welt.de","faz.net","sueddeutsche.de","focus.de","nytimes.com","washingtonpost.com","wsj.com","apnews.com","reuters.com","cnn.com","npr.org"]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FluffelNexus")
        self.resize(390, 720)
        self.setMinimumSize(350, 600)
        self.gesture_process = self.scheduler_process = None
        self.saved_settings = None
        central = QWidget(); self.setCentralWidget(central); layout = QVBoxLayout(central)
        self.gesture_button = QPushButton("Start Gesture Control"); self.gesture_button.clicked.connect(self.toggle_gesture); layout.addWidget(self.gesture_button)
        self.settings_toggle = QPushButton("⚙️ Show Settings"); self.settings_toggle.setCheckable(True); self.settings_toggle.toggled.connect(self.toggle_settings); layout.addWidget(self.settings_toggle)
        self.settings = QWidget(); form = QVBoxLayout(self.settings)
        form.addWidget(QLabel("Name:")); self.name_input = QLineEdit(); form.addWidget(self.name_input)
        form.addWidget(QLabel("City:")); self.city_input = QLineEdit(); form.addWidget(self.city_input)
        form.addWidget(QLabel("Daily briefing time:")); self.time_box = QComboBox(); self.time_box.addItems(["06:30","07:00","07:30","08:00","18:38"]); form.addWidget(self.time_box)
        form.addWidget(QLabel("News language:")); self.language_box = QComboBox(); self.language_box.addItem("Deutsch","de"); self.language_box.addItem("English","en"); form.addWidget(self.language_box)
        form.addWidget(QLabel("Weather units:")); self.units_box = QComboBox(); self.units_box.addItem("Metric (°C)","metric"); self.units_box.addItem("Imperial (°F)","imperial"); self.units_box.addItem("Standard (K)","standard"); form.addWidget(self.units_box)
        form.addWidget(QLabel("News sources:")); self.sources = QListWidget(); self.sources.setMaximumHeight(130)
        for source in SOURCES:
            item = QListWidgetItem(source); item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled); item.setCheckState(Qt.CheckState.Unchecked); self.sources.addItem(item)
        form.addWidget(self.sources); save = QPushButton("Save Settings"); save.clicked.connect(self.save); form.addWidget(save)
        self.settings.hide(); layout.addWidget(self.settings)
        self.scheduler_button = QPushButton("Start Daily Briefing Scheduler"); self.scheduler_button.setEnabled(False); self.scheduler_button.clicked.connect(self.toggle_scheduler); layout.addWidget(self.scheduler_button)
        self.status = QLabel("Ready. Save settings to configure the briefing."); self.status.setWordWrap(True); layout.addWidget(self.status); layout.addStretch(1)
        self.load_saved()

    def toggle_settings(self, visible):
        self.settings.setVisible(visible); self.settings_toggle.setText("⚙️ Hide Settings" if visible else "⚙️ Show Settings")

    def load_saved(self):
        try: s = load_settings()
        except Exception as e: self.status.setText(f"Could not load settings: {e}"); return
        if not s: return
        self.saved_settings = s; self.name_input.setText(s.get("name","")); self.city_input.setText(s.get("city",""))
        self.time_box.setCurrentText(s.get("briefing_time","07:00"))
        i = self.language_box.findData(s.get("lang_code","de"))
        if i >= 0: self.language_box.setCurrentIndex(i)
        i = self.units_box.findData(s.get("weather_units","metric"))
        if i >= 0: self.units_box.setCurrentIndex(i)
        selected = set(s.get("news_sources","").split(","))
        for i in range(self.sources.count()):
            item = self.sources.item(i); item.setCheckState(Qt.CheckState.Checked if item.text() in selected else Qt.CheckState.Unchecked)
        self.scheduler_button.setEnabled(True); self.status.setText("Saved settings loaded.")

    def save(self):
        name, city = self.name_input.text().strip(), self.city_input.text().strip()
        selected = [self.sources.item(i).text() for i in range(self.sources.count()) if self.sources.item(i).checkState() == Qt.CheckState.Checked]
        if not name or not city: self.status.setText("Enter a name and city."); return
        if not selected: self.status.setText("Select at least one news source."); return
        s = {"name":name,"city":city,"briefing_time":self.time_box.currentText(),"language":self.language_box.currentText(),"lang_code":self.language_box.currentData(),"news_sources":",".join(selected),"weather_units":self.units_box.currentData()}
        try: save_settings(s)
        except Exception as e: self.status.setText(f"Could not save settings: {e}"); return
        if self.scheduler_process and self.scheduler_process.poll() is None: self.stop_scheduler()
        self.saved_settings = s; self.scheduler_button.setEnabled(True); self.status.setText("Settings saved.")

    def toggle_gesture(self):
        if self.gesture_process and self.gesture_process.poll() is None: self.stop_gesture(); return
        try:
            self.gesture_process = subprocess.Popen([sys.executable,str(BASE/"vision"/"gesture_control.py")],cwd=BASE)
            self.gesture_button.setText("Stop Gesture Control"); self.status.setText("Gesture control running. Press Q in the preview to exit.")
        except OSError as e: self.status.setText(f"Could not start gesture control: {e}")

    @staticmethod
    def stop_process(process):
        if not process or process.poll() is not None: return
        process.terminate()
        try: process.wait(timeout=3)
        except subprocess.TimeoutExpired: process.kill(); process.wait(timeout=3)

    def stop_gesture(self):
        self.stop_process(self.gesture_process); self.gesture_process = None; self.gesture_button.setText("Start Gesture Control")

    def toggle_scheduler(self):
        if self.scheduler_process and self.scheduler_process.poll() is None: self.stop_scheduler(); return
        if not self.saved_settings: self.status.setText("Save settings first."); return
        s = self.saved_settings
        args = [sys.executable,str(BASE/"briefing_scheduler.py"),s["briefing_time"],s["city"],s["lang_code"],s["news_sources"],s["weather_units"]]
        try:
            self.scheduler_process = subprocess.Popen(args,cwd=BASE)
            self.scheduler_button.setText("Stop Daily Briefing Scheduler"); self.status.setText(f"Scheduled daily for {s['briefing_time']}.")
        except OSError as e: self.status.setText(f"Could not start scheduler: {e}")

    def stop_scheduler(self):
        self.stop_process(self.scheduler_process); self.scheduler_process = None; self.scheduler_button.setText("Start Daily Briefing Scheduler")

    def closeEvent(self, event):
        self.stop_gesture(); self.stop_scheduler(); event.accept()

def start_gui():
    app = QApplication.instance() or QApplication(sys.argv)
    app.setStyleSheet("QWidget { background:#121212; color:white; font-family:'Segoe UI'; } QPushButton { background:#1e88e5; border:0; border-radius:5px; padding:10px; } QPushButton:hover { background:#1565c0; } QLineEdit,QComboBox,QListWidget { background:#202020; border:1px solid #444; padding:5px; }")
    window = MainWindow(); window.show(); app.exec()

if __name__ == "__main__": start_gui()
