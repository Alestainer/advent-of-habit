#!/bin/bash

# Exit on error
set -e

echo "Building macOS app..."
pyinstaller Advent_of_Habit.spec --noconfirm

echo "App bundle created at: dist/Advent of Habit.app" 