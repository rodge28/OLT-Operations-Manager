import ttkbootstrap as ttk

from db.database import DatabaseManager
from gui.dialogs.add_olt_dialog import AddOLTDialog
from services.olt_service import OLTService


class OLTPage(ttk.Frame):

    def __init__(self, master):

        super().__init__(master)

        database = DatabaseManager()
        session = database.get_session()

        self.service = OLTService(session)

        self.create_widgets()
        self.load_data()

    def create_widgets(self):

        title = ttk.Label(
            self,
            text="OLT Manager",
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=10)

        columns = (
            "Hostname",
            "Cluster",
            "IP Address",
            "Vendor",
            "Model"
        )

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=15
        )

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.column("Hostname", width=180)
        self.tree.column("Cluster", width=120)
        self.tree.column("IP Address", width=150)
        self.tree.column("Vendor", width=120)
        self.tree.column("Model", width=180)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # -----------------------------------------------------------------
        # Buttons
        # -----------------------------------------------------------------

        button_frame = ttk.Frame(self)
        button_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ttk.Button(
            button_frame,
            text="Add OLT",
            bootstyle="success",
            command=self.add_olt
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Refresh",
            command=self.load_data
        ).pack(side="left", padx=5)

    def load_data(self):

        # Clear Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load OLTs
        for olt in self.service.get_all():

            self.tree.insert(
                "",
                "end",
                values=(
                    olt.hostname,
                    olt.cluster.name if olt.cluster else "",
                    olt.ip_address,
                    olt.vendor,
                    olt.model
                )
            )

    def add_olt(self):

        AddOLTDialog(
            self,
            self.service.session,
            self.load_data
        )
