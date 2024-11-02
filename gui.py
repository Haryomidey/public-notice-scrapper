import tkinter as tk
from tkinter import ttk, messagebox
from scraper import scrape_first_public_notice

def start_scraping(search_input_var, start_date_var, end_date_var, state_var, country_var, notice_type_var):
    search_input = search_input_var.get()
    start_date = start_date_var.get()
    end_date = end_date_var.get()
    state = state_var.get()
    country = country_var.get()
    notice_type = notice_type_var.get()

    messagebox.showinfo("Scraping Started", "Scraping process has begun. Please do not close the interface.")
    result_message = scrape_first_public_notice(search_input, start_date, end_date, state, country, notice_type)
    messagebox.showinfo("Scraping Finished", result_message)

def create_gui():
    window = tk.Tk()
    window.title("Public Notices Scraper")
    window.geometry("400x500")

    search_input_var = tk.StringVar()
    start_date_var = tk.StringVar()
    end_date_var = tk.StringVar()
    state_var = tk.StringVar()
    country_var = tk.StringVar()
    notice_type_var = tk.StringVar()

    frame = ttk.Frame(window, padding="20")
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Search Input:").pack(pady=(0, 5))
    ttk.Entry(frame, textvariable=search_input_var, width=40).pack(pady=(0, 10))

    ttk.Label(frame, text="Start Date (MM/DD/YYYY):").pack(pady=(0, 5))
    ttk.Entry(frame, textvariable=start_date_var, width=40).pack(pady=(0, 10))

    ttk.Label(frame, text="End Date (MM/DD/YYYY):").pack(pady=(0, 5))
    ttk.Entry(frame, textvariable=end_date_var, width=40).pack(pady=(0, 10))

    ttk.Label(frame, text="State:").pack(pady=(0, 5))
    ttk.Entry(frame, textvariable=state_var, width=40).pack(pady=(0, 10))

    ttk.Label(frame, text="Country:").pack(pady=(0, 5))
    ttk.Entry(frame, textvariable=country_var, width=40).pack(pady=(0, 10))

    ttk.Label(frame, text="Notice Type:").pack(pady=(0, 5))
    ttk.Entry(frame, textvariable=notice_type_var, width=40).pack(pady=(0, 10))

    start_button = tk.Button(frame, text="Start Scraping", command=lambda: start_scraping(search_input_var, start_date_var, end_date_var, state_var, country_var, notice_type_var), cursor="hand2", font=("Arial", 10, "bold"))
    start_button.pack(pady=20)

    window.mainloop()
