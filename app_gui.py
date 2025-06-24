import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, filedialog
from tracker import add_job, list_jobs, update_status, clear_jobs, JOB_STAGES
import pandas as pd

class JobTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Your Unemployment Prevention Device (We are so cooked)")
        self.jobs = []

        self.create_menu()
        self.create_widgets()
        self.refresh_jobs()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Change Background Colour", command=self.change_bg_colour)
        settings_menu.add_command(label="Change Text Colour", command=self.change_text_colour)

        # Export menu
        export_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Export", menu=export_menu)
        export_menu.add_command(label="Export to Excel", command=self.export_to_excel)
        export_menu.add_command(label="Export to PDF", command=self.export_to_pdf)

    def change_bg_colour(self):
        color = colorchooser.askcolor(title="Choose background color")[1]
        if color:
            self.root.configure(bg=color)

    def change_text_colour(self):
        color = colorchooser.askcolor(title="Choose text color")[1]
        if color:
            for widget in self.root.winfo_children():
                try:
                    widget.configure(fg=color)
                except:
                    pass

    def export_to_excel(self):
        jobs = list_jobs()
        if not jobs:
            messagebox.showinfo("Export", "No jobs to export.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df = pd.DataFrame(jobs)
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Export", f"Exported to {file_path}")

    def export_to_pdf(self):
        try:
            from fpdf import FPDF
        except ImportError:
            messagebox.showerror("Missing Package", "Please install fpdf: pip install fpdf")
            return
        jobs = list_jobs()
        if not jobs:
            messagebox.showinfo("Export", "No jobs to export.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Job Applications", ln=True, align='C')
            pdf.ln(10)
            for job in jobs:
                line = f"Company: {job['company']} | Role: {job['role']} | Stage: {job['status']} | Date: {job['applied_date']}"
                pdf.multi_cell(0, 10, line)
            pdf.output(file_path)
            messagebox.showinfo("Export", f"Exported to {file_path}")
    def create_widgets(self):
        # Input Section
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Company:").grid(row=0, column=0)
        self.company_entry = tk.Entry(input_frame)
        self.company_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Role:").grid(row=1, column=0)
        self.role_entry = tk.Entry(input_frame)
        self.role_entry.grid(row=1, column=1)

        add_btn = tk.Button(input_frame, text="Add Application", command=self.add_application)
        add_btn.grid(row=0, column=2, rowspan=2, padx=10)

        # Filter/Search Section
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Filter by Status:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="All")
        filter_options = ["All"] + JOB_STAGES
        self.filter_dropdown = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=filter_options, state="readonly")
        self.filter_dropdown.pack(side=tk.LEFT, padx=5)
        self.filter_dropdown.bind("<<ComboboxSelected>>", lambda e: self.refresh_jobs())

        tk.Label(filter_frame, text="Search:").pack(side=tk.LEFT, padx=(10, 0))
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(filter_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT)
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_jobs())

        # Job List Section
        self.tree = ttk.Treeview(self.root, columns=("Company", "Role", "Stage", "Date"), show="headings")
        self.tree.heading("Company", text="Company")
        self.tree.heading("Role", text="Role")
        self.tree.heading("Stage", text="Stage")
        self.tree.heading("Date", text="Applied Date")
        self.tree.pack(pady=10)

        # Tag Styles (for row colors)
        self.tree.tag_configure("applied", background="#e6f7ff")
        self.tree.tag_configure("interview", background="#fff2cc")
        self.tree.tag_configure("assessment", background="#ffe6cc")
        self.tree.tag_configure("offer", background="#d9fdd3")
        self.tree.tag_configure("rejected", background="#f4cccc")

        # Update Section
        update_frame = tk.Frame(self.root)
        update_frame.pack(pady=5)

        tk.Label(update_frame, text="Update selected job to:").pack(side=tk.LEFT)
        self.stage_var = tk.StringVar()
        self.stage_dropdown = ttk.Combobox(update_frame, textvariable=self.stage_var, values=JOB_STAGES, state="readonly")
        self.stage_dropdown.pack(side=tk.LEFT, padx=5)
        update_btn = tk.Button(update_frame, text="Update", command=self.update_selected_status)
        update_btn.pack(side=tk.LEFT)

        # Clear All Button
        clear_btn = tk.Button(self.root, text="Clear Application", fg="red", command=self.clear_application)
        clear_btn.pack(pady=10)


    def add_application(self):
            company = self.company_entry.get().strip()
            role = self.role_entry.get().strip()
            if company and role:
                add_job(company, role)
                self.company_entry.delete(0, tk.END)
                self.role_entry.delete(0, tk.END)
                self.refresh_jobs()
            else:
                messagebox.showwarning("Missing Info", "Please enter both company and role.")

    def refresh_jobs(self):
        all_jobs = list_jobs()

        # Apply status filter
        selected_filter = self.filter_var.get() if hasattr(self, "filter_var") else "All"
        if selected_filter != "All":
            all_jobs = [job for job in all_jobs if job["status"] == selected_filter]

        # Apply search filter
        search_term = self.search_var.get().lower() if hasattr(self, "search_var") else ""
        if search_term:
            all_jobs = [job for job in all_jobs if
                        search_term in job["company"].lower() or
                        search_term in job["role"].lower()]

        self.jobs = all_jobs
        self.tree.delete(*self.tree.get_children())
        for idx, job in enumerate(self.jobs):
            tag = job["status"].lower()
            self.tree.insert("", "end", iid=idx, values=(
                job["company"], job["role"], job["status"], job["applied_date"]), tags=(tag,))

    def update_selected_status(self):
                selected = self.tree.focus()
                if selected:
                    new_status = self.stage_var.get()
                    if new_status:
                        update_status(int(selected), new_status)
                        self.refresh_jobs()
                    else:
                        messagebox.showwarning("Select Status", "Please choose a new status.")
                else:
                    messagebox.showwarning("No Selection", "Please select a job to update.")

    def clear_application(self):
            selected = self.tree.focus()
            if selected:
                messagebox.askyesno("Is it over?", "Are you sure you want to delete this?")
                clear_jobs(int(selected))
                self.refresh_jobs()


if __name__ == "__main__":
    root = tk.Tk()
    app = JobTrackerApp(root)
    root.mainloop()
