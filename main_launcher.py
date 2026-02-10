import os
import sys
import tkinter as tk
from tkinter import ttk

from 自動創建商戶測試 import SiteAApp
from 自動開關遊戲測試 import SiteBApp
from 限紅 import SiteCApp

import json
from pathlib import Path
UI_STATE_PATH = Path("ui_state.json")

def load_ui_state():
    if UI_STATE_PATH.exists():
        try:
            return json.loads(UI_STATE_PATH.read_text(encoding="utf-8"))
        except:
            return {}
    return {}

def save_ui_state(state: dict):
    UI_STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def restart_program():
    """重啟目前程式，吃到最新 .py"""
    python = sys.executable
    os.execl(python, python, *sys.argv)


def main():
    root = tk.Tk()
    root.title("自動化工具")
    root.geometry("1000x700")

    # 頂部工具列（放刷新按鈕）
    topbar = ttk.Frame(root)
    topbar.pack(fill="x")

    btn_reload = ttk.Button(topbar, text="🔄 刷新（重啟程式）", command=restart_program)
    btn_reload.pack(side="left", padx=8, pady=6)

    # 你也可以加快捷鍵：Ctrl+R
    root.bind("<Control-r>", lambda e: restart_program())
    root.bind("<Control-R>", lambda e: restart_program())

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)

    tabA = ttk.Frame(nb)
    tabB = ttk.Frame(nb)
    tabC = ttk.Frame(nb)

    nb.add(tabA, text="創建商戶")
    nb.add(tabB, text="開關遊戲")
    nb.add(tabC, text="限紅設定")

    SiteAApp(tabA)
    SiteBApp(tabB)
    siteC = SiteCApp(tabC)

    #回到原頁面
    # -------- 記住/回復：主 Tab + SiteC 內層 Tab + 平台 --------
    state = load_ui_state()

    def save_all_state(event=None):
        s = load_ui_state()
        # 外層 Notebook 的 tab
        s["active_tab"] = nb.index(nb.select())

        # SiteC 內層狀態
        try:
            s["siteC"] = {
                "platform": siteC.platform_var.get(),                  # wp / ldb
                "inner_tab": siteC.nb.index(siteC.nb.select())         # SiteC 內層 Notebook index
            }
        except Exception:
            pass

        save_ui_state(s)

    # 外層 tab 切換就存
    nb.bind("<<NotebookTabChanged>>", save_all_state)

    # SiteC 內層 tab 切換也存
    siteC.nb.bind("<<NotebookTabChanged>>", save_all_state)

    # SiteC 平台切換也存（wp/ldb）
    siteC.platform_var.trace_add("write", lambda *args: save_all_state())

    # ---- 啟動時回復 ----
    # 1) 回外層 tab
    last = state.get("active_tab", 0)
    try:
        nb.select(last)
    except:
        pass

    # 2) 回 SiteC 平台 + 內層 tab
    sc = state.get("siteC", {})
    try:
        if "platform" in sc:
            siteC.platform_var.set(sc["platform"])
            siteC._on_platform_switch()  # 讓帳密跟著平台刷新
        if "inner_tab" in sc:
            siteC.nb.select(sc["inner_tab"])
    except:
        pass

    # 存一次（避免第一次沒資料）
    save_all_state()

    root.mainloop()



if __name__ == "__main__":
    main()
