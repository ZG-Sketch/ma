import customtkinter as ctk
import webbrowser

NAV_ITEMS = [
    ("", "批量重命名", "rename"),
    ("", "自动分类", "classify"),
    ("", "空目录清理", "cleanup"),
    ("", "重复检测", "dedupe"),
]
NAV_DICT = {key: label for _, label, key in NAV_ITEMS}


class FileBatchApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FileBatch Pro v1.0.0")
        self.geometry("960x640")
        self.minsize(800, 500)
        self.grid_rowconfigure(0, minsize=40, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, minsize=28, weight=0)
        self.grid_columnconfigure(0, minsize=180, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # Top bar
        top = ctk.CTkFrame(self, height=40, corner_radius=0)
        top.grid(row=0, column=0, columnspan=2, sticky="nsew")
        top.grid_propagate(False)
        ctk.CTkLabel(top, text="  FileBatch Pro v1.0.0",
            font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", padx=10, pady=5)

        # Sidebar
        side = ctk.CTkFrame(self, width=180, corner_radius=0)
        side.grid(row=1, column=0, sticky="nsew")
        side.grid_propagate(False)
        side_title = ctk.CTkLabel(side, text="FUNCTIONS",
            font=ctk.CTkFont(size=10), text_color=("gray50","gray50"))
        side_title.pack(fill="x", padx=10, pady=(10,5))

        self.nav_buttons = {}
        for icon, label, key in NAV_ITEMS:
            try:
                btn = ctk.CTkButton(
                    side, text=label,
                    text_color="white",
                    fg_color="#2b6cb0",
                    hover_color="#3182ce",
                    height=38,
                    corner_radius=4,
                    anchor="w",
                    command=lambda k=key: self.switch_module(k)
                )
                btn.pack(fill="x", padx=6, pady=3)
                self.nav_buttons[key] = btn
            except Exception as e:
                print(f"Button error: {e}")

        # About button at bottom
        side_pad = ctk.CTkFrame(side, height=0, fg_color="transparent")
        side_pad.pack(fill="x")
        self.about_btn = ctk.CTkButton(
            side, text="About FileBatch Pro",
            fg_color="transparent",
            text_color=("gray55", "gray50"),
            hover_color=("gray90", "gray25"),
            height=28, font=ctk.CTkFont(size=11),
            anchor="center", command=self.show_about
        )
        self.about_btn.pack(side="bottom", fill="x", padx=5, pady=(0, 5))

        # Content
        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.grid(row=1, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.placeholder = ctk.CTkLabel(self.content_frame, text="Select a module",
            font=ctk.CTkFont(size=18))
        self.placeholder.grid(row=0, column=0)

        # Status bar
        sb = ctk.CTkFrame(self, height=28, corner_radius=0)
        sb.grid(row=2, column=0, columnspan=2, sticky="nsew")
        sb.grid_propagate(False)
        self.status_label = ctk.CTkLabel(sb, text="Ready",
            font=ctk.CTkFont(size=11), anchor="w")
        self.status_label.pack(side="left", padx=8, pady=2)
        self.modules = {}
        self._current_module = None

    def register_module(self, key, frame_class):
        self.modules[key] = frame_class(self.content_frame)

    def switch_module(self, key):
        if hasattr(self, "placeholder") and self.placeholder.winfo_exists():
            self.placeholder.grid_remove()
        if self._current_module is not None:
            old = self.modules.get(self._current_module)
            if old is not None:
                old.grid_remove()
        new = self.modules.get(key)
        if new is not None:
            new.grid(row=0, column=0, sticky="nsew")
            self._current_module = key
        label = NAV_DICT.get(key, "")
        if label:
            self.set_status("Module: " + label)

    def set_status(self, text):
        self.status_label.configure(text=text)

    def show_about(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("About FileBatch Pro")
        dialog.geometry("380x280")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - 380) // 2
        y = self.winfo_y() + (self.winfo_height() - 280) // 2
        dialog.geometry(f"+{x}+{y}")
        dialog.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(dialog, text="FileBatch Pro",
            font=ctk.CTkFont(size=22, weight="bold")
        ).grid(row=0, column=0, pady=(30, 5))

        ctk.CTkLabel(dialog, text="v1.0.0",
            font=ctk.CTkFont(size=12), text_color=("gray50", "gray60")
        ).grid(row=1, column=0, pady=(0, 15))

        ctk.CTkLabel(dialog, text="Cross-platform file batch processing tool",
            font=ctk.CTkFont(size=12)
        ).grid(row=2, column=0, pady=2)

        # Chinese subtitle using unicode escapes
        subtxt = "\u6279\u91cf\u91cd\u547d\u540d / \u81ea\u52a8\u5206\u7c7b / \u7a7a\u76ee\u5f55\u6e05\u7406 / \u91cd\u590d\u68c0\u6d4b"
        ctk.CTkLabel(dialog, text=subtxt,
            font=ctk.CTkFont(size=11), text_color=("gray40", "gray60")
        ).grid(row=3, column=0, pady=2)

        ctk.CTkButton(dialog, text="Close", width=100,
            command=dialog.destroy
        ).grid(row=4, column=0, pady=(20, 0))


if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    app = FileBatchApp()
    app.mainloop()
