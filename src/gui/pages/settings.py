from __future__ import annotations

import ttkbootstrap as ttk


class SettingsPage(ttk.Frame):

    def __init__(self, master):

        super().__init__(master)

        ttk.Label(
            self,
            text="OLT Manager",
            font=("Segoe UI", 20, "bold")
        ).pack(padx=20, pady=20)
