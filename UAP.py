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

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.import_button = tk.Button(self.frame, text="Import CSV", command=self.import_csv)
        self.import_button.pack(side=tk.LEFT)

        self.add_button = tk.Button(self.frame, text="Add Reservation", command=self.add_reservation)
        self.add_button.pack(side=tk.LEFT)

        self.view_button = tk.Button(self.frame, text="View Reservations", command=self.view_reservations)
        self.view_button.pack(side=tk.LEFT)

        self.update_button = tk.Button(self.frame, text="Update Reservation", command=self.update_reservation)
        self.update_button.pack(side=tk.LEFT)

        self.delete_button = tk.Button(self.frame, text="Delete Reservation", command=self.delete_reservation)
        self.delete_button.pack(side=tk.LEFT)

        self.search_button = tk.Button(self.frame, text="Search Reservation", command=self.search_reservation)
        self.search_button.pack(side=tk.LEFT)

    def import_csv(self):
        filename = filedialog.askopenfilename()
        self.system.import_from_csv(filename)
        messagebox.showinfo("Success", "Reservations imported successfully")

    def add_reservation(self):
        id = simpledialog.askstring("Input", "Enter ID:")
        name = simpledialog.askstring("Input", "Enter Name:")
        date = simpledialog.askstring("Input", "Enter Date (YYYY-MM-DD):")
        time = simpledialog.askstring("Input", "Enter Time (HH:MM):")
        service = simpledialog.askstring("Input", "Enter Service:")

        reservation = Reservation(id, name, date, time, service)
        self.system.add_reservation(reservation)
        messagebox.showinfo("Success", "Reservation added successfully")

    def view_reservations(self):
        self.system.sort_reservations()
        reservations = self.system.view_reservations()
        result = "\n".join([f"{r.id}, {r.name}, {r.date}, {r.time}, {r.service}" for r in reservations])
        messagebox.showinfo("Reservations", result)

    def update_reservation(self):
        id = simpledialog.askstring("Input", "Enter ID of the reservation to update:")
        name = simpledialog.askstring("Input", "Enter new Name:")
        date = simpledialog.askstring("Input", "Enter new Date (YYYY-MM-DD):")
        time = simpledialog.askstring("Input", "Enter new Time (HH:MM):")
        service = simpledialog.askstring("Input", "Enter new Service:")

        new_reservation = Reservation(id, name, date, time, service)
        if self.system.update_reservation(id, new_reservation):
            messagebox.showinfo("Success", "Reservation updated successfully")
        else:
            messagebox.showwarning("Error", "Reservation not found")

    def delete_reservation(self):
        id = simpledialog.askstring("Input", "Enter ID of the reservation to delete:")
        if self.system.delete_reservation(id):
            messagebox.showinfo("Success", "Reservation deleted successfully")
        else:
            messagebox.showwarning("Error", "Reservation not found")

    def search_reservation(self):
        name = simpledialog.askstring("Input", "Enter Name to search:")
        result = self.system.search_reservation(name)
        if result:
            result_str = "\n".join([f"{r.id}, {r.name}, {r.date}, {r.time}, {r.service}" for r in result])
            messagebox.showinfo("Search Result", result_str)
        else:
            messagebox.showinfo("Search Result", "No reservations found")

if __name__ == "__main__":
    root = tk.Tk()
    system = SalonReservationSystem()
    app = ReservationApp(root, system)
    root.mainloop()
