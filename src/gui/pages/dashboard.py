from __future__ import annotations

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class DashboardPage(ttk.Frame):

    def __init__(self, master):

        super().__init__(master)

        title = ttk.Label(
            self,
            text="Dashboard",
            font=("Segoe UI", 22, "bold")
        )
        title.pack(anchor="w", padx=20, pady=(20, 5))

        subtitle = ttk.Label(
            self,
            text="Welcome to OLT Operations Manager"
        )
        subtitle.pack(anchor="w", padx=20)
