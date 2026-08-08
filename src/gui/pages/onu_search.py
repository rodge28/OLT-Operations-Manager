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

        # -------------------------------------------------
        # Get selected package
        # -------------------------------------------------

        package = self.get_selected_package()

        if package is None:

            Messagebox.show_warning(
                "Please select a package.",
                "No Package Selected"
            )

            return

        # -------------------------------------------------
        # Current package
        # -------------------------------------------------

        current_profile = self.current_subscriber.inbound_profile
        new_profile = package.profile_name
        service_port = self.current_subscriber.service_port

        # -------------------------------------------------
        # Prevent unnecessary change
        # -------------------------------------------------

        if current_profile == new_profile:

            Messagebox.show_info(
                "The subscriber is already using this package.",
                "No Change Required"
            )

            return

        # -------------------------------------------------
        # Confirmation
        # -------------------------------------------------

        message = (
            f"Subscriber : {self.current_subscriber.customer_name}\n\n"
            f"Service Port : {service_port}\n\n"
            f"Current Package\n"
            f"{current_profile}\n\n"
            f"New Package\n"
            f"{new_profile}\n\n"
            "Continue?"
        )

        answer = Messagebox.yesno(
            title="Confirm Package Change",
            message=message,
        )

        if answer != "Yes":
            return

        # -------------------------------------------------
        # Start operation
        # -------------------------------------------------

        self.status.config(
            text=f"Changing package to {new_profile}..."
        )

        self.change_button.config(
            state=DISABLED
        )

        self.package_combo.config(
            state=DISABLED
        )

        self.update_idletasks()

        try:

            # -------------------------------------------------
            # Find the OLT
            # -------------------------------------------------

            target_olt = None

            for olt in self.olt_service.get_all():

                subscriber = self.subscriber_service.find_by_serial(
                    olt.id,
                    self.current_subscriber.serial,
                )

                if subscriber:

                    target_olt = olt
                    break

            if target_olt is None:

                raise Exception(
                    "Unable to determine the OLT for this subscriber."
                )

            # -------------------------------------------------
            # Execute package change
            # -------------------------------------------------

            from drivers.huawei_driver import HuaweiDriver

            driver = HuaweiDriver(
                host=target_olt.ip_address,
                username=target_olt.username,
                password=target_olt.password,
            )

            try:

                driver.connect()

                result = driver.change_traffic_profile(
                    service_port=service_port,
                    profile_name=new_profile,
                )

            finally:

                driver.disconnect()

            # -------------------------------------------------
            # Check result
            # -------------------------------------------------

            if result is not True:

                    raise Exception(
                        "Package change verification failed.\n\n"
                        f"Expected package:\n"
                        f"{new_profile}\n\n"
                        "The OLT did not confirm the package change."
                )
            # -------------------------------------------------
            # Update local subscriber object
            # -------------------------------------------------

            self.current_subscriber.inbound_profile = new_profile
            self.current_subscriber.outbound_profile = new_profile

            self.info_labels["Current Package"].config(
                text=new_profile
            )

            # -------------------------------------------------
            # Success
            # -------------------------------------------------

            self.status.config(
                text=f"Package changed successfully to {new_profile}."
            )

            Messagebox.show_info(
                f"Package successfully changed to:\n\n"
                f"{new_profile}\n\n"
                f"Service Port: {service_port}",
                "Package Change Successful"
            )

        except Exception as e:

            print("Package change error:", e)

            self.status.config(
                text="Package change failed."
            )

            Messagebox.show_error(
                str(e),
                "Package Change Failed"
            )

        finally:

            self.change_button.config(
                state=NORMAL
            )

            self.package_combo.config(
                state="readonly"
            )
