import csv
from typing import List, Tuple

def export_positions_to_csv(positions: List[Tuple[int, int]], filepath: str) -> None:
    """座標データをCSVファイルにエクスポートします。"""
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x", "y"])
        for x, y in positions:
            writer.writerow([x, y])

def parse_csv_positions(filepath: str) -> List[Tuple[int, int]]:
    """CSVファイルから座標データを読み込みます。"""
    with open(filepath, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if (
            header is None
            or len(header) < 2
            or header[0].lower() != "x"
            or header[1].lower() != "y"
        ):
            raise ValueError("CSVファイルのヘッダーが不正です（x,yが必要）")
        return [
            (int(float(row[0])), int(float(row[1]))) for row in reader if len(row) >= 2
        ] 