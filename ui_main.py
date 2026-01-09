# -*- coding: utf-8 -*-
# ui_main.py
# Canvas-based UI for "Checklist Quest"

import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk

PURPLE = "#6a1b9a"
PAGE_BG_FALLBACK = "#e7cbff"  # light purple that matches your art

ASSETS_DIR = Path(__file__).parent / "assets"


class ChecklistUI:
    def __init__(self, root: tk.Tk):
        self.root = root

        # image storage
        self.base_tabbar_img = None
        self.base_app_bg_img = None
        self.checkbox_unchecked = None
        self.checkbox_checked = None
        self.icon_min = None
        self.icon_max = None
        self.icon_close = None
        self.images: dict[str, object] = {}

        self.title_height = 60
        self._drag_data = {"x": 0, "y": 0}
        self._is_maximized = False
        self._original_geom = ""

        # build basic window + UI structure
        self._build_window()
        self._load_images()
        self._build_menus()
        self._build_titlebar()
        self._build_canvas_and_content()

        self.cb_nudge_y = 0  # use -1 or -2 if boxes sit slightly low

        # canvas-list state MUST exist before _build_list
        self.canvas_items = []
        self.list_padx = 24
        self.list_start_y = 172
        self.row_h = 35.6

        self._build_title()
        
        self.max_rows = 20
        self.item_texts = [""] * self.max_rows
        self._build_add_bar()
        self._build_list()


        # # DEBUG + first render
        # print("=== ABOUT TO CALL _render_backgrounds DIRECTLY ===")
        # self._render_backgrounds()
        # print("=== RETURNED FROM _render_backgrounds ===")

        # re-render after layout settles
        self.root.after(50, self._render_backgrounds)

    # ---------- window ----------
    def _build_window(self):
        self.root.title("Checklist Quest")
        self.root.geometry("600x800")
        self.root.minsize(600, 800)
        self.root.configure(bg=PAGE_BG_FALLBACK)
        self.root.overrideredirect(True)  # remove OS title bar
        self.root.bind("<Configure>", self._on_resize)

    # ---------- load images ----------
    def _load_images(self):
        print("ASSETS_DIR =", ASSETS_DIR.resolve())

        def dbg(name: str):
            p = ASSETS_DIR / name
            print(name, "exists:", p.exists(), "->", p)
            return p

        # tab bar (top)
        p = dbg("tabbar.png")
        if p.exists():
            self.base_tabbar_img = Image.open(p).convert("RGBA")

        # SINGLE full-window background image (your merged art)
        p = dbg("app_background.png")
        if p.exists():
            self.base_app_bg_img = Image.open(p).convert("RGBA")
        else:
            self.base_app_bg_img = None

        # checkboxes
        p_unchecked = dbg("checkbox_unchecked.png")
        p_checked = dbg("checkbox_checked_purple.png")
        if p_unchecked.exists() and p_checked.exists():
            self.checkbox_unchecked = ImageTk.PhotoImage(
                Image.open(p_unchecked).convert("RGBA")
            )
            self.checkbox_checked = ImageTk.PhotoImage(
                Image.open(p_checked).convert("RGBA")
            )
            self.images["cb_unchecked"] = self.checkbox_unchecked
            self.images["cb_checked"] = self.checkbox_checked

        # window icons
        def load_icon(name: str, size=(20, 20)):
            p = dbg(name)
            if p.exists():
                img = Image.open(p).convert("RGBA").resize(size, Image.BILINEAR)
                tk_img = ImageTk.PhotoImage(img)
                self.images[name] = tk_img
                return tk_img
            return None

        self.icon_min = load_icon("minimize.png")
        self.icon_max = load_icon("maximize.png")
        self.icon_close = load_icon("close.png")

    # ---------- menus ----------
    def _build_menus(self):
        self.file_menu = tk.Menu(self.root, tearoff=0)
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

        self.settings_menu = tk.Menu(self.root, tearoff=0)
        self.settings_menu.add_command(label="Title Font...", command=self._todo)
        self.settings_menu.add_command(label="Title Color...", command=self._todo)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label="Item Font...", command=self._todo)
        self.settings_menu.add_command(label="Item Color...", command=self._todo)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label="Bullet Style...", command=self._todo)

        self.themes_menu = tk.Menu(self.root, tearoff=0)
        self.themes_menu.add_command(label="Default", command=self._todo)
        self.themes_menu.add_command(label="Goth Girly", command=self._todo)
        self.themes_menu.add_command(label="Pastel Gamer", command=self._todo)
        self.themes_menu.add_command(label="Custom...", command=self._todo)

        self.tools_menu = tk.Menu(self.root, tearoff=0)
        self.tools_menu.add_command(label="Task Timer", command=self._todo)
        self.tools_menu.add_command(label="Clear Completed", command=self._todo)

        self.xp_menu = tk.Menu(self.root, tearoff=0)
        self.xp_menu.add_command(label="My Stickers", command=self._todo)
        self.xp_menu.add_command(label="Progress", command=self._todo)
        self.xp_menu.add_separator()
        self.xp_menu.add_command(
            label="Watch Ad for Sticker (coming soon)",
            state="disabled",
            command=self._todo,
        )

    # ---------- title bar ----------
    def _build_titlebar(self):
        self.title_canvas = tk.Canvas(
            self.root,
            height=self.title_height,
            highlightthickness=0,
            bd=0,
            bg=PURPLE,
        )
        self.title_canvas.pack(fill="x", side="top")

        self._render_tabbar()

        # drag + clicks
        self.title_canvas.bind("<ButtonPress-1>", self._start_move)
        self.title_canvas.bind("<B1-Motion>", self._on_move)
        self.title_canvas.bind("<Button-1>", self._on_title_click)

    def _build_add_bar(self):
        self.add_bar = tk.Frame(self.content, bg="white", bd=0, highlightthickness=0)
        self.add_bar.pack(fill="x", padx=20, pady=(0, 10))

        self.new_item_var = tk.StringVar()

        entry = tk.Entry(
            self.add_bar,
            textvariable=self.new_item_var,
            font=("Consolas", 14),
            bd=0,
            highlightthickness=1,
            relief="solid",
            bg="#ffffff",
            insertbackground=PURPLE,
        )
        entry.pack(side="left", fill="x", expand=True)

        btn = tk.Button(
            self.add_bar,
            text="Add",
            font=("Consolas", 12, "bold"),
            bd=0,
            padx=14,
            pady=6,
            bg=PURPLE,
            fg="white",
            activebackground=PURPLE,
            activeforeground="white",
            command=self._add_item_from_bar,
        )
        btn.pack(side="left", padx=(10, 0))

        entry.bind("<Return>", lambda e: self._add_item_from_bar())

    def _render_tabbar(self):
        self.title_canvas.delete("all")
        width = max(self.root.winfo_width(), 1)
        height = self.title_height

        # bar
        if self.base_tabbar_img is not None:
            resized = self.base_tabbar_img.resize((width, height), Image.BILINEAR)
            self.images["tabbar_scaled"] = ImageTk.PhotoImage(resized)
            self.title_canvas.create_image(
                0, 0, anchor="nw", image=self.images["tabbar_scaled"], tags="tabbar"
            )
        else:
            self.title_canvas.create_rectangle(
                0, 0, width, height, fill=PURPLE, outline="", tags="tabbar"
            )

        # window icons (aligned vertically)
        cy = height // 2
        if self.icon_min:
            self.title_canvas.create_image(
                int(width * 0.88), cy, image=self.icon_min, tags="icons"
            )
        if self.icon_max:
            self.title_canvas.create_image(
                int(width * 0.93), cy, image=self.icon_max, tags="icons"
            )
        if self.icon_close:
            self.title_canvas.create_image(
                int(width * 0.98), cy, image=self.icon_close, tags="icons"
            )

    # ---------- canvas + content ----------
    def _build_canvas_and_content(self):
        self.header_panel_id = None
        # main canvas holds background image + content frame
        self.canvas = tk.Canvas(
            self.root,
            highlightthickness=0,
            bd=0,
            bg=PAGE_BG_FALLBACK,
        )
        self.canvas.pack(fill="both", expand=True)

        # drag from empty canvas
        self.canvas.bind("<ButtonPress-1>", self._start_move)
        self.canvas.bind("<B1-Motion>", self._on_move)

        # background image will be drawn here
        self.bg_image_id = None

        # content frame (everything except tabbar)
        self.content = tk.Frame(self.canvas, bg="white", bd=0, highlightthickness=0)

        # place content using create_window so it moves with canvas
        self.content_window_id = self.canvas.create_window(
            0,
            0,
            anchor="nw",
            window=self.content,
        )
    def _render_header_panel(self):
        # Must run after widgets have sizes
        self.root.update_idletasks()

        w = self.canvas.winfo_width()
        if w < 10:
            return

        # Measure how tall the title + add bar area actually is
        title_h = self.title_frame.winfo_height() if hasattr(self, "title_frame") else 0
        add_h = self.add_bar.winfo_height() if hasattr(self, "add_bar") else 0

        panel_h = max(120, title_h + add_h + 30)  # extra padding

        if self.header_panel_id is None:
            self.header_panel_id = self.canvas.create_rectangle(
                0, 0, w, panel_h,
                fill="white",
                outline=""
            )
        else:
            self.canvas.coords(self.header_panel_id, 0, 0, w, panel_h)

        # Layering: background at back, then panel, then content widgets
        if self.bg_image_id is not None:
            self.canvas.tag_lower(self.bg_image_id)
        self.canvas.tag_raise(self.header_panel_id)
        self.canvas.tag_raise(self.content_window_id)


        # keep content stretched horizontally when canvas resizes
        def on_canvas_resize(event):
            # keep content frame stretched
            self.canvas.itemconfigure(
                self.content_window_id,
                width=event.width,
            )

            # only redraw background when the canvas is actually a real size
            if event.width > 10 and event.height > 10:
                
                print("  on_canvas_resize -> calling _render_backgrounds")
                self._render_backgrounds()
                self._render_header_panel()

        self.canvas.bind("<Configure>", on_canvas_resize)
        



    # # ---------- backgrounds ----------
    def _render_backgrounds(self):
        if self.base_app_bg_img is None:
            return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 5 or h < 5:
            return

        resized = self.base_app_bg_img.resize((w, h), Image.BILINEAR)
        self.images["app_bg_scaled"] = ImageTk.PhotoImage(resized)

        if self.bg_image_id is None:
            self.bg_image_id = self.canvas.create_image(
                0, 0, anchor="nw", image=self.images["app_bg_scaled"]
            )
            self.canvas.tag_lower(self.bg_image_id)  # ← RIGHT HERE
        else:
            self.canvas.itemconfig(
                self.bg_image_id, image=self.images["app_bg_scaled"]
            )

        # keep canvas checklist aligned
        self._layout_canvas_list()
        
        self._render_header_panel()

   

    # ---------- title inside content ----------
    def _build_title(self):
        self.title_frame = tk.Frame(self.content, bg="white", highlightthickness=0, bd=0)
        self.title_frame.pack(fill="x", padx=20, pady=(20, 10))

        self.title_var = tk.StringVar(value="Check List Title")

        title_entry = tk.Entry(
            self.title_frame,
            textvariable=self.title_var,
            font=("Consolas", 28, "bold"),
            bd=0,
            highlightthickness=0,
            fg=PURPLE,
            bg="#ffffff",
            insertbackground=PURPLE,
        )
        title_entry.pack(fill="x")

    # ---------- list ----------
    def _build_list(self):
        # Canvas-based list (no Frames, no Checkbutton widgets)
        self.canvas_items.clear()

        # create 12 empty rows
        for i in range(self.max_rows):
            var = tk.BooleanVar(value=False)

            # create checkbox image
            cb_img = self.checkbox_checked if var.get() else self.checkbox_unchecked
            cb_id = self.canvas.create_image(0, 0, anchor="nw", image=cb_img)

            # create text
            text_id = self.canvas.create_text(
                0, 0,
                anchor="nw",
                text=self.item_texts[i],
                font=("Consolas", 14),
                fill="black"
            )

            # editing entry (hidden until used)
            entry = tk.Entry(
                self.root,                 # root is fine; it will be embedded into canvas
                font=("Consolas", 14),
                bd=0,
                highlightthickness=1,
                relief="solid",
                bg="#ffffff",
                insertbackground=PURPLE
            )
            entry_win_id = self.canvas.create_window(0, 0, anchor="nw", window=entry)
            self.canvas.itemconfigure(entry_win_id, state="hidden")

            item = {
                "var": var,
                "cb_id": cb_id,
                "text_id": text_id,
                "entry": entry,
                "entry_win_id": entry_win_id,
            }
            self.canvas_items.append(item)

            # bindings
            self.canvas.tag_bind(cb_id, "<Button-1>", lambda e, idx=i: self._toggle_item(idx))
            self.canvas.tag_bind(text_id, "<Button-1>", lambda e, idx=i: self._start_edit_item(idx))

            entry.bind("<Return>", lambda e, idx=i: self._finish_edit_item(idx))
            entry.bind("<FocusOut>", lambda e, idx=i: self._finish_edit_item(idx))

        # initial layout
        self._layout_canvas_list()

    def _layout_canvas_list(self):
        if not self.canvas_items:
            return

        w = self.canvas.winfo_width()
        if w < 10:
            return

        x0 = self.list_padx
        y0 = self.list_start_y

        cb_size = 24  
        text_x = x0 + cb_size + 14
        max_text_w = max(100, w - text_x - self.list_padx)

        for i, item in enumerate(self.canvas_items):
            y_line = int(round(self.list_start_y + i * self.row_h))  # this is the ruled line Y

            cb_y = y_line - (cb_size // 2) + self.cb_nudge_y
            self.canvas.coords(item["cb_id"], x0, cb_y)

            # keep text aligned to the same line
            self.canvas.coords(item["text_id"], text_x, y_line - 10)   # adjust only if needed
            self.canvas.coords(item["entry_win_id"], text_x, y_line - 12)

            # keep entry aligned with text, when shown
            self.canvas.coords(item["entry_win_id"], text_x, y+4)
            self.canvas.itemconfigure(item["entry_win_id"], width=max_text_w)

    def _add_item_from_bar(self):
        text = self.new_item_var.get().strip()
        if not text:
            return

        idx = self._first_empty_row()
        if idx is None:
            return  # no space left (could expand max_rows later)

        self.item_texts[idx] = text
        self.canvas.itemconfig(self.canvas_items[idx]["text_id"], text=text)
        self.new_item_var.set("")

    def _first_empty_row(self):
        for i, t in enumerate(self.item_texts):
            if not t.strip():
                return i
        return None

    def _toggle_item(self, idx: int):
        item = self.canvas_items[idx]
        v = item["var"]
        v.set(not v.get())

        img = self.checkbox_checked if v.get() else self.checkbox_unchecked
        self.canvas.itemconfig(item["cb_id"], image=img)

    def _start_edit_item(self, idx: int):
        item = self.canvas_items[idx]
        current = self.canvas.itemcget(item["text_id"], "text")

        ent = item["entry"]
        ent.delete(0, "end")
        ent.insert(0, current)

        self.canvas.itemconfigure(item["entry_win_id"], state="normal")
        ent.focus_set()
        ent.icursor("end")

    def _finish_edit_item(self, idx: int):
        item = self.canvas_items[idx]
        ent = item["entry"]

        new_text = ent.get()
        self.item_texts[idx] = new_text
        self.canvas.itemconfig(item["text_id"], text=new_text)

        self.canvas.itemconfigure(item["entry_win_id"], state="hidden")
        return "break"


    # ---------- events ----------
    def _on_resize(self, event):
        if event.widget is self.root:
            self._render_tabbar()
            self._render_backgrounds()

    def _start_move(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def _on_move(self, event):
        if not self._is_maximized:
            x = event.x_root - self._drag_data["x"]
            y = event.y_root - self._drag_data["y"]
            self.root.geometry(f"+{x}+{y}")

    def _on_title_click(self, event):
        width = max(self.title_canvas.winfo_width(), 1)
        r = event.x / width  # 0..1

        # tabs based on 600px design
        if r < (100 / 600):
            self._open_menu("File", event)
        elif r < (200 / 600):
            self._open_menu("Settings", event)
        elif r < (300 / 600):
            self._open_menu("Themes", event)
        elif r < (400 / 600):
            self._open_menu("Tools", event)
        elif r < (500 / 600):
            self._open_menu("XP", event)
        # window buttons right side
        elif r >= (570 / 600):
            self._close()
        elif r >= (540 / 600):
            self._toggle_max()
        elif r >= (515 / 600):
            self._minimize()

    def _open_menu(self, label, event):
        x = self.title_canvas.winfo_rootx() + event.x
        y = self.title_canvas.winfo_rooty() + self.title_height
        if label == "File":
            self.file_menu.tk_popup(x, y)
        elif label == "Settings":
            self.settings_menu.tk_popup(x, y)
        elif label == "Themes":
            self.themes_menu.tk_popup(x, y)
        elif label == "Tools":
            self.tools_menu.tk_popup(x, y)
        elif label == "XP":
            self.xp_menu.tk_popup(x, y)

    def _minimize(self):
        self.root.iconify()

    def _toggle_max(self):
        if not self._is_maximized:
            self._original_geom = self.root.geometry()
            self.root.state("zoomed")
            self._is_maximized = True
        else:
            self.root.state("normal")
            if self._original_geom:
                self.root.geometry(self._original_geom)
            self._is_maximized = False

    def _close(self):
        self.root.destroy()

    def _todo(self):
        print("TODO: Not implemented yet")

