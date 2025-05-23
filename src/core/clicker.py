import pyautogui
import keyboard
import time
from typing import List, Tuple, Callable

class AutoClicker:
    def __init__(self, status_callback: Callable[[str], None] = None):
        self.status_callback = status_callback or (lambda x: None)
        self._is_running = False

    def click_positions(
        self,
        positions: List[Tuple[int, int]],
        count: int,
        interval: float,
        on_complete: Callable[[], None] = None
    ) -> None:
        """指定された位置を指定回数クリックします。"""
        self._is_running = True
        try:
            for i in range(1, count + 1):
                if keyboard.is_pressed("esc"):
                    self.status_callback("キャンセルされました。")
                    break

                for x, y in positions:
                    if keyboard.is_pressed("esc"):
                        self.status_callback("キャンセルされました。")
                        return
                    pyautogui.click(x, y)
                    self.status_callback(f"{i}回目: ({x}, {y}) クリック完了")
                    time.sleep(interval)

            self.status_callback("クリック完了。")
        finally:
            self._is_running = False
            if on_complete:
                on_complete()

    def is_running(self) -> bool:
        """クリッカーが実行中かどうかを返します。"""
        return self._is_running

    def get_current_position(self) -> Tuple[int, int]:
        """現在のマウス位置を取得します。"""
        return pyautogui.position() 