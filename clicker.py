import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pyautogui
import keyboard
import threading
import time
import json
import os

POSITIONS_FILE = "positions.json"

# 座標リスト
positions = []


def save_positions():
    with open(POSITIONS_FILE, "w") as f:
        json.dump([{"x": x, "y": y} for x, y in positions], f)


def load_positions():
    if os.path.exists(POSITIONS_FILE):
        try:
            with open(POSITIONS_FILE, "r") as f:
                loaded = json.load(f)
                # 正しい形式でなければ例外にする
                if not isinstance(loaded, list) or not all(
                    isinstance(item, dict) and "x" in item and "y" in item
                    for item in loaded
                ):
                    raise ValueError("不正なフォーマット")

                positions.clear()
                positions.extend((item["x"], item["y"]) for item in loaded)
                return  # 成功したのでreturn
        except Exception as e:
            print(f"[警告] positions.json の読み込みに失敗しました: {e}")

    # 失敗した場合 → 空の状態でpositions.jsonを上書き
    positions.clear()
    save_positions()
    print("[情報] 初期状態でpositions.jsonを再作成しました")


def export_positions():
    filepath = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
        title="座標データをエクスポート",
    )
    if filepath:
        with open(filepath, "w") as f:
            json.dump([{"x": x, "y": y} for x, y in positions], f)
        status_var.set(f"座標をエクスポートしました: {filepath}")


def import_positions():
    filepath = filedialog.askopenfilename(
        filetypes=[("JSON files", "*.json")], title="座標データをインポート"
    )
    if filepath:
        try:
            with open(filepath, "r") as f:
                imported = json.load(f)
                positions.clear()
                positions.extend((item["x"], item["y"]) for item in imported)
                update_position_list()
                save_positions()
                status_var.set(f"座標をインポートしました: {filepath}")
        except Exception as e:
            status_var.set(f"インポート失敗: {e}")


def record_position():
    status_var.set("3秒以内に記録したい位置にマウスを移動してください...")
    root.update()

    def delayed_capture():
        time.sleep(3)
        x, y = pyautogui.position()
        positions.append((x, y))
        update_position_list()
        save_positions()
        status_var.set(f"位置を記録しました: ({x}, {y})")

    threading.Thread(target=delayed_capture, daemon=True).start()


def update_position_list():
    listbox.delete(0, tk.END)
    for i, (x, y) in enumerate(positions, 1):
        listbox.insert(tk.END, f"{i}: ({x}, {y})")


def clear_positions():
    positions.clear()
    update_position_list()
    save_positions()
    status_var.set("すべての位置を削除しました。")


def start_clicking():
    try:
        count = int(entry_count.get())
        interval = float(entry_interval.get())
    except ValueError:
        messagebox.showerror("エラー", "回数とインターバルは数値で入力してください。")
        return

    if not positions:
        messagebox.showwarning("警告", "クリック位置が登録されていません。")
        return

    btn_start.config(state="disabled")
    status_var.set("クリック開始（Escでキャンセル）")

    def click_task():
        for i in range(1, count + 1):
            if keyboard.is_pressed("esc"):
                status_var.set("キャンセルされました。")
                break
            for x, y in positions:
                if keyboard.is_pressed("esc"):
                    status_var.set("キャンセルされました。")
                    btn_start.config(state="normal")
                    return
                pyautogui.click(x, y)
                status_var.set(f"{i}回目: ({x}, {y}) クリック完了")
                root.update()
                time.sleep(interval)
        status_var.set("クリック完了。")
        btn_start.config(state="normal")

    threading.Thread(target=click_task, daemon=True).start()


# GUI セットアップ
root = tk.Tk()
root.title("多点Auto Clicker")

# クリック回数
tk.Label(root, text="クリック回数:").grid(row=0, column=0, sticky="e")
entry_count = tk.Entry(root)
entry_count.insert(0, "10")
entry_count.grid(row=0, column=1)

# インターバル
tk.Label(root, text="インターバル（秒）:").grid(row=1, column=0, sticky="e")
entry_interval = tk.Entry(root)
entry_interval.insert(0, "1")
entry_interval.grid(row=1, column=1)

# 座標登録ボタン
btn_record = tk.Button(root, text="現在のマウス位置を記録", command=record_position)
btn_record.grid(row=2, column=0, columnspan=2, pady=5)

# 座標一覧表示
listbox = tk.Listbox(root, width=30)
listbox.grid(row=3, column=0, columnspan=2)

# 座標クリアボタン
btn_clear = tk.Button(root, text="座標を全て削除", command=clear_positions)
btn_clear.grid(row=4, column=0, columnspan=2, pady=5)


tk.Button(root, text="インポート", command=import_positions).grid(
    row=5, column=0, pady=(5, 0)
)
tk.Button(root, text="エクスポート", command=export_positions).grid(
    row=5, column=1, pady=(5, 0)
)

# クリック開始ボタン
btn_start = tk.Button(root, text="クリック開始", command=start_clicking)
btn_start.grid(row=6, column=0, columnspan=2, pady=10)

# ステータス表示
status_var = tk.StringVar()
status_var.set("待機中...")
tk.Label(root, textvariable=status_var, fg="blue").grid(row=7, column=0, columnspan=2)

# Escキーの注意表示（常時表示）
tk.Label(root, text="※クリック中に Esc キーでキャンセル可能", fg="red").grid(
    row=8, column=0, columnspan=2, pady=(5, 10)
)

load_positions()
update_position_list()
root.mainloop()
