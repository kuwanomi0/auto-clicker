import pyautogui
import keyboard
import time
import threading
from typing import List, Tuple, Callable

class AutoClicker:
    def __init__(self, status_callback: Callable[[str], None] = None):
        self.status_callback = status_callback or (lambda x: None)
        self._is_running = False
        self._should_cancel = False

    def click_positions(
        self,
        positions: List[Tuple[int, int]],
        count: int,
        interval: float,
        on_complete: Callable[[], None] = None
    ) -> None:
        """指定された位置を指定回数クリックします。"""
        self._is_running = True
        self._should_cancel = False

        def check_esc():
            while self._is_running:
                if keyboard.is_pressed("esc"):
                    self._should_cancel = True
                    self.status_callback("キャンセルされました。")
                    break
                time.sleep(0.1)

        cancel_thread = threading.Thread(target=check_esc, daemon=True)
        cancel_thread.start()

        try:
            for i in range(1, count + 1):
                if self._should_cancel:
                    break

                for x, y in positions:
                    if self._should_cancel:
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