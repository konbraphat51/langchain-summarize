"""
LangChain Map-Reduce PDF Summarizer

このスクリプトはPDFファイルをmap-reduce方式で要約します：
- Map: PDFを指定された基準でセクションに分割
- Reduce: 各セクションを詳細に要約
"""

import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


class PDFSummarizer:
    """Map-Reduce方式でPDFを要約するクラス"""

    def __init__(
        self,
        openai_api_key: str = None,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.3,
    ):
        """
        初期化

        Args:
            openai_api_key: OpenAI APIキー（Noneの場合は環境変数から取得）
            model_name: 使用するOpenAIモデル
            temperature: 生成時の温度パラメータ
        """
        # 環境変数を読み込み
        load_dotenv()

        # APIキーの設定
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI APIキーが設定されていません。"
                "環境変数OPENAI_API_KEYまたは引数で指定してください。"
            )

        # LLMの初期化
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            openai_api_key=self.api_key,
        )

        # プロンプトディレクトリのパス
        self.prompts_dir = Path(__file__).parent / "prompts"

    def load_prompt(self, prompt_file: str) -> str:
        """
        プロンプトファイルを読み込む

        Args:
            prompt_file: プロンプトファイル名

        Returns:
            プロンプトの内容
        """
        prompt_path = self.prompts_dir / prompt_file
        if not prompt_path.exists():
            raise FileNotFoundError(f"プロンプトファイルが見つかりません: {prompt_path}")

        with open(prompt_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # コメント行を除外
        lines = [line for line in content.split("\n") if not line.strip().startswith("#")]
        return "\n".join(lines).strip()

    def create_map_prompt(self) -> PromptTemplate:
        """
        Mapステップ用のプロンプトを作成

        Returns:
            Map用プロンプトテンプレート
        """
        base_prompt = self.load_prompt("map_base.txt")
        custom_prompt = self.load_prompt("map_custom.txt")

        # カスタムプロンプトが空でない場合は結合
        if custom_prompt:
            full_prompt = f"{base_prompt}\n\n追加要件：\n{custom_prompt}\n\n{{text}}"
        else:
            full_prompt = f"{base_prompt}\n\n{{text}}"

        return PromptTemplate(template=full_prompt, input_variables=["text"])

    def create_reduce_prompt(self) -> PromptTemplate:
        """
        Reduceステップ用のプロンプトを作成

        Returns:
            Reduce用プロンプトテンプレート
        """
        base_prompt = self.load_prompt("reduce_base.txt")
        custom_prompt = self.load_prompt("reduce_custom.txt")

        # カスタムプロンプトが空でない場合は結合
        if custom_prompt:
            full_prompt = f"{base_prompt}\n\n追加要件：\n{custom_prompt}\n\n{{text}}"
        else:
            full_prompt = f"{base_prompt}\n\n{{text}}"

        return PromptTemplate(template=full_prompt, input_variables=["text"])

    def load_pdf(self, pdf_path: str) -> List[Document]:
        """
        PDFファイルを読み込む

        Args:
            pdf_path: PDFファイルのパス

        Returns:
            ドキュメントのリスト
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDFファイルが見つかりません: {pdf_path}")

        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        if not documents:
            raise ValueError("PDFから内容を読み込めませんでした")

        return documents

    def summarize(self, pdf_path: str) -> str:
        """
        PDFファイルを要約する

        Args:
            pdf_path: PDFファイルのパス

        Returns:
            要約テキスト
        """
        # PDFを読み込み
        print(f"PDFを読み込んでいます: {pdf_path}")
        documents = self.load_pdf(pdf_path)
        print(f"読み込み完了: {len(documents)}ページ")

        # プロンプトを作成
        map_prompt = self.create_map_prompt()
        reduce_prompt = self.create_reduce_prompt()

        # Map-Reduceチェーンを作成
        chain = load_summarize_chain(
            llm=self.llm,
            chain_type="map_reduce",
            map_prompt=map_prompt,
            combine_prompt=reduce_prompt,
            verbose=True,
        )

        # 要約を実行
        print("\n要約を実行中...")
        result = chain.invoke({"input_documents": documents})

        return result["output_text"]


def main():
    """メイン関数"""
    import sys

    if len(sys.argv) < 2:
        print("使用方法: python summarize.py <PDFファイルのパス>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    try:
        # サマライザーを初期化
        summarizer = PDFSummarizer()

        # PDFを要約
        summary = summarizer.summarize(pdf_path)

        # 結果を表示
        print("\n" + "=" * 80)
        print("要約結果")
        print("=" * 80)
        print(summary)
        print("=" * 80)

        # 結果をファイルに保存
        output_path = pdf_path.replace(".pdf", "_summary.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"\n要約を保存しました: {output_path}")

    except Exception as e:
        print(f"エラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
