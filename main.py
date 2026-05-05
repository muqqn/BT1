import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.filename = "weather_data.json"
        self.data = self.load_data()

        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack()

        tk.Label(frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0)
        self.ent_date = tk.Entry(frame)
        self.ent_date.grid(row=0, column=1)

        tk.Label(frame, text="Температура (°C):").grid(row=1, column=0)
        self.ent_temp = tk.Entry(frame)
        self.ent_temp.grid(row=1, column=1)

        tk.Label(frame, text="Описание:").grid(row=2, column=0)
        self.ent_desc = tk.Entry(frame)
        self.ent_desc.grid(row=2, column=1)

        self.var_precip = tk.BooleanVar()
        tk.Checkbutton(frame, text="Осадки", variable=self.var_precip).grid(row=3, column=1)

        tk.Button(frame, text="Добавить запись", command=self.add_entry).grid(row=4, columnspan=2, pady=5)

        f_frame = tk.LabelFrame(root, text="Фильтры", padx=10, pady=5)
        f_frame.pack(fill="x", padx=10)

        tk.Label(f_frame, text="Мин. темп:").grid(row=0, column=0)
        self.ent_f_temp = tk.Entry(f_frame, width=10)
        self.ent_f_temp.grid(row=0, column=1)

        tk.Label(f_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=2)
        self.ent_f_date = tk.Entry(f_frame, width=12)
        self.ent_f_date.grid(row=0, column=3)

        tk.Button(f_frame, text="Применить", command=self.apply_filter).grid(row=0, column=4, padx=5)
        tk.Button(f_frame, text="Сброс", command=self.show_all).grid(row=0, column=5)

        self.tree = ttk.Treeview(root, columns=("Date", "Temp", "Desc", "Precip"), show="headings")
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Temp", text="Темп.")
        self.tree.heading("Desc", text="Описание")
        self.tree.heading("Precip", text="Осадки")
        self.tree.pack(padx=10, pady=10)

        self.show_all()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    return json.load(f)
            except: return []
        return []

    def save_data(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

    def add_entry(self):
        try:
            date_str = self.ent_date.get()
            datetime.strptime(date_str, "%Y-%m-%d")
            temp = float(self.ent_temp.get())
            desc = self.ent_desc.get()
            if not desc: raise ValueError("Описание пустое")
            
            self.data.append({
                "date": date_str, "temp": temp, 
                "desc": desc, "precip": self.var_precip.get()
            })
            self.save_data()
            self.show_all()
            self.clear_inputs()
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректный ввод: {e}")
            def clear_inputs(self):
        self.ent_date.delete(0, tk.END)
        self.ent_temp.delete(0, tk.END)
        self.ent_desc.delete(0, tk.END)
        self.var_precip.set(False)

    def show_all(self):
        self.tree.delete(*self.tree.get_children())
        for item in self.data:
            self.tree.insert("", "end", values=(item["date"], item["temp"], item["desc"], "Да" if item["precip"] else "Нет"))

    def apply_filter(self):
        self.tree.delete(*self.tree.get_children())
        f_temp = self.ent_f_temp.get()
        f_date = self.ent_f_date.get()

        for item in self.data:
            match_temp = True
            match_date = True
            if f_temp and item["temp"] <= float(f_temp): match_temp = False
            if f_date and item["date"] != f_date: match_date = False
            if match_temp and match_date:
                self.tree.insert("", "end", values=(item["date"], item["temp"], item["desc"], "Да" if item["precip"] else "Нет"))

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
