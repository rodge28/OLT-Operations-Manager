from __future__ import annotations

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from db.database import DatabaseManager

from services.olt_service import OLTService
from services.package_service import PackageService
from services.subscriber_service import SubscriberService

from gui.pages.dashboard import DashboardPage
from gui.pages.olts import OLTPage
from gui.pages.traffic import TrafficPage
from gui.pages.jobs import JobsPage
from gui.pages.reports import ReportsPage
from gui.pages.settings import SettingsPage
from gui.pages.onu_search import ONUPage

class MainWindow:

    def __init__(self):

        self.root = ttk.Window(
            title="OLT Operations Manager",
            themename="darkly",
            size=(1200, 750),
        )
        self.db = DatabaseManager()
        self.session = self.db.get_session()

        self.olt_service = OLTService(self.session)
        self.package_service = PackageService(self.session)
        self.subscriber_service = SubscriberService(self.olt_service)

        self.create_layout()

    def create_layout(self):

        # =============================
        # Navigation Panel
        # =============================

        self.navigation = ttk.Frame(self.root, width=220)
        self.navigation.pack(side=LEFT, fill=Y)

        # =============================
        # Content Area
        # =============================

        self.content = ttk.Frame(self.root)
        self.content.pack(side=LEFT, fill=BOTH, expand=True)

        # =============================
        # Pages
        # =============================

        self.pages = {
            "Dashboard": DashboardPage(self.content),
            "OLTs": OLTPage(self.content),
            "Traffic": TrafficPage(self.content),
            "Jobs": JobsPage(self.content),
            "Reports": ReportsPage(self.content),
            "Settings": SettingsPage(self.content),
            "ONU Search": ONUPage(
                self.content,
                self.subscriber_service,
                self.package_service,
                self.olt_service,
            ),
        }

        # =============================
        # Title
        # =============================

        ttk.Label(
            self.navigation,
            text="OLT Manager",
            font=("Segoe UI", 16, "bold"),
        ).pack(pady=20)

        # =============================
        # Navigation Buttons
        # =============================

        for page_name in self.pages:

            ttk.Button(
                self.navigation,
                text=page_name,
                width=22,
                command=lambda name=page_name: self.show_page(name),
            ).pack(fill=X, padx=10, pady=4)

        # Push status bar to bottom
        ttk.Frame(self.navigation).pack(expand=True, fill=BOTH)

        # =============================
        # Status Bar
        # =============================

        self.status = ttk.Label(
            self.root,
            text="Ready",
            anchor=W,
            relief="sunken",
        )

        self.status.pack(side=BOTTOM, fill=X)

        # Show Dashboard first
        self.show_page("Dashboard")

    # ======================================

    def show_page(self, page_name: str):

        for page in self.pages.values():
            page.pack_forget()

        page = self.pages[page_name]
        page.pack(fill=BOTH, expand=True)

        self.status.config(text=f"Current Page : {page_name}")

    # ======================================

    def run(self):
        self.root.mainloop()
