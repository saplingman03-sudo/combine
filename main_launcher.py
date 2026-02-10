import tkinter as tk
from tkinter import ttk
from 自動創建商戶測試 import SiteAApp  
from 自動開關遊戲測試 import SiteBApp
from 限紅 import SiteCApp 



def main():
    root = tk.Tk()
    root.title("自動化工具")

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)
    root.geometry("1000x700")  # ✅ 加大視窗


    tabA = ttk.Frame(nb)
    tabB = ttk.Frame(nb)
    tabC = ttk.Frame(nb)  

    nb.add(tabA, text="創建商戶")
    nb.add(tabB, text="開關遊戲")
    nb.add(tabC, text="限紅設定")  

    SiteAApp(tabA)
    SiteBApp(tabB)
    SiteCApp(tabC)  

    root.mainloop()

if __name__ == "__main__":
    main()
