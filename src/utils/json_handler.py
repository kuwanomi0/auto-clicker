import json
import os
from typing import List, Tuple

def load_positions(filepath: str) -> List[Tuple[int, int]]:
    """JSONファイルから座標データを読み込みます。"""
    try:
        with open(filepath, "r") as f:
            loaded = json.load(f)
            if not isinstance(loaded, list) or not all(
                isinstance(item, dict) and "x" in item and "y" in item
                for item in loaded
            ):
                raise ValueError("不正なフォーマット")
            return [(item["x"], item["y"]) for item in loaded]
    except Exception as e:
        raise ValueError(f"JSONファイルの読み込みに失敗しました: {e}")

def export_positions_to_json(positions: List[Tuple[int, int]], filepath: str) -> None:
    """座標データをJSONファイルにエクスポートします。"""
    # ディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump([{"x": x, "y": y} for x, y in positions], f, indent=2) 