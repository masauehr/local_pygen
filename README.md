# local_pygen — ローカルLLM AIエージェントシステム

## 概要

ローカルLLM（Ollama）を活用して、Claude Codeに似たAIエージェント機能を実現するプロジェクト。
インターネット接続不要・プライバシー保護を重視しつつ、VS Code上でAI支援開発を行う。

## システム構成

```
VS Code
  └── Continue 拡張機能
        └── Ollama（ローカルLLMサーバー）
              └── 軽量モデル（例: codellama, qwen2.5-coder, deepseek-coder 等）
```

## 目的・ゴール

- Claude Code に近い「コード生成・編集・説明・デバッグ支援」をローカル環境で実現
- APIコスト・通信量ゼロで動作
- 軽量モデルでも効果的に使えるプロンプト設計・設定を探求
- カスタムエージェント・スラッシュコマンドの整備

## 技術スタック

| 要素 | 内容 |
|---|---|
| エディタ | VS Code |
| AI統合拡張 | [Continue](https://www.continue.dev/) |
| LLMランタイム | [Ollama](https://ollama.com/) |
| モデル候補 | `qwen2.5-coder`, `codellama`, `deepseek-coder`, `phi3` 等 |
| スクリプト | Python 3.x（自動化・補助スクリプト）|

## ディレクトリ構成

```
local_pygen/
├── README.md                       # このファイル
├── CLAUDE.md                       # Claude Code向け作業指示
├── .gitignore
├── config/
│   ├── config.json                 # Continue用設定テンプレート
│   └── README.md                   # 設定の詳細説明・適用手順
├── prompts/
│   ├── system_coder.md             # システムプロンプト（標準）
│   ├── system_lightweight.md       # システムプロンプト（軽量モデル向け）
│   ├── slash_debug.md              # /debug コマンド定義
│   └── slash_translate.md          # /translate コマンド定義
└── scripts/
    ├── check_ollama.py             # Ollama動作確認ツール
    └── ollama_chat.py              # CLIチャットクライアント
```

## セットアップ手順

### 1. Ollama のインストール

```bash
# macOS
brew install ollama

# サービス起動
ollama serve
```

### 2. モデルのダウンロード

```bash
# コーディング特化モデル（推奨）
ollama pull qwen2.5-coder:7b

# 軽量モデル（低スペックPC向け）
ollama pull qwen2.5-coder:3b
ollama pull phi3:mini
```

### 3. VS Code に Continue をインストール

VS Code 拡張機能マーケットプレイスから `Continue` を検索してインストール。

### 4. Continue の設定

`config/config.json` を `~/.continue/config.json` にコピーして使用。
→ 詳細は [config/README.md](config/README.md) を参照。

## 軽量モデル運用のポイント

- **コンテキスト長を絞る**: 不要な情報を含めない簡潔なプロンプト
- **タスクを細分化**: 一度に大きなタスクを渡さず、ステップごとに指示
- **モデル選定**: コーディングタスクには `qwen2.5-coder` 系が高性能
- **システムプロンプト最適化**: 軽量モデルに合わせた短くクリアな指示

## 参考リンク

- [Continue 公式ドキュメント](https://docs.continue.dev/)
- [Ollama モデル一覧](https://ollama.com/library)
- [Continue カスタムエージェント設定](https://docs.continue.dev/customize/overview)

## 状態

🔧 構築中
