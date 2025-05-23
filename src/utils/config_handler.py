import configparser
import os
from typing import Tuple

DEFAULT_CLICKS = 10
DEFAULT_INTERVAL = 1.0
CONFIG_FILENAME = "auto_clicker.ini"

def save_config(clicks: int, interval: float) -> None:
    """設定をiniファイルに保存します。"""
    config = configparser.ConfigParser()
    config["Settings"] = {
        "clicks": str(clicks),
        "interval": str(interval)
    }
    
    with open(CONFIG_FILENAME, "w") as f:
        config.write(f)

def load_config() -> Tuple[int, float]:
    """iniファイルから設定を読み込みます。"""
    if not os.path.exists(CONFIG_FILENAME):
        return DEFAULT_CLICKS, DEFAULT_INTERVAL
    
    config = configparser.ConfigParser()
    try:
        config.read(CONFIG_FILENAME)
        clicks = config.getint("Settings", "clicks", fallback=DEFAULT_CLICKS)
        interval = config.getfloat("Settings", "interval", fallback=DEFAULT_INTERVAL)
        return clicks, interval
    except Exception as e:
        print(f"[警告] 設定ファイルの読み込みに失敗しました: {e}")
        return DEFAULT_CLICKS, DEFAULT_INTERVAL 