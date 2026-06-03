# 開発環境のセットアップ

## 必要な環境

- Python 3.8 以上（3.13未満）
- Poetry

## Poetry のインストール

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

## 依存関係のインストール

```powershell
poetry install
```

## アプリケーションの実行

### 方法1: poetry run コマンドを使用

```powershell
poetry run python -m src.main
```

または、用意されているバッチファイルを使用：

```powershell
.\run.bat
```

### 方法2: 仮想環境に入って実行

```powershell
poetry shell
python -m src.main
```

## ビルド

実行可能ファイル（.exe）を作成する場合：

```powershell
poetry run pyinstaller --noconfirm --onefile --windowed --name auto-clicker src/main.py
```

または、用意されているバッチファイルを使用：

```powershell
.\build.bat
```

ビルドされたファイルは `dist` フォルダに生成されます。

## プロジェクト構成

```txt
auto-clicker/
├── src/
│   ├── main.py           # エントリーポイント
│   ├── version.py        # バージョン情報
│   ├── core/
│   │   └── clicker.py    # クリック処理の実装
│   ├── gui/
│   │   └── app.py        # GUIの実装
│   └── utils/
│       ├── config_handler.py  # 設定ファイルの処理
│       ├── csv_handler.py     # CSV処理
│       └── json_handler.py    # JSON処理
├── build.bat             # ビルド用スクリプト
├── run.bat               # 実行用スクリプト
├── pyproject.toml        # Poetry設定ファイル
└── poetry.lock           # 依存関係のロックファイル
```

## よくある問題

### poetry コマンドが見つからない

PowerShell を再起動するか、PATH を再読み込みしてください：

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","User") + ";" + [System.Environment]::GetEnvironmentVariable("Path","Machine")
```

### Python バージョンの互換性

pyinstaller の制約により、Python 3.13 以降では動作しません。Python 3.8 から 3.12 の範囲を使用してください。
