# ui_main.py
# All UI layout lives here.

import tkinter as tk
from pathlib import Path

PURPLE = "#6a1b9a"
PAGE_BG = "#ffffff"
LINE_COLOR = "#6a1b9a"
MARGIN_COLOR = "#6a1b9a"

ASSETS_DIR = Path(__file__).parent / "assets" / "ui"


class ChecklistUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.images = {}
        self._load_images()
        self._build_window()
        self._build_menus()
        self._build_custom_titlebar()
        self._build_page()
        self._build_title()
        self._build_list()

    # ---------- assets ----------
    def _load_images(self):
        """Load PNGs/JPGs if you have them. Safe if they don't exist yet."""
        bg_path = ASSETS_DIR / "background.png"
        if bg_path.exists():
            self.images["background"] = tk.PhotoImage(file=str(bg_path))

        # later you can add:
        # self.images["tab_file"] = tk.PhotoImage(file=ASSETS_DIR / "tab_file.png")
        # etc.

    # ---------- window base ----------
    def _build_window(self):
        self.root.title("Checklist Quest")
        self.root.geometry("600x800")
        self.root.minsize(500, 600)
        self.root.configure(bg=PURPLE)

    # ---------- logical menus (back-end) ----------
    def _build_menus(self):
        self.menubar = tk.Menu(self.root)

        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="New List", command=self._todo)
        self.file_menu.add_command(label="Open...", command=self._todo)
        self.file_menu.add_command(label="Save", command=self._todo)
        self.file_menu.add_command(label="Save As...", command=self._todo)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Export...", command=self._todo)
        self.file_menu.add_command(label="Import...", command=self._todo)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Pin to Desktop", command=self._todo)
        self.file_menu.add_command(label="Reset Template", command=self._todo)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.settings_menu = tk.Menu(self.menubar, tearoff=0)
        self.settings_menu.add_command(label="Title Font...", command=self._todo)
        self.settings_menu.add_command(label="Title Color...", command=self._todo)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label="Item Font...", command=self._todo)
        self.settings_menu.add_command(label="Item Color...", command=self._todo)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label="Bullet Style...", command=self._todo)

        self.themes_menu = tk.Menu(self.menubar, tearoff=0)
        self.themes_menu.add_command(label="Default", command=self._todo)
        self.themes_menu.add_command(label="Goth Girly", command=self._todo)
        self.themes_menu.add_command(label="Pastel Gamer", command=self._todo)
        self.themes_menu.add_command(label="Custom...", command=self._todo)

        self.tools_menu = tk.Menu(self.menubar, tearoff=0)
        self.tools_menu.add_command(label="Task Timer", command=self._todo)
        self.tools_menu.add_command(label="Clear Completed", command=self._todo)

        self.xp_menu = tk.Menu(self.menubar, tearoff=0)
        self.xp_menu.add_command(label="My Stickers", command=self._todo)
        self.xp_menu.add_command(label="Progress", command=self._todo)
        self.xp_menu.add_separator()
        self.xp_menu.add_command(
            label="Watch Ad for Sticker (coming soon)",
            state="disabled",
            command=self._todo,
        )

        # NOTE: we do NOT attach this to root as a classic menubar.
        # It will be used as popup menus from the custom tabs.

    # ---------- custom titlebar with tabs ----------
    def _build_custom_titlebar(self):
        TITLE_BAR_HEIGHT = 30

        title_bar = tk.Frame(self.root, bg=PURPLE, height=TITLE_BAR_HEIGHT)
        title_bar.pack(fill="x", side="top")

        tabs_frame = tk.Frame(title_bar, bg=PURPLE)
        tabs_frame.pack(side="left", padx=4)

        def make_tab(text, menu_obj):
            tab = tk.Label(
                tabs_frame,
                text=text,
                bg="#fdfdfd",
                fg="black",
                padx=12,
                pady=4,
                bd=1,
                relief="ridge",
                font=("Consolas", 10, "bold"),
            )
            tab.pack(side="left", padx=(0, 2), pady=(4, 0))

            def on_click(event):
                x = tab.winfo_rootx()
                y = tab.winfo_rooty() + tab.winfo_height()
                menu_obj.tk_popup(x, y)

            tab.bind("<Button-1>", on_click)
            return tab

        make_tab("File", self.file_menu)
        make_tab("Settings", self.settings_menu)
        make_tab("Themes", self.themes_menu)
        make_tab("Tools", self.tools_menu)
        make_tab("XP", self.xp_menu)

        # window buttons
        buttons_frame = tk.Frame(title_bar, bg=PURPLE)
        buttons_frame.pack(side="right", padx=4)

        btn_min = tk.Button(
            buttons_frame,
            text="-",
            command=self.root.iconify,
            bg=PURPLE,
            fg="white",
            bd=0,
            padx=6,
        )
        btn_min.pack(side="left")

        self._is_maximized = False
        self._original_geom = ""

        def toggle_maximize():
            if not self._is_maximized:
                self._original_geom = self.root.geometry()
                self.root.state("zoomed")
                self._is_maximized = True
            else:
                self.root.state("normal")
                if self._original_geom:
                    self.root.geometry(self._original_geom)
                self._is_maximized = False

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
            command=self.root.destroy,
            bg=PURPLE,
            fg="white",
            bd=0,
            padx=6,
        )
        btn_close.pack(side="left")

    # ---------- page ----------
    def _build_page(self):
        outer = tk.Frame(self.root, bg=PURPLE)
        outer.pack(fill="both", expand=True)

        page_container = tk.Frame(
            outer,
            bg=PURPLE,
            padx=40,
            pady=40,
        )
        page_container.pack(fill="both", expand=True)

        # if you later set a background image, you can put a Canvas/Label here
        self.page = tk.Frame(page_container, bg=PAGE_BG, bd=0, highlightthickness=0)
        self.page.pack(fill="both", expand=True)

    # ---------- title ----------
    def _build_title(self):
        title_frame = tk.Frame(self.page, bg=PAGE_BG)
        title_frame.pack(fill="x", padx=20, pady=(20, 10))

        self.title_var = tk.StringVar(value="Check List Title")

        title_entry = tk.Entry(
            title_frame,
            textvariable=self.title_var,
            font=("Consolas", 28, "bold"),
            bd=0,
            highlightthickness=0,
            fg=PURPLE,
            bg=PAGE_BG,
            insertbackground=PURPLE,
        )
        title_entry.pack(fill="x")

    # ---------- list ----------
    def _build_list(self):
        list_frame = tk.Frame(self.page, bg=PAGE_BG)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        margin = tk.Frame(list_frame, bg=MARGIN_COLOR, width=4)
        margin.pack(side="left", fill="y", padx=(0, 12))

        rows_frame = tk.Frame(list_frame, bg=PAGE_BG)
        rows_frame.pack(side="left", fill="both", expand=True)

        self.items = []

        for _ in range(12):
            row_container = tk.Frame(rows_frame, bg=PAGE_BG)
            row_container.pack(fill="x")

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

            self.items.append((var, entry))

    # ---------- placeholder ----------
    def _todo(self):
        print("TODO: Not implemented yet")
