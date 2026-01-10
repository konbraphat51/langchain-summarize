# LangChain PDF Summarizer (Map-Reduce)

PDFファイルをLangChainのMap-Reduce方式で詳細に要約するツールです。

## 特徴

- **Map-Reduce要約**: PDFを複数のセクションに分割し、各セクションを詳細に要約
- **カスタマイズ可能なプロンプト**: 分割方法と要約方法をそれぞれカスタマイズ可能
- **LangChain v2対応**: 最新のLangChainアーキテクチャを使用
- **OpenAI統合**: GPTモデルによる高品質な要約

## 要件

- Python 3.9以上
- uv（パッケージ管理）
- OpenAI APIキー

## インストール

### 1. リポジトリをクローン

```bash
git clone https://github.com/konbraphat51/langchain-summarize.git
cd langchain-summarize
```

### 2. uvのインストール

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. 依存関係のインストール

```bash
uv sync
```

### 4. 環境変数の設定

`.env.example`を`.env`にコピーして、OpenAI APIキーを設定：

```bash
cp .env.example .env
```

`.env`ファイルを編集：

```
OPENAI_API_KEY=your_actual_api_key_here
```

## 使い方

### 基本的な使用方法

```bash
uv run python summarize.py path/to/your/document.pdf
```

要約結果は以下の2箇所に出力されます：
- コンソール（標準出力）
- `document_summary.txt`（PDFと同じディレクトリ）

### プロンプトのカスタマイズ

要約の動作をカスタマイズするには、`prompts/`ディレクトリ内のファイルを編集します：

#### Map（分割）のカスタマイズ

`prompts/map_custom.txt`を編集して、PDFをどのように区分するかを指定：

```
# 例：5ページごとに区切る
ドキュメントを5ページごとのセクションに分割してください。

# 例：特定のトピックで区切る
「はじめに」「方法」「結果」「考察」のセクションに分割してください。
```

#### Reduce（要約）のカスタマイズ

`prompts/reduce_custom.txt`を編集して、要約の形式や重点を指定：

```
# 例：箇条書き形式
各セクションを以下の形式で箇条書きにまとめてください：
- 主要なポイント
- 重要な詳細
- キーとなる結論

# 例：技術文書向け
技術的な詳細、使用された手法、具体的な数値データを重視して要約してください。
```

## プロンプトファイル構成

```
prompts/
├── map_base.txt       # Map処理の基本プロンプト
├── map_custom.txt     # Map処理のカスタム要件
├── reduce_base.txt    # Reduce処理の基本プロンプト
└── reduce_custom.txt  # Reduce処理のカスタム要件
```

- **base.txt**: 基本的な動作を定義（通常は変更不要）
- **custom.txt**: プロジェクトや用途に応じてカスタマイズ

## Map-Reduceアプローチについて

このツールは以下の2段階で要約を行います：

### Map段階
1. PDFを論理的なセクション（チャンク）に分割
2. 各セクションを個別に処理
3. `map_base.txt`と`map_custom.txt`のプロンプトを使用

### Reduce段階
1. Map段階で作成された各セクションの要約を受け取る
2. 全体を統合して詳細な最終要約を生成
3. `reduce_base.txt`と`reduce_custom.txt`のプロンプトを使用

このアプローチにより、長いPDFでも各セクションの詳細を保持しながら要約できます。

## 例

### 学術論文の要約

```bash
# prompts/reduce_custom.txt に以下を追加
研究の目的、手法、主要な発見、結論を明確に区別して要約してください。
統計的な結果や実験データを含めてください。

# 実行
uv run python summarize.py research_paper.pdf
```

### ビジネスレポートの要約

```bash
# prompts/reduce_custom.txt に以下を追加
ビジネス上の影響、推奨事項、重要な数値指標を強調してください。
エグゼクティブサマリーとして使用できる形式で要約してください。

# 実行
uv run python summarize.py business_report.pdf
```

## トラブルシューティング

### OpenAI APIキーエラー
- `.env`ファイルが正しく設定されているか確認
- APIキーが有効か確認

### PDFが読み込めない
- PDFファイルのパスが正しいか確認
- PDFが破損していないか確認
- テキスト抽出可能なPDFか確認（スキャン画像のみのPDFは未対応）

### メモリ不足
- 非常に大きなPDFの場合、GPT-4よりGPT-3.5-turboを使用
- `summarize.py`内の`model_name`を変更

## ライセンス

MITライセンス

## 貢献

プルリクエストを歓迎します！

## 作者

konbraphat51
