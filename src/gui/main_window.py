from __future__ import annotations

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from gui.pages.dashboard import DashboardPage
from gui.pages.olts import OLTPage
from gui.pages.traffic import TrafficPage
from gui.pages.jobs import JobsPage
from gui.pages.reports import ReportsPage
from gui.pages.settings import SettingsPage


class MainWindow:

    def __init__(self):

        self.root = ttk.Window(
            title="OLT Operations Manager",
            themename="darkly",
            size=(1200, 750),
        )

        self.create_layout()

    def create_layout(self):

        self.navigation = ttk.Frame(self.root, width=220)
        self.navigation.pack(side=LEFT, fill=Y)

        self.content = ttk.Frame(self.root)
        self.content.pack(side=LEFT, fill=BOTH, expand=True)

        self.pages = {
            "Dashboard": DashboardPage(self.content),
            "OLTs": OLTPage(self.content),
            "Traffic": TrafficPage(self.content),
            "Jobs": JobsPage(self.content),
            "Reports": ReportsPage(self.content),
            "Settings": SettingsPage(self.content),
        }

        ttk.Label(
            self.navigation,
            text="OLT Manager",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)

        for page_name in self.pages.keys():

            ttk.Button(
                self.navigation,
                text=page_name,
                width=22,
                command=lambda p=page_name: self.show_page(p)
            ).pack(pady=4)

        self.status = ttk.Label(
            self.root,
            text="Ready",
            anchor=W
        )

        self.status.pack(side=BOTTOM, fill=X)
        self.show_page("Dashboard")
    def show_page(self, page_name):

        for page in self.pages.values():
            page.pack_forget()

        self.pages[page_name].pack(fill=BOTH, expand=True)

        self.status.config(text=f"Current Page : {page_name}")

    def run(self):
        self.root.mainloop()
