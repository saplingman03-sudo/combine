import tkinter as tk
from tkinter import ttk
from 自動創建商戶測試 import SiteAApp  # 檔名依你實際的改

def main():
    root = tk.Tk()
    root.title("自動化工具")
    root.geometry("900x950")

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)

    tab_a = tk.Frame(nb)
    nb.add(tab_a, text="創建商戶")

    SiteAApp(tab_a)

    root.mainloop()

if __name__ == "__main__":
    main()
