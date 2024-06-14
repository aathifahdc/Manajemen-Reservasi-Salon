import csv
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import filedialog


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

    def update_reservation(self, reservation_id, new_reservation):
        for i, reservation in enumerate(self.reservations):
            if reservation.id == reservation_id:
                self.reservations[i] = new_reservation
                return True
        return False

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

# GUI with tkinter
class ReservationApp:
    def __init__(self, root, system):
        self.system = system
        self.root = root
        self.root.title("Salon Reservation System")
        self.root.geometry("800x600")

        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=5)

        self.import_button = tk.Button(buttons_frame, text="Import CSV", command=self.import_csv)
        self.import_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_button = tk.Button(buttons_frame, text="Add Reservation", command=self.add_reservation)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.view_button = tk.Button(buttons_frame, text="View Reservations", command=self.view_reservations)
        self.view_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.update_button = tk.Button(buttons_frame, text="Update Reservation", command=self.update_reservation)
        self.update_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = tk.Button(buttons_frame, text="Delete Reservation", command=self.delete_reservation)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.search_button = tk.Button(buttons_frame, text="Search Reservation", command=self.search_reservation)
        self.search_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.canvas = tk.Canvas(main_frame)
        self.scroll_frame = tk.Frame(self.canvas)
        self.scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def import_csv(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.system.import_from_csv(filename)
            self.update_listbox()
            messagebox.showinfo("Success", "Reservations imported successfully")

    def add_reservation(self):
        id = simpledialog.askstring("Input", "Enter ID:")
        name = simpledialog.askstring("Input", "Enter Name:")
        date = simpledialog.askstring("Input", "Enter Date (YYYY-MM-DD):")
        time = simpledialog.askstring("Input", "Enter Time (HH:MM):")
        service = simpledialog.askstring("Input", "Enter Service:")

        if id and name and date and time and service:
            reservation = Reservation(id, name, date, time, service)
            self.system.add_reservation(reservation)
            self.update_listbox()
            messagebox.showinfo("Success", "Reservation added successfully")
        else:
            messagebox.showwarning("Input Error", "All fields must be filled out")

    def view_reservations(self):
        self.system.sort_reservations()
        self.update_listbox()

    def update_reservation(self):
        id = simpledialog.askstring("Input", "Enter ID of the reservation to update:")
        if id:
            name = simpledialog.askstring("Input", "Enter new Name:")
            date = simpledialog.askstring("Input", "Enter new Date (YYYY-MM-DD):")
            time = simpledialog.askstring("Input", "Enter new Time (HH:MM):")
            service = simpledialog.askstring("Input", "Enter new Service:")

            if name and date and time and service:
                new_reservation = Reservation(id, name, date, time, service)
                if self.system.update_reservation(id, new_reservation):
                    self.update_listbox()
                    messagebox.showinfo("Success", "Reservation updated successfully")
                else:
                    messagebox.showwarning("Error", "Reservation not found")
            else:
                messagebox.showwarning("Input Error", "All fields must be filled out")
        else:
            messagebox.showwarning("Input Error", "ID must be provided")

    def delete_reservation(self):
        id = simpledialog.askstring("Input", "Enter ID of the reservation to delete:")
        if id:
            if self.system.delete_reservation(id):
                self.update_listbox()
                messagebox.showinfo("Success", "Reservation deleted successfully")
            else:
                messagebox.showwarning("Error", "Reservation not found")
        else:
            messagebox.showwarning("Input Error", "ID must be provided")

    def search_reservation(self):
        name = simpledialog.askstring("Input", "Enter Name to search:")
        if name:
            result = self.system.search_reservation(name)
            if result:
                self.update_listbox(result)
            else:
                messagebox.showinfo("Search Result", "No reservations found")
        else:
            messagebox.showwarning("Input Error", "Name must be provided")

    def update_listbox(self, reservations=None):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if reservations is None:
            reservations = self.system.view_reservations()

        ascii_art_top = """
        .-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-.
        |         RESERVATION DETAILS           |
        `-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-'
        """
        ascii_art_bottom = """
        .-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-.
        |                 CARD                  |
        `-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-'
        """

        for idx, reservation in enumerate(reservations):
            card = tk.Frame(self.scroll_frame, bd=2, relief=tk.SOLID, padx=10, pady=10)
            card.pack(fill=tk.X, pady=5, padx=10)

            if idx % 2 == 0:
                card.config(bg='pink')
            else:
                card.config(bg='lightblue')

            tk.Label(card, text=ascii_art_top, bg=card.cget("bg")).pack(anchor='w')
            tk.Label(card, text=f"ID: {reservation.id}", bg=card.cget("bg")).pack(anchor='w')
            tk.Label(card, text=f"Name: {reservation.name}", bg=card.cget("bg")).pack(anchor='w')
            tk.Label(card, text=f"Date: {reservation.date}", bg=card.cget("bg")).pack(anchor='w')
            tk.Label(card, text=f"Time: {reservation.time}", bg=card.cget("bg")).pack(anchor='w')
            tk.Label(card, text=f"Service: {reservation.service}", bg=card.cget("bg")).pack(anchor='w')
            tk.Label(card, text=ascii_art_bottom, bg=card.cget("bg")).pack(anchor='w')
            

if __name__ == "__main__":
    root = tk.Tk()
    system = SalonReservationSystem()
    app = ReservationApp(root, system)
    root.mainloop()
