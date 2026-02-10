import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk, simpledialog
import requests
import json
import os
import threading
import math
from concurrent.futures import ThreadPoolExecutor, as_completed

# 檔案路徑
CACHE_FILE = "config_cache.json"
TEMPLATE_FILE = "templates.json"
MERCHANT_TEMPLATE_FILE = "merchant_templates.json"   # 商戶群組模板
MERCHANT_ALIAS_FILE = "merchant_aliases.json"       # 商戶帳號→名稱對照表

class SiteBApp:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        self.root = parent

        self.BASE_URLS = {
            "王牌": "https://wpapi.ldjzmr.top/admin",
            "樂多寶": "https://ldbapi.ledb.top/admin",
        }

        # 目前選擇的平台
        self.platform_var = tk.StringVar(value="王牌")
        self.base_url = self.BASE_URLS[self.platform_var.get()]
                # 平台 -> 檔案對照（依平台隔離）
        self.PLATFORM_FILES = {
            "王牌": {
                "cache": "config_cache_wp.json",
                "aliases": "merchant_aliases_wp.json",
            },
            "樂多寶": {
                "cache": "config_cache_ldb.json",
                "aliases": "merchant_aliases_ldb.json",
            }
        }
        self.current_platform = "All"

        # 動態檔案路徑（會跟平台切換）
        self.cache_file = None
        self.alias_file = None
        self._apply_platform_files()  # 初始化套用檔案路徑

        # 用平台對應的檔案載入資料
        self.config = self.load_json(self.cache_file, {})
        self.merchants = self.config.get("merchants", [])
        self.merchant_aliases = self.load_json(self.alias_file, {})

        # 其他固定檔案（你要不要也分平台都可以，先不動）
        self.templates = self.load_json(TEMPLATE_FILE, {})
        self.merchant_templates = self.load_json(MERCHANT_TEMPLATE_FILE, {})


        # 狀態變數
        self.token = None
        self.game_data_map = {}
        self.all_games_data = []

        # 商戶名稱（別名）與商戶群組模板
        self.merchant_aliases = self.load_json(MERCHANT_ALIAS_FILE, {})
        self.merchant_templates = self.load_json(MERCHANT_TEMPLATE_FILE, {})

        self.im_checked = "☑"
        self.im_unchecked = "☐"
        self.selected_codes = set()  # 全域記住勾選的 code

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)
        self.tab1 = tk.Frame(self.notebook)
        self.tab2 = tk.Frame(self.notebook)

        self.notebook.add(self.tab1, text=" ⚙️ 拖曳操作面板 ")
        self.notebook.add(self.tab2, text=" 🧾 日誌 ")  # ✅ 加入這一行


        self.setup_tab1()
        self.setup_tab2()  # 記得實作這個方法來建立日誌面板
    def _apply_platform_files(self):
        p = self.platform_var.get()
        files = self.PLATFORM_FILES.get(p, {})
        self.cache_file = files.get("cache", "config_cache.json")
        self.alias_file = files.get("aliases", "merchant_aliases.json")

    def setup_tab1(self):
        # === 平台選擇 ===
        platform_frame = tk.LabelFrame(self.tab1, text="🛰 平台選擇")
        platform_frame.pack(fill="x", padx=10, pady=5)

        def on_platform_switch():
            # 1) 換 base_url
            self.base_url = self.BASE_URLS[self.platform_var.get()]

            # 2) 換檔案路徑
            self._apply_platform_files()

            # 3) 重新載入平台專用資料
            self.config = self.load_json(self.cache_file, {})
            self.merchants = self.config.get("merchants", [])
            self.merchant_aliases = self.load_json(self.alias_file, {})

            # 4) 套到 UI（帳密、清單）
            self.ent_user.delete(0, tk.END)
            self.ent_user.insert(0, self.config.get("user", ""))
            self.ent_pw.delete(0, tk.END)
            self.ent_pw.insert(0, self.config.get("pw", ""))

            self.refresh_merchant_listbox()
            self.filter_merchants()  # 有搜尋框時更穩

            # 5) 清掉遊戲/Token狀態，避免混用
            self.token = None
            self.all_games_data = []
            self.game_data_map = {}
            self.selected_codes = set()
            self.ent_ids.delete(0, tk.END)

            if hasattr(self, "tree"):
                self.tree.delete(*self.tree.get_children())

            self.log(f"🔁 已切換平台：{self.platform_var.get()} | URL={self.base_url}")
            self.log(f"📦 cache={self.cache_file} | aliases={self.alias_file}")
        tk.Radiobutton(
            platform_frame, text="王牌",
            variable=self.platform_var, value="王牌",
            command=on_platform_switch
        ).pack(side="left", padx=10, pady=2)

        tk.Radiobutton(
            platform_frame, text="樂多寶",
            variable=self.platform_var, value="樂多寶",
            command=on_platform_switch
        ).pack(side="left", padx=10, pady=2)




        # 2. 商戶登入區
        top_frame = tk.LabelFrame(self.tab1, text="👤 商戶登入")
        top_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(top_frame, text="商戶帳號:").grid(row=0, column=0)
        self.ent_user = tk.Entry(top_frame, width=20)
        self.ent_user.insert(0, self.config.get("user", ""))
        self.ent_user.grid(row=0, column=1, padx=5)
        tk.Label(top_frame, text="密碼:").grid(row=0, column=2)
        self.ent_pw = tk.Entry(top_frame, width=20, show="*")
        self.ent_pw.insert(0, self.config.get("pw", ""))
        self.ent_pw.grid(row=0, column=3, padx=5)

        # 2.5 商戶清單（可複選）
        merchant_frame = tk.LabelFrame(self.tab1, text="🏪 商戶清單（可複選）")
        merchant_frame.pack(fill="x", padx=10, pady=5)

        search_m_frame = tk.Frame(merchant_frame)
        search_m_frame.pack(fill="x", padx=5)

        tk.Label(search_m_frame, text="🔍 搜尋商戶：").pack(side="left")
        self.ent_merchant_search = tk.Entry(search_m_frame)
        self.ent_merchant_search.pack(side="left", fill="x", expand=True, padx=5)
        self.ent_merchant_search.bind("<KeyRelease>", self.filter_merchants)

        self.lst_merchants = tk.Listbox(merchant_frame, selectmode="extended", height=5)
        self.lst_merchants.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        self.lst_merchants.bind("<Double-Button-1>", self.edit_merchant_double_click)
        self.lst_merchants.bind("<Button-3>", self.show_merchant_context_menu)  # 右鍵


        btns = tk.Frame(merchant_frame)
        btns.pack(side="left", padx=5)

        tk.Button(btns, text="➕ 加入", width=10, command=self.add_merchant).pack(pady=2)
        tk.Button(btns, text="🗑 刪除", width=10, command=self.remove_merchant).pack(pady=2)
        tk.Button(btns, text="✅ 全選", width=10, command=lambda: self.lst_merchants.select_set(0, tk.END)).pack(pady=2)
        tk.Button(btns, text="⬜ 清空", width=10, command=lambda: self.lst_merchants.select_clear(0, tk.END)).pack(pady=2)

        # 2.6 商戶群組模板 + 名稱設定
        m_tmpl_frame = tk.LabelFrame(self.tab1, text="🏷 商戶群組模板 / 名稱")
        m_tmpl_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(m_tmpl_frame, text="模板：").pack(side="left", padx=(8, 2))
        self.mtmpl_combo = ttk.Combobox(m_tmpl_frame, state="readonly")
        self.mtmpl_combo.pack(side="left", padx=5, pady=5)

        tk.Button(m_tmpl_frame, text="套用模板", command=self.apply_merchant_template).pack(side="left", padx=5)
        tk.Button(m_tmpl_frame, text="儲存目前選取", command=self.save_merchant_template).pack(side="left", padx=5)
        tk.Button(m_tmpl_frame, text="刪除模板", command=self.delete_merchant_template).pack(side="left", padx=5)
        tk.Button(m_tmpl_frame, text="✏️ 設定商戶名稱", command=self.set_merchant_alias).pack(side="left", padx=5)
       
        self.refresh_merchant_listbox()

        # 初始化商戶模板下拉選單
        if hasattr(self, "mtmpl_combo"):
            self.mtmpl_combo["values"] = list(self.merchant_templates.keys())

        # ✅ 關鍵修改：建立一個並排按鈕區
        sync_btn_frame = tk.Frame(self.tab1)
        sync_btn_frame.pack(fill="x", padx=10, pady=5)

        # 🔄 原本的登入同步按鈕 (改為放在左邊)
        tk.Button(
            sync_btn_frame, text="🔄 登入並同步總站",
            bg="#2196F3", fg="white", height=2, width=25,
            command=self.fetch_games
        ).pack(side="left", padx=5)

        # 🟢 搬上來的開啟按鈕
        tk.Button(
            sync_btn_frame, text="🟢 開啟所選遊戲",
            bg="green", fg="white", height=2, width=20,
            command=lambda: self.start_work(1)
        ).pack(side="left", padx=5)

        # 🔴 搬上來的關閉按鈕
        tk.Button(
            sync_btn_frame, text="🔴 關閉所選遊戲",
            bg="red", fg="white", height=2, width=20,
            command=lambda: self.start_work(-1)
        ).pack(side="left", padx=5)

        # 3. 搜尋與模板管理
        mid_frame = tk.Frame(self.tab1)
        mid_frame.pack(fill="x", padx=10)

        tk.Label(mid_frame, text="🔍 搜尋:").pack(side="left")
        self.ent_search = tk.Entry(mid_frame)
        self.ent_search.pack(side="left", fill="x", expand=True, padx=5)
        self.ent_search.bind("<KeyRelease>", self.filter_games)

        tk.Label(mid_frame, text="平台:").pack(side="left", padx=(10, 2))

        self.platform_combo = ttk.Combobox(
            mid_frame,
            state="readonly",
            width=12,
            values=["All"]  # 先給 All，之後動態補
        )
        self.platform_combo.current(0)
        self.platform_combo.pack(side="left")
        self.platform_combo.bind("<<ComboboxSelected>>", self.on_platform_change)


        tmpl_frame = tk.LabelFrame(self.tab1, text="💾 模板管理")
        tmpl_frame.pack(fill="x", padx=10, pady=5)
        self.tmpl_combo = ttk.Combobox(tmpl_frame, values=list(self.templates.keys()), state="readonly")
        self.tmpl_combo.pack(side="left", padx=5, pady=5)
        tk.Button(tmpl_frame, text="套用", command=self.apply_template).pack(side="left", padx=5)
        tk.Button(tmpl_frame, text="儲存當前勾選", command=self.save_new_template).pack(side="left", padx=5)
        tk.Button(tmpl_frame, text="✅ 全選", command=self.select_all).pack(side="left", padx=5)
        tk.Button(tmpl_frame, text="⬜ 全不選", command=self.clear_all).pack(side="left", padx=5)
        tk.Button(tmpl_frame, text="✅ 選基準商戶已開啟", command=self.select_enabled_in_baseline).pack(side="left", padx=5)
        tk.Button(tmpl_frame, text="🗑 刪除模板", command=self.delete_template).pack(side="left", padx=5)



        # 4. 核心：帶捲軸的 Treeview (拖曳版)
        list_frame = tk.Frame(self.tab1)
        list_frame.pack(padx=10, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        cols = ("check", "name", "id", "status")
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=20, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        self.tree.heading("check", text="選取")
        self.tree.heading("name", text="遊戲名稱 (平台_名稱)")
        self.tree.heading("id", text="ID")
        self.tree.heading("status", text="狀態")

        self.tree.column("check", width=50, anchor="center")
        self.tree.column("name", width=400)
        self.tree.column("id", width=100)
        self.tree.column("status", width=80, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.toggle_check)

        bottom_frame = tk.Frame(self.tab1)
        bottom_frame.pack(side="bottom", fill="x", pady=10)  # 確保在最下方

        # 這裡改為顯示遊戲 Code，因為 Code 才是跨商戶通用的基準
        self.ent_ids = tk.Entry(bottom_frame, width=70, fg="blue", font=("Arial", 10, "bold"))
        self.ent_ids.pack(pady=5)

        btn_box = tk.Frame(bottom_frame)
        btn_box.pack(pady=5)
        self.root.after(0, on_platform_switch)


    def filter_merchants(self, event=None):
        q = (self.ent_merchant_search.get() or "").strip().lower()

        self.lst_merchants.delete(0, tk.END)

        # 這個列表用來記住「目前 listbox 每一行對應到 self.merchants 的哪個 index」
        self.merchant_view_indexes = []

        for idx, m in enumerate(self.merchants):
            label = self.merchant_label(m)
            hay = f"{m.get('user','')} {self.merchant_aliases.get(m.get('user',''), '')} {label}".lower()

            if (not q) or (q in hay):
                self.lst_merchants.insert(tk.END, label)
                self.merchant_view_indexes.append(idx)


    def edit_merchant_double_click(self, event=None):
        sel = self.lst_merchants.curselection()
        if not sel:
            return

        idx = sel[0]
        old_user = self.merchants[idx].get("user", "")
        old_pw = self.merchants[idx].get("pw", "")

        new_user = simpledialog.askstring("編輯商戶", "商戶帳號：", initialvalue=old_user)
        if not new_user:
            return

        new_pw = simpledialog.askstring("編輯商戶", "密碼：", initialvalue=old_pw, show="*")
        if new_pw is None:
            return

        # 防止帳號重複（如果你改成另一個已存在的 user）
        for i, m in enumerate(self.merchants):
            if i != idx and m.get("user") == new_user:
                messagebox.showwarning("提醒", f"帳號 {new_user} 已存在於清單中")
                return

        self.merchants[idx] = {"user": new_user.strip(), "pw": new_pw.strip()}
        self.refresh_merchant_listbox()
        self.save_config()
        self.log(f"✏️ 已編輯商戶：{old_user} → {new_user}")

    def refresh_merchant_listbox(self):
        """刷新商戶清單顯示"""
        if not hasattr(self, "lst_merchants"):
            return
        self.lst_merchants.delete(0, tk.END)

        # ------------------------------------------------------------
        # [LOOP L1] 商戶清單渲染迴圈
        # 目的：把 self.merchants 內的商戶帳號渲染到 Listbox
        # 迭代單位：每筆商戶 dict（至少含 user/pw）
        # 依賴：self.merchants（來源為 config_cache.json 或使用者新增）
        # 產出：Listbox 的 UI 顯示內容
        # ------------------------------------------------------------
        for m in self.merchants:
            self.lst_merchants.insert(tk.END, self.merchant_label(m))

        # 同步模板下拉（避免新增/刪除模板後 UI 沒更新）
        if hasattr(self, "mtmpl_combo"):
            self.mtmpl_combo["values"] = list(self.merchant_templates.keys())

    def merchant_label(self, m: dict) -> str:
        """Listbox 顯示文字：優先顯示名稱，其次顯示帳號。

        例：台中逢甲店 (168168)
        """
        user = (m.get("user") or "").strip()
        # name 來源：若 API 未提供，就用本機 aliases
        name = (m.get("name") or "").strip()
        if not name:
            name = (self.merchant_aliases.get(user) or "").strip()

        return f"{name} ({user})" if (name and user) else (user or name or "")

    def save_config(self):
        self.config["user"] = self.ent_user.get()
        self.config["pw"] = self.ent_pw.get()
        self.config["merchants"] = self.merchants
        self.save_json(self.cache_file, self.config)


    def add_merchant(self):
        """新增商戶到清單"""
        u = self.ent_user.get().strip()
        p = self.ent_pw.get().strip()
        if not u or not p:
            messagebox.showwarning("提醒", "請先輸入商戶帳號與密碼，再按加入")
            return

        # 防重複
        if any(x.get("user") == u for x in self.merchants):
            messagebox.showinfo("提醒", f"{u} 已在清單內")
            return

        self.merchants.append({"user": u, "pw": p})
        self.refresh_merchant_listbox()
        self.save_config()
        self.log(f"✅ 已加入商戶：{u}")

    def remove_merchant(self):
        """刪除選取的商戶"""
        sel = list(self.lst_merchants.curselection())
        if not sel:
            return

        # ------------------------------------------------------------
        # [LOOP L1] 反向刪除商戶迴圈
        # 目的：依照 Listbox 被選取的 index，從 self.merchants 移除對應商戶
        # 迭代單位：被選取的 index（反向跑避免 pop 後 index 位移）
        # 依賴：self.lst_merchants.curselection() 回傳的 index 集合
        # 產出：self.merchants 減少、log 新增、UI 刷新 + config 落盤
        # ------------------------------------------------------------
        for i in reversed(sel):
            u = self.merchants[i]["user"]
            self.merchants.pop(i)
            self.log(f"🗑 已刪除商戶：{u}")

        self.refresh_merchant_listbox()
        self.save_config()

    def get_selected_merchants(self):
        idxs = self.lst_merchants.curselection()
        # 沒過濾時 merchant_view_indexes 可能不存在，保底用原本 index
        if not hasattr(self, "merchant_view_indexes") or not self.merchant_view_indexes:
            return [self.merchants[i] for i in idxs]
        real_idxs = [self.merchant_view_indexes[i] for i in idxs]
        return [self.merchants[i] for i in real_idxs]

    def fetch_games(self):
        user, pw = self.ent_user.get(), self.ent_pw.get()
        self.config.update({"user": user, "pw": pw})
        self.save_json(self.cache_file, self.config)


        try:
            # 自動登入拿基準 Token
            res = requests.post(f"{self.base_url}/login", json={"username": user, "password": pw}, timeout=10).json()
            self.token = f"Bearer {res['data']['token']}"

            headers = {"Authorization": self.token}
            all_games = []
            p = 1
            self.log(f"📡 正在抓取基準商戶({user})清單...")
            session = requests.Session()
            session.headers.update(headers)

            # ============================================================
            # [LOOP L0] 基準商戶遊戲清單分頁抓取主迴圈
            # 目的：把 /platform_game API 的所有頁面資料抓齊，整合成 all_games
            # 迭代單位：分頁頁碼 p（pagesize 固定 100）
            # 輸入來源：Admin API /platform_game?pagenum=...&pagesize=...
            # 產出/副作用：all_games 會逐步累積，最後寫入 self.all_games_data
            # 終止條件：
            #   - 已抓到 total 筆數
            #   - 或當頁 data 為空（API 無更多資料）
            # ============================================================
            while True:
                r = session.get(f"{self.base_url}/platform_game?pagenum={p}&pagesize=200", timeout=15).json()
                data = r.get('data', {}).get('data', [])
                all_games.extend(data)
                if len(all_games) >= r.get('data', {}).get('total', 0) or not data:
                    break
                p += 1

            self.all_games_data = all_games
            platforms = set()
            for g in all_games:
                pg = g.get("platform_game") or {}
                p = pg.get("platform")
                if p:
                    platforms.add(p)

            platform_list = ["All"] + sorted(platforms)
            self.platform_combo["values"] = platform_list
            self.platform_combo.current(0)


            self.game_data_map = {}

            # ------------------------------------------------------------
            # [LOOP L1] 建立「Code → 遊戲完整資料」映射表
            # 目的：把基準商戶抓回來的 all_games，整理成可快速查詢的 dict
            # 迭代單位：每筆遊戲資料 g（包含 platform_game 的資訊）
            # 依賴：g['platform_game'] 內的 code（跨商戶通用識別）
            # 產出：self.game_data_map[str(code)] = g
            # 用途：給 sync_master_template 用 Master.code 去對 Admin.platform_game.code
            # ------------------------------------------------------------
            for g in all_games:
                pg = g.get('platform_game') or {}
                code = pg.get('code') if isinstance(pg, dict) else g.get('platform_game.code')

                if code:
                    self.game_data_map[str(code)] = g

            # 顯示全部資料
            self.refresh_tree(self.all_games_data)
            self.log(f"✨ 載入完成，共 {len(all_games)} 款遊戲。")

        except Exception as e:
            self.log(f"💥 錯誤: {e}")
    def on_platform_change(self, event=None):
        self.current_platform = self.platform_combo.get()
        self.filter_games()

    def refresh_tree(self, data_list):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for g in data_list:
            pg = g.get('platform_game') or {}
            g_name = pg.get('platform_name') or '未知'
            p_name = pg.get('platform') or '未知'
            display_name = f"{g_name}_{p_name}"

            g_code = (pg.get('code') or '未知')
            status_icon = "✅" if g.get('status') == 1 else "❌"

            check = self.im_checked if str(g_code).strip() in self.selected_codes else self.im_unchecked
            self.tree.insert("", "end", values=(check, display_name, g_code, status_icon))


    def filter_games(self, event=None):
        query = (self.ent_search.get() or "").lower()
        platform = self.current_platform

        filtered = []

        for g in self.all_games_data:
            pg = g.get("platform_game") or {}
            name = (pg.get("platform_name") or "").lower()
            p = pg.get("platform")

            if query and query not in name:
                continue

            if platform != "All" and p != platform:
                continue

            filtered.append(g)

        self.refresh_tree(filtered)


    def apply_template(self):
        name = self.tmpl_combo.get()
        if name not in self.templates:
            return

        ids_str = self.templates[name].strip()
        if not ids_str:
            return

        self.ent_ids.delete(0, tk.END)
        self.ent_ids.insert(0, ids_str)

        selected_ids = set([x.strip() for x in ids_str.split(",") if x.strip()])
        self.selected_codes = selected_ids
        self.sync_ids_from_selected()
        self.refresh_tree(self.all_games_data)

        for item in self.tree.get_children():
            vals = list(self.tree.item(item, "values"))
            vals[0] = self.im_checked if str(vals[2]) in selected_ids else self.im_unchecked
            self.tree.item(item, values=vals)

        self.log(f"✅ 模板 '{name}' 已套用（admin.id）。")

    def select_all(self):
        for item in self.tree.get_children():
            vals = list(self.tree.item(item, "values"))
            vals[0] = self.im_checked
            self.selected_codes.add(str(vals[2]).strip())
            self.tree.item(item, values=vals)
        self.sync_ids_from_selected()

    def clear_all(self):
        for item in self.tree.get_children():
            vals = list(self.tree.item(item, "values"))
            vals[0] = self.im_unchecked
            self.selected_codes.discard(str(vals[2]).strip())
            self.tree.item(item, values=vals)
        self.sync_ids_from_selected()

    def select_enabled_in_baseline(self):
        """只勾選基準商戶（目前載入的 all_games_data）狀態為開啟(status==1)的遊戲"""
        if not self.all_games_data:
            self.log("⚠️ 尚未載入遊戲清單，請先按『登入並同步總站』")
            return

        # 取出 status==1 的 code
        enabled_codes = set()
        for g in self.all_games_data:
            if g.get("status") == 1:
                pg = g.get("platform_game") or {}
                code = pg.get("code") if isinstance(pg, dict) else None
                if not code:
                    code = g.get("platform_game.code")
                if code:
                    enabled_codes.add(str(code).strip())

        self.selected_codes = enabled_codes
        self.sync_ids_from_selected()
        self.refresh_tree(self.all_games_data)
        self.log(f"✅ 已選取基準商戶『已開啟』遊戲：{len(enabled_codes)} 筆")


    def toggle_check(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            return

        vals = list(self.tree.item(item, "values"))
        code = str(vals[2]).strip()

        if vals[0] == self.im_unchecked:
            vals[0] = self.im_checked
            self.selected_codes.add(code)
        else:
            vals[0] = self.im_unchecked
            self.selected_codes.discard(code)

        self.tree.item(item, values=vals)
        self.sync_ids_from_selected()

    def sync_ids_from_selected(self):
        self.ent_ids.delete(0, tk.END)
        self.ent_ids.insert(0, ",".join(sorted(self.selected_codes)))

    def start_work(self, status):
        target_codes = [c.strip() for c in self.ent_ids.get().split(",") if c.strip()]
        if not target_codes:
            self.log("⚠️ 尚未選取任何遊戲，請先在列表中勾選或套用模板")
            return

        selected = self.get_selected_merchants()

        if selected:
            threading.Thread(target=self.run_multi_merchants, args=(selected, status), daemon=True).start()
        else:
            if not self.token:
                self.log("⚠️ 尚未選取商戶，也尚未登入。請先登入或在商戶清單複選。")
                return
            threading.Thread(target=self.run_single_merchant, args=(status,), daemon=True).start()

    def run_single_merchant(self, status):
        """單商戶批次更新"""
        target_codes = [c.strip() for c in self.ent_ids.get().split(",") if c.strip()]
        if not target_codes:
            self.log("⚠️ 沒有選取任何遊戲 Code")
            return

        if not self.token:
            self.log("⚠️ 請先按「登入」取得 Token")
            return

        code_to_real_info = {}
        for g in self.all_games_data:
            pg = g.get("platform_game") or {}
            code = pg.get("code")
            if code:
                code_to_real_info[str(code).strip()] = {
                    "id": g["id"],
                    "brand_id": g["brand_id"],
                    "game_id": g["game_id"]
                }

        headers = {"Authorization": self.token}

        success = 0
        missing = 0

        for code in target_codes:
            c = str(code).strip()
            if c not in code_to_real_info:
                missing += 1
                continue

            info = code_to_real_info[c]
            payload = {
                "id": int(info["id"]),
                "brand_id": info["brand_id"],
                "game_id": info["game_id"],
                "status": status
            }

            try:
                requests.put(
                    f"{self.base_url}/platform_game/{info['id']}",
                    json=payload,
                    headers=headers,
                    timeout=15
                )
                success += 1
            except Exception as e:
                self.log(f"❌ 更新失敗 code={c} | err={e}")

        self.log(f"✅ 單商戶更新完成：成功 {success}/{len(target_codes)} | 找不到 {missing} 筆（該商戶不存在此 code）")

    def batch_process_worker(self, brands, codes, status):
        for brand_acc in brands:
            self.log(f"--- 🚀 開始處理商戶：{brand_acc} ---")

            brand_game_map = {}
            try:
                pass
            except Exception as e:
                self.log(f"❌ 無法獲取商戶 {brand_acc} 的資料: {e}")
                continue

            success = 0
            fail = 0
            session = requests.Session()
            session.headers.update({"Authorization": self.token})

            def do_one(key):
                g = brand_game_map.get(key)
                if not g:
                    return (key, False, "找不到對應資料")

                real_id = g.get("id")
                payload = {
                    "id": int(real_id),
                    "brand_id": g.get("brand_id"),
                    "game_id": g.get("game_id"),
                    "status": status
                }
                try:
                    r = session.put(f"{self.base_url}/platform_game/{real_id}", json=payload, timeout=15)
                    return (key, r.status_code == 200, "" if r.status_code == 200 else r.text[:100])
                except Exception as e:
                    return (key, False, str(e))

            with ThreadPoolExecutor(max_workers=15) as ex:
                futures = [ex.submit(do_one, k) for k in codes]
                for fu in as_completed(futures):
                    _, ok, err = fu.result()
                    if ok:
                        success += 1
                    else:
                        fail += 1

            self.log(f"✅ 商戶 {brand_acc} 處理完畢: 成功 {success} 失敗 {fail}")

        self.log("🏁 所有選中商戶批次執行完畢")

    def load_json(self, path, default=None):
        """安全讀取 JSON。

        - 檔案不存在 / 內容壞掉：回傳 default（預設 {}）
        """
        if default is None:
            default = {}
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return default

    def save_json(self, path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def log(self, msg):
        self.log_area.insert(tk.END, msg + "\n")
        self.log_area.see(tk.END)

    def save_new_template(self):
        name = simpledialog.askstring("模板", "輸入模板名稱:")
        if name:
            self.templates[name] = self.ent_ids.get()
            self.save_json(TEMPLATE_FILE, self.templates)
            self.tmpl_combo['values'] = list(self.templates.keys())
    def delete_template(self):
        name = self.tmpl_combo.get()
        if not name:
            messagebox.showwarning("提醒", "請先選擇要刪除的模板")
            return

        if name not in self.templates:
            messagebox.showwarning("提醒", f"模板不存在：{name}")
            return

        ok = messagebox.askyesno("確認刪除", f"確定要刪除模板『{name}』嗎？\n(此操作不可復原)")
        if not ok:
            return

        # 刪除 + 存檔
        self.templates.pop(name, None)
        self.save_json(TEMPLATE_FILE, self.templates)

        # 更新下拉選單
        self.tmpl_combo["values"] = list(self.templates.keys())
        self.tmpl_combo.set("")

        self.log(f"🗑 已刪除遊戲模板：{name}")


    # =============================
    # 商戶群組模板 / 名稱（別名）
    # =============================
    def apply_merchant_template(self):
        """套用商戶群組模板：自動勾選一整組商戶"""
        name = self.mtmpl_combo.get() if hasattr(self, "mtmpl_combo") else ""
        if not name or name not in self.merchant_templates:
            return

        users = set(self.merchant_templates.get(name) or [])
        self.lst_merchants.select_clear(0, tk.END)

        for i, m in enumerate(self.merchants):
            if (m.get("user") or "").strip() in users:
                self.lst_merchants.select_set(i)

        self.log(f"📂 已套用商戶模板：{name}（{len(users)} 家）")

    def save_merchant_template(self):
        """把目前勾選的商戶存成一個群組模板"""
        name = simpledialog.askstring("商戶群組模板", "輸入模板名稱:")
        if not name:
            return

        idxs = self.lst_merchants.curselection()
        if not idxs:
            messagebox.showwarning("提醒", "請先在商戶清單勾選要存成模板的商戶")
            return

        users = [self.merchants[i].get("user") for i in idxs if self.merchants[i].get("user")]
        self.merchant_templates[name] = users
        self.save_json(MERCHANT_TEMPLATE_FILE, self.merchant_templates)

        if hasattr(self, "mtmpl_combo"):
            self.mtmpl_combo["values"] = list(self.merchant_templates.keys())
            self.mtmpl_combo.set(name)

        self.log(f"💾 已儲存商戶模板：{name}（{len(users)} 家）")

    def delete_merchant_template(self):
        """刪除商戶群組模板"""
        name = self.mtmpl_combo.get() if hasattr(self, "mtmpl_combo") else ""
        if not name:
            return
        if name not in self.merchant_templates:
            return

        if not messagebox.askyesno("確認", f"確定要刪除商戶模板『{name}』嗎？"):
            return

        self.merchant_templates.pop(name, None)
        self.save_json(MERCHANT_TEMPLATE_FILE, self.merchant_templates)
        if hasattr(self, "mtmpl_combo"):
            self.mtmpl_combo["values"] = list(self.merchant_templates.keys())
            self.mtmpl_combo.set("")

        self.log(f"🗑 已刪除商戶模板：{name}")

    def set_merchant_alias(self):
        """把商戶帳號映射成顯示名稱（只影響 UI 顯示，不影響 API 呼叫）"""
        idxs = self.lst_merchants.curselection()
        if not idxs:
            messagebox.showwarning("提醒", "請先選取一個商戶")
            return

        i = idxs[0]
        m = self.merchants[i]
        user = (m.get("user") or "").strip()
        if not user:
            return

        old = (self.merchant_aliases.get(user) or "").strip()
        alias = simpledialog.askstring("設定商戶名稱", f"輸入 {user} 的顯示名稱：", initialvalue=old)
        if alias is None:
            return

        alias = alias.strip()
        if alias:
            self.merchant_aliases[user] = alias
        else:
            # 空字串視為清除別名
            self.merchant_aliases.pop(user, None)

        self.save_json(self.alias_file, self.merchant_aliases)
        self.refresh_merchant_listbox()
        self.log(f"🏷 已更新商戶名稱：{user} → {alias or '(清除)'}")

    def show_merchant_context_menu(self, event):
        """商戶右鍵選單"""
        # 先選取點擊的項目
        index = self.lst_merchants.nearest(event.y)
        self.lst_merchants.selection_clear(0, tk.END)
        self.lst_merchants.selection_set(index)
        
        # 建立選單
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="📋 複製帳號", command=self.copy_merchant_user)
        menu.add_command(label="🔑 複製密碼", command=self.copy_merchant_pw)
        menu.add_command(label="📝 複製帳號+密碼", command=self.copy_merchant_both)
        menu.add_separator()
        menu.add_command(label="✏️ 編輯", command=self.edit_merchant_double_click)
        menu.add_command(label="🗑️ 刪除", command=self.remove_merchant)
        
        menu.post(event.x_root, event.y_root)

    def copy_merchant_user(self):
        """複製選取商戶的帳號"""
        sel = self.lst_merchants.curselection()
        if not sel:
            return
        
        if hasattr(self, "merchant_view_indexes") and self.merchant_view_indexes:
            idx = self.merchant_view_indexes[sel[0]]
        else:
            idx = sel[0]
        
        user = self.merchants[idx].get("user", "")
        self.root.clipboard_clear()
        self.root.clipboard_append(user)
        self.log(f"📋 已複製帳號：{user}")

    def copy_merchant_pw(self):
        """複製選取商戶的密碼"""
        sel = self.lst_merchants.curselection()
        if not sel:
            return
        
        if hasattr(self, "merchant_view_indexes") and self.merchant_view_indexes:
            idx = self.merchant_view_indexes[sel[0]]
        else:
            idx = sel[0]
        
        pw = self.merchants[idx].get("pw", "")
        self.root.clipboard_clear()
        self.root.clipboard_append(pw)
        self.log(f"📋 已複製密碼")

    def copy_merchant_both(self):
        """複製帳號和密碼（格式：帳號\t密碼）"""
        sel = self.lst_merchants.curselection()
        if not sel:
            return
        
        if hasattr(self, "merchant_view_indexes") and self.merchant_view_indexes:
            idx = self.merchant_view_indexes[sel[0]]
        else:
            idx = sel[0]
        
        m = self.merchants[idx]
        user = m.get("user", "")
        pw = m.get("pw", "")
        
        text = f"{user}\t{pw}"  # Tab 分隔，可直接貼到 Excel
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.log(f"📋 已複製：{user} (含密碼)")

    def run_multi_merchants(self, merchants, status):
        """多商戶核心：用 platform_game.code 做匹配；PUT 用各商戶各自的 platform_game.id"""
        target_codes = [c.strip() for c in self.ent_ids.get().split(",") if c.strip()]
        if not target_codes:
            self.log("⚠️ 沒有選取任何遊戲 Code")
            return

        target_codes_set = set(target_codes)
        self.log(f"🚀 多商戶批次開始：{len(merchants)} 個商戶 | Code {len(target_codes_set)} 筆")

        ok_merchants = 0

        for m in merchants:
            user, pw = m["user"], m["pw"]
            self.log(f"--- 🚀 開始處理商戶：{user} ---")
            try:
                # 1) login -> token
                res = requests.post(
                    f"{self.base_url}/login",
                    json={"username": user, "password": pw},
                    timeout=15
                ).json()
                token = f"Bearer {res['data']['token']}"
                headers = {"Authorization": token}

                # 2) 抓該商戶 platform_game 全清單（分頁）
                this_merchant_games = []
                p = 1
                while True:
                    r = requests.get(
                        f"{self.base_url}/platform_game?pagenum={p}&pagesize=200",
                        headers=headers,
                        timeout=15
                    ).json()
                    d = r.get("data", {}).get("data", [])
                    this_merchant_games.extend(d)
                    if len(this_merchant_games) >= r.get("data", {}).get("total", 0) or not d:
                        break
                    p += 1

                # 3) 建 code -> info（這裡的 id 是該商戶自己的 platform_game.id）
                code_to_info = {}
                for g in this_merchant_games:
                    pg = g.get("platform_game") or {}

                    code = pg.get("code")
                    if not code:
                        code = g.get("platform_game.code")

                    if code:
                        c = str(code).strip()
                        code_to_info[c] = {
                            "id": g["id"],
                            "brand_id": g["brand_id"],
                            "game_id": g["game_id"]
                        }

                # 4) 併發 PUT 更新
                session = requests.Session()
                session.headers.update(headers)

                def do_put(code):
                    if code not in code_to_info:
                        return (code, False, "missing")

                    info = code_to_info[code]
                    payload = {
                        "id": int(info["id"]),
                        "brand_id": info["brand_id"],
                        "game_id": info["game_id"],
                        "status": status
                    }

                    try:
                        r = session.put(
                            f"{self.base_url}/platform_game/{info['id']}",
                            json=payload,
                            timeout=15
                        )
                        return (code, r.status_code == 200, "" if r.status_code == 200 else r.text[:80])
                    except Exception as e:
                        return (code, False, str(e))

                success = 0
                missing = 0
                fail = 0

                with ThreadPoolExecutor(max_workers=15) as ex:
                    futures = [ex.submit(do_put, code) for code in target_codes_set]
                    for fu in as_completed(futures):
                        _, ok, err = fu.result()
                        if ok:
                            success += 1
                        else:
                            if err == "missing":
                                missing += 1
                            else:
                                fail += 1

                self.log(f"✅ 商戶 {user} 完成：成功 {success}/{len(target_codes_set)} | 找不到 {missing} | 失敗 {fail}")
                ok_merchants += 1

            except Exception as e:
                self.log(f"❌ 商戶 {user} 發生錯誤: {e}")

        self.log(f"🏁 多商戶批次結束：完成 {ok_merchants}/{len(merchants)} 個商戶")

    def start_refresh_merchant_summary(self):
        threading.Thread(target=self.refresh_merchant_summary, daemon=True).start()

    def refresh_merchant_summary(self):
        selected = self.get_selected_merchants()
        if not selected:
            self.root.after(0, lambda: self._set_summary_text("⚠️ 尚未選取商戶，請先在商戶清單複選。"))
            return

        lines = []
        lines.append(f"📡 統計中...（{len(selected)} 個商戶）\n")

        for m in selected:
            user = m["user"]
            pw = m["pw"]

            try:
                res = requests.post(
                    f"{self.base_url}/login",
                    json={"username": user, "password": pw},
                    timeout=15
                )
                res.raise_for_status()
                token = f"Bearer {res.json()['data']['token']}"
                headers = {"Authorization": token}

                all_games = []
                p = 1

                while True:
                    r = requests.get(
                        f"{self.base_url}/platform_game?pagenum={p}&pagesize=200",
                        headers=headers,
                        timeout=15
                    )
                    r.raise_for_status()
                    j = r.json()

                    data = j.get("data", {}).get("data", [])
                    total = j.get("data", {}).get("total", 0)

                    all_games.extend(data)

                    if total and len(all_games) >= total:
                        break
                    if not data:
                        break
                    p += 1

                total_count = len(all_games)
                enabled_count = sum(1 for g in all_games if g.get("status") == 1)

                lines.append(f"🏪 {user}：✅ 開啟 {enabled_count} / {total_count}")

            except Exception as e:
                lines.append(f"🏪 {user}：❌ 統計失敗 ({e})")

        text = "\n".join(lines)
        self.root.after(0, lambda: self._set_summary_text(text))

    def _set_summary_text(self, text):
        self.txt_summary.delete("1.0", tk.END)
        self.txt_summary.insert(tk.END, text)
    def setup_tab2(self):
        """設定日誌分頁"""
        log_frame = tk.LabelFrame(self.tab2, text="🧾 系統日誌")
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_area = scrolledtext.ScrolledText(
            log_frame,
            width=100,
            height=30,
            bg="#f0f0f0"
        )
        self.log_area.pack(fill="both", expand=True, padx=5, pady=5)
if __name__ == "__main__":
    root = tk.Tk()
    app = SiteBApp(root)  # 改這裡
    root.mainloop()
