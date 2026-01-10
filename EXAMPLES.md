# 使用例 / Usage Examples

## 基本的な使用方法 / Basic Usage

### 1. 環境設定 / Environment Setup

```bash
# .envファイルを作成
cp .env.example .env

# .envファイルを編集してAPIキーを設定
# Edit .env file and set your API key
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

### 2. PDFの要約 / Summarize PDF

```bash
# uvを使用する場合 / Using uv
uv run python summarize.py document.pdf

# または直接Pythonで / Or directly with Python
python summarize.py document.pdf
```

## カスタマイズ例 / Customization Examples

### 例1: 学術論文の要約 / Example 1: Academic Paper

**prompts/map_custom.txt**
```
各ページの内容を論文の構造（背景、方法、結果、考察）を意識して分析してください。
```

**prompts/reduce_custom.txt**
```
以下の形式で要約してください：

1. 研究の背景と目的
2. 使用した手法とデータ
3. 主要な発見と結果
4. 結論と今後の課題

具体的な数値やデータを含めてください。
```

### 例2: ビジネスレポートの要約 / Example 2: Business Report

**prompts/map_custom.txt**
```
各ページのビジネス上の重要な情報（売上、市場動向、戦略など）を特定してください。
```

**prompts/reduce_custom.txt**
```
エグゼクティブサマリーとして、以下を含めてください：

- 主要な発見
- ビジネス上の影響
- 推奨される行動
- リスクと機会

箇条書きで簡潔にまとめてください。
```

### 例3: 技術文書の要約 / Example 3: Technical Documentation

**prompts/map_custom.txt**
```
技術的な詳細（API、アーキテクチャ、実装方法など）を重点的に抽出してください。
```

**prompts/reduce_custom.txt**
```
技術者向けに、以下の情報を含めてください：

- システムアーキテクチャの概要
- 主要なコンポーネントと機能
- 実装の詳細
- 使用技術とツール
- 注意点と制約事項

コード例やコマンドがある場合は含めてください。
```

## プログラムからの使用 / Using from Python Code

```python
from summarize import PDFSummarizer

# サマライザーを初期化
summarizer = PDFSummarizer(
    model_name="gpt-4",  # より高品質な要約にはGPT-4を使用
    temperature=0.3
)

# PDFを要約
summary = summarizer.summarize("document.pdf")

# 結果を表示
print(summary)

# ファイルに保存
with open("summary.txt", "w", encoding="utf-8") as f:
    f.write(summary)
```

## 複数のPDFを一括処理 / Batch Process Multiple PDFs

```python
from pathlib import Path
from summarize import PDFSummarizer

# サマライザーを初期化
summarizer = PDFSummarizer()

# PDFディレクトリ内のすべてのPDFを処理
pdf_dir = Path("pdfs")
for pdf_file in pdf_dir.glob("*.pdf"):
    print(f"Processing: {pdf_file.name}")
    
    # 要約を生成
    summary = summarizer.summarize(str(pdf_file))
    
    # 結果を保存
    output_file = pdf_file.with_suffix(".txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(summary)
    
    print(f"Saved: {output_file.name}\n")
```

## Tips

### より詳細な要約が必要な場合
- `temperature`を低く設定（0.1-0.3）
- GPT-4を使用
- `reduce_custom.txt`で具体的な詳細を要求

### より簡潔な要約が必要な場合
- `reduce_custom.txt`で「簡潔に」「箇条書きで」などを指定
- 重要なポイントのみを要求

### 大きなPDFの処理
- ページ数が多い場合は処理に時間がかかります
- 必要に応じてページ範囲を指定する機能を追加できます

### コスト削減
- GPT-3.5-turbo を使用（デフォルト）
- 長いドキュメントの場合、最初に数ページでテスト
