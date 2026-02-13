from logging import log
import os
import platform
import re
import threading
import traceback
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
import requests
####這裡尚未找到沒有在上面的解決方案
            #     try:
            #         # 找到所有表格行
            #         rows = page.locator("table:visible tr").all()
                    
            #         for row in rows:
            #             try:
            #                 # 獲取該行的 Min 和 Max 文字
            #                 cells = row.locator("td").all()
            #                 if len(cells) < 3:
            #                     continue
                                
            #                 # 檢查是否為 100 / 20,000 這一行
            #                 min_text = cells[1].inner_text().strip().replace(",", "")
            #                 max_text = cells[2].inner_text().strip().replace(",", "")

                            
            #                 if match_uncheck(min_text, max_text, uncheck_set):


            #                     # 找到這一行的 checkbox
            #                     checkbox = row.locator("input[type='checkbox']").first
                                
            #                     # 檢查是否已勾選
            #                     is_checked = checkbox.is_checked()
                                
            #                     if is_checked:
            #                         checkbox.click(force=True)
            #                         log(f"🧹 已取消勾選：Min={min_text}, Max={max_text}")
            #                     else:
            #                         log("ℹ️  偵測中")
                                
                                
            #             except:
            #                 continue
                            
            #     except Exception as e:
            #         log(f"⚠️  取消勾選 100/20000 時發生錯誤: {e}")
                
            #     page.wait_for_timeout(500)
                
            #     # === 步驟 2: 勾選 Min=100, Max=10,000 ===
            #     try:
            #         rows = page.locator("table:visible tr").all()
                    
            #         for row in rows:
            #             try:
            #                 cells = row.locator("td").all()
            #                 if len(cells) < 3:
            #                     continue
                                
            #                 # 檢查是否為 100 / 10,000 這一行
            #                 min_text = cells[1].inner_text().strip().replace(",", "")
            #                 max_text = cells[2].inner_text().strip().replace(",", "")
                            
            #                 if (min_text, max_text) in check_set:
            #                     checkbox = row.locator("input[type='checkbox']").first
                                
            #                     is_checked = checkbox.is_checked()
                                
            #                     if not is_checked:
            #                         checkbox.click(force=True)
            #                         log("✅ 已勾選：Min=100, Max=10,000")
            #                     else:
            #                         log("ℹ️  Min=100, Max=10,000 原本就已勾選")
                                
                               
            #             except:
            #                 continue
                            
            #     except Exception as e:
            #         log(f"⚠️  勾選 100/10000 時發生錯誤: {e}")
                
            #     page.wait_for_timeout(500)

 


            #     log("🎉 Bet Limit 設定完成")
            # def click_siteE_confirm(page):
            #     # 彈窗根節點（你 inspector 上看到的那個 section）
            #     dialog = page.locator("section.card.member-betlimit-dialog").first
            #     dialog.wait_for(state="visible", timeout=10000)

            #     # Confirm 就是 submit
            #     btn = dialog.locator('button[type="submit"]:has-text("Confirm")').first

            #     # 有些站會是大寫/有空白，補一個兜底：只用 type=submit
            #     if btn.count() == 0:
            #         btn = dialog.locator('button[type="submit"]').first

            #     btn.wait_for(state="visible", timeout=10000)
            #     btn.scroll_into_view_if_needed()
            #     btn.click(force=True)
            #     log("🚀 已點擊 Confirm 送出設定！")

            # if do_confirm:
            #     try:
            #         log("🖱️ SiteE：準備點擊 Confirm（送出 Bet Limit）")
            #         click_siteE_confirm(page)
            #         log("✅ SiteE：已點 Confirm")
            #         page.wait_for_timeout(800)  # 給它一點時間做提交/刷新
            #     except Exception as e:
            #         log(f"❌ SiteE：Confirm 點擊失敗：{e}")
            # else:
            #     log("⏭️ SiteE：已設定為不送出 Confirm（只勾選不提交）")




        # # ✅ 如果 UI 沒填 targets，就用預設測試 target（之後不想要直接註解掉這段）
        # if not target_list:
        #     target_list = [DEBUG_DEFAULT_TARGET]   # ← 不想自動塞就註解這行
        #     log(f"🧪 SiteB 使用預設測試 target：{target_list[0]}")

        # # ===== DEBUG 測試用預設 target（不想用就註解掉這行）=====
        # DEBUG_DEFAULT_TARGET = "ab1ecca08d3a7f15wrb"


#        input("⏸ 已暫停（畫面保留中），處理完請按 Enter 繼續或關閉…") debug時需要

# ==================== 爬蟲相關配置 ====================
API_BASE_URL = "https://wpapi.ldjzmr.top/master"
BEARER_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3dwYXBpLmxkanptci50b3AvbWFzdGVyL2xvZ2luIiwiaWF0IjoxNzcwNDI5NjIxLCJleHAiOjE4MDE5NjU2MjEsIm5iZiI6MTc3MDQyOTYyMSwianRpIjoicXpGSUx5c296eHZPczhyTSIsInN1YiI6IjExIiwicHJ2IjoiMTg4ODk5NDM5MDUwZTVmMzc0MDliMThjYzZhNDk1NjkyMmE3YWIxYiJ9.FJwCCTCn6CmghjL6gCTxyVDwa9-UZH25GiHT_JrIhYg"
# 配置檔路徑
CONFIG_PATH = Path("config_cache_siteC.json")  # ✅ 改成獨立的 config
# ===== DEBUG 測試用預設 target（不想用就註解掉這行）=====
DEBUG_DEFAULT_TARGET = "ab1ecca08d3a7f15wrb"

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}

    try:
        cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except:
        return {}

    # ✅ 舊版扁平格式：{"SA": {...}, "WM": {...}}
    # ✅ 新版格式：{"wp": {"SA": {...}}, "ldb": {"SA": {...}}}
    if cfg and ("wp" not in cfg and "ldb" not in cfg):
        cfg = {"wp": cfg, "ldb": {}}   # 舊資料先當作 wp
        save_config(cfg)

    # 保險：確保兩個 key 都存在
    cfg.setdefault("wp", {})
    cfg.setdefault("ldb", {})
    return cfg

def save_config(cfg: dict):
    CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")

# ==================== 爬蟲函數 ====================
def fetch_machines_from_api(page: int = 1, page_size: int = 100, log_fn=None):
    """從 API 獲取機器列表"""
    def log(msg):
        if log_fn:
            log_fn(msg)
    
    url = f"{API_BASE_URL}/machine"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {"pagenum": page, "pagesize": page_size}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        if log_fn:
            log(f"❌ API 請求失敗: {e}")
        return None


def parse_machine_data(api_response, log_fn=None):
    """解析 API 回傳的機器資料"""
    if not api_response:
        return []
    
    machines = []
    items = []
    
    if isinstance(api_response, dict) and "data" in api_response:
        data = api_response["data"]
        if isinstance(data, dict) and "data" in data:
            items = data["data"]
    
    for item in items:
        try:
            machine_id = str(item.get("id", ""))
            machine_name = item.get("name", "")
            brand = item.get("brand", {})
            brand_name = brand.get("name", "") if brand else ""
            user = item.get("user", {})
            
            if user:
                wm_id = user.get("WM_id") or ""
                ab_id = user.get("AB_id") or ""
                mt_id = user.get("MT_id") or ""
                t9_id = user.get("T9_id") or ""
                sa_id = user.get("SA_id") or ""
            else:
                wm_id = ab_id = mt_id = t9_id = sa_id = ""
            
            machines.append({
                "機器ID": machine_id,
                "商戶名稱": brand_name,
                "機器名稱": machine_name,
                "WM帳號": wm_id,
                "AB帳號": ab_id,
                "MT帳號": mt_id,
                "T9帳號": t9_id,
                "SA帳號": sa_id,
            })
        except:
            continue
    
    return machines


def crawl_all_machines(log_fn=None):
    """爬取所有機器的帳號資料"""
    def log(msg):
        if log_fn:
            log_fn(msg)
    
    log("🚀 開始爬取機器帳號...")
    all_machines = []
    page = 1
    page_size = 1000  # API 最大支援 1000，盡量減少請求次數
    
    while True:
        log(f"📄 正在抓取第 {page} 頁...")
        api_response = fetch_machines_from_api(page=page, page_size=page_size, log_fn=log_fn)
        
        if not api_response:
            log("❌ 無法獲取資料")
            break
        
        machine_data = parse_machine_data(api_response, log_fn=log_fn)
        
        if not machine_data:
            log(f"📌 已到達最後一頁（共 {page} 頁）")
            break
        
        log(f"✅ 第 {page} 頁：{len(machine_data)} 筆")
        all_machines.extend(machine_data)
        
        if len(machine_data) < page_size:
            break
        
        page += 1
    
    # 統計
    wm_count = sum(1 for m in all_machines if m.get("WM帳號"))
    ab_count = sum(1 for m in all_machines if m.get("AB帳號"))
    mt_count = sum(1 for m in all_machines if m.get("MT帳號"))
    t9_count = sum(1 for m in all_machines if m.get("T9帳號"))
    sa_count = sum(1 for m in all_machines if m.get("SA帳號"))
    
    log(f"\n✅ 總共 {len(all_machines)} 筆")
    log(f"📊 WM:{wm_count} AB:{ab_count} MT:{mt_count} T9:{t9_count} SA:{sa_count}")
    
    return all_machines



def run_site_A(platform: str, username: str, password: str, target_list: list,
               headless: bool, log_fn,
               process_group_a: bool, process_group_b: bool, process_group_c: bool = True,
               do_confirm: bool = True):
    def log(msg: str):
        log_fn(msg)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()


        # 1) 打開登入頁
        log("🔐 打開登入頁…")
        page.goto("https://hp8.pokp02.net/index.php?ctrl=login_c.php", wait_until="domcontentloaded")
        page.wait_for_timeout(600)

        # 切換語言為 English（登入前）
        page.locator("#language-type").click()
        page.wait_for_timeout(300)  # 給下拉一點動畫時間（可留）

        page.locator("#language-list-en").click()
        page.wait_for_timeout(500)  # 等語言套用

        user_input = page.get_by_placeholder("Account")
        pass_input = page.get_by_placeholder("password")

        # 兜底
        if user_input.count() == 0:
            user_input = page.locator('input[type="text"]').first
        if pass_input.count() == 0:
            pass_input = page.locator('input[type="password"]').first

        if user_input.count() == 0 or pass_input.count() == 0:
            browser.close()
            raise RuntimeError("找不到登入輸入框（帳號/密碼）")

        # 3) 輸入帳密
        log("✍️ 輸入帳密…")
        user_input.click()
        user_input.fill(username)
        pass_input.click()
        pass_input.fill(password)


        login_btn = page.get_by_role("button", name="LOGIN")
        if login_btn.count() == 0:
            login_btn = page.locator('button:has-text("LOGIN"), input[type="submit"], button[type="submit"]').first


        log("➡️ 送出登入（第 1 次）")
        login_btn.scroll_into_view_if_needed()
        login_btn.click(force=True)

        page.wait_for_timeout(2000)

        logged_in = False
        try:
            page.wait_for_url("**ctrl=ctrl_home**", timeout=5000)
            logged_in = True
            log("✅ 已登入成功（URL 判斷）")
        except:
            log("⚠️ URL 尚未進入 ctrl_home，準備第二次登入")
        if not logged_in:
            try:
                log("🔁 送出登入（第二次）")
                login_btn.scroll_into_view_if_needed(timeout=3000)
                login_btn.click(force=True)

                page.wait_for_url("**ctrl=ctrl_home**", timeout=8000)
                log("✅ 已登入成功（第二次 URL）")
            except Exception:
                log("❌ 第二次登入仍未進入 ctrl_home，繼續流程")




        # 5) 等登入成功（不要用 expect_navigation）
        try:
            page.wait_for_url("**ctrl=ctrl_home**", timeout=15000)
        except PWTimeout:
            page.locator("text=User Management").wait_for(timeout=15000)

        log(f"✅ 已登入：{page.url}")
        page.wait_for_timeout(400)

        log("📂 前往： User Management → User List")
        page.get_by_text("User Management", exact=True).click()
        page.wait_for_timeout(200)
        page.get_by_text("User List", exact=True).click()
        #input("⏸ 已暫停（畫面保留中），處理完請按 Enter 繼續或關閉…")

        # ✅ 等 User List 頁面穩定（你可以用你頁面上一定會出現的字）
        page.wait_for_timeout(8000)
        log("🧩 掃描所有 frames：找 search / placeholder …")

        keywords = ["id=\"search\"", "Please search", "name=\"account\"", "input#search"]
        hit_frames = []

        for i, f in enumerate(page.frames):
            try:
                html = f.content()
                hit = any(k in html for k in keywords)
                log(f"[frame {i}] url={f.url} hit={hit}")
                if hit:
                    hit_frames.append((i, f.url))
            except Exception as e:
                log(f"[frame {i}] url={f.url} read error: {e}")

        if not hit_frames:
            raise RuntimeError("所有 frame 都沒包含 search 相關字樣（可能是新分頁或更深層 iframe）")

        log(f"✅ 命中 frames: {hit_frames}")
        # 找第一個命中 frame
        for target_account in target_list:
            try:
                target_frame = None
                for f in page.frames:
                    try:
                        html = f.content()
                        if "id=\"search\"" in html or "Please search" in html or "name=\"account\"" in html:
                            target_frame = f
                            break
                    except:
                        pass

                if not target_frame:
                    raise RuntimeError("命中 frame 列表存在，但取不到 target_frame（奇怪）")

                log(f"🎯 使用 frame: {target_frame.url}")

                search = target_frame.locator('input#search, input[name="account"]').first
                search.wait_for(state="attached", timeout=15000)
                search.click(force=True)
                search.fill(target_account)
                log(f"✅ 已填入：{target_account}")

                for i, f in enumerate(page.frames):
                    print(i, f.url)
                target_frame = None
                for f in page.frames:
                    if f.locator('a[data-target="#popwindow"]').count() > 0:
                        target_frame = f
                        break

                if not target_frame:
                    raise RuntimeError("找不到 Search 按鈕所在的 frame")

                target_frame.locator('a[data-target="#popwindow"]').first.click(force=True)

                log("🚀 搜尋指令已送出！")

                        # 1) 確認 popwindow 還在（保險）
                modal = target_frame.locator("#popwindow")
                modal.wait_for(state="visible", timeout=15000)

                log("🔎 搜尋結果彈窗已存在，準備點擊帳號…")

                # 2) 用 href 的 aid 參數找連結（最穩）
                aid = target_account
                result_link = modal.locator(f'a[href*="aid={aid}"]').first

                result_link.wait_for(state="visible", timeout=15000)
                result_link.click(force=True)

                log(f"✅ 已點擊 target account：{aid}")
                page.wait_for_timeout(8000)
                log("已等待八秒")
                log("✏️ 準備點擊 Edit 按鈕…")

                # Edit 按鈕通常在同一個 frame（User List 那個）
                edit_btn = target_frame.locator('button[onclick*="UserAdd.php"]').first

                edit_btn.wait_for(state="visible", timeout=15000)
                edit_btn.click(force=True)

                log("✅ 已點擊 Edit，進入編輯頁")
                page.wait_for_timeout(4000)
                log("已等待4秒")
                def find_frame_containing(page):
                    """
                    找出包含 Code / Handicap / Baccarat 的 iframe
                    不吃可視範圍（就算畫面還沒滑到也能找到）
                    """
                    keywords = [
                        "Handicap",
                        "Code",
                    ]

                    for i, f in enumerate(page.frames):
                        try:
                            hit = 0
                            for k in keywords:
                                if f.locator(f"text={k}").count() > 0:
                                    hit += 1
                            if hit >= 1:  # 命中至少一個就很有可能
                                return f
                        except:
                            pass

                    return None
                frame = find_frame_containing(page)
                
                if not frame:
                    raise RuntimeError("找不到包含 Code / Handicap 的 iframe")
                log("✅ 找到 Code/Handicap 的 iframe")
                # 1. 定義分組
                groups = {
                    "群組 10K (4, 8, 13, 17, 58)": ["4", "8", "13", "17", "58"],
                    "群組 20K (21, 23, 25, 27, 172)": ["21", "23", "25", "27", "172"],
                    "群組 5K (3, 7, 12, 16, 57)": ["3", "7", "12", "16", "57"]
                }

                # 確保頁面加載
                frame.locator("text=Code").first.wait_for(state="visible", timeout=15000)

                groups_to_process = {}
                if process_group_a:
                    groups_to_process["群組 10K (4, 8, 13, 17, 58)"] = groups["群組 10K (4, 8, 13, 17, 58)"]
                if process_group_b:
                    groups_to_process["群組 20K (21, 23, 25, 27, 172)"] = groups["群組 20K (21, 23, 25, 27, 172)"]
                if process_group_c:
                    groups_to_process["群組 5K (3, 7, 12, 16, 57)"] = groups["群組 5K (3, 7, 12, 16, 57)"]

                for group_name, codes in groups_to_process.items():
                    log(f"\n--- 正在處理 {group_name} ---")
                    
                    for code in codes:
                        try:
                            # 定義號碼定位器
                            code_badge = frame.locator(f"xpath=//*[normalize-space(text())='{code}']").first
                            code_badge.wait_for(state="visible", timeout=5000)
                            # 找前面的 Checkbox 容器 (span)
                            box = code_badge.locator("xpath=preceding::span[1]").first                                                                                             
                            # 執行點擊 
                            click_target = box.locator("xpath=..").first
                            click_target.click(force=True)        
                        except Exception as e:
                            # 捕捉錯誤，不讓程式因為某個號碼沒找到就中斷
                            log(f"號碼 {code.ljust(3)}: ❌ 處理失敗 (找不到元素或超時)")

                if do_confirm:
                    log("🖱️ 準備捲動至頁面底部並點擊 Confirm...")
                    page.wait_for_timeout(300)

                    confirm_btn = frame.locator('button[onclick="dosubmit();"]').first

                    try:
                        confirm_btn.wait_for(state="attached", timeout=10000)
                        confirm_btn.scroll_into_view_if_needed()
                        log("✅ 已捲動到 Confirm 按鈕位置")

                        confirm_btn.click(force=True)
                        log("🚀 已點擊 CONFIRM 送出設定！")

                        page.wait_for_timeout(2000)
                    except Exception as e:
                        log(f"❌ 點擊 Confirm 失敗: {e}")
                else:
                    log("⏭️ 已設定為『不送出 Confirm』：跳過 Confirm 點擊（只做勾選不提交）")
                
                # page.wait_for_selector("th:has-text('Account')", state="visible", timeout=10000)
                # log("✅ 已回到 User List 頁面，準備處理下一個帳號（如果有的話）")
                # continue# 跳下一個帳號，避免下面的等待讓整個流程變慢

                
                def click_swal_ok(page):
                    frame = page.frame(url=re.compile("UserModify.php"))
                    if not frame:
                        log("⚠️ 找不到 UserModify iframe，略過 swal")
                        return

                    btn = frame.locator("button.swal-button--confirm")
                    if btn.count() > 0:
                        btn.first.click()
                        log("✅ 已點擊彈窗的 OK 按鈕")
                    else:
                        log("ℹ️ 沒有 swal OK 按鈕，正常略過")
                click_swal_ok(page)

                page.wait_for_timeout(3000)




            except Exception as e:
                log(f"❌ 帳號 {target_account} 執行中斷: {e}")
                # 發生錯誤時，嘗試回到 User List 頁面嘗試下一個，不讓整個程式當掉
                page.goto("原本 User List 的 URL") 
                continue



        page.wait_for_timeout(10_000_000)  # debug用，讓瀏覽器保持開啟


        browser.close()
def run_site_B(platform: str, username: str, password: str, target_list: list,
               headless: bool, log_fn,
               handicap_choice: str = "100_10K",
               do_submit: bool = True):
    def log(msg: str):
        log_fn(msg)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        log("🔐 SiteB")
        page.goto("https://ams.allbetgaming.net", wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        log("🌐 SiteB English...")
        label = page.locator('div.current-language-label').first
        label.wait_for(state="visible", timeout=10000)
        clickable = label.locator(
            "xpath=ancestor::a[1] | ancestor::button[1] | ancestor::div[1]"
        )
        clickable.click(force=True)
        page.locator(".language-item:has-text('English')").first.click(force=True)
        page.wait_for_timeout(600)
        log("✅ SiteB：語言已切換為 English")

        inputs = page.locator("input.el-input__inner")
        user_input = inputs.nth(0)
        pass_input = inputs.nth(1)
        user_input.click()
        user_input.fill(username)
        pass_input.click()
        pass_input.fill(password)

        login_span = page.locator("span:has-text('Login')").first
        login_span.click(force=True)
        pass_input.press("Enter")
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Players").click()

        if not target_list:
            target_list = ["ab1ecca08d3a7f15wrb"]
            log(f"🧪 SiteB 使用預設測試 target：{target_list[0]}")

        for target_account in target_list:
            log(f"\n{'='*50}")
            log(f"🔎 SiteB 搜尋：{target_account}")

            inputs = page.locator("input.el-input")
            target_input = inputs.first
            target_input.wait_for(state="visible", timeout=10000)
            target_input.click()
            target_input.press("Control+A")
            target_input.press("Backspace")
            target_input.type(target_account, delay=50)

            search_icon = page.locator("svg:has(title:has-text('search'))").first
            search_icon.wait_for(state="visible", timeout=10000)
            search_icon.click(force=True)
            log("✅ SiteB：已送出搜尋")
            page.wait_for_timeout(2000)

            # 找到 Handicap(Bet Limit) 旁的 Edit
            label_el = page.get_by_text("Handicap(Bet Limit)").first
            label_el.wait_for(state="visible", timeout=10000)
            btn = label_el.locator("xpath=following::button[.//span[normalize-space()='Edit']][1]").first
            btn.scroll_into_view_if_needed()
            btn.click(force=True)
            log("✅ SiteB：已點 Edit Handicap")
            page.wait_for_timeout(1500)

            # 鎖定彈窗
            modal = page.get_by_text("Edit Handicap(Bet Limit)", exact=False)\
                        .locator("xpath=ancestor::div[3]").first
            modal.wait_for(state="visible", timeout=10000)
            log("✅ Edit Handicap 彈窗已開啟")

            # ─── 步驟 1：取消所有已勾選的 checkbox ───
            # ─── 步驟 1：取消所有已勾選的 checkbox ───
            log("🧹 步驟 1：取消所有已勾選…")
            unchecked_count = page.evaluate("""() => {
                let count = 0;
                document.querySelectorAll('span.is-checked.el-checkbox__input').forEach(span => {
                    const inner = span.querySelector('.el-checkbox__inner');
                    if (inner) { inner.click(); count++; }
                });
                return count;
            }""")
            log(f"   🧹 已取消 {unchecked_count} 個勾選")
            page.wait_for_timeout(500)



            # ─── 步驟 2：勾選目標 ───
            log(f"✅ 步驟 2：勾選 → {handicap_choice}")
            try:
                # 用 JS 在彈窗內精確找到目標行的 checkbox 並點擊
                result = page.evaluate("""(choice) => {
                    const rows = document.querySelectorAll('tr');
                    for (const row of rows) {
                        const tds = row.querySelectorAll('td');
                        for (const td of tds) {
                            if (td.textContent.trim() === choice) {
                                const cb = row.querySelector('.el-checkbox__inner');
                                if (cb) { cb.click(); return 'clicked'; }
                                return 'no_checkbox';
                            }
                        }
                    }
                    return 'not_found';
                }""", handicap_choice)

                if result == "clicked":
                    log(f"   ✅ 已勾選：{handicap_choice}")
                elif result == "no_checkbox":
                    log(f"   ⚠️ 找到行但沒有 checkbox")
                else:
                    log(f"   ❌ 找不到 {handicap_choice} 這一行")
            except Exception as e:
                log(f"   ❌ 勾選失敗: {e}")

            page.wait_for_timeout(500)


            page.locator('button:has-text("Next")').first.click(force=True)

            log(f"✅ SiteB：已點 Next")
            log(f"✅ 步驟 2：勾選 → V_2K_20K")
            try:
                # 用 JS 在彈窗內精確找到目標行的 checkbox 並點擊
                result = page.evaluate("""(choice) => {
                    const rows = document.querySelectorAll('tr');
                    for (const row of rows) {
                        const tds = row.querySelectorAll('td');
                        for (const td of tds) {
                            if (td.textContent.trim() === choice) {
                                const cb = row.querySelector('.el-checkbox__inner');
                                if (cb) { cb.click(); return 'clicked'; }
                                return 'no_checkbox';
                            }
                        }
                    }
                    return 'not_found';
                }""", "V_2K_20K")

                if result == "clicked":
                    log(f"   ✅ 已勾選：V_2K_20K")
                elif result == "no_checkbox":
                    log(f"   ⚠️ 找到行但沒有 checkbox")
                else:
                    log(f"   ❌ 找不到 V_2K_20K 這一行")
            except Exception as e:
                log(f"   ❌ 勾選失敗: {e}")

            page.locator('button:has-text("Next")').first.click(force=True)
            log(f"✅ SiteB：已點 Next（第二次）")

            password_input = page.locator("input[placeholder='Operator Password']")
            password_input.fill("Asdf1234=")  # 這個密碼是固定的（目前沒看到 UI 可以改）
            log("✅ 已填入 Operator Password")

            page.wait_for_timeout(300)

            if do_submit:
                    log("🖱️ SiteB：準備點擊 Submit...")
                    submit_button = page.locator('button:has-text("Submit")')
                    submit_button.first.click(force=True)
                    log("✅ SiteB：已點擊 Submit 送出設定！")
            else:
                log("⏭️ SiteB：設定為『不送出 Submit』，跳過最後一步。")

            # submit_button = page.locator('button:has-text("Submit")')
            # submit_button.first.click(force=True)



        page.wait_for_timeout(10_000_000)  # debug用
        browser.close()



        

def run_site_C(platform: str, username: str, password: str, target_list: list,
               headless: bool, log_fn, normal_max: str, deluxe_max: str,            do_confirm: bool = True):
    def log(msg: str):
        log_fn(msg) # 這樣就不用每次都傳 log_fn 了
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        log("🔐 SiteC：進入MT後台")
        page.goto("http://uag533.ofalive99.net ", wait_until="domcontentloaded")
        page.wait_for_timeout(300)
        user_input = page.get_by_placeholder("Username")
        pass_input = page.get_by_placeholder("Password")

        # 兜底
        if user_input.count() == 0:
            user_input = page.locator('input[type="text"]').first
        if pass_input.count() == 0:
            pass_input = page.locator('input[type="password"]').first

        if user_input.count() == 0 or pass_input.count() == 0:
            browser.close()
            raise RuntimeError("找不到登入輸入框（帳號/密碼）")

        # 3) 輸入帳密
        log("✍️ 輸入帳密…")
        user_input.click()
        user_input.fill(username)
        pass_input.click()
        pass_input.fill(password)
        page.get_by_role("button", name="Login").click()
        log("⏳ SiteC：等待登入成功（出現 Dashboard）...    ")

        page.wait_for_timeout(1000)

        # 點擊「帳號」選單
        log("📂 點擊「帳號」選單")
        page.locator('text=帳號').first.click(force=True)
        page.wait_for_timeout(800)

        # 點擊「用戶管理」
        log("📂 點擊「用戶管理」")
        page.locator('text=用戶管理').first.click(force=True)
        page.wait_for_timeout(2000)

        if not target_list:
            target_list = ["5d761fddf0b0aa3b891c"]   # ← 不想自動塞就註解這行
            log(f"🧪 SiteB 使用預設測試 target：{target_list[0]}")
        # 處理每個 target 帳號
        for target_account in target_list:
            log(f"🔎 查詢帳號：{target_account}")
            
            # 填入帳號
            search_input = page.locator('input[type="text"]').first
            search_input.click()
            search_input.press("Control+A")
            search_input.press("Backspace")
            search_input.fill(target_account)
            
            # 點查詢
            page.locator('button.ant-btn.ant-btn-primary').first.click(force=True)
            log("✅ 查詢指令已送出！")
            page.wait_for_timeout(2000)
            log(f"✅ {target_account} 查詢完成")
            # 點「限紅組設定」
            log("🖱️ 點擊「限紅組設定」")
            page.locator('button:has-text("限紅組設定")').first.click(force=True)
            page.wait_for_timeout(1500)
            log("✅ 已進入限紅組設定頁面")

            # === 處理限紅組勾選 ===
            page.wait_for_timeout(1000)

            # 定義目標限紅組對應關係
            target_map = {
                "10000": ("100", "10000"),  
                "20000": ("100", "20000"),    
                "5000": ("100", "5000")      
            }

            if normal_max in target_map:
                target_min, target_max = target_map[normal_max]
                log(f"🎯 目標限紅組：最小={target_min}, 最大={target_max}")
                
                try:
                    # 等待彈窗完全載入
                    page.wait_for_timeout(800)
                    
                    # 掃描所有表格行
                    all_rows = page.locator("tr").all()
                    log(f"📋 掃描到 {len(all_rows)} 行")
                    
                    found = False
                    for idx, row in enumerate(all_rows):
                        try:
                            # 獲取該行的所有單元格
                            cells = row.locator("td").all()
                            
                            # 至少要有 3 個 td
                            if len(cells) < 3:
                                continue
                            
                            # 讀取最小下注和最大下注
                            min_text = cells[1].inner_text().strip()
                            max_text = cells[2].inner_text().strip()
                            
                            # 檢查是否為目標
                            if min_text == target_min and max_text == target_max:
                                log(f"✅ 找到目標：第 {idx} 行，最小={min_text}, 最大={max_text}")
                                
                                # 捲動到該行
                                row.scroll_into_view_if_needed()
                                page.wait_for_timeout(300)
                                
                                # 找到該行的開關
                                toggle = row.locator('input[type="checkbox"]').first
                                
                                # 如果找不到 checkbox，試 ant-switch
                                if toggle.count() == 0:
                                    toggle = row.locator('.ant-switch').first
                                
                                if toggle.count() > 0:
                                    # 檢查是否已開啟
                                    is_on = False
                                    try:
                                        is_on = toggle.is_checked()
                                    except:
                                        try:
                                            classes = toggle.get_attribute("class") or ""
                                            is_on = "ant-switch-checked" in classes or "checked" in classes
                                        except:
                                            pass
                                    
                                    if not is_on:
                                        toggle.click(force=True)
                                        page.wait_for_timeout(500)
                                        log(f"✅ 已開啟限紅組：{min_text}-{max_text}")
                                    else:
                                        log(f"ℹ️ 限紅組 {min_text}-{max_text} 已經是開啟狀態")
                                    
                                    found = True
                                    break
                                else:
                                    log(f"⚠️ 找到目標行但找不到開關元件")
                                    
                        except Exception as e:
                            continue
                    
                    if not found:
                        log(f"❌ 找不到限紅組 {target_min}-{target_max}")
                        
                except Exception as e:
                    log(f"❌ 處理限紅組時發生錯誤: {e}")
                    log(traceback.format_exc())
                    
            else:
                log("⚠️ 未選擇有效的限紅組（10000/20000/5000）")

            page.wait_for_timeout(800)

            # === 點擊「儲存」按鈕 ===
            if do_confirm:
                log("🖱️ 準備點擊「儲存」按鈕...")
                try:
                    # 先等一下，確保彈窗穩定
                    page.wait_for_timeout(1000)
                    
                    # 方法1：捲到彈窗內容最底部
                    dialog_body = page.locator('.ant-modal-body, div[role="dialog"]').first
                    if dialog_body.count() > 0:
                        dialog_body.evaluate("(el) => el.scrollTo(0, el.scrollHeight)")
                        page.wait_for_timeout(500)
                    
                    # 方法2：也捲整個頁面
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(500)
                    
                    # 找儲存按鈕（根據截圖，是在底部的按鈕）
                    # 先試最精確的
                    save_btn = page.locator('button:has-text("儲存"):not(:has-text("取消"))').first
                    
                    if save_btn.count() == 0:
                        # 備用方案1：找所有包含「儲」字的按鈕
                        save_btn = page.locator('button:has-text("儲")').first
                    
                    if save_btn.count() == 0:
                        # 備用方案2：找底部區域的按鈕
                        footer_buttons = page.locator('.ant-modal-footer button, .dialog-footer button').all()
                        for btn in footer_buttons:
                            try:
                                text = btn.inner_text()
                                if "儲" in text or "存" in text or "Save" in text:
                                    save_btn = btn
                                    log(f"✅ 在底部找到按鈕：{text}")
                                    break
                            except:
                                continue
                    
                    if save_btn and save_btn.count() > 0:
                        # 確保按鈕完全可見
                        save_btn.wait_for(state="visible", timeout=5000)
                        save_btn.scroll_into_view_if_needed()
                        page.wait_for_timeout(500)
                        
                        # 檢查按鈕是否可點擊（沒有 disabled）
                        is_disabled = save_btn.is_disabled()
                        if is_disabled:
                            log("⚠️ 儲存按鈕是 disabled 狀態")
                        
                        # 嘗試點擊
                        try:
                            save_btn.click(timeout=5000)
                            log("✅ 已點擊「儲存」（方法1）")
                        except:
                            try:
                                save_btn.click(force=True)
                                log("✅ 已點擊「儲存」（方法2：force）")
                            except:
                                try:
                                    # 用座標點擊
                                    box = save_btn.bounding_box()
                                    if box:
                                        x = box["x"] + box["width"] / 2
                                        y = box["y"] + box["height"] / 2
                                        page.mouse.click(x, y)
                                        log("✅ 已點擊「儲存」（方法3：座標）")
                                    else:
                                        raise Exception("無法取得按鈕位置")
                                except Exception as e3:
                                    # 最後一招：JS 點擊
                                    save_btn.evaluate("(el) => el.click()")
                                    log("✅ 已點擊「儲存」（方法4：JS）")
                        
                        page.wait_for_timeout(2000)
                        log("✅ 已送出限紅組設定")
                    else:
                        log("❌ 找不到儲存按鈕")
                        
                        # Debug：列出所有可見的按鈕
                        all_btns = page.locator('button:visible').all()
                        log(f"📋 頁面上有 {len(all_btns)} 個可見按鈕：")
                        for i, btn in enumerate(all_btns):
                            try:
                                text = btn.inner_text().strip()
                                if text:
                                    log(f"  按鈕 {i+1}: [{text}]")
                            except:
                                pass
                        
                except Exception as e:
                    log(f"❌ 點擊儲存時發生錯誤: {e}")
                    log(traceback.format_exc())
            else:
                log("⏭️ 設定為不送出（只勾選不儲存）")


        page.wait_for_timeout(10_000_000)  # debug用
        browser.close()

def run_site_D(platform: str, username: str, password: str, target_list: list,
               headless: bool, log_fn, normal_max: str, deluxe_max: str,
               do_confirm: bool = True):
    def log(msg: str):
        log_fn(msg)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        log("🔐 SiteD：進入T9後台")
        page.goto("https://dash.t9cn818.online", wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        # 找帳號輸入框（第一個 input）
        log("✍️ 填入帳號...")
        user_input = page.locator('input[type="text"]').first
        if user_input.count() == 0:
            user_input = page.locator('input.el-input').first
        
        if user_input.count() == 0:
            # 用 class 找
            user_input = page.locator('.el-input__inner').first
        
        user_input.wait_for(state="visible", timeout=10000)
        user_input.click()
        user_input.fill(username)
        log(f"✅ 已填入帳號：{username}")

        # 找密碼輸入框（第二個 input 或 type=password）
        log("✍️ 填入密碼...")
        pass_input = page.locator('input[type="password"]').first
        if pass_input.count() == 0:
            # 備用：找第二個 input
            pass_input = page.locator('input.el-input__inner').nth(1)
        
        pass_input.wait_for(state="visible", timeout=10000)
        pass_input.click()
        pass_input.fill(password)
        log("✅ 已填入密碼")

        page.wait_for_timeout(500)

        # 點登入按鈕（黃色按鈕，文字是「登入」）
        log("🖱️ 點擊登入按鈕...")
        login_btn = page.locator('button:has-text("登入")').first
        
        if login_btn.count() == 0:
            # 備用：找黃色按鈕
            login_btn = page.locator('button.el-button.bg-yellow').first
        
        if login_btn.count() == 0:
            # 再備用：找 type=button 或 submit
            login_btn = page.locator('button[type="button"], button[type="submit"]').first
        
        login_btn.wait_for(state="visible", timeout=10000)
        login_btn.click(force=True)
        log("✅ 已點擊登入按鈕")

        # 等待登入成功（URL 變化或出現特定元素）
        log("⏳ 等待登入成功...")
        page.wait_for_timeout(3000)
        
        # 檢查是否登入成功（可能會跳轉到 dashboard 或 home）
        try:
            # 等待 URL 變化
            page.wait_for_url("**/home", timeout=10000)
            log("✅ 登入成功（URL 已變化）")
        except:
            try:
                # 或者等待某個登入後才會出現的元素
                page.wait_for_selector("text=代理商管理系統", timeout=10000)
                log("✅ 登入成功（偵測到管理系統）")
            except:
                log("⚠️ 無法確認登入狀態，繼續執行...")

        log(f"📍 當前 URL: {page.url}")



        # === 點擊「玩家」選單 ===
        log("📂 點擊「玩家」選單...")
        try:
            # 方法1：直接用文字
            player_menu = page.locator('text=玩家').first
            
            # 如果找不到，可能在側邊欄
            if player_menu.count() == 0:
                player_menu = page.locator('.sidebar text=玩家, a:has-text("玩家")').first
            
            player_menu.wait_for(state="visible", timeout=10000)
            player_menu.click(force=True)
            log("✅ 已點擊「玩家」")
            page.wait_for_timeout(1500)
            
        except Exception as e:
            log(f"❌ 點擊「玩家」失敗: {e}")
            raise

        # === 處理每個 target 帳號 ===
        if not target_list:
            target_list = ["bada3a98436fe12dbf717a21a6ff90"]  # 測試用，之後可以註解掉
            log(f"🧪 使用測試 target：{target_list[0]}")

        for target_account in target_list:
            try:
                log(f"\n{'='*50}")
                log(f"🔎 處理帳號：{target_account}")
                
                # === 填入搜尋框 ===
                log("✍️ 填入搜尋框...")
                
                # 找可見的 input（排除 hidden）
                search_input = page.locator('input.el-input:visible').first
                
                if search_input.count() == 0:
                    # 備用1：找 el-input__inner（這是 Element UI 真正的輸入框）
                    search_input = page.locator('input.el-input__inner:visible').first
                
                if search_input.count() == 0:
                    # 備用2：在搜尋區域找 input
                    search_input = page.locator('.agentSearchBar input:visible, .search-bar input:visible').first
                
                if search_input.count() == 0:
                    # 備用3：找 type=text 且可見的
                    search_input = page.locator('input[type="text"]:visible').first
                
                if search_input.count() == 0:
                    log("❌ 找不到可見的搜尋框")
                    raise RuntimeError("找不到搜尋框")
                
                search_input.wait_for(state="visible", timeout=10000)
                search_input.scroll_into_view_if_needed()
                page.wait_for_timeout(300)
                
                search_input.click()
                
                # 清空舊內容
                search_input.press("Control+A")
                search_input.press("Backspace")
                page.wait_for_timeout(300)
                
                # 填入 target
                search_input.fill(target_account)
                log(f"✅ 已填入：{target_account}")
                page.wait_for_timeout(500)
                
                # === 點擊搜尋按鈕（放大鏡）===
                log("🖱️ 點擊搜尋按鈕...")
                
                # 方法1：找 filter-item button（根據 DevTools 看到的結構）
                search_btn = page.locator('.filter-item button').first
                
                if search_btn.count() == 0:
                    # 方法2：找包含 SVG 圖標的按鈕
                    search_btn = page.locator('button:has(svg)').first
                
                if search_btn.count() == 0:
                    # 方法3：找 el-button
                    search_btn = page.locator('button.el-button').first
                
                if search_btn.count() == 0:
                    # 方法4：在搜尋框旁邊找按鈕
                    search_btn = page.locator('.filter-wrap button, .search-bar button').first
                
                if search_btn.count() > 0:
                    search_btn.wait_for(state="visible", timeout=5000)
                    search_btn.scroll_into_view_if_needed()
                    page.wait_for_timeout(300)
                    search_btn.click(force=True)
                    log("✅ 已點擊搜尋按鈕")
                else:
                    # 方法5：直接按 Enter
                    log("⌨️ 找不到按鈕，嘗試按 Enter...")
                    search_input.press("Enter")
                    log("✅ 已按 Enter 送出")
                
                page.wait_for_timeout(2000)
                log("✅ 已送出搜尋，等待結果...")
                
                # TODO: 這裡加入後續操作
                # 例如：點擊搜尋結果、進入詳情、設定限紅等
                
                log(f"✅ 帳號 {target_account} 搜尋完成")
                
            except Exception as e:
                log(f"❌ 處理帳號 {target_account} 時發生錯誤: {e}")
                log(traceback.format_exc())
                continue


            page.wait_for_timeout(1000)

            
            # === 點擊「遊戲限紅設定」按鈕 ===
            log("🖱️ 點擊「遊戲限紅設定」...")
            try:
                # 方法1：直接用文字找
                limit_btn = page.locator('button:has-text("遊戲限紅設定")').first
                
                if limit_btn.count() == 0:
                    # 方法2：找黃色按鈕（可能只顯示部分文字）
                    limit_btn = page.locator('button.bg-yellow:has-text("限紅")').first
                
                if limit_btn.count() == 0:
                    # 方法3：在搜尋結果區域找黃色按鈕
                    limit_btn = page.locator('.list-item button.bg-yellow, .el-button.bg-yellow').first
                
                if limit_btn.count() == 0:
                    raise RuntimeError("找不到「遊戲限紅設定」按鈕")
                
                limit_btn.wait_for(state="visible", timeout=10000)
                limit_btn.scroll_into_view_if_needed()
                page.wait_for_timeout(300)
                limit_btn.click(force=True)
                log("✅ 已點擊「遊戲限紅設定」")
                
                page.wait_for_timeout(2000)
                
                # TODO: 這裡加入限紅設定的後續操作
                
            except Exception as e:
                log(f"❌ 點擊「遊戲限紅設定」失敗: {e}")
                raise

            log("📋 等待限紅設定頁面載入...")
            page.wait_for_timeout(1500)
            
            # === T9 遊戲限紅設定 ===
            log("🎯 開始設定遊戲限紅...")
            
            # 確認彈窗已開啟
            dialog = page.locator('text=遊戲限紅設定').first
            dialog.wait_for(state="visible", timeout=10000)
            log("✅ 限紅設定彈窗已開啟")
            
            log("📋 等待限紅設定頁面載入...")
            page.wait_for_timeout(1500)
            
            # === T9 遊戲限紅設定 ===
            log("🎯 開始設定遊戲限紅...")
            
            # 確認彈窗已開啟
            dialog = page.locator('text=遊戲限紅設定').first
            dialog.wait_for(state="visible", timeout=10000)
            log("✅ 限紅設定彈窗已開啟")
            
            # 從參數取得目標金額
            target_max = normal_max
            if not target_max or target_max not in ["5000", "10000", "20000"]:
                target_max = "10000"
            
            log(f"🎯 目標最大限紅：{target_max}")
            
            # 找到所有「最大限紅」的輸入框（應該有3個）
            max_inputs = page.locator('input.el-input__inner:visible').all()
            
            # 過濾出真正的最大限紅輸入框（通常是偶數位置：1, 3, 5）
            target_inputs = []
            for i, inp in enumerate(max_inputs):
                try:
                    # 檢查 input 的值，最大限紅通常比較大
                    val = inp.input_value()
                    if val and int(val.replace(',', '')) >= 10000:
                        target_inputs.append(inp)
                except:
                    # 如果無法取得值，用位置判斷（奇數位是最大限紅）
                    if i % 2 == 1:
                        target_inputs.append(inp)
            
            # 如果上面邏輯找不到，就用簡單的方法：取第 1, 3, 5 個
            if len(target_inputs) < 3:
                target_inputs = [max_inputs[1], max_inputs[3], max_inputs[5]] if len(max_inputs) >= 6 else max_inputs
            
            log(f"📋 找到 {len(target_inputs)} 個最大限紅輸入框")
            
            # 三個類別的名稱（用於 log）
            categories = ["真人1類", "區塊鏈1類", "區塊鏈2類"]
            
            # 處理每個輸入框
            for idx in range(min(3, len(target_inputs))):
                category = categories[idx] if idx < len(categories) else f"類別{idx+1}"
                
                try:
                    log(f"\n--- 處理 {category} ---")
                    
                    max_input = target_inputs[idx]
                    
                    # 清空並填入新值
                    max_input.scroll_into_view_if_needed()
                    page.wait_for_timeout(200)
                    max_input.click()
                    page.wait_for_timeout(200)
                    
                    # 清空（多種方法確保清空）
                    max_input.press("Control+A")
                    max_input.press("Backspace")
                    page.wait_for_timeout(200)
                    max_input.fill("")
                    page.wait_for_timeout(200)
                    
                    # 填入新值
                    max_input.fill(target_max)
                    log(f"✅ 已設定最大限紅：{target_max}")
                    page.wait_for_timeout(500)
                    
                    # === 點擊「儲存為預設值」按鈕 ===
                    if do_confirm:
                        log(f"🖱️ 點擊 {category} 的「儲存為預設值」...")
                        
                        try:
                            # 從當前 input 往後找按鈕
                            save_btn = max_input.locator('xpath=following::button[1]').first
                            
                            if save_btn.count() == 0:
                                # 備用：找所有按鈕，取第 idx 個
                                all_save_btns = page.locator('button:has-text("儲存為預設值")').all()
                                if idx < len(all_save_btns):
                                    save_btn = all_save_btns[idx]
                            
                            if save_btn and save_btn.count() > 0:
                                save_btn.scroll_into_view_if_needed()
                                page.wait_for_timeout(300)
                                save_btn.click(force=True)
                                log(f"✅ 已點擊 {category} 的「儲存為預設值」")
                                page.wait_for_timeout(1000)
                            else:
                                log(f"⚠️ 找不到 {category} 的儲存按鈕")
                                
                        except Exception as e:
                            log(f"❌ 點擊儲存按鈕失敗: {e}")
                    
                except Exception as e:
                    log(f"❌ 處理 {category} 時發生錯誤: {e}")
                    log(traceback.format_exc())
                    continue
            

        page.wait_for_timeout(10_000_000)  # debug用
        browser.close()

  



    
        
def run_site_E(platform: str, username: str, password: str, target_list: list,
               headless: bool, log_fn, normal_max: str, deluxe_max: str,
               do_confirm: bool = True):

    def log(msg: str):
        log_fn(msg)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        log("🔐 SA：進入 https://bop.sa-bo.net ...")
        page.goto("https://bop.sa-bo.net", wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        log("🌐 SiteE：準備切換語言到 English...")

        # 1) 點「简体中文」下拉（用 id 最穩）
        lang_btn = page.locator("#dropdownMenuLink")
        lang_btn.wait_for(state="visible", timeout=10000)
        lang_btn.click(force=True)

        # 2) 點 English（可能在 dropdown 裡，保守用文字匹配）
        en_item = page.locator('span.dropdown-item.cursor-pointer:has-text("English")')
        if en_item.count() == 0:
            # 兜底：有些站 dropdown-item 可能不是 span
            en_item = page.locator('.dropdown-item.cursor-pointer:has-text("English")')

        en_item.wait_for(state="visible", timeout=10000)
        en_item.click(force=True)

        page.wait_for_timeout(600)
        log("✅ SiteE：語言已切換為 English")

        user_input = page.get_by_placeholder("Username")
        pass_input = page.get_by_placeholder("Password")

        # 兜底
        if user_input.count() == 0:
            user_input = page.locator('input[type="text"]').first
        if pass_input.count() == 0:
            pass_input = page.locator('input[type="password"]').first

        if user_input.count() == 0 or pass_input.count() == 0:
            browser.close()
            raise RuntimeError("找不到登入輸入框（帳號/密碼）")

        # 3) 輸入帳密
        log("✍️ 輸入帳密…")
        user_input.click()
        user_input.fill(username)
        pass_input.click()
        pass_input.fill(password)

        log("⏳ SiteE：等待登入成功（出現 Functions）...")
        page.get_by_text("Functions", exact=True).wait_for(timeout=180000)  # 給你 3 分鐘輸驗證碼
        log("✅ SiteE：偵測到 Functions（登入成功）")

        # 7) 點 Functions
        page.get_by_text("Functions", exact=True).click()
        page.wait_for_timeout(500)
        page.get_by_text("Account Management", exact=True).click()
        page.wait_for_timeout(500)

        log("🖱️ SiteE：點擊第一筆 Username")

            # 等 Account Management 表格出現
        page.locator("table").wait_for(timeout=15000)

        # 點第一個 Username 連結（藍色）
        username_link = page.locator("table a").first
        username_link.wait_for(state="visible", timeout=15000)
        username_link.click(force=True)
        page.wait_for_timeout(1000)
        username_link = page.locator("table a").first
        username_link.wait_for(state="visible", timeout=15000)
        username_link.click(force=True)

        log("✅ SiteE：已點擊第一筆 Username")
        if not target_list:
            target_list = ["e75d6c5cd07c669f067"]   # ← 不想自動塞就註解這行
            log(f"🧪 SiteB 使用預設測試 target：{target_list[0]}")
        for target_account in target_list:
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(300)
            log(f"🔎 將 Username 搜尋改為：{target_account}")

            # 1️⃣ 等 Username 搜尋框
            username_input = page.locator('input[name="searchUserName"], input[placeholder="Username"]').first
            username_input.wait_for(state="visible", timeout=15000)

            # 2️⃣ 清空（一定要這樣，不要只用 fill）
            username_input.click()
            username_input.press("Control+A")
            username_input.press("Backspace")

            # 3️⃣ 輸入 target account
            if platform =="wp":
                username_input.fill(f"{target_account}@a13154")
            else:
                username_input.fill(f"{target_account}@a14251")

            # 4️⃣ 點 Search
            search_btn = page.locator('button:has-text("Search")').first
            search_btn.click(force=True)

            log("✅ 已送出 Username 搜尋")
            member_table = page.locator("table").nth(1)

            bet_icon = member_table.locator("i.icon-betlimit").first
            bet_icon.wait_for(state="visible", timeout=15000)
            bet_icon.scroll_into_view_if_needed()
            page.wait_for_timeout(200)

            # 方案 A：先點外層（很多時候真正可點的是 a/button/td）
            try:
                bet_clickable = bet_icon.locator("xpath=ancestor::a[1] | ancestor::button[1] | ancestor::td[1]").first
                bet_clickable.click(timeout=3000)
                log("✅ Bet Limit：已點外層容器")
            except Exception as e1:
                log(f"⚠️ 外層點擊失敗，改用中心點座標點擊：{e1}")

                # 方案 B：中心點座標點擊（必殺）
                box = bet_icon.bounding_box()
                if not box:
                    raise RuntimeError("抓不到 Bet Limit icon 的 bounding box（可能被遮住或不在視窗內）")

                x = box["x"] + box["width"] / 2
                y = box["y"] + box["height"] / 2

                page.mouse.click(x, y)
                page.wait_for_timeout(200)

                # 方案 C：再補一個 JS click（保險）
                try:
                    bet_icon.evaluate("(el) => el.click()")
                    log("✅ Bet Limit：中心點 + JS click 補刀完成")
                except Exception as e2:
                    log(f"⚠️ JS click 也失敗：{e2}")


            log("🎯 開始處理 Bet Limit 設定...")

            # 等待彈窗出現
            page.wait_for_timeout(1500)
            # 找到包含 Min/Max 的表格
            title = page.get_by_text("Game Bet Limit Options", exact=False).first
            title.wait_for(state="visible", timeout=10000)
            
            log("✅ Bet Limit 彈窗已開啟")
            # === 開始處理各個遊戲分頁 ===
            exclude_games = ["Carnival Treasure"]
            special_games = ["Deluxe Blackjack"]

            tab_names = [
                "Andar Bahar", "Baccarat", "Dragon Tiger", "Fish Prawn Crab",
                "Pok Deng", "Roulette", "Sic Bo", "Teen Patti 20-20",
                "Thai HiLo", "Ultra Roulette", "Xoc Dia",
                "Deluxe Blackjack",  # ✅ 你要處理它，就要把它放進來
            ]

            for game_name in tab_names:
                if game_name in exclude_games:
                    log(f"⏩ 跳過不處理：{game_name}")
                    continue

                log(f"🔄 正在處理遊戲：{game_name}")
                page.get_by_role("listitem").get_by_text(game_name, exact=True).click()
                page.wait_for_timeout(500)

                NORMAL_CHOICES = {"10000", "20000", "5000"}  # 想加 5000 就加
                DELUXE_CHOICES = {"10000", "20000", "5000"}

                def match_uncheck(min_text: str, max_text: str, uncheck_set: set) -> bool:
                    # uncheck_set 內容像 {("*","10000"), ("100","20000")...}
                    for rmin, rmax in uncheck_set:
                        min_ok = (rmin == "*" or min_text == str(rmin))
                        max_ok = (rmax == "*" or max_text == str(rmax))
                        if min_ok and max_ok:
                            return True
                    return False
                if game_name == "Deluxe Blackjack":
                    uncheck_set = {("200", m) for m in DELUXE_CHOICES}   # 先清掉同 min 候選
                    check_set   = {("200", deluxe_max)}                  # 再勾你選的
                    log(f"🎯 特殊處理：{game_name} → 勾 200-{deluxe_max}")
                else:
                    # ✅ Ultra Roulette + 5000 → 改用 50-5000
                    if game_name == "Ultra Roulette" and normal_max == "5000":
                        base_min = "50"
                        uncheck_base_min="*"
                        log("🧠 Ultra Roulette 偵測到 Max=5000，改用 Min=50（因為沒有 100-5000）")
                    else:
                        base_min = "100"
                        uncheck_base_min="*"

                    target_max = normal_max
                    choices = NORMAL_CHOICES

                    uncheck_set = {(uncheck_base_min, m) for m in choices}      # 清同 min 的候選
                    check_set   = {(base_min, target_max)}              # 勾你選的那個
                    log(f"🎯 {game_name} → 目標勾選 {base_min}-{target_max}")
                
                

             
                try:
                    # 找到所有表格行
                    rows = page.locator("table:visible tr").all()
                    
                    for row in rows:
                        try:
                            # 獲取該行的 Min 和 Max 文字
                            cells = row.locator("td").all()
                            if len(cells) < 3:
                                continue
                                
                            # 檢查是否為 100 / 20,000 這一行
                            min_text = cells[1].inner_text().strip().replace(",", "")
                            max_text = cells[2].inner_text().strip().replace(",", "")

                            
                            if match_uncheck(min_text, max_text, uncheck_set):


                                # 找到這一行的 checkbox
                                checkbox = row.locator("input[type='checkbox']").first
                                
                                # 檢查是否已勾選
                                is_checked = checkbox.is_checked()
                                
                                if is_checked:
                                    checkbox.click(force=True)
                                    log(f"🧹 已取消勾選：Min={min_text}, Max={max_text}")
                                else:
                                    log("ℹ️  偵測中")
                                
                                
                        except:
                            continue
                            
                except Exception as e:
                    log(f"⚠️  取消勾選 100/20000 時發生錯誤: {e}")
                

                
                # === 步驟 2: 勾選 Min=100, Max=10,000 ===
                try:
                    rows = page.locator("table:visible tr").all()
                    
                    for row in rows:
                        try:
                            cells = row.locator("td").all()
                            if len(cells) < 3:
                                continue
                                
                            # 檢查是否為 100 / 10,000 這一行
                            min_text = cells[1].inner_text().strip().replace(",", "")
                            max_text = cells[2].inner_text().strip().replace(",", "")
                            
                            if (min_text, max_text) in check_set:
                                checkbox = row.locator("input[type='checkbox']").first
                                
                                is_checked = checkbox.is_checked()
                                
                                if not is_checked:
                                    checkbox.click(force=True)
                                    log("✅ 已勾選：Min=100, Max=10,000")
                                else:
                                    log("ℹ️  Min=100, Max=10,000 原本就已勾選")
                                
                               
                        except:
                            continue
                            
                except Exception as e:
                    log(f"⚠️  勾選 100/10000 時發生錯誤: {e}")
                
                page.wait_for_timeout(500)

 


                log("🎉 Bet Limit 設定完成")
            def click_siteE_confirm(page):
                # 彈窗根節點（你 inspector 上看到的那個 section）
                dialog = page.locator("section.card.member-betlimit-dialog").first
                dialog.wait_for(state="visible", timeout=10000)

                # Confirm 就是 submit
                btn = dialog.locator('button[type="submit"]:has-text("Confirm")').first

                # 有些站會是大寫/有空白，補一個兜底：只用 type=submit
                if btn.count() == 0:
                    btn = dialog.locator('button[type="submit"]').first

                btn.wait_for(state="visible", timeout=10000)
                btn.scroll_into_view_if_needed()
                btn.click(force=True)
                log("🚀 已點擊 Confirm 送出設定！")

            if do_confirm:
                try:
                    log("🖱️ SiteE：準備點擊 Confirm（送出 Bet Limit）")
                    click_siteE_confirm(page)
                    log("✅ SiteE：已點 Confirm")
                    page.wait_for_timeout(800)  # 給它一點時間做提交/刷新
                except Exception as e:
                    log(f"❌ SiteE：Confirm 點擊失敗：{e}")
            else:
                log("⏭️ SiteE：已設定為不送出 Confirm（只勾選不提交）")


                        


        page.wait_for_timeout(10_000_000)  # debug用，讓瀏覽器保持開啟


        browser.close()


class SiteCApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        self.cfg = load_config()
        # ===== Platform =====
        self.platform_var = tk.StringVar(value="wp")  # wp=王牌, ldb=樂多寶

        platform_frame = ttk.LabelFrame(self, text="平台")
        platform_frame.pack(fill="x", padx=12, pady=(10, 0))

        ttk.Radiobutton(
            platform_frame, text="王牌",
            variable=self.platform_var, value="wp",
            command=self._on_platform_switch
        ).pack(side="left", padx=10, pady=4)

        ttk.Radiobutton(
            platform_frame, text="樂多寶",
            variable=self.platform_var, value="ldb",
            command=self._on_platform_switch
        ).pack(side="left", padx=10, pady=4)
        # ===== 商戶篩選 =====
        merchant_frame = ttk.LabelFrame(self, text="商戶篩選")
        merchant_frame.pack(fill="x", padx=12, pady=(10, 0))

        ttk.Label(merchant_frame, text="選擇商戶：").pack(side="left", padx=10, pady=4)

        self.merchant_var = tk.StringVar(value="請選取")
        self.merchant_combo = ttk.Combobox(
            merchant_frame, 
            textvariable=self.merchant_var,
            values=["請選取"],
            width=30
            # ← 不要 state="readonly"，這樣就可以輸入搜尋了
        )
        self.merchant_combo.pack(side="left", padx=10, pady=4)
        # ✅ 綁定即時搜尋過濾
        self.all_merchants = ["請選取"]  # 儲存完整商戶列表
        self.merchant_combo.bind('<KeyRelease>', self._filter_merchants)
        


        # ===== Notebook =====
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="x", padx=12, pady=10)

        self.tabs = {}
        self.site_names = ["WM", "歐博", "MT", "T9", "SA"]

        for site in self.site_names:
            frame = ttk.Frame(self.nb, padding=10)
            self.nb.add(frame, text=site)
            self.tabs[site] = frame

            self._build_site_tab(frame, site)

        # ===== buttons =====
        btnfrm = ttk.Frame(self, padding=(12, 0, 12, 8))
        btnfrm.pack(fill="x")



        self.btn_run = ttk.Button(btnfrm, text="執行目前分頁", command=self.on_run_current_tab)
        self.btn_run.pack(side="left")
        # ✅ 新增爬蟲按鈕
        self.btn_crawl = ttk.Button(btnfrm, text="爬取機器帳號", command=self.on_crawl_accounts)
        self.btn_crawl.pack(side="left", padx=8)

        self.var_headless = tk.BooleanVar(value=False)
        ttk.Checkbutton(btnfrm, text="幹您娘", variable=self.var_headless)\
            .pack(side="left", padx=12)

        self.btn_clear = ttk.Button(btnfrm, text="清空 Log", command=lambda: self.txt.delete("1.0", "end"))
        self.btn_clear.pack(side="left", padx=8)

        # ===== log =====
        self.txt = ScrolledText(self, height=18)
        self.txt.pack(fill="both", expand=True, padx=12, pady=8)

        self.log("🟦 每個分頁是一個站台，每個站台有自己的帳密（會記憶在 config_cache.json）。")
        self.running = set()  # 正在跑的站台集合

    def _get_platform_cfg(self):
        p = self.platform_var.get()  # "wp" or "ldb"
        if p not in self.cfg:
            self.cfg[p] = {}
        return p, self.cfg[p]
    
    def _filter_merchants(self, event):
        """即時過濾商戶列表（修正版）"""
        typed = self.merchant_var.get()
        
        # 如果按下 Enter，選中第一個結果（排除提示訊息）
        if event.keysym == 'Return':
            current_values = self.merchant_combo['values']
            if current_values and len(current_values) > 0:
                first = current_values[0]
                if not first.startswith("（"):  # 不是提示訊息
                    self.merchant_var.set(first)
                    self.merchant_combo.selection_clear()
            return
        
        # 如果按下 Escape，清空並恢復全部列表
        if event.keysym == 'Escape':
            self.merchant_var.set("全部")
            self.merchant_combo['values'] = self.all_merchants
            return
        
        # 如果清空了，恢復全部列表
        if not typed or typed == "全部":
            self.merchant_combo['values'] = self.all_merchants
            return
        
        # ✅ 修正：移除空格後搜尋，不區分大小寫
        typed_clean = typed.replace(" ", "").lower()
        
        # ✅ 過濾邏輯：移除商戶名稱的空格後比對
        filtered = []
        for merchant in self.all_merchants:
            if merchant == "全部":
                continue  # 跳過「全部」選項
            merchant_clean = merchant.replace(" ", "").lower()
            if typed_clean in merchant_clean:
                filtered.append(merchant)
        
        # 如果沒有結果，顯示提示
        if not filtered:
            filtered = ["（找不到符合的商戶）"]
        
        # ✅ Bug 修正：永遠保留「全部」在列表最前面
        if filtered[0] != "（找不到符合的商戶）":
            filtered = ["全部"] + filtered
        
        self.merchant_combo['values'] = filtered
    def _on_platform_switch(self):
        p, pcfg = self._get_platform_cfg()

        for site in self.site_names:
            v = self.tabs[site].vars
            site_cfg = pcfg.get(site, {})
            v["user"].set(site_cfg.get("username", ""))
            v["pass"].set(site_cfg.get("password", ""))

        self.log(f"🔁 已切換平台：{'王牌' if p=='wp' else '樂多寶'}（帳密已載入）")

    # -------------------------
    # 每個站台 tab 的 UI
    # -------------------------
    def _build_site_tab(self, parent, site: str):
        # 站台帳密（各自獨立）
        ttk.Label(parent, text=f"{site} 帳號").grid(row=0, column=0, sticky="w")
        p = getattr(self, "platform_var", tk.StringVar(value="wp")).get()
        var_user = tk.StringVar(value=self.cfg.get(p, {}).get(site, {}).get("username", ""))
        ent_user = ttk.Entry(parent, textvariable=var_user, width=30)
        ent_user.grid(row=0, column=1, padx=8, pady=4, sticky="w")

        ttk.Label(parent, text=f"{site} 密碼").grid(row=0, column=2, sticky="w")
        var_pass = tk.StringVar(value=self.cfg.get(p, {}).get(site, {}).get("password", ""))
        ent_pass = ttk.Entry(parent, textvariable=var_pass, show="*", width=30)
        ent_pass.grid(row=0, column=3, padx=8, pady=4, sticky="w")

        ttk.Separator(parent).grid(row=1, column=0, columnspan=4, sticky="ew", pady=10)

        # targets（每站都先放，之後你可改成該站特有欄位）
        ttk.Label(parent, text="targets (每行一個)").grid(row=2, column=0, sticky="nw")
        txt_targets = ScrolledText(parent, width=34, height=6)
        txt_targets.grid(row=2, column=1, padx=8, pady=4, sticky="w")

        # WM 有群組
        wm_vars = None
        if site == "WM":
            ttk.Label(parent, text="WM 群組").grid(row=3, column=0, sticky="w", pady=(6, 0))
            var_c = tk.BooleanVar(value=True)
            var_a = tk.BooleanVar(value=True)
            var_b = tk.BooleanVar(value=True)

            rowbox = ttk.Frame(parent)
            rowbox.grid(row=3, column=1, sticky="w", pady=(6, 0))
            ttk.Checkbutton(rowbox, text="群組 5K", variable=var_c).pack(side="left")
            ttk.Checkbutton(rowbox, text="群組 10K", variable=var_a).pack(side="left", padx=10)
            ttk.Checkbutton(rowbox, text="群組 20K", variable=var_b).pack(side="left")

            # ✅ 新增：Confirm 開關
            var_do_confirm = tk.BooleanVar(value=True)
            row_confirm = ttk.Frame(parent)
            row_confirm.grid(row=4, column=1, sticky="w", pady=(6, 0))
            ttk.Checkbutton(row_confirm, text="點 Confirm 送出設定", variable=var_do_confirm).pack(side="left")

            wm_vars = (var_a, var_b, var_c, var_do_confirm)

        # 把變數存起來，on_run 讀得到
        self.tabs[site].vars = {
            "user": var_user,
            "pass": var_pass,
            "targets": txt_targets,
            "wm_groups": wm_vars
        }


        if site == "歐博":
                    ttk.Label(parent, text="Handicap 選項").grid(row=3, column=0, sticky="nw", pady=(6, 0))
                    opt_b = ttk.Frame(parent)
                    opt_b.grid(row=3, column=1, columnspan=3, sticky="w", pady=(6, 0))

                    ttk.Label(opt_b, text="要勾選的 Handicap：").grid(row=0, column=0, sticky="w")
                    var_handicap = tk.StringVar(value="100_10K")
                    cb_handicap = ttk.Combobox(
                        opt_b, textvariable=var_handicap,
                        values=["100_5K", "100_10K", "100_20K"],
                        width=12, state="readonly"
                    )
                    cb_handicap.grid(row=0, column=1, padx=8, sticky="w")
                    self.tabs[site].vars["handicap_choice"] = var_handicap
                        # 1. 定義變數 (放在 self.vars 之類的地方)
                    self.site_b_do_submit = tk.BooleanVar(value=True) 

                    # 2. 建立 UI 組件 (放在你其他 Checkbutton 旁邊)
                    self.chk_b_submit = tk.Checkbutton(
                        parent, 
                        text="開啟 Site B 自動提交 (Submit)", 
                        variable=self.site_b_do_submit
                    )
                    self.chk_b_submit.grid(row=5, column=1, sticky="w", pady=(6, 0))



        if site == "MT":
            ttk.Label(parent, text="限紅組選項").grid(row=3, column=0, sticky="nw", pady=(6, 0))
            
            opt_mt = ttk.Frame(parent)
            opt_mt.grid(row=3, column=1, columnspan=3, sticky="w", pady=(6, 0))
            
            ttk.Label(opt_mt, text="要勾選的限紅組：").grid(row=0, column=0, sticky="w")
            var_mt_max = tk.StringVar(value="10000")
            cb_mt = ttk.Combobox(
                opt_mt, textvariable=var_mt_max,
                values=["10000", "20000", "5000"],
                width=12, state="readonly"
            )
            cb_mt.grid(row=0, column=1, padx=8, sticky="w")
            ttk.Label(opt_mt, text="(100-10,000 / 100-20,000 / 100-5,000)").grid(row=0, column=2, sticky="w")
            
            # 儲存開關
            var_mt_confirm = tk.BooleanVar(value=True)
            ttk.Checkbutton(opt_mt, text="點擊儲存送出設定", variable=var_mt_confirm)\
                .grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 0))
            
            self.tabs[site].vars["mt_max"] = var_mt_max
            self.tabs[site].vars["mt_confirm"] = var_mt_confirm


        if site == "T9":
            ttk.Label(parent, text="限紅設定").grid(row=3, column=0, sticky="nw", pady=(6, 0))
            
            opt_t9 = ttk.Frame(parent)
            opt_t9.grid(row=3, column=1, columnspan=3, sticky="w", pady=(6, 0))
            
            ttk.Label(opt_t9, text="最大限紅：").grid(row=0, column=0, sticky="w")
            var_t9_max = tk.StringVar(value="10000")
            cb_t9 = ttk.Combobox(
                opt_t9, textvariable=var_t9_max,
                values=["5000", "10000", "20000"],
                width=12, state="readonly"
            )
            cb_t9.grid(row=0, column=1, padx=8, sticky="w")
            ttk.Label(opt_t9, text="(5,000 / 10,000 / 20,000)").grid(row=0, column=2, sticky="w")
            
            # 儲存開關
            var_t9_confirm = tk.BooleanVar(value=True)
            ttk.Checkbutton(opt_t9, text="點擊「儲存為預設值」", variable=var_t9_confirm)\
                .grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 0))
            
            self.tabs[site].vars["t9_max"] = var_t9_max
            self.tabs[site].vars["t9_confirm"] = var_t9_confirm



        if site == "SA":
            ttk.Label(parent, text="Bet Limit 選項").grid(row=3, column=0, sticky="nw", pady=(6, 0))

            opt = ttk.Frame(parent)
            opt.grid(row=3, column=1, columnspan=3, sticky="w", pady=(6, 0))

            # 一般遊戲（Min=100）
            ttk.Label(opt, text="一般遊戲 Min=100 要勾 Max：").grid(row=0, column=0, sticky="w")
            var_normal_max = tk.StringVar(value="10000")  # ✅ 預設不變
            cb_normal = ttk.Combobox(
                opt, textvariable=var_normal_max,
                values=["10000", "20000", "5000"],  # 你要加 5000 就加進來
                width=10, state="readonly"
            )
            cb_normal.grid(row=0, column=1, padx=8, sticky="w")
            ttk.Label(opt, text="(10,000 / 20,000 / 5,000)").grid(row=0, column=2, sticky="w")
            # Deluxe Blackjack（Min=200）
            ttk.Label(opt, text="Deluxe Blackjack Min=200 要勾 Max：").grid(row=1, column=0, sticky="w", pady=(6, 0))
            var_deluxe_max = tk.StringVar(value="10000")  # ✅ 預設不變
            cb_deluxe = ttk.Combobox(
                opt, textvariable=var_deluxe_max,
                values=["10000", "20000", "5000"],  # 你要加 5000 就加進來
                width=10, state="readonly"
            )
            cb_deluxe.grid(row=1, column=1, padx=8, sticky="w", pady=(6, 0))
            ttk.Label(opt, text="(10,000 / 20,000)").grid(row=1, column=2, sticky="w", pady=(6, 0))

            # 存起來給 on_run 讀
            self.tabs[site].vars["normal_max"] = var_normal_max
            self.tabs[site].vars["deluxe_max"] = var_deluxe_max
            # ✅ SiteE Confirm 開關
            var_do_confirm_e = tk.BooleanVar(value=True)
            ttk.Checkbutton(opt, text="點 Confirm 送出設定", variable=var_do_confirm_e)\
                .grid(row=2, column=0, sticky="w", pady=(8, 0))

            self.tabs[site].vars["do_confirm_e"] = var_do_confirm_e




    # -------------------------
    # log
    # -------------------------
    def log(self, msg: str):
                from datetime import datetime
                ts = datetime.now().strftime("%H:%M:%S")
                self.txt.insert("end", f"[{ts}] {msg}\n")
                self.txt.see("end")
                self.update_idletasks()

    # -------------------------
    # 執行：依目前分頁跑對應站台
    # -------------------------
    def on_run_current_tab(self):
        headless = self.var_headless.get()

        current_tab = self.nb.select()
        site = self.nb.tab(current_tab, "text")  # WM / SiteB...

        v = self.tabs[site].vars
        username = v["user"].get().strip()
        password = v["pass"].get().strip()
        raw = v["targets"].get("1.0", "end").strip()
        targets = [x.strip() for x in raw.splitlines() if x.strip()]

        if not username or not password:
            messagebox.showerror("缺少資料", f"{site}：請輸入帳號/密碼")
            return
        

        # 先存帳密（每站各自記憶）
        p, pcfg = self._get_platform_cfg()
        pcfg[site] = {"username": username, "password": password}
        save_config(self.cfg)

        site = self.nb.tab(current_tab, "text")

        # if site in self.running:
        #     messagebox.showinfo("正在執行", f"{site} 已在執行中，避免重複啟動。")
        #     return

        # ✅ 不要再 disable 全域按鈕
        self.running.add(site)
        self.log(f"▶ 開始：站台={site} ...")

        def worker():
            try:
                if site == "WM":
                    var_a, var_b, var_c, var_do_confirm = v["wm_groups"]
                    process_a = var_a.get()
                    process_b = var_b.get()
                    process_c = var_c.get()
                    do_confirm = var_do_confirm.get()

                    if not (process_a or process_b or process_c):
                        raise RuntimeError("WM：請至少勾選一個群組")

                    platform = self.platform_var.get()
                    run_site_A(
                        platform, username, password, targets, headless, self.log,
                        process_a, process_b, process_c,
                        do_confirm=do_confirm
                    )

                elif site == "歐博":
                    platform = self.platform_var.get()
                    handicap_choice = v.get("handicap_choice")
                    handicap_choice = handicap_choice.get() if handicap_choice else "100_10K"
                    run_site_B(platform, username, password, targets, headless, self.log,
                               handicap_choice=handicap_choice, do_submit=self.site_b_do_submit.get())
                elif site == "MT":
                    platform = self.platform_var.get()
                    mt_max = v.get("mt_max").get() if "mt_max" in v else "10000"
                    mt_confirm = v.get("mt_confirm").get() if "mt_confirm" in v else True
                    run_site_C(platform, username, password, targets, headless, self.log,
                            normal_max=mt_max, deluxe_max="", do_confirm=mt_confirm)
                
                elif site == "T9":
                    platform = self.platform_var.get()
                    t9_max = v.get("t9_max").get() if "t9_max" in v else "10000"
                    t9_confirm = v.get("t9_confirm").get() if "t9_confirm" in v else True
                    run_site_D(platform, username, password, targets, headless, self.log,
                            normal_max=t9_max, deluxe_max="", do_confirm=t9_confirm)


                else:
                    if site == "SA":
                        normal_max = v["normal_max"].get()
                        deluxe_max = v["deluxe_max"].get()
                        do_confirm = v.get("do_confirm_e").get() if "do_confirm_e" in v else True
                        platform = self.platform_var.get()

                        run_site_E(platform, username, password, targets, headless, self.log,
                                normal_max, deluxe_max, do_confirm=do_confirm)

                  
                

                    else:
                        self.log(f"🟨 {site} 尚未實作：先只做 SA")


                self.log("✅ 流程結束。")

            except Exception as e:
                self.log("💥 發生錯誤：")
                self.log(str(e))
                self.log(traceback.format_exc())
                messagebox.showerror("執行失敗", str(e))
            finally:
                self.btn_run.config(state="normal")

        threading.Thread(target=worker, daemon=True).start()

    def on_crawl_accounts(self):
        """爬取所有機器帳號"""
        self.log("=" * 60)
        self.log("🕷️ 開始爬取機器帳號...")
        
        def worker():
            try:
                machines = crawl_all_machines(log_fn=self.log)
                
                if machines:
                    self.log("\n✅ 爬取完成！")
                    self.machines_data = machines  # 儲存結果
                    
                    # ✅ 提取所有商戶名稱並更新下拉選單
                    merchants = set()
                    for m in machines:
                        brand = m.get("商戶名稱", "")
                        if brand:
                            merchants.add(brand)
                    
                    merchant_list = ["請選取"] + sorted(list(merchants))
                    self.all_merchants = merchant_list  # ✅ 加上這一行！
                    self.merchant_combo['values'] = merchant_list
                    self.log(f"📋 發現 {len(merchants)} 個商戶")
                else:
                    self.log("⚠️ 沒有抓取到資料")
                    
            except Exception as e:
                self.log(f"❌ 爬取失敗: {e}")
                self.log(traceback.format_exc())
        
        threading.Thread(target=worker, daemon=True).start()

if __name__ == "__main__":
    SiteCApp().mainloop()