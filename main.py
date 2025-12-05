# main.py
import tkinter as tk
from ui_main import ChecklistUI

def main():
    root = tk.Tk()
    ui = ChecklistUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
