import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent

# 你的舊工具檔名（照你目前專案看起來就是這三個）
TOOLS = [
    ("對帳工具", "自動對帳工具.py"),
    ("自動創建商戶", "自動創建商戶.py"),
    ("自動開關遊戲", "自動開關遊戲.py"),
]

def launch_py_file(py_filename: str):
    """用新的 Python 行程開啟舊工具（最穩）"""
    target = BASE_DIR / py_filename
    if not target.exists():
        messagebox.showerror("找不到檔案", f"找不到：{target}")
        return

    try:
        # 用同一個 Python 執行器（避免環境不同）
        subprocess.Popen([sys.executable, str(target)], cwd=str(BASE_DIR))
    except Exception as e:
        messagebox.showerror("啟動失敗", str(e))

def main():
    root = tk.Tk()
    root.title("COMBINE 控制台（啟動器）")
    root.geometry("520x320")

    frm = ttk.Frame(root, padding=16)
    frm.pack(fill="both", expand=True)

    title = ttk.Label(frm, text="請選擇要開啟的工具", font=("Microsoft JhengHei", 16))
    title.pack(pady=(0, 18))

    for label, filename in TOOLS:
        btn = ttk.Button(frm, text=label, command=lambda f=filename: launch_py_file(f))
        btn.pack(fill="x", pady=8, ipady=8)

    hint = ttk.Label(frm, text="點了會跳出對應的舊工具視窗（各自獨立執行）", foreground="gray")
    hint.pack(pady=(18, 0))

    root.mainloop()

if __name__ == "__main__":
    main()
