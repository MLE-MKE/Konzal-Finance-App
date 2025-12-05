# -*- coding: utf-8 -*-

import tkinter as tk

# Colors
PURPLE = "#6a1b9a"      # outer background / accents
PAGE_BG = "#ffffff"     # inner page background
LINE_COLOR = "#6a1b9a"  # notebook horizontal lines
MARGIN_COLOR = "#6a1b9a"


def todo():
    print("TODO: Not implemented yet")


# ---------- ROOT WINDOW ----------
root = tk.Tk()
root.title("Checklist Quest")
root.geometry("600x800")
root.minsize(500, 600)
root.configure(bg=PURPLE)


# ---------- MENUBAR ----------
menubar = tk.Menu(root)

# File menu
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="New List", command=todo)
file_menu.add_command(label="Open...", command=todo)
file_menu.add_command(label="Save", command=todo)
file_menu.add_command(label="Save As...", command=todo)
file_menu.add_separator()
file_menu.add_command(label="Export...", command=todo)
file_menu.add_command(label="Import...", command=todo)
file_menu.add_separator()
file_menu.add_command(label="Pin to Desktop", command=todo)
file_menu.add_command(label="Reset Template", command=todo)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)

# Settings menu
settings_menu = tk.Menu(menubar, tearoff=0)
settings_menu.add_command(label="Title Font...", command=todo)
settings_menu.add_command(label="Title Color...", command=todo)
settings_menu.add_separator()
settings_menu.add_command(label="Item Font...", command=todo)
settings_menu.add_command(label="Item Color...", command=todo)
settings_menu.add_separator()
settings_menu.add_command(label="Bullet Style...", command=todo)
menubar.add_cascade(label="Settings", menu=settings_menu)

# Themes menu
themes_menu = tk.Menu(menubar, tearoff=0)
themes_menu.add_command(label="Default", command=todo)
themes_menu.add_command(label="Goth Girly", command=todo)
themes_menu.add_command(label="Pastel Gamer", command=todo)
themes_menu.add_command(label="Custom...", command=todo)
menubar.add_cascade(label="Themes", menu=themes_menu)

# Tools menu
tools_menu = tk.Menu(menubar, tearoff=0)
tools_menu.add_command(label="Task Timer", command=todo)
tools_menu.add_command(label="Clear Completed", command=todo)
menubar.add_cascade(label="Tools", menu=tools_menu)

# XP menu
xp_menu = tk.Menu(menubar, tearoff=0)
xp_menu.add_command(label="My Stickers", command=todo)
xp_menu.add_command(label="Progress", command=todo)
xp_menu.add_separator()
xp_menu.add_command(
    label="Watch Ad for Sticker (coming soon)",
    state="disabled",
    command=todo,
)
menubar.add_cascade(label="XP", menu=xp_menu)

# root.config(menu=menubar)
# ---------- CUSTOM TITLE BAR (tabs + window buttons) ----------

TITLE_BAR_HEIGHT = 30

title_bar = tk.Frame(root, bg=PURPLE, height=TITLE_BAR_HEIGHT)
title_bar.pack(fill="x", side="top")

# Container for tabs on the left
tabs_frame = tk.Frame(title_bar, bg=PURPLE)
tabs_frame.pack(side="left", padx=4)

# Helper to create one "tab" label
def make_tab(text, menu_obj):
    tab = tk.Label(
        tabs_frame,
        text=text,
        bg="#fdfdfd",          # white tab
        fg="black",
        padx=12,
        pady=4,
        bd=1,
        relief="ridge",
        font=("Consolas", 10, "bold")
    )

    # Slight top "notch" effect: pad bottom so it looks like a tab
    tab.pack(side="left", padx=(0, 2), pady=(4, 0))

    # On click, show the popup menu
    def on_click(event):
        # Compute screen coords for popup
        x = tab.winfo_rootx()
        y = tab.winfo_rooty() + tab.winfo_height()
        menu_obj.tk_popup(x, y)

    tab.bind("<Button-1>", on_click)
    return tab

# Create tabs using the existing menus
file_tab = make_tab("File", file_menu)
settings_tab = make_tab("Settings", settings_menu)
themes_tab = make_tab("Themes", themes_menu)
tools_tab = make_tab("Tools", tools_menu)
xp_tab = make_tab("XP", xp_menu)

# Window control buttons on the right
buttons_frame = tk.Frame(title_bar, bg=PURPLE)
buttons_frame.pack(side="right", padx=4)

def minimize():
    root.iconify()

# Basic maximize toggle (very simple)
is_maximized = {"value": False}
original_geometry = {"value": root.geometry()}

def toggle_maximize():
    if not is_maximized["value"]:
        original_geometry["value"] = root.geometry()
        root.state("zoomed")       # maximize
        is_maximized["value"] = True
    else:
        root.state("normal")
        root.geometry(original_geometry["value"])
        is_maximized["value"] = False

def close():
    root.destroy()

btn_min = tk.Button(
    buttons_frame,
    text="-",
    command=minimize,
    bg=PURPLE,
    fg="white",
    bd=0,
    padx=6,
)
btn_min.pack(side="left")

btn_max = tk.Button(
    buttons_frame,
    text="□",
    command=toggle_maximize,
    bg=PURPLE,
    fg="white",
    bd=0,
    padx=6,
)
btn_max.pack(side="left")

btn_close = tk.Button(
    buttons_frame,
    text="X",
    command=close,
    bg=PURPLE,
    fg="white",
    bd=0,
    padx=6,
)
btn_close.pack(side="left")



# ---------- PAGE CONTAINER ----------
outer = tk.Frame(root, bg=PURPLE)
outer.pack(fill="both", expand=True)

page_container = tk.Frame(
    outer,
    bg=PURPLE,
    padx=40,
    pady=40,
)
page_container.pack(fill="both", expand=True)

page = tk.Frame(page_container, bg=PAGE_BG, bd=0, highlightthickness=0)
page.pack(fill="both", expand=True)


# ---------- TITLE AREA ----------
title_frame = tk.Frame(page, bg=PAGE_BG)
title_frame.pack(fill="x", padx=20, pady=(20, 10))

title_var = tk.StringVar(value="Check List Title")

title_entry = tk.Entry(
    title_frame,
    textvariable=title_var,
    font=("Consolas", 28, "bold"),
    bd=0,
    highlightthickness=0,
    fg=PURPLE,
    bg=PAGE_BG,
    insertbackground=PURPLE,
)
title_entry.pack(fill="x")


# ---------- LIST AREA ----------
list_frame = tk.Frame(page, bg=PAGE_BG)
list_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

# Left margin line
margin = tk.Frame(list_frame, bg=MARGIN_COLOR, width=4)
margin.pack(side="left", fill="y", padx=(0, 12))

# Rows area
rows_frame = tk.Frame(list_frame, bg=PAGE_BG)
rows_frame.pack(side="left", fill="both", expand=True)

items = []

for _ in range(12):
    row_container = tk.Frame(rows_frame, bg=PAGE_BG)
    row_container.pack(fill="x")

    # horizontal line
    line = tk.Frame(row_container, bg=LINE_COLOR, height=2)
    line.pack(fill="x", side="bottom")

    row = tk.Frame(row_container, bg=PAGE_BG)
    row.pack(fill="x", pady=2)

    var = tk.BooleanVar()
    cb = tk.Checkbutton(
        row,
        variable=var,
        bg=PAGE_BG,
        activebackground=PAGE_BG,
        highlightthickness=0,
        bd=0,
    )
    cb.pack(side="left")

    entry = tk.Entry(
        row,
        font=("Consolas", 14),
        bd=0,
        highlightthickness=0,
        bg=PAGE_BG,
    )
    entry.pack(side="left", fill="x", expand=True, padx=(10, 0))

    items.append((var, entry))


# ---------- MAINLOOP ----------
root.mainloop()
