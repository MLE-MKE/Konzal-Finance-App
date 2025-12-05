# -*- coding: utf-8 -*-

import tkinter as tk

PURPLE = "#6a1b9a"
BG = "#ffffff"


class ChecklistApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window basics
        self.title("Checklist Quest")
        self.geometry("600x800")
        self.configure(bg=BG)

        # Build UI
        self._create_menubar()
        self._create_title_area()
        self._create_list_area()

    # MENUS
    def _create_menubar(self):
        menubar = tk.Menu(self)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New List", command=self._todo)
        file_menu.add_command(label="Open...", command=self._todo)
        file_menu.add_command(label="Save", command=self._todo)
        file_menu.add_command(label="Save As...", command=self._todo)
        file_menu.add_separator()
        file_menu.add_command(label="Export...", command=self._todo)
        file_menu.add_command(label="Import...", command=self._todo)
        file_menu.add_separator()
        file_menu.add_command(label="Pin to Desktop", command=self._todo)
        file_menu.add_command(label="Reset Template", command=self._todo)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Title Font...", command=self._todo)
        settings_menu.add_command(label="Title Color...", command=self._todo)
        settings_menu.add_separator()
        settings_menu.add_command(label="Item Font...", command=self._todo)
        settings_menu.add_command(label="Item Color...", command=self._todo)
        settings_menu.add_separator()
        settings_menu.add_command(label="Bullet Style...", command=self._todo)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        # Themes menu
        themes_menu = tk.Menu(menubar, tearoff=0)
        themes_menu.add_command(label="Default", command=self._todo)
        themes_menu.add_command(label="Goth Girly", command=self._todo)
        themes_menu.add_command(label="Pastel Gamer", command=self._todo)
        themes_menu.add_command(label="Custom...", command=self._todo)
        menubar.add_cascade(label="Themes", menu=themes_menu)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Task Timer", command=self._todo)
        tools_menu.add_command(label="Clear Completed", command=self._todo)
        menubar.add_cascade(label="Tools", menu=tools_menu)

        # XP menu
        xp_menu = tk.Menu(menubar, tearoff=0)
        xp_menu.add_command(label="My Stickers", command=self._todo)
        xp_menu.add_command(label="Progress", command=self._todo)
        xp_menu.add_separator()
        xp_menu.add_command(
            label="Watch Ad for Sticker (coming soon)",
            state="disabled",
            command=self._todo,
        )
        menubar.add_cascade(label="XP", menu=xp_menu)

        self.config(menu=menubar)

    # TITLE
    def _create_title_area(self):
        title_frame = tk.Frame(self, bg=BG)
        title_frame.pack(fill="x", padx=20, pady=(20, 10))

        self.title_var = tk.StringVar(value="Check List Title")

        title_entry = tk.Entry(
            title_frame,
            textvariable=self.title_var,
            font=("Consolas", 28, "bold"),
            bd=0,
            highlightthickness=0,
            fg=PURPLE,
            bg=BG,
            insertbackground=PURPLE,
        )
        title_entry.pack(fill="x")

    # LIST AREA
    def _create_list_area(self):
        list_frame = tk.Frame(self, bg=BG)
        list_frame.pack(fill="both", expand=True, padx=40, pady=(10, 20))

        self.items = []

        for _ in range(12):
            row = tk.Frame(list_frame, bg=BG)
            row.pack(fill="x", pady=2)

            var = tk.BooleanVar()
            cb = tk.Checkbutton(
                row,
                variable=var,
                bg=BG,
                activebackground=BG,
                highlightthickness=0,
                bd=0,
            )
            cb.pack(side="left")

            entry = tk.Entry(
                row,
                font=("Consolas", 14),
                bd=0,
                highlightthickness=0,
                bg=BG,
            )
            entry.pack(side="left", fill="x", expand=True, padx=(10, 0))

            self.items.append((var, entry))

    def _todo(self):
        print("TODO: Not implemented yet")


if __name__ == "__main__":
    app = ChecklistApp()
    app.mainloop()
