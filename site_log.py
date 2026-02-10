import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

class SiteBLog:
    def __init__(self, parent, bus):
        self.bus = bus

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        box = ttk.LabelFrame(self.frame, text="🧾 系統日誌", padding=10)
        box.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_area = ScrolledText(box, width=100, height=30)
        self.log_area.pack(fill="both", expand=True)

        # 讓 bus 連到這個視窗
        self.bus.attach(self)

    def append(self, msg: str):
        self.log_area.insert(tk.END, msg + "\n")
        self.log_area.see(tk.END)
