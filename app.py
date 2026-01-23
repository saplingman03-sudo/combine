import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os, sys

def base_dir():
    # 永遠回到「啟動器所在資料夾」
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)   # app.exe 所在資料夾
    return os.path.dirname(os.path.abspath(__file__))

TOOLS = [
    ("自動對帳工具", "對帳工具"),
    ("自動創建商戶", "創建商戶"),
    ("自動開關遊戲", "開關遊戲"),
]

def open_tool(name_no_ext: str):
    folder = base_dir()

    exe_path = os.path.join(folder, f"{name_no_ext}.exe")
    py_path  = os.path.join(folder, f"{name_no_ext}.py")

    # ① 先 try exe
    if os.path.exists(exe_path):
        try:
            subprocess.Popen([exe_path], cwd=folder)
            return
        except Exception as e:
            messagebox.showerror("啟動 exe 失敗", str(e))
            return

    # ② 再 try py
    if os.path.exists(py_path):
        try:
            # 優先用同資料夾的 venv python
            venv_py = os.path.join(folder, ".venv", "Scripts", "python.exe")
            python_bin = venv_py if os.path.exists(venv_py) else sys.executable
            subprocess.Popen([python_bin, py_path], cwd=folder)
            return
        except Exception as e:
            messagebox.showerror("啟動 py 失敗", str(e))
            return

    # ③ 都沒有
    messagebox.showerror(
        "找不到工具",
        f"同資料夾找不到：\n{name_no_ext}.exe\n或\n{name_no_ext}.py"
    )

def main():
    root = tk.Tk()
    root.title("COMBINE 控制台（啟動器）")
    root.geometry("520x320")

    frm = ttk.Frame(root, padding=16)
    frm.pack(fill="both", expand=True)

    ttk.Label(frm, text="請選擇要開啟的工具", font=("Microsoft JhengHei", 16)).pack(pady=(0, 18))

    for label, name in TOOLS:
        ttk.Button(
            frm,
            text=label,
            command=lambda n=name: open_tool(n)
        ).pack(fill="x", pady=8, ipady=8)

    ttk.Label(
        frm,
        text="會優先啟動 exe，沒有才使用 py",
        foreground="gray"
    ).pack(pady=(18, 0))

    root.mainloop()

if __name__ == "__main__":
    main()
