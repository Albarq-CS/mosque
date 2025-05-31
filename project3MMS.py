import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import folium
import webbrowser
import difflib
import os

# Database Class
class MosqueDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("Mosques.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Mosques (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Name TEXT,
                                Type TEXT,
                                Address TEXT,
                                Coordinates TEXT,
                                Imam_Name TEXT)''')
        self.conn.commit()

    def display(self):
        self.cursor.execute("SELECT * FROM Mosques")
        return self.cursor.fetchall()

    def search(self, name):
        self.cursor.execute("SELECT * FROM Mosques WHERE Name = ?", (name,))
        return self.cursor.fetchone()

    def insert(self, ID, name, type_, address, coordinates, imam_name):
        self.cursor.execute("INSERT INTO Mosques (ID, Name, Type, Address, Coordinates, Imam_Name) VALUES (?, ?, ?, ?, ?, ?)",
                            (ID, name, type_, address, coordinates, imam_name))
        self.conn.commit()

    def update(self, ID, imam_name):
        self.cursor.execute("UPDATE Mosques SET Imam_Name = ? WHERE ID = ?", (imam_name, ID))
        self.conn.commit()

    def delete(self, ID):
        self.cursor.execute("DELETE FROM Mosques WHERE ID = ?", (ID,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

# GUI Class
class MosquesManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Mosque Management System")
        self.db = MosqueDatabase()

        # Configure main window grid
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Combined frame for Part 1 and Part 3
        main_frame = tk.Frame(self.root)
        main_frame.grid(row=0, column=0, padx=10, pady=0, sticky="nsew")

        # Part 1: Input Fields (Inside main_frame)
        input_frame = tk.LabelFrame(main_frame, text="Part 1: Input Fields", borderwidth=0, highlightthickness=0)
        input_frame.grid(row=0, column=0, pady=0, sticky="nw")

        # Column 1: ID, Type, Coordinates
        tk.Label(input_frame, text="ID").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.id_entry = tk.Entry(input_frame)
        self.id_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Type").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.type_menu = ttk.Combobox(input_frame, values=["Islamic Center", "mosques", "masjid"])
        self.type_menu.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Coordinates").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.coordinates_entry = tk.Entry(input_frame)
        self.coordinates_entry.grid(row=2, column=1, padx=5, pady=2)

        # Column 2: Name, Address, Imam Name
        tk.Label(input_frame, text="Name").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(input_frame, text="Address").grid(row=1, column=2, padx=5, pady=2, sticky="w")
        self.address_entry = tk.Entry(input_frame)
        self.address_entry.grid(row=1, column=3, padx=5, pady=2)

        tk.Label(input_frame, text="Imam Name").grid(row=2, column=2, padx=5, pady=2, sticky="w")
        self.imam_entry = tk.Entry(input_frame)
        self.imam_entry.grid(row=2, column=3, padx=5, pady=2)

        # Part 3: Operations Buttons (Inside main_frame, directly below Part 1)
        ops_frame = tk.LabelFrame(main_frame, text="Part 3: Operations", borderwidth=0, highlightthickness=0)
        ops_frame.grid(row=1, column=0, pady=(0, 0), sticky="ew")

        # Row 0: Display All, Search by Name, Update Entry
        tk.Button(ops_frame, text="Display All", command=self.display_all).grid(row=0, column=0, padx=5, pady=2, sticky="ew")
        tk.Button(ops_frame, text="Search By Name", command=self.search_by_name).grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        tk.Button(ops_frame, text="Update Entry", command=self.update_entry).grid(row=0, column=2, padx=5, pady=2, sticky="ew")

        # Row 1: Add Entry, Delete Entry, Display on Map
        tk.Button(ops_frame, text="Add Entry", command=self.add_entry).grid(row=1, column=0, padx=5, pady=2, sticky="ew")
        tk.Button(ops_frame, text="Delete Entry", command=self.delete_entry).grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        tk.Button(ops_frame, text="Display on Map", command=self.display_on_map).grid(row=1, column=2, padx=5, pady=2, sticky="ew")

        # Configure ops_frame columns to expand evenly
        ops_frame.columnconfigure(0, weight=1)
        ops_frame.columnconfigure(1, weight=1)
        ops_frame.columnconfigure(2, weight=1)

        # Part 2: Records Listbox (Right, Spanning All Rows)
        part2_frame = tk.LabelFrame(self.root, text="Part 2: Records")
        part2_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=0, sticky="nsew")

        v_scrollbar = tk.Scrollbar(part2_frame, orient=tk.VERTICAL)
        h_scrollbar = tk.Scrollbar(part2_frame, orient=tk.HORIZONTAL)

        self.records_listbox = tk.Listbox(part2_frame, width=70, height=20,
                                          yscrollcommand=v_scrollbar.set,
                                          xscrollcommand=h_scrollbar.set)

        v_scrollbar.config(command=self.records_listbox.yview)
        h_scrollbar.config(command=self.records_listbox.xview)

        self.records_listbox.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        part2_frame.grid_rowconfigure(0, weight=1)
        part2_frame.grid_columnconfigure(0, weight=1)

    def display_all(self):
        self.records_listbox.delete(0, tk.END)
        records = self.db.display()
        for record in records:
            self.records_listbox.insert(tk.END, f"ID: {record[0]}, Name: {record[1]}, Type: {record[2]}, Address: {record[3]}, Coordinates: {record[4]}, Imam: {record[5]}")

    def search_by_name(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter a name to search.")
            return

        records = self.db.display()
        names = [record[1] for record in records]
        close_matches = difflib.get_close_matches(name, names, n=3, cutoff=0.6)

        if close_matches:
            if len(close_matches) > 1:
                self.show_close_matches(close_matches)
            else:
                record = self.db.search(close_matches[0])
                self.records_listbox.delete(0, tk.END)
                self.records_listbox.insert(tk.END, f"ID: {record[0]}, Name: {record[1]}, Type: {record[2]}, Address: {record[3]}, Coordinates: {record[4]}, Imam: {record[5]}")
        else:
            messagebox.showinfo("Not Found", "No matching mosque found.")

    def show_close_matches(self, matches):
        match_window = tk.Toplevel(self.root)
        match_window.title("Select a Match")
        tk.Label(match_window, text="Select the correct mosque name:").pack(pady=5)

        selected_name = tk.StringVar()
        for match in matches:
            tk.Radiobutton(match_window, text=match, variable=selected_name, value=match).pack(anchor="w")

        def on_select():
            selected = selected_name.get()
            if selected:
                record = self.db.search(selected)
                self.records_listbox.delete(0, tk.END)
                self.records_listbox.insert(tk.END, f"ID: {record[0]}, Name: {record[1]}, Type: {record[2]}, Address: {record[3]}, Coordinates: {record[4]}, Imam: {record[5]}")
            match_window.destroy()

        tk.Button(match_window, text="Select", command=on_select).pack(pady=5)

    def add_entry(self):
        try:
            ID = self.id_entry.get() if self.id_entry.get() else None
            name = self.name_entry.get()
            type_ = self.type_menu.get()
            address = self.address_entry.get()
            coordinates = self.coordinates_entry.get()
            imam_name = self.imam_entry.get()

            if not name or not type_:
                messagebox.showerror("Error", "Name and Type are required.")
                return

            self.db.insert(ID, name, type_, address, coordinates, imam_name)
            messagebox.showinfo("Success", "Record added successfully.")
            self.clear_entries()
            self.display_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_entry(self):
        try:
            ID = self.id_entry.get()
            imam_name = self.imam_entry.get()

            if not ID or not imam_name:
                messagebox.showerror("Error", "ID and Imam Name are required.")
                return

            self.db.update(ID, imam_name)
            messagebox.showinfo("Success", "Record updated successfully.")
            self.display_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_entry(self):
        try:
            ID = self.id_entry.get()
            if not ID:
                messagebox.showerror("Error", "Please enter an ID to delete.")
                return

            self.db.delete(ID)
            messagebox.showinfo("Success", "Record deleted successfully.")
            self.clear_entries()
            self.display_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_on_map(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Enter the mosque name first.")
            return

        record = self.db.search(name)
        if not record:
            messagebox.showerror("Error", "Mosque not found.")
            return

        coordinates = record[4]
        if not coordinates:
            messagebox.showerror("Error", "No coordinates available for the mosque.")
            return

        try:
            lat, lon = map(float, coordinates.split(","))
            m = folium.Map(location=[lat, lon], zoom_start=15)
            folium.Marker([lat, lon], popup=record[1]).add_to(m)

            map_file = "mosque_map.html"
            m.save(map_file)
            full_path = os.path.abspath(map_file)
            webbrowser.open(f"file://{full_path}")
            messagebox.showinfo("Success", "Mosque displayed on map.")
        except ValueError:
            messagebox.showerror("Error", "Invalid coordinates format. Use: latitude,longitude")
        except Exception as e:
            messagebox.showerror("Error", f"Error displaying map: {str(e)}")

    def clear_entries(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.type_menu.set("")
        self.address_entry.delete(0, tk.END)
        self.coordinates_entry.delete(0, tk.END)
        self.imam_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = MosquesManagementSystem(root)
    root.mainloop()