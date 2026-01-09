# main.py
import tkinter as tk
from ui_main import ChecklistUI

def main():
    root = tk.Tk()
    ui = ChecklistUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

#I PUSHED THIS TO THE WRONG REPOSITORY AHHHHHH

# Things to add and do later so I dont loose track of my structure. 
# ui main dot py main window layout and widget wiring

# tasks.py task list logic and Task model

# file_manager.py save/open/import/export logic

# settings_manager.py  fonts, colors, bullet styles

# theme_manager.py  themes, backgrounds, “stickers later”

# xp_manager.py XP, projects completed, sticker unlocks

# timer.py  task timer logic (Tools → Task Timer)

# config.py – constants, paths, version, defaults (optional but clean)

# Core classes: ~8–12

# ChecklistApp (main Tk app)

# Task (single item)

# TaskList or TaskListController

# FileManager

# SettingsManager

# ThemeManager

# XPManager

# TaskTimer

# Possibly small helper classes for dialogs or custom widgets (like a PixelButton or StickerIcon later)