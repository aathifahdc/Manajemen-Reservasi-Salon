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
                next(reader)  
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

        self.main_frame = tk.Frame(root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.front_page = tk.Frame(self.main_frame, bg='#FF69B4')
        self.front_page.pack(fill=tk.BOTH, expand=True)
        
        self.login_page = tk.Frame(self.main_frame, bg='#FF69B4')  
        
        self.reservation_page = tk.Frame(self.main_frame)

        
        self.salon_name_label = tk.Label(self.front_page, text="Dapper and Divine", font=("Arial", 24), bg='#FF69B4')
        self.salon_name_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.salon_subtitle_label = tk.Label(self.front_page, text="Let Your Beauty Shine Ahead", font=("Arial", 16), bg='#FF69B4')
        self.salon_subtitle_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.enter_button = tk.Button(self.front_page, text="Enter", command=self.show_login_page)
        self.enter_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.setup_login_page()
        self.setup_reservation_page()

    def setup_login_page(self):
        tk.Label(self.login_page, text="Admin Login", font=("Arial", 24), bg='#FF69B4').pack(pady=20) 
        tk.Label(self.login_page, text="Username", bg='#FF69B4').pack(pady=5)  
        self.username_entry = tk.Entry(self.login_page)
        self.username_entry.pack(pady=5)

        tk.Label(self.login_page, text="Password", bg='#FF69B4').pack(pady=5) 
        self.password_entry = tk.Entry(self.login_page, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.login_page, text="Login", command=self.check_login)
        self.login_button.pack(pady=20)

    def show_login_page(self):
        self.front_page.pack_forget()
        self.login_page.pack(fill=tk.BOTH, expand=True)

    def show_reservation_page(self):
        self.login_page.pack_forget()
        self.reservation_page.pack(fill=tk.BOTH, expand=True)

    def setup_login_page(self):
        tk.Label(self.login_page, text="Admin Login", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.login_page, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self.login_page)
        self.username_entry.pack(pady=5)

        tk.Label(self.login_page, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self.login_page, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.login_page, text="Login", command=self.check_login)
        self.login_button.pack(pady=20)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "BeauMin" and password == "beauty":  
            messagebox.showinfo("Success", "Login successful")
            self.show_reservation_page()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def setup_reservation_page(self):
        left_frame = tk.Frame(self.reservation_page)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        right_frame = tk.Frame(self.reservation_page)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        
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
            messagebox.showwarning("Error", "All fields must be filled out")

    def view_reservations(self):
        self.update_listbox()

    def update_listbox(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        reservations = self.system.view_reservations()
        for reservation in reservations:
            tk.Label(self.scroll_frame, text=f"ID: {reservation.id}, Name: {reservation.name}, Date: {reservation.date}, Time: {reservation.time}, Service: {reservation.service}").pack()

    def delete_reservation(self):
        reservation_id = simpledialog.askstring("Cancel Reservation", "Enter reservation ID to cancel:")
        if reservation_id:
            if self.system.delete_reservation(reservation_id):
                self.update_listbox()
                messagebox.showinfo("Success", "Reservation cancelled successfully")
            else:
                messagebox.showwarning("Error", "Reservation ID not found")

    def update_reservation_window(self):
        reservation_id = simpledialog.askstring("Update Reservation", "Enter reservation ID to update:")
        if reservation_id:
            result = self.system.search_reservation(reservation_id)
            if result:
                self.update_reservation_window = tk.Toplevel(self.root)
                self.update_reservation_window.title("Update Reservation")

                tk.Label(self.update_reservation_window, text="Name").pack(pady=5)
                self.update_name_entry = tk.Entry(self.update_reservation_window)
                self.update_name_entry.pack(pady=5)
                self.update_name_entry.insert(0, result[0].name)

                tk.Label(self.update_reservation_window, text="Date").pack(pady=5)
                self.update_date_entry = tk.Entry(self.update_reservation_window)
                self.update_date_entry.pack(pady=5)
                self.update_date_entry.insert(0, result[0].date)

                tk.Label(self.update_reservation_window, text="Time").pack(pady=5)
                self.update_time_entry = tk.Entry(self.update_reservation_window)
                self.update_time_entry.pack(pady=5)
                self.update_time_entry.insert(0, result[0].time)

                tk.Label(self.update_reservation_window, text="Service").pack(pady=5)
                self.update_service_entry = tk.Entry(self.update_reservation_window)
                self.update_service_entry.pack(pady=5)
                self.update_service_entry.insert(0, result[0].service)

                tk.Button(self.update_reservation_window, text="Update", command=lambda: self.update_reservation(reservation_id)).pack(pady=20)
            else:
                messagebox.showwarning("Error", "Reservation ID not found")

    def update_reservation(self, reservation_id):
        updated_name = self.update_name_entry.get()
        updated_date = self.update_date_entry.get()
        updated_time = self.update_time_entry.get()
        updated_service = self.update_service_entry.get()

        updated_reservation = Reservation(reservation_id, updated_name, updated_date, updated_time, updated_service)
        if self.system.update_reservation(reservation_id, updated_reservation):
            self.update_reservation_window.destroy()
            self.update_listbox()
            messagebox.showinfo("Success", "Reservation updated successfully")
        else:
            messagebox.showwarning("Error", "Reservation ID not found")

    def search_reservation(self):
        name = simpledialog.askstring("Search Reservation", "Enter name to search:")
        if name:
            results = self.system.search_reservation(name)
            if results:
                self.update_listbox()
                for result in results:
                    tk.Label(self.scroll_frame, text=f"ID: {result.id}, Name: {result.name}, Date: {result.date}, Time: {result.time}, Service: {result.service}").pack()
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
            color = random.choice(colors)

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

            card = tk.Frame(self.scroll_frame, bd=2, relief=tk.SOLID, bg=color)
            card.pack(fill=tk.X, pady=5, padx=10)

            tk.Label(card, text=ascii_art_top, bg=color).pack(anchor='w')

            tk.Label(card, text=f"Name: {reservation.name}", bg=color).pack(anchor='w')
            tk.Label(card, text=f"Date: {reservation.date}", bg=color).pack(anchor='w')
            tk.Label(card, text=f"Time: {reservation.time}", bg=color).pack(anchor='w')
            tk.Label(card, text=f"Service: {reservation.service}", bg=color).pack(anchor='w')
            tk.Label(card, text=f"ID: {reservation.id}", bg=color).pack(anchor='w')
            
            tk.Label(card, text=ascii_art_bottom, bg=color).pack(anchor='w')

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
