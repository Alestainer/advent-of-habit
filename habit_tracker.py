#!/usr/bin/env python3
import os
import sys
import json
import calendar
import platform
from datetime import datetime, timedelta, time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QCheckBox, QPushButton, QLabel, QSystemTrayIcon, QMenu,
                           QLineEdit, QHBoxLayout, QMessageBox, QDialog,
                           QTimeEdit, QCalendarWidget, QTabWidget, QRadioButton)
from PyQt6.QtCore import Qt, QTimer, QTime, QDate
from PyQt6.QtGui import QFont, QIcon, QAction, QTextCharFormat, QColor, QPixmap, QPainter, QPen


def get_data_dir() -> Path:
    """Get the appropriate data directory for the current platform."""
    system = platform.system()
    home = Path.home()
    
    if system == "Darwin":  # macOS
        return home / "Library/Application Support/Advent of Habit"
    elif system == "Windows":
        return Path(os.getenv("APPDATA")) / "Advent of Habit"
    else:  # Linux and others
        return home / ".local/share/advent-of-habit"


def get_system_font() -> str:
    """Get the appropriate system font for the current platform."""
    system = platform.system()
    
    if system == "Darwin":
        return ".AppleSystemUIFont"
    elif system == "Windows":
        return "Segoe UI"
    else:  # Linux and others
        return "Ubuntu"


class InitialSetupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Welcome to Advent of Habit")
        self.setModal(True)
        self.habits = []
        self.is_morning = True  # Default to morning
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Welcome message
        welcome = QLabel("Welcome! Please enter up to 3 habits you want to track:")
        welcome.setFont(QFont(".AppleSystemUIFont", 14))
        layout.addWidget(welcome)
        
        # Habit input fields
        self.habit_inputs = []
        for i in range(3):
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"Habit {i+1}")
            self.habit_inputs.append(input_field)
            layout.addWidget(input_field)
        
        # Set default values
        defaults = ["Meditation", "Journaling", "Exercise"]
        for input_field, default in zip(self.habit_inputs, defaults):
            input_field.setText(default)
        
        # Time preference selection
        time_label = QLabel("When do you prefer to check in?")
        time_label.setFont(QFont(".AppleSystemUIFont", 12))
        layout.addWidget(time_label)
        
        time_layout = QHBoxLayout()
        
        self.morning_radio = QRadioButton("Morning (6-11 AM)")
        self.evening_radio = QRadioButton("Evening (6-11 PM)")
        self.morning_radio.setChecked(True)
        
        time_layout.addWidget(self.morning_radio)
        time_layout.addWidget(self.evening_radio)
        
        layout.addLayout(time_layout)
        
        # Done button
        done_button = QPushButton("Start Tracking")
        done_button.clicked.connect(self.accept)
        layout.addWidget(done_button)
        
        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background-color: #2C3E50;
                color: white;
            }
            QLabel {
                color: white;
                padding: 10px;
            }
            QLineEdit {
                background-color: #34495E;
                color: white;
                border: 2px solid #ECF0F1;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
            }
            QRadioButton {
                color: white;
                padding: 8px;
                font-size: 14px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
            }
            QRadioButton::indicator:unchecked {
                background-color: #34495E;
                border: 2px solid #ECF0F1;
                border-radius: 10px;
            }
            QRadioButton::indicator:checked {
                background-color: #27AE60;
                border: 2px solid #ECF0F1;
                border-radius: 10px;
            }
            QPushButton {
                background-color: #27AE60;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #219A52;
            }
        """)
    
    def getHabits(self) -> List[str]:
        habits = []
        for input_field in self.habit_inputs:
            habit = input_field.text().strip()
            if habit:
                habits.append(habit)
        return habits[:3]
    
    def getTimeWindow(self) -> Tuple[QTime, QTime]:
        if self.morning_radio.isChecked():
            return QTime(6, 0), QTime(11, 0)
        else:
            return QTime(18, 0), QTime(23, 0)


class CalendarView(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGridVisible(True)
        self.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.setStyleSheet("""
            QCalendarWidget {
                background-color: #2C3E50;
                color: white;
            }
            QCalendarWidget QTableView {
                alternate-background-color: #34495E;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: white;
            }
            QCalendarWidget QAbstractItemView:disabled {
                color: #7F8C8D;
            }
        """)
    
    def updateHabitData(self, data: Dict[str, Dict[str, bool]], habit: str):
        success_format = QTextCharFormat()
        success_format.setBackground(QColor("#27AE60"))
        success_format.setForeground(QColor("white"))
        
        failure_format = QTextCharFormat()
        failure_format.setBackground(QColor("#E74C3C"))
        failure_format.setForeground(QColor("white"))
        
        # Reset all dates
        self.setDateTextFormat(QDate(), QTextCharFormat())
        
        # Mark completed and missed days
        for date_str, habits in data.items():
            date = QDate.fromString(date_str, "yyyy-MM-dd")
            if habit in habits:
                if habits[habit]:
                    self.setDateTextFormat(date, success_format)
                else:
                    self.setDateTextFormat(date, failure_format)


class HabitWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        # Set up proper platform-specific paths
        self.data_dir = get_data_dir()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.data_file = self.data_dir / "habit_data.json"
        self.config_file = self.data_dir / "config.json"
        
        # Platform-specific window flags
        self.system = platform.system()
        
        # Check if this is first launch
        if not self.config_file.exists():
            self.setupInitialConfig()
        else:
            self.loadConfig()
        
        self.initUI()
        self.setupTrayIcon()
        self.loadData()
        
        # Set up morning check timer
        self.setupMorningCheck()
    
    def setupInitialConfig(self) -> None:
        dialog = InitialSetupDialog(self)
        if dialog.exec():
            self.habits = dialog.getHabits()
            self.start_time, self.end_time = dialog.getTimeWindow()
            self.saveConfig()
        else:
            self.habits = ["Meditation", "Journaling", "Exercise"]
            self.start_time = QTime(6, 0)
            self.end_time = QTime(11, 0)
    
    def loadConfig(self) -> None:
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.habits = config.get('habits', ["Meditation", "Journaling", "Exercise"])
                self.start_time = QTime.fromString(config.get('start_time', '06:00'), "HH:mm")
                self.end_time = QTime.fromString(config.get('end_time', '11:00'), "HH:mm")
        except (json.JSONDecodeError, FileNotFoundError):
            self.habits = ["Meditation", "Journaling", "Exercise"]
            self.start_time = QTime(6, 0)
            self.end_time = QTime(11, 0)
    
    def saveConfig(self) -> None:
        with open(self.config_file, 'w') as f:
            json.dump({
                'habits': self.habits,
                'start_time': self.start_time.toString("HH:mm"),
                'end_time': self.end_time.toString("HH:mm")
            }, f, indent=2)
    
    def initUI(self) -> None:
        self.setWindowTitle("Advent of Habit")
        
        # Platform-specific window flags
        if self.system == "Darwin":  # macOS
            self.setWindowFlags(
                Qt.WindowType.WindowStaysOnTopHint |
                Qt.WindowType.FramelessWindowHint |
                Qt.WindowType.Tool
            )
        elif self.system == "Windows":
            self.setWindowFlags(
                Qt.WindowType.WindowStaysOnTopHint |
                Qt.WindowType.FramelessWindowHint |
                Qt.WindowType.SubWindow
            )
        else:  # Linux
            self.setWindowFlags(
                Qt.WindowType.WindowStaysOnTopHint |
                Qt.WindowType.FramelessWindowHint |
                Qt.WindowType.Dialog
            )
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        
        # Add close button at the top
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        close_button = QPushButton("✕")
        close_button.setFixedSize(24, 24)
        close_button.setObjectName("close")  # For styling
        close_button.clicked.connect(self.hide)
        close_layout.addWidget(close_button)
        main_layout.addLayout(close_layout)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Create and add the habits tab
        habits_tab = QWidget()
        habits_layout = QVBoxLayout()
        habits_tab.setLayout(habits_layout)
        
        # Add checkboxes for habits
        self.checkboxes = {}
        for habit in self.habits:
            checkbox = QCheckBox(habit)
            checkbox.stateChanged.connect(lambda state, h=habit: self.habitStateChanged(h, state))
            self.checkboxes[habit] = checkbox
            habits_layout.addWidget(checkbox)
            
            # Add completion ratio label
            ratio_label = QLabel()
            ratio_label.setObjectName(f"ratio_{habit}")  # For updating later
            habits_layout.addWidget(ratio_label)
        
        habits_layout.addStretch()
        tab_widget.addTab(habits_tab, "Habits")
        
        # Create and add the calendar tab
        calendar_tab = QWidget()
        calendar_layout = QVBoxLayout()
        calendar_tab.setLayout(calendar_layout)
        
        # Add habit selection for calendar
        habit_selector = QHBoxLayout()
        for habit in self.habits:
            radio = QRadioButton(habit)
            radio.toggled.connect(lambda checked, h=habit: self.updateCalendar(h) if checked else None)
            habit_selector.addWidget(radio)
        
        calendar_layout.addLayout(habit_selector)
        
        # Add calendar widget
        self.calendar = CalendarView()
        calendar_layout.addWidget(self.calendar)
        
        tab_widget.addTab(calendar_tab, "Calendar")
        
        main_layout.addWidget(tab_widget)
        
        # Platform-specific styling
        system_font = get_system_font()
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: #2C3E50;
            }}
            QWidget {{
                color: white;
                font-family: "{system_font}";
            }}
            QTabWidget::pane {{
                border: none;
            }}
            QTabWidget::tab-bar {{
                alignment: center;
            }}
            QTabBar::tab {{
                background-color: #34495E;
                color: white;
                padding: 8px 20px;
                margin: 2px;
                border-radius: 4px;
            }}
            QTabBar::tab:selected {{
                background-color: #3498DB;
            }}
            QPushButton#close {{
                background-color: transparent;
                color: white;
                border: none;
                font-size: 16px;
            }}
            QPushButton#close:hover {{
                background-color: #E74C3C;
            }}
            QCheckBox {{
                color: white;
                font-size: 14px;
                padding: 8px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
            }}
            QCheckBox::indicator:unchecked {{
                background-color: #34495E;
                border: 2px solid #ECF0F1;
                border-radius: 4px;
            }}
            QCheckBox::indicator:checked {{
                background-color: #27AE60;
                border: 2px solid #ECF0F1;
                border-radius: 4px;
            }}
            QRadioButton {{
                color: white;
                padding: 8px;
            }}
            QRadioButton::indicator {{
                width: 20px;
                height: 20px;
            }}
            QRadioButton::indicator:unchecked {{
                background-color: #34495E;
                border: 2px solid #ECF0F1;
                border-radius: 10px;
            }}
            QRadioButton::indicator:checked {{
                background-color: #27AE60;
                border: 2px solid #ECF0F1;
                border-radius: 10px;
            }}
            QLabel {{
                color: white;
                padding: 5px;
            }}
        """)
        
        self.setFixedSize(400, 500)
    
    def setupTrayIcon(self) -> None:
        # Create the tray icon
        self.tray_icon = QSystemTrayIcon(self)
        
        # Create the tray menu
        tray_menu = QMenu()
        show_action = QAction("Show Window", self)
        quit_action = QAction("Quit", self)
        
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.quit_app)
        
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        
        # Set up platform-specific tray icon behavior
        if platform.system() == "Darwin":  # macOS
            # Create a green checkmark icon
            pixmap = QPixmap(32, 32)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setPen(QPen(QColor("#27AE60"), 3))
            painter.drawLine(8, 16, 14, 22)
            painter.drawLine(14, 22, 24, 12)
            painter.end()
            self.tray_icon.setIcon(QIcon(pixmap))
        else:  # Windows and Linux
            # Load the app icon for the tray
            self.tray_icon.setIcon(QIcon("images/icon.png"))
        
        # Show the tray icon
        self.tray_icon.show()
        
        # Connect the tray icon activation signal
        if platform.system() == "Darwin":  # macOS
            # macOS: left-click shows context menu
            self.tray_icon.activated.connect(lambda reason: self.tray_icon.contextMenu().popup(
                self.tray_icon.geometry().center()
            ))
        else:  # Windows and Linux
            # Windows/Linux: left-click shows window, right-click shows menu
            self.tray_icon.activated.connect(self.trayIconActivated)
    
    def trayIconActivated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if platform.system() != "Darwin":  # Not needed on macOS
            if reason == QSystemTrayIcon.ActivationReason.Trigger:  # Left click
                self.show()
            elif reason == QSystemTrayIcon.ActivationReason.Context:  # Right click
                self.tray_icon.contextMenu().popup(
                    self.tray_icon.geometry().center()
                )
    
    def quit_app(self) -> None:
        """Properly clean up before quitting."""
        self.tray_icon.hide()
        QApplication.quit()
    
    def calculateStats(self, habit: str, data: Dict[str, Dict[str, bool]]) -> Tuple[int, int]:
        today = datetime.now().date()
        completed_days = 0
        total_days = 0
        
        for i in range(21):
            check_date = today - timedelta(days=i)
            date_str = check_date.strftime("%Y-%m-%d")
            if date_str in data:
                total_days += 1
                if data[date_str].get(habit, False):
                    completed_days += 1
        
        return completed_days, total_days if total_days > 0 else 1
    
    def loadData(self) -> None:
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    today = datetime.now().strftime("%Y-%m-%d")
                    
                    if today in data:
                        for habit, checked in data[today].items():
                            if habit in self.checkboxes:
                                self.checkboxes[habit].setChecked(checked)
                    
                    for habit in self.habits:
                        completed, total = self.calculateStats(habit, data)
                        self.streak_labels[habit].setText(f"{completed}/{total}")
                        
                    # Update calendar if a habit is selected
                    if self.habit_selector.activeAction():
                        self.updateCalendar(self.habit_selector.activeAction().text())
            except (json.JSONDecodeError, FileNotFoundError):
                pass
    
    def saveData(self) -> None:
        today = datetime.now().strftime("%Y-%m-%d")
        data = {}
        
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        data[today] = {
            habit: checkbox.isChecked()
            for habit, checkbox in self.checkboxes.items()
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        for habit in self.habits:
            completed, total = self.calculateStats(habit, data)
            self.streak_labels[habit].setText(f"{completed}/{total}")
            
        # Update calendar if a habit is selected
        if self.habit_selector.activeAction():
            self.updateCalendar(self.habit_selector.activeAction().text())
    
    def closeEvent(self, event) -> None:
        event.ignore()
        self.hide()


def main() -> None:
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = HabitWindow()
    window.show()
    sys.exit(app.exec()) 