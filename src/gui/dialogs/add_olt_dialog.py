import ttkbootstrap as ttk
from tkinter import messagebox

from services.cluster_service import ClusterService
from services.olt_service import OLTService


class AddOLTDialog(ttk.Toplevel):

    def __init__(self, master, session, refresh_callback):

        super().__init__(master)

        self.title("Add OLT")
        self.geometry("500x650")
        self.resizable(True, True)

        self.refresh_callback = refresh_callback

        self.cluster_service = ClusterService(session)
        self.olt_service = OLTService(session)

        self.create_widgets()
        self.load_clusters()

        self.grab_set()

    def create_widgets(self):

        padding = 10

        ttk.Label(self, text="Cluster").pack(
            anchor="w",
            padx=padding,
            pady=(15, 0)
        )

        self.cluster = ttk.Combobox(
            self,
            state="readonly"
        )
        self.cluster.pack(fill="x", padx=padding)

        ttk.Label(self, text="Hostname").pack(
            anchor="w",
            padx=padding,
            pady=(10, 0)
        )

        self.hostname = ttk.Entry(self)
        self.hostname.pack(fill="x", padx=padding)

        ttk.Label(self, text="IP Address").pack(
            anchor="w",
            padx=padding,
            pady=(10, 0)
        )

        self.ip = ttk.Entry(self)
        self.ip.pack(fill="x", padx=padding)

        ttk.Label(self, text="SSH Username").pack(
            anchor="w",
            padx=padding,
            pady=(10, 0)
        )

        self.username = ttk.Entry(self)
        self.username.pack(fill="x", padx=padding)

        ttk.Label(self, text="SSH Password").pack(
            anchor="w",
            padx=padding,
            pady=(10, 0)
        )

        self.password = ttk.Entry(
            self,
            show="*"
        )
        self.password.pack(fill="x", padx=padding)

        ttk.Button(
            self,
            text="Save",
            bootstyle="success",
            command=self.save
        ).pack(pady=20)

    def load_clusters(self):

        self.clusters = self.cluster_service.get_all()

        self.cluster["values"] = [
            cluster.name
            for cluster in self.clusters
        ]

        if self.clusters:
            self.cluster.current(0)

    def save(self):

        if not self.hostname.get().strip():

            messagebox.showerror(
                "Validation",
                "Hostname is required."
            )
            return

        cluster = self.clusters[self.cluster.current()]

        self.olt_service.add(
            cluster.id,
            self.hostname.get().strip(),
            self.ip.get().strip(),
            self.username.get().strip(),
            self.password.get()
        )

        self.refresh_callback()

        self.destroy()
