import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import time
from typing import List, Tuple

from src.core.clicker import AutoClicker
from src.utils.csv_handler import export_positions_to_csv, parse_csv_positions
from src.utils.json_handler import export_positions_to_json, load_positions
from src.utils.config_handler import save_config, load_config
from src.version import VERSION

class AutoClickerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"Auto Clicker v{VERSION}")
        self.positions: List[Tuple[int, int]] = []
        self.clicker = AutoClicker(self.update_status)
        self.setup_gui()
        self.load_settings()

    def validate_number(self, P):
        """数字のみを許可するバリデーション関数"""
        if P == "":
            return True
        try:
            float(P)
            return True
        except ValueError:
            return False

    def adjust_value(self, entry, delta, is_count=True):
        """値を増減させる"""
        try:
            current = float(entry.get())
            if is_count:
                # クリック回数は整数で、最小値は1
                new_value = max(1, current + delta)
                entry.delete(0, tk.END)
                entry.insert(0, str(int(new_value)))
            else:
                # インターバルは小数点以下1桁まで、最小値は0.1
                new_value = max(0.1, current + delta)
                entry.delete(0, tk.END)
                entry.insert(0, f"{new_value:.1f}")
        except ValueError:
            pass

    def on_mousewheel(self, event, entry, is_count=True):
        """マウススクロールで値を増減"""
        delta = 1 if event.delta > 0 else -1
        if not is_count:
            delta *= 0.1
        self.adjust_value(entry, delta, is_count)

    def on_key_press(self, event, entry, is_count=True):
        """キー入力で値を増減"""
        if event.keysym == "Up":
            delta = 1 if is_count else 0.1
            self.adjust_value(entry, delta, is_count)
        elif event.keysym == "Down":
            delta = -1 if is_count else -0.1
            self.adjust_value(entry, delta, is_count)

    def setup_gui(self):
        # 数字のみを許可するバリデーション関数を登録
        vcmd = (self.root.register(self.validate_number), '%P')

        # クリック回数
        tk.Label(self.root, text="クリック回数:").grid(row=0, column=0, sticky="e")
        self.entry_count = tk.Entry(self.root, validate='key', validatecommand=vcmd)
        self.entry_count.grid(row=0, column=1)
        self.entry_count.bind("<MouseWheel>", lambda e: self.on_mousewheel(e, self.entry_count, True))
        self.entry_count.bind("<Key>", lambda e: self.on_key_press(e, self.entry_count, True))

        # インターバル
        tk.Label(self.root, text="インターバル（秒）:").grid(row=1, column=0, sticky="e")
        self.entry_interval = tk.Entry(self.root, validate='key', validatecommand=vcmd)
        self.entry_interval.grid(row=1, column=1)
        self.entry_interval.bind("<MouseWheel>", lambda e: self.on_mousewheel(e, self.entry_interval, False))
        self.entry_interval.bind("<Key>", lambda e: self.on_key_press(e, self.entry_interval, False))

        # 座標登録ボタン
        self.btn_record = tk.Button(
            self.root, text="現在のマウス位置を記録", command=self.record_position
        )
        self.btn_record.grid(row=2, column=0, columnspan=2, pady=5)

        # 座標一覧表示
        self.listbox = tk.Listbox(self.root, width=30)
        self.listbox.grid(row=3, column=0, columnspan=2)

        # 座標クリアボタン
        self.btn_clear = tk.Button(
            self.root, text="座標を全て削除", command=self.clear_positions
        )
        self.btn_clear.grid(row=4, column=0, columnspan=2, pady=5)

        # インポート/エクスポートボタン
        tk.Button(self.root, text="インポート", command=self.import_positions).grid(
            row=5, column=0, pady=(5, 0)
        )
        tk.Button(self.root, text="CSVエクスポート", command=self.export_positions_csv).grid(
            row=5, column=1, pady=(5, 0)
        )

        # オプション
        self.toggle_label = tk.Label(
            self.root,
            text="▼ オプション",
            font=("TkDefaultFont", 9),
            cursor="hand2",
        )
        self.toggle_label.bind("<Button-1>", lambda e: self.toggle_advanced())
        self.toggle_label.grid(row=6, column=1, columnspan=2, pady=(5, 0))

        # 隠す用フレーム
        self.advanced_frame = tk.Frame(self.root)
        self.json_export_btn = tk.Button(
            self.advanced_frame,
            text="JSONでエクスポート",
            command=self.export_positions_json
        )
        self.json_export_btn.pack(side="left", padx=5)

        # クリック開始ボタン
        self.btn_start = tk.Button(self.root, text="クリック開始", command=self.start_clicking)
        self.btn_start.grid(row=8, column=0, columnspan=2, pady=10)

        # ステータス表示
        self.status_var = tk.StringVar()
        self.status_var.set("待機中...")
        tk.Label(self.root, textvariable=self.status_var, fg="blue").grid(
            row=9, column=0, columnspan=2
        )

        # Escキーの注意表示
        tk.Label(
            self.root,
            text="※クリック中に Esc キーでキャンセル可能",
            fg="red"
        ).grid(row=10, column=0, columnspan=2, pady=(5, 10))

    def update_status(self, message: str):
        self.status_var.set(message)
        self.root.update()

    def record_position(self):
        self.update_status("3秒以内に記録したい位置にマウスを移動してください...")
        
        def delayed_capture():
            time.sleep(3)
            x, y = self.clicker.get_current_position()
            self.positions.append((x, y))
            self.update_position_list()
            self.save_positions()
            self.update_status(f"位置を記録しました: ({x}, {y})")

        threading.Thread(target=delayed_capture, daemon=True).start()

    def update_position_list(self):
        self.listbox.delete(0, tk.END)
        for i, (x, y) in enumerate(self.positions, 1):
            self.listbox.insert(tk.END, f"{i}: ({x}, {y})")

    def clear_positions(self):
        self.positions.clear()
        self.update_position_list()
        self.save_positions()
        self.update_status("すべての位置を削除しました。")

    def save_positions(self):
        """座標データをCSVファイルに保存します。"""
        export_positions_to_csv(self.positions, "positions.csv")

    def load_positions(self):
        """CSVファイルから座標データを読み込みます。"""
        try:
            self.positions = parse_csv_positions("positions.csv")
            self.update_position_list()
        except Exception as e:
            print(f"[警告] positions.csv の読み込みに失敗しました: {e}")
            # エラー時は空のリストで初期化
            self.positions = []
            self.update_position_list()
            # 空のファイルを作成
            export_positions_to_csv([], "positions.csv")

    def import_positions(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON or CSV files", "*.json *.csv")],
            title="座標データをインポート",
        )
        if not filepath:
            return

        try:
            ext = filepath.lower().endswith
            if ext(".json"):
                self.positions = load_positions(filepath)
            elif ext(".csv"):
                self.positions = parse_csv_positions(filepath)
            else:
                raise ValueError("サポートされていないファイル形式です")

            self.update_position_list()
            self.save_positions()
            self.update_status(f"座標をインポートしました: {filepath}")

        except Exception as e:
            self.update_status(f"インポート失敗: {e}")

    def export_positions_csv(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="CSVで座標データをエクスポート",
        )
        if not filepath:
            return

        try:
            export_positions_to_csv(self.positions, filepath)
            self.update_status(f"エクスポート成功: {filepath}")
        except Exception as e:
            self.update_status(f"エクスポート失敗: {e}")

    def export_positions_json(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="座標データをエクスポート",
        )
        if not filepath:
            return

        try:
            export_positions_to_json(self.positions, filepath)
            self.update_status(f"エクスポート成功: {filepath}")
        except Exception as e:
            self.update_status(f"エクスポート失敗: {e}")

    def toggle_advanced(self):
        if self.advanced_frame.winfo_ismapped():
            self.advanced_frame.grid_forget()
            self.toggle_label.config(text="▼ オプション")
        else:
            self.advanced_frame.grid(row=7, column=1, columnspan=2, padx=5, pady=5)
            self.toggle_label.config(text="▲ オプション")

    def load_settings(self):
        """設定を読み込みます。"""
        clicks, interval = load_config()
        self.entry_count.delete(0, tk.END)
        self.entry_count.insert(0, str(clicks))
        self.entry_interval.delete(0, tk.END)
        self.entry_interval.insert(0, str(interval))

    def start_clicking(self):
        try:
            count = int(self.entry_count.get())
            interval = float(self.entry_interval.get())
        except ValueError:
            messagebox.showerror("エラー", "回数とインターバルは数値で入力してください。")
            return

        if not self.positions:
            messagebox.showwarning("警告", "クリック位置が登録されていません。")
            return

        # 設定を保存
        save_config(count, interval)

        self.btn_start.config(state="disabled")
        self.update_status("クリック開始（Escでキャンセル）")

        def on_complete():
            self.btn_start.config(state="normal")

        threading.Thread(
            target=lambda: self.clicker.click_positions(
                self.positions, count, interval, on_complete
            ),
            daemon=True
        ).start()

    def run(self):
        self.load_positions()
        self.root.mainloop() 