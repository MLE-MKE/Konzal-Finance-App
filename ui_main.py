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

        # build UI inside content frame
        self._build_title()
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
        self.content = tk.Frame(self.canvas, bg="", bd=0, highlightthickness=0)

        # place content using create_window so it moves with canvas
        self.content_window_id = self.canvas.create_window(
            0,
            0,
            anchor="nw",
            window=self.content,
        )

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

        self.canvas.bind("<Configure>", on_canvas_resize)


    def _render_backgrounds(self):
        print("=== _render_backgrounds CALLED ===")
        if self.base_app_bg_img is None:
            print("No app bg loaded")
            return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        print("Canvas size:", w, "x", h)

        if w < 5 or h < 5:
            return  # window hasn't drawn yet

        resized = self.base_app_bg_img.resize((w, h), Image.BILINEAR)
        self.images["app_bg_scaled"] = ImageTk.PhotoImage(resized)

        if self.bg_image_id is None:
            self.bg_image_id = self.canvas.create_image(
                0, 0,
                anchor="nw",
                image=self.images["app_bg_scaled"]
            )
            print("Created bg_image_id:", self.bg_image_id)
        else:
            self.canvas.itemconfig(self.bg_image_id, image=self.images["app_bg_scaled"])
            print("Updated bg_image_id:", self.bg_image_id)

    # # ---------- backgrounds ----------
    # def _render_backgrounds(self):
  

    #     if self.base_app_bg_img is not None and self.canvas is not None:
    #         w = max(self.canvas.winfo_width(), 1)
    #         h = max(self.canvas.winfo_height(), 1)
    #         resized = self.base_app_bg_img.resize((w, h), Image.BILINEAR)
    #         self.images["app_bg_scaled"] = ImageTk.PhotoImage(resized)

    #         if self.bg_image_id is None:
    #             self.bg_image_id = self.canvas.create_image(
    #                 0, 0, anchor="nw", image=self.images["app_bg_scaled"], tags="bg"
    #             )
    #             # make sure bg is at the back
    #             self.canvas.tag_lower("bg")
    #         else:
    #             self.canvas.itemconfig(self.bg_image_id, image=self.images["app_bg_scaled"])   
    #     else:
    #         # solid fallback
    #         self.canvas.configure(bg=PAGE_BG_FALLBACK)

    # ---------- title inside content ----------
    def _build_title(self):
        title_frame = tk.Frame(self.content, bg="", highlightthickness=0, bd=0)
        title_frame.pack(fill="x", padx=20, pady=(20, 10))

        self.title_var = tk.StringVar(value="Check List Title")

        title_entry = tk.Entry(
            title_frame,
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
        list_frame = tk.Frame(self.content, bg="", highlightthickness=0, bd=0)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # allow dragging from empty areas in list_frame
        list_frame.bind("<ButtonPress-1>", self._start_move)
        list_frame.bind("<B1-Motion>", self._on_move)

        self.items = []

        for i in range(12):
            row_frame = tk.Frame(list_frame, bg="", highlightthickness=0, bd=0)
            row_frame.pack(fill="x", pady=4)

            var = tk.BooleanVar(value=False)

            # base checkbox kwargs
            cb_kwargs = dict(
                variable=var,
                highlightthickness=0,
                bd=0,
                pady=0,
                padx=0,
                # let Tk use the parent bg instead of painting a solid block
            )


            # use custom images if available
            if self.checkbox_unchecked and self.checkbox_checked:
                cb_kwargs.update(
                    image=self.checkbox_unchecked,
                    selectimage=self.checkbox_checked,
                    indicatoron=False,
                    compound="center",
                )

            cb = tk.Checkbutton(row_frame, **cb_kwargs)
            cb.pack(side="left")

            # label that visually sits on background (same color as page)
            label = tk.Label(
                row_frame,
                text="",
                font=("Consolas", 14),
                fg="black",
                anchor="w",
            )

            label.pack(side="left", fill="x", expand=True, padx=(10, 0))

            # hidden Entry used only while editing
            entry = tk.Entry(
                row_frame,
                font=("Consolas", 14),
                bd=0,
                highlightthickness=0,
                bg="#ffffff",
                insertbackground=PURPLE,
            )

            def start_edit(event, lbl=label, ent=entry):
                # copy current label text into entry
                ent.delete(0, "end")
                ent.insert(0, lbl.cget("text"))

                # place entry exactly over label
                ent.place(x=lbl.winfo_x(), y=lbl.winfo_y(),
                          width=lbl.winfo_width(), height=lbl.winfo_height())
                ent.focus_set()

            def finish_edit(event, lbl=label, ent=entry):
                lbl.config(text=ent.get())
                ent.place_forget()
                return "break"

            label.bind("<Button-1>", start_edit)
            entry.bind("<Return>", finish_edit)
            entry.bind("<FocusOut>", finish_edit)

            self.items.append((var, cb, label, entry))

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

