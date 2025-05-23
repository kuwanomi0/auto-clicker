import json
import os
from typing import List, Tuple

def save_positions(positions: List[Tuple[int, int]], filepath: str = "positions.json") -> None:
    """座標データをJSONファイルに保存します。"""
    with open(filepath, "w") as f:
        json.dump([{"x": x, "y": y} for x, y in positions], f)

def load_positions(filepath: str = "positions.json") -> List[Tuple[int, int]]:
    """JSONファイルから座標データを読み込みます。"""
    try:
        # ファイルパスが空の場合は空のリストを返す
        if not filepath:
            print("[情報] 初期状態でpositions.jsonを再作成しました")
            save_positions([], "positions.json")
            return []

        # ファイルが存在しない場合は空のリストを返す
        if not os.path.exists(filepath):
            print("[情報] 初期状態でpositions.jsonを再作成しました")
            save_positions([], filepath)
            return []

        with open(filepath, "r") as f:
            loaded = json.load(f)
            if not isinstance(loaded, list) or not all(
                isinstance(item, dict) and "x" in item and "y" in item
                for item in loaded
            ):
                raise ValueError("不正なフォーマット")
            return [(item["x"], item["y"]) for item in loaded]
    except Exception as e:
        print(f"[警告] {filepath} の読み込みに失敗しました: {e}")
        # エラー時も初期状態として扱う
        print("[情報] 初期状態でpositions.jsonを再作成しました")
        save_positions([], "positions.json")
        return []

def export_positions_to_json(positions: List[Tuple[int, int]], filepath: str) -> None:
    """座標データをJSONファイルにエクスポートします。"""
    # ディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump([{"x": x, "y": y} for x, y in positions], f, indent=2) 