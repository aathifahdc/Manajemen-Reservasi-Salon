import csv
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import random

class Reservation:
    def __init__(self, id, name, date, time, service):
        self.id = id
        self.name = name
        self.date = date
        self.time = time
        self.service = service

class SalonReservationSystem:
    def __init__(self):
        self.reservations = []

    def add_reservation(self, reservation):
        self.reservations.append(reservation)

    def view_reservations(self):
        return self.reservations

    def delete_reservation(self, reservation_id):
        for i, reservation in enumerate(self.reservations):
            if reservation.id == reservation_id:
                del self.reservations[i]
                return True
        return False

    def import_from_csv(self, filename):
        try:
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    self.add_reservation(Reservation(row[0], row[1], row[2], row[3], row[4]))
        except Exception as e:
            print(f"Error reading CSV file: {e}")

    def search_reservation(self, name):
        result = [reservation for reservation in self.reservations if reservation.name.lower() == name.lower()]
        return result

    def sort_reservations(self):
        self.reservations.sort(key=lambda x: (x.date, x.time))

    def update_reservation(self, id, updated_reservation):
        for reservation in self.reservations:
            if reservation.id == id:
                reservation.name = updated_reservation.name
                reservation.date = updated_reservation.date
                reservation.time = updated_reservation.time
                reservation.service = updated_reservation.service
                return True
        return False

class ReservationApp:
    def __init__(self, root, system):
        self.system = system
        self.root = root
        self.root.title("Salon Reservation System")
        self.root.geometry("800x600")

        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left Frame Widgets
        tk.Label(left_frame, text="Data Pemesanan").pack()

        self.id_entry = tk.Entry(left_frame)
        self.id_entry.pack()
        self.id_entry.insert(0, "ID")
        self.id_entry.bind("<FocusIn>", self.clear_placeholder)
        self.id_entry.bind("<FocusOut>", self.add_placeholder)

        self.name_entry = tk.Entry(left_frame)
        self.name_entry.pack()
        self.name_entry.insert(0, "Name")
        self.name_entry.bind("<FocusIn>", self.clear_placeholder)
        self.name_entry.bind("<FocusOut>", self.add_placeholder)

        self.date_entry = tk.Entry(left_frame)
        self.date_entry.pack()
        self.date_entry.insert(0, "Date")
        self.date_entry.bind("<FocusIn>", self.clear_placeholder)
        self.date_entry.bind("<FocusOut>", self.add_placeholder)

        self.time_entry = tk.Entry(left_frame)
        self.time_entry.pack()
        self.time_entry.insert(0, "Time")
        self.time_entry.bind("<FocusIn>", self.clear_placeholder)
        self.time_entry.bind("<FocusOut>", self.add_placeholder)

        self.service_entry = tk.Entry(left_frame)
        self.service_entry.pack()
        self.service_entry.insert(0, "Service")
        self.service_entry.bind("<FocusIn>", self.clear_placeholder)
        self.service_entry.bind("<FocusOut>", self.add_placeholder)

        self.add_button = tk.Button(left_frame, text="Add Reservation", command=self.add_reservation)
        self.add_button.pack(pady=5)

        self.import_button = tk.Button(left_frame, text="Import CSV", command=self.import_csv)
        self.import_button.pack(pady=5)

        self.view_button = tk.Button(left_frame, text="View Reservations", command=self.view_reservations)
        self.view_button.pack(pady=5)

        self.delete_button = tk.Button(left_frame, text="Cancel Reservation", command=self.delete_reservation)
        self.delete_button.pack(pady=5)

        self.update_button = tk.Button(left_frame, text="Update Reservation", command=self.update_reservation_window)
        self.update_button.pack(pady=5)

        self.search_button = tk.Button(left_frame, text="Search Reservation", command=self.search_reservation)
        self.search_button.pack(pady=5)

        # Right Frame for displaying reservations
        self.informasi_label = tk.Label(right_frame, text="Informasi Pemesanan")
        self.informasi_label.pack()

        self.canvas = tk.Canvas(right_frame)
        self.scroll_frame = tk.Frame(self.canvas)
        self.scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def clear_placeholder(self, event):
        if event.widget.get() in ["ID", "Name", "Date", "Time", "Service"]:
            event.widget.delete(0, tk.END)
            event.widget.config(fg='black')

    def add_placeholder(self, event):
        if event.widget.get() == "":
            placeholder = {
                self.id_entry: "ID",
                self.name_entry: "Name",
                self.date_entry: "Date",
                self.time_entry: "Time",
                self.service_entry: "Service"
            }
            event.widget.insert(0, placeholder[event.widget])
            event.widget.config(fg='grey')

    def import_csv(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.system.import_from_csv(filename)
            self.update_listbox()
            messagebox.showinfo("Success", "Reservations imported successfully")

    def add_reservation(self):
        id = self.id_entry.get()
        name = self.name_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        service = self.service_entry.get()

        if id not in ["ID", ""] and name not in ["Name", ""] and date not in ["Date", ""] and time not in ["Time", ""] and service not in ["Service", ""]:
            reservation = Reservation(id, name, date, time, service)
            self.system.add_reservation(reservation)
            self.update_listbox()
            messagebox.showinfo("Success", "Reservation added successfully")
        else:
            messagebox.showwarning("Input Error", "All fields must be filled out")

    def view_reservations(self):
        self.system.sort_reservations()
        self.update_listbox()

    def delete_reservation(self):
        id = simpledialog.askstring("Input", "Enter ID of the reservation to cancel:")
        if id:
            if self.system.delete_reservation(id):
                self.update_listbox()
                self.reset_form()
                messagebox.showinfo("Success", "Reservation cancelled successfully")
            else:
                messagebox.showwarning("Error", "Reservation not found")
        else:
            messagebox.showwarning("Input Error", "ID must be provided")

    def update_reservation_window(self):
        id = simpledialog.askstring("Input", "Enter ID of the reservation to update:")
        if id:
            existing_reservation = next((r for r in self.system.view_reservations() if r.id == id), None)
            if existing_reservation:
                self.show_update_dialog(existing_reservation)
            else:
                messagebox.showwarning("Error", "Reservation not found")
        else:
            messagebox.showwarning("Input Error", "ID must be provided")

    def show_update_dialog(self, reservation):
        update_dialog = tk.Toplevel(self.root)
        update_dialog.title("Update Reservation")

        tk.Label(update_dialog, text="Update Reservation", font=('Helvetica', 14)).pack(pady=10)

        tk.Label(update_dialog, text="Name:").pack()
        name_entry = tk.Entry(update_dialog, width=30)
        name_entry.pack()
        name_entry.insert(0, reservation.name)

        tk.Label(update_dialog, text="Date:").pack()
        date_entry = tk.Entry(update_dialog, width=30)
        date_entry.pack()
        date_entry.insert(0, reservation.date)

        tk.Label(update_dialog, text="Time:").pack()
        time_entry = tk.Entry(update_dialog, width=30)
        time_entry.pack()
        time_entry.insert(0, reservation.time)

        tk.Label(update_dialog, text="Service:").pack()
        service_entry = tk.Entry(update_dialog, width=30)
        service_entry.pack()
        service_entry.insert(0, reservation.service)

        update_button = tk.Button(update_dialog, text="Update", command=lambda: self.update_reservation(id, name_entry.get(), date_entry.get(), time_entry.get(), service_entry.get(), update_dialog))
        update_button.pack(pady=10)

    def update_reservation(self, id, name, date, time, service, update_dialog):
        if name and date and time and service:
            updated_reservation = Reservation(id, name, date, time, service)
            if self.system.update_reservation(id, updated_reservation):
                update_dialog.destroy()
                self.update_listbox()
                messagebox.showinfo("Success", "Reservation updated successfully")
            else:
                messagebox.showwarning("Error", "Reservation not found")
        else:
            messagebox.showwarning("Input Error", "All fields must be filled out")

    def search_reservation(self):
        name = simpledialog.askstring("Input", "Enter name to search:")
        if name:
            results = self.system.search_reservation(name)
            if results:
                self.update_listbox(results)
            else:
                messagebox.showinfo("No Results", "No reservations found for the given name")
        else:
            messagebox.showwarning("Input Error", "Name must be provided")

    def update_listbox(self, reservations=None):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if reservations is None:
            reservations = self.system.view_reservations()

        colors = ['#FFB6C1', '#ADD8E6', '#90EE90', '#FFD700', '#C0C0C0', '#FFA07A', '#87CEFA']
        
        for reservation in reservations:
            # Pilih warna acak dari daftar warna
            color = random.choice(colors)

            # ASCII art untuk bagian atas kartu
            ascii_art_top = """
            .-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-.
            |         RESERVATION DETAILS           |
            `-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-'
            """

            # ASCII art untuk bagian bawah kartu
            ascii_art_bottom = """
            .-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-.
            |                 CARD                  |
            `-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-'
            """

            # Tambahkan kartu ke dalam scroll_frame
            card = tk.Frame(self.scroll_frame, bd=2, relief=tk.SOLID, bg=color)
            card.pack(fill=tk.X, pady=5, padx=10)

            # Tambahkan ASCII art ke dalam kartu
            tk.Label(card, text=ascii_art_top, bg=color).pack(anchor='w')

            # Tampilkan detail reservasi dalam warna yang sama
            tk.Label(card, text=f"Name: {reservation.name}", bg=color).pack(anchor='w')
            tk.Label(card, text=f"Date: {reservation.date}", bg=color).pack(anchor='w')
            tk.Label(card, text=f"Time: {reservation.time}", bg=color).pack(anchor='w')
            tk.Label(card, text=f"Service: {reservation.service}", bg=color).pack(anchor='w')
            tk.Label(card, text=f"ID: {reservation.id}", bg=color).pack(anchor='w')

            # Tambahkan ASCII art bawah ke dalam kartu
            tk.Label(card, text=ascii_art_bottom, bg=color).pack(anchor='w')

            # Tambahkan garis pemisah solid
            tk.Frame(card, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)

    def reset_form(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.service_entry.delete(0, tk.END)

        self.id_entry.insert(0, "ID")
        self.name_entry.insert(0, "Name")
        self.date_entry.insert(0, "Date")
        self.time_entry.insert(0, "Time")
        self.service_entry.insert(0, "Service")

        self.id_entry.config(fg='grey')
        self.name_entry.config(fg='grey')
        self.date_entry.config(fg='grey')
        self.time_entry.config(fg='grey')
        self.service_entry.config(fg='grey')

if __name__ == "__main__":
    root = tk.Tk()
    system = SalonReservationSystem()
    app = ReservationApp(root, system)
    root.mainloop()
