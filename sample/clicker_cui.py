import pyautogui
import time
import keyboard  # ← 新しく使うライブラリ

# クリック回数とインターバルを設定
click_count = 10       # 長めでも安心
interval = 10          # クリック間隔（秒）
wait_time = 5           # 座標取得までの待機時間（秒）

print(f"{wait_time}秒以内にマウスをクリックしたい場所へ移動してください...")
time.sleep(wait_time)

# 現在のマウス座標を取得
x, y = pyautogui.position()
print(f"座標を取得しました：({x}, {y})")
print(f"{click_count}回クリックを開始します。途中で止めるには Esc キーを押してください。")

# 指定回数クリック（Escキーでキャンセル可能）
for i in range(1, click_count + 1):
    if keyboard.is_pressed('esc'):
        print("キャンセルされました。")
        break
    pyautogui.click(x, y)
    print(f"{i}回目のクリック完了")
    time.sleep(interval)

print("クリック処理を終了しました。")
