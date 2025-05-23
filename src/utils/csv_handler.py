import csv
import os
from typing import List, Tuple

def export_positions_to_csv(positions: List[Tuple[int, int]], filepath: str) -> None:
    """座標データをCSVファイルにエクスポートします。"""
    # ファイルパスが空の場合は処理をスキップ
    if not filepath:
        return

    # ディレクトリが存在しない場合は作成
    dirname = os.path.dirname(filepath)
    if dirname:  # ディレクトリパスが存在する場合のみ作成
        os.makedirs(dirname, exist_ok=True)

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x", "y"])
        for x, y in positions:
            writer.writerow([x, y])

def parse_csv_positions(filepath: str) -> List[Tuple[int, int]]:
    """CSVファイルから座標データを読み込みます。"""
    # ファイルパスが空の場合は空のリストを返す
    if not filepath:
        print("[情報] 初期状態でpositions.csvを再作成しました")
        export_positions_to_csv([], "positions.csv")
        return []

    # ファイルが存在しない場合は空のリストを返す
    if not os.path.exists(filepath):
        print("[情報] 初期状態でpositions.csvを再作成しました")
        export_positions_to_csv([], filepath)
        return []

    try:
        with open(filepath, "r", newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if (
                header is None
                or len(header) < 2
                or header[0].lower() != "x"
                or header[1].lower() != "y"
            ):
                print("[警告] CSVファイルのヘッダーが不正です（x,yが必要）")
                export_positions_to_csv([], filepath)
                return []
            return [
                (int(float(row[0])), int(float(row[1]))) for row in reader if len(row) >= 2
            ]
    except Exception as e:
        print(f"[警告] {filepath} の読み込みに失敗しました: {e}")
        # エラー時も初期状態として扱う
        print("[情報] 初期状態でpositions.csvを再作成しました")
        export_positions_to_csv([], filepath)
        return [] 