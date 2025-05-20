import tkinter as tk
from tkinter import messagebox
import pyautogui
import keyboard
import time
import threading

def start_clicking():
    try:
        count = int(entry_count.get())
        interval = float(entry_interval.get())
    except ValueError:
        messagebox.showerror("エラー", "回数とインターバルは数値で入力してください。")
        return

    btn_start.config(state="disabled")
    status_var.set("5秒以内にマウスを目的の位置へ移動してください...")
    root.update()
    time.sleep(5)
    x, y = pyautogui.position()
    status_var.set(f"座標取得: ({x}, {y}) - クリック開始中（Escで中止）")
    root.update()

    def click_task():
        for i in range(1, count + 1):
            if keyboard.is_pressed('esc'):
                status_var.set("キャンセルされました。")
                break
            pyautogui.click(x, y)
            status_var.set(f"{i}/{count}回クリック完了")
            root.update()
            time.sleep(interval)
        status_var.set("クリック完了。")
        btn_start.config(state="normal")

    threading.Thread(target=click_task, daemon=True).start()

# GUI セットアップ
root = tk.Tk()
root.title("Auto Clicker (Windows GUI)")

tk.Label(root, text="クリック回数：").grid(row=0, column=0, sticky="e")
entry_count = tk.Entry(root)
entry_count.insert(0, "10")
entry_count.grid(row=0, column=1)

tk.Label(root, text="インターバル（秒）：").grid(row=1, column=0, sticky="e")
entry_interval = tk.Entry(root)
entry_interval.insert(0, "1")
entry_interval.grid(row=1, column=1)

btn_start = tk.Button(root, text="開始", command=start_clicking)
btn_start.grid(row=2, column=0, columnspan=2, pady=10)

status_var = tk.StringVar()
status_var.set("待機中...")
status_label = tk.Label(root, textvariable=status_var, fg="blue")
status_label.grid(row=3, column=0, columnspan=2)

root.mainloop()
