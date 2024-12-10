#!/usr/bin/env python3
import sys
import json
import calendar
from datetime import datetime, timedelta, time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QCheckBox, QPushButton, QLabel, QSystemTrayIcon, QMenu,
                           QLineEdit, QHBoxLayout, QMessageBox, QDialog,
                           QTimeEdit, QCalendarWidget, QTabWidget, QRadioButton)
from PyQt6.QtCore import Qt, QTimer, QTime, QDate
from PyQt6.QtGui import QFont, QIcon, QAction, QTextCharFormat, QColor


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
        
        # Set up proper macOS paths
        app_support = Path.home() / "Library/Application Support/Advent of Habit"
        app_support.mkdir(parents=True, exist_ok=True)
        self.data_file = app_support / "habit_data.json"
        self.config_file = app_support / "config.json"
        
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
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
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
        
        # Habits tab
        habits_widget = QWidget()
        habits_layout = QVBoxLayout()
        
        # Add date
        date_label = QLabel(datetime.now().strftime("%B %d, %Y"))
        date_label.setFont(QFont(".AppleSystemUIFont", 14, QFont.Weight.Bold))
        date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        habits_layout.addWidget(date_label)
        
        # Add habits and streak tracking
        self.checkboxes: Dict[str, QCheckBox] = {}
        self.streak_labels: Dict[str, QLabel] = {}
        
        for habit in self.habits:
            habit_layout = QHBoxLayout()
            
            # Checkbox
            checkbox = QCheckBox(habit)
            checkbox.setFont(QFont(".AppleSystemUIFont", 12))
            checkbox.stateChanged.connect(self.saveData)
            self.checkboxes[habit] = checkbox
            habit_layout.addWidget(checkbox)
            
            # Streak label
            streak_label = QLabel("0/0")
            streak_label.setFont(QFont(".AppleSystemUIFont", 12))
            streak_label.setStyleSheet("color: #27AE60;")
            self.streak_labels[habit] = streak_label
            habit_layout.addWidget(streak_label)
            
            habits_layout.addLayout(habit_layout)
        
        habits_widget.setLayout(habits_layout)
        tab_widget.addTab(habits_widget, "Today")
        
        # Calendar tab
        calendar_widget = QWidget()
        calendar_layout = QVBoxLayout()
        
        # Habit selector for calendar
        self.habit_selector = QMenu()
        habit_button = QPushButton("Select Habit")
        for habit in self.habits:
            action = self.habit_selector.addAction(habit)
            action.triggered.connect(lambda checked, h=habit: self.updateCalendar(h))
        
        habit_button.clicked.connect(lambda: self.habit_selector.exec(habit_button.mapToGlobal(habit_button.rect().bottomLeft())))
        calendar_layout.addWidget(habit_button)
        
        # Calendar
        self.calendar = CalendarView()
        calendar_layout.addWidget(self.calendar)
        
        calendar_widget.setLayout(calendar_layout)
        tab_widget.addTab(calendar_widget, "Calendar")
        
        main_layout.addWidget(tab_widget)
        
        # Set window properties
        self.setStyleSheet("""
            QMainWindow, QTabWidget, QWidget {
                background-color: #2C3E50;
                color: white;
            }
            QTabWidget::pane {
                border: none;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background-color: #34495E;
                color: white;
                padding: 8px 20px;
                margin: 2px;
                border-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #3498DB;
            }
            QCheckBox {
                color: white;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #34495E;
                border: 2px solid #ECF0F1;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                background-color: #27AE60;
                border: 2px solid #ECF0F1;
                border-radius: 4px;
            }
            QLabel {
                color: white;
                padding: 10px;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QPushButton#close {
                background-color: transparent;
                color: #E74C3C;
                font-weight: bold;
                font-size: 16px;
                border-radius: 12px;
                padding: 0;
                margin: 5px;
            }
            QPushButton#close:hover {
                background-color: #E74C3C;
                color: white;
            }
        """)
        
        self.setFixedSize(400, 500)
        self.move(50, 50)
    
    def updateCalendar(self, habit: str) -> None:
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.calendar.updateHabitData(data, habit)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    def setupMorningCheck(self) -> None:
        self.morning_timer = QTimer(self)
        self.morning_timer.timeout.connect(self.checkMorningShow)
        self.morning_timer.start(60000)  # Check every minute
        self.checkMorningShow()
    
    def checkMorningShow(self) -> None:
        current_time = QTime.currentTime()
        
        # Show between start_time and end_time if not checked today
        if self.start_time <= current_time <= self.end_time:
            today = datetime.now().strftime("%Y-%m-%d")
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    if today not in data:
                        self.show()
                        self.raise_()
                        self.activateWindow()
            except (json.JSONDecodeError, FileNotFoundError):
                self.show()
                self.raise_()
                self.activateWindow()
    
    def setupTrayIcon(self) -> None:
        self.tray_icon = QSystemTrayIcon(self)
        
        icon = QIcon.fromTheme("checkbox")
        if not icon.isNull():
            self.tray_icon.setIcon(icon)
        
        tray_menu = QMenu()
        show_action = QAction("Show", self)
        quit_action = QAction("Quit", self)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(QApplication.instance().quit)
        
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        self.tray_icon.activated.connect(self.trayIconActivated)
    
    def trayIconActivated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show()
    
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