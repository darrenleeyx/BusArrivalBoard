import requests
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import ttk

def fetch_data(bus_stop_id):
    response = requests.get(f"https://arrivelah2.busrouter.sg/?id={bus_stop_id}")
    if response.status_code == 200:
        return response.json()
    else:
        mb.showerror("Error", f"Invalid bus stop ID: {bus_stop_id}")
        return None

def update_gui():
    bus_stop_id = bus_stop_entry.get()
    if not bus_stop_id.isdigit():
        mb.showerror("Error", "Bus stop ID must be a number")
        return

    loading_label.grid(row=1, column=0, columnspan=3, pady=10)
    root.update_idletasks()

    data = fetch_data(bus_stop_id)
    loading_label.grid_forget()

    if data:
        services = data.get('services', [])
        for widget in frame.winfo_children():
            widget.destroy() 

        headers = ["Service No", "Next Bus (min)", "Subsequent Bus (min)"]
        for col, header in enumerate(headers):
            ttk.Label(frame, text=header, style="Header.TLabel").grid(row=0, column=col, padx=5, pady=5)

        for row, service in enumerate(services, start=1):
            service_no = service.get('no', 'N/A')
            next_bus = service.get('next', {}).get('duration_ms', 0) // 60000
            subsequent_bus = service.get('subsequent', {}).get('duration_ms', 0) // 60000

            next_bus_text = "ARR" if next_bus <= 0 else next_bus
            subsequent_bus_text = "ARR" if subsequent_bus <= 0 else subsequent_bus

            ttk.Label(frame, text=service_no, style="Service.TLabel").grid(row=row, column=0, padx=5, pady=5)
            ttk.Label(frame, text=next_bus_text, style="Time.TLabel").grid(row=row, column=1, padx=5, pady=5)
            ttk.Label(frame, text=subsequent_bus_text, style="Time.TLabel").grid(row=row, column=2, padx=5, pady=5)
    
    root.update_idletasks()
    root.geometry("")

def start_countdown():
    global countdown_id
    countdown_time = 10
    refresh_button.config(text=f"Refresh ({countdown_time})")
    countdown_id = root.after(1000, countdown, countdown_time - 1)

def countdown(time_left):
    global countdown_id
    if time_left > 0:
        refresh_button.config(text=f"Refresh ({time_left})")
        countdown_id = root.after(1000, countdown, time_left - 1)
    else:
        update_gui()
        start_countdown()

def refresh_data():
    global countdown_id
    if countdown_id:
        root.after_cancel(countdown_id)
    update_gui()
    start_countdown()

root = tk.Tk()
root.title("Bus Arrival Time")

style = ttk.Style()
style.configure("Header.TLabel", font=("Helvetica", 12, "bold"))
style.configure("Service.TLabel", font=("Helvetica", 14, "bold"))
style.configure("Time.TLabel", font=("Helvetica", 10))

input_frame = ttk.Frame(root)
input_frame.grid(row=0, column=0, pady=10)

ttk.Label(input_frame, text="Bus Stop ID:").grid(row=0, column=0, padx=5)
bus_stop_entry = ttk.Entry(input_frame)
bus_stop_entry.grid(row=0, column=1, padx=5)
bus_stop_entry.insert(0, "44591")
bus_stop_entry.focus()

refresh_button = ttk.Button(input_frame, text="Refresh", command=refresh_data)
refresh_button.grid(row=0, column=2, padx=5)

loading_label = ttk.Label(root, text="Loading...", font=("Helvetica", 10))

frame = ttk.Frame(root)
frame.grid(row=1, column=0, sticky="nsew")

countdown_id = None

update_gui()
start_countdown()

root.mainloop()