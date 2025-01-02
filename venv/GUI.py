import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from enum import Enum


# Enums for DCOP Type and Algorithm
class DcopType(Enum):
    sparse_random_uniform = 1
    dense_random_uniform = 2
    graph_coloring = 3


class Algorithm(Enum):
    branch_and_bound = 1
    dsa_c = 2
    MGM = 3


class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DCOP Management Dashboard")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)

        # Layout Configuration
        self.setup_sidebar()
        self.show_dcop_setup()

    def setup_sidebar(self):
        """Set up sidebar with navigation buttons."""
        sidebar = ttkb.Frame(self.root, width=200, bootstyle="secondary")
        sidebar.pack(side="left", fill="y")

        # Title with icon
        title_label = ttkb.Label(sidebar, text="🗃️ DCOP", font=("Helvetica", 24, "bold"), foreground="#f50057")
        title_label.pack(pady=(20, 10))

        # Navigation options
        nav_items = [
            ("🏠 Home", self.show_dcop_setup),
            ("📊 Results", self.show_results),
            ("📝 Query", self.show_query),
            ("⚙️ Settings", self.show_settings),
        ]

        for text, command in nav_items:
            btn = ttkb.Button(sidebar, text=text, bootstyle="outline", width=16, command=command)
            btn.pack(pady=5, padx=20)

    def show_dcop_setup(self):
        """Show the DCOP setup page."""
        self.clear_main_area()

        # Main setup frame
        setup_frame = ttkb.Frame(self.root, padding=20)
        setup_frame.pack(fill="both", expand=True)

        # Title
        title_label = ttkb.Label(setup_frame, text="DCOP Setup", font=("Helvetica", 24, "bold"), foreground="#00e676")
        title_label.pack(anchor="w", pady=20)

        # Form fields
        self.agents_count = tk.StringVar()
        self.domain_size = tk.StringVar()
        self.dcop_type = tk.StringVar()
        self.algorithm = tk.StringVar()

        # Input Fields
        self.create_input_field(setup_frame, "Number of Agents (1-30):", self.agents_count)
        self.create_input_field(setup_frame, "Size of Domain (1-10):", self.domain_size)
        self.create_dropdown_field(setup_frame, "DCOP Type:", self.dcop_type, DcopType)
        self.create_dropdown_field(setup_frame, "Algorithm:", self.algorithm, Algorithm)

        # Run and Clear Buttons
        buttons_frame = ttkb.Frame(setup_frame)
        buttons_frame.pack(pady=10)

        run_button = ttkb.Button(buttons_frame, text="Run 🚀", command=self.run_dcop, bootstyle="success-outline")
        run_button.pack(side="left", padx=5)
        clear_button = ttkb.Button(buttons_frame, text="Clear ❌", command=self.clear_form, bootstyle="danger-outline")
        clear_button.pack(side="left", padx=5)

    def run_dcop(self):
        try:
            # Validate and run DCOP
            agents = int(self.agents_count.get())
            domain = int(self.domain_size.get())
            dcop_type = self.dcop_type.get()
            algorithm = self.algorithm.get()

            if not (1 <= agents <= 30):
                raise ValueError("Number of agents must be between 1 and 30.")
            if not (1 <= domain <= 10):
                raise ValueError("Domain size must be between 1 and 10.")
            if not dcop_type:
                raise ValueError("Please select a valid DCOP Type.")
            if not algorithm:
                raise ValueError("Please select a valid Algorithm.")

            # Placeholder for DCOP execution
            messagebox.showinfo("DCOP Running", "DCOP setup is running with the provided configuration.")
            self.show_results()

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def show_results(self):
        """Show results page."""
        self.clear_main_area()

        results_frame = ttkb.Frame(self.root, padding=20)
        results_frame.pack(fill="both", expand=True)

        # Title
        title_label = ttkb.Label(results_frame, text="Results", font=("Helvetica", 24, "bold"), foreground="#00e676")
        title_label.pack(anchor="w", pady=20)

        # Results content (sample data)
        sample_text = "Global cost: 150\nAssignments:\nAgent 1 -> Value 2\nAgent 2 -> Value 3\n..."
        results_label = ttkb.Label(results_frame, text=sample_text, font=("Helvetica", 14), anchor="w")
        results_label.pack(fill="x", padx=20, pady=20)

        # Proceed to Query Button
        query_button = ttkb.Button(results_frame, text="Proceed to Query 📝", command=self.show_query, bootstyle="primary-outline")
        query_button.pack(pady=20)

    def show_query(self):
        """Show the query page."""
        self.clear_main_area()

        query_frame = ttkb.Frame(self.root, padding=20)
        query_frame.pack(fill="both", expand=True)

        # Title
        title_label = ttkb.Label(query_frame, text="Query Setup", font=("Helvetica", 24, "bold"), foreground="#00e676")
        title_label.pack(anchor="w", pady=20)

        # Sample query setup fields
        query_label = ttkb.Label(query_frame, text="Specify agent categories for query", font=("Helvetica", 16))
        query_label.pack(anchor="w", pady=10)

        # Example categories and buttons
        categories_frame = ttkb.Frame(query_frame)
        categories_frame.pack(pady=10)

        for i in range(1, 4):
            category_label = ttkb.Label(categories_frame, text=f"Agent {i}: Category {i} 🧑‍💻", font=("Helvetica", 14))
            category_label.pack(anchor="w", padx=20, pady=5)

        submit_button = ttkb.Button(query_frame, text="Submit Query 🚀", command=self.submit_query, bootstyle="success-outline")
        submit_button.pack(pady=20)

    def submit_query(self):
        """Submit the query."""
        messagebox.showinfo("Query Submitted", "Your query has been submitted successfully!")

    def show_settings(self):
        """Show settings page."""
        self.clear_main_area()

        settings_frame = ttkb.Frame(self.root, padding=20)
        settings_frame.pack(fill="both", expand=True)

        # Title
        title_label = ttkb.Label(settings_frame, text="Settings", font=("Helvetica", 24, "bold"), foreground="#00e676")
        title_label.pack(anchor="w", pady=20)

        # Sample settings content
        setting_label = ttkb.Label(settings_frame, text="Adjust your preferences here.", font=("Helvetica", 16))
        setting_label.pack(anchor="w", padx=20, pady=20)

    def create_input_field(self, parent, label_text, var_name):
        frame = ttkb.Frame(parent)
        frame.pack(fill="x", pady=10)
        label = ttkb.Label(frame, text=f"{label_text} 🔢", font=("Helvetica", 14), foreground="white")
        label.pack(side="left", padx=5)
        entry = ttkb.Entry(frame, textvariable=var_name, width=10)
        entry.pack(side="left", padx=10, fill="x", expand=True)

    def create_dropdown_field(self, parent, label_text, var_name, enum_class):
        frame = ttkb.Frame(parent)
        frame.pack(fill="x", pady=10)
        label = ttkb.Label(frame, text=f"{label_text} 🔽", font=("Helvetica", 14), foreground="white")
        label.pack(side="left", padx=5)
        values = [e.name for e in enum_class]
        combo = ttkb.Combobox(frame, textvariable=var_name, values=values, state="readonly")
        combo.pack(side="left", padx=10, fill="x", expand=True)

    def clear_form(self):
        """Clear the DCOP setup form inputs."""
        self.agents_count.set("")
        self.domain_size.set("")
        self.dcop_type.set("")
        self.algorithm.set("")

    def clear_main_area(self):
        """Clear main area to display a new section."""
        for widget in self.root.pack_slaves():
            widget.pack_forget()


if __name__ == "__main__":
    root = ttkb.Window(themename="cyborg")
    app = DashboardApp(root)
    root.mainloop()
