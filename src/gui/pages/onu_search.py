import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox


class ONUPage(ttk.Frame):

    def __init__(
        self,
        parent,
        subscriber_service,
        package_service,
        olt_service,
    ):
        super().__init__(parent)

        # Save the services
        self.subscriber_service = subscriber_service
        self.package_service = package_service
        self.olt_service = olt_service

        self.pack(fill=BOTH, expand=True, padx=15, pady=15)

        self.create_search_frame()
        self.create_info_frame()
        self.create_package_frame()
        self.create_status_bar()

    # =====================================================

    def create_search_frame(self):

        frame = ttk.LabelFrame(
            self,
            text="Search Subscriber",
        )
        frame.pack(fill=X, pady=(0, 10))

        container = ttk.Frame(frame)
        container.pack(fill=X, padx=15, pady=15)

        ttk.Label(
            container,
            text="Serial Number"
        ).grid(row=0, column=0, sticky=W)

        self.serial_entry = ttk.Entry(
            container,
            width=40,
        )
        self.serial_entry.grid(
            row=1,
            column=0,
            padx=(0, 10),
            pady=5,
        )

        self.search_button = ttk.Button(
            container,
            text="Search",
            bootstyle=PRIMARY,
            command=self.search_subscriber,
        )
        self.search_button.grid(
            row=1,
            column=1,
        )

    # =====================================================

    def create_info_frame(self):

        frame = ttk.LabelFrame(
            self,
            text="Subscriber Information",
        )
        frame.pack(fill=X, pady=(0, 10))

        container = ttk.Frame(frame)
        container.pack(fill=X, padx=15, pady=15)

        self.info_labels = {}

        fields = [
            "Account Number",
            "Customer Name",
            "OLT",
            "F/S/P",
            "ONT ID",
            "Service Port",
            "Current Package",
        ]

        for row, field in enumerate(fields):

            ttk.Label(
                container,
                text=f"{field}:",
                width=18,
            ).grid(
                row=row,
                column=0,
                sticky=W,
                pady=2,
            )

            value = ttk.Label(
                container,
                text="-",
            )

            value.grid(
                row=row,
                column=1,
                sticky=W,
                padx=10,
            )

            self.info_labels[field] = value

    # =====================================================

    def create_package_frame(self):

        frame = ttk.LabelFrame(
            self,
            text="Package Change",
        )
        frame.pack(fill=X)

        container = ttk.Frame(frame)
        container.pack(fill=X, padx=15, pady=15)

        ttk.Label(
            container,
            text="Target Package",
        ).grid(
            row=0,
            column=0,
            sticky=W,
        )

        self.package_combo = ttk.Combobox(
            container,
            width=35,
            state="readonly",
        )

        self.package_combo.grid(
            row=1,
            column=0,
            pady=5,
        )

        self.change_button = ttk.Button(
            container,
            text="Change Package",
            bootstyle=SUCCESS,
            state=DISABLED,
            command=self.change_package,
        )

        self.change_button.grid(
            row=1,
            column=1,
            padx=10,
        )
        packages = self.package_service.get_all()

        self.package_map = {}

        values = []

        for package in packages:

            values.append(package.name)
            self.package_map[package.name] = package

        self.package_combo["values"] = values

    # =====================================================

    def create_status_bar(self):

        self.status = ttk.Label(
            self,
            text="Ready.",
            anchor=W,
        )

        self.status.pack(
            fill=X,
            pady=(15, 0),
        )

    def search_subscriber(self):

        serial = self.serial_entry.get().strip().upper()

        if not serial:
            self.status.config(text="Enter a serial number.")
            return

        self.status.config(text="Searching...")

        subscriber = None
        olt_name = ""

        for olt in self.olt_service.get_all():

            subscriber = self.subscriber_service.find_by_serial(
                olt.id,
                serial,
            )

            if subscriber:
                olt_name = olt.hostname
                break

        if subscriber is None:

            self.status.config(text="Subscriber not found.")

            return

        self.info_labels["Account Number"].config(
            text=subscriber.account_number
        )

        self.info_labels["Customer Name"].config(
            text=subscriber.customer_name
        )

        self.info_labels["OLT"].config(
            text=olt_name
        )

        self.info_labels["F/S/P"].config(
            text=subscriber.fsp
        )

        self.info_labels["ONT ID"].config(
            text=subscriber.ont_id
        )

        self.info_labels["Service Port"].config(
            text=subscriber.service_port
        )

        self.info_labels["Current Package"].config(
            text=subscriber.inbound_profile
        )

        packages = self.package_service.get_all()

        self.package_combo["values"] = [
            pkg.name for pkg in packages
        ]

        self.change_button.config(state=NORMAL)

        self.status.config(text="Subscriber found.")

        self.current_subscriber = subscriber


    def get_selected_package(self):

        name = self.package_combo.get()

        return self.package_map.get(name)


    def change_package(self):

        package = self.get_selected_package()

        if package is None:

            Messagebox.show_warning(
                "Please select a package.",
                "No Package Selected"
            )

            return

        current_profile = self.current_subscriber.inbound_profile

        message = (
            f"Subscriber : {self.current_subscriber.customer_name}\n\n"
            f"Service Port : {self.current_subscriber.service_port}\n\n"
            f"Current Package\n"
            f"{current_profile}\n\n"
            f"New Package\n"
            f"{package.profile_name}\n\n"
            "Continue?"
        )

        answer = Messagebox.yesno(
            title="Confirm Package Change",
            message=message,
        )

        if answer != "Yes":
            return

        print("Confirmed!")
