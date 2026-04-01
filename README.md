# local_pygen — ローカルLLM AIエージェントシステム

## 概要

ローカルLLM（Ollama）を活用して、Claude Codeに似たAIエージェント機能を実現するプロジェクト。
インターネット接続不要・プライバシー保護を重視しつつ、VS Code上でAI支援開発を行う。

## システム構成

```
VS Code
  └── Continue 拡張機能
        └── Ollama（ローカルLLMサーバー）
              └── 軽量モデル（例: qwen2.5, deepseek-coder 等）
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
| モデル | `qwen2.5:7b`（チャット）/ `deepseek-coder:1.3b`（補完） |
| スクリプト | Python 3.x（自動化・補助スクリプト）|

## ディレクトリ構成

```
local_pygen/
├── README.md                       # このファイル
├── CLAUDE.md                       # Claude Code向け作業指示
├── .gitignore
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
# チャット用メインモデル（推奨）
ollama pull qwen2.5:7b

# タブ補完専用
ollama pull deepseek-coder:1.3b
```

### 3. VS Code に Continue をインストール

VS Code 拡張機能マーケットプレイスから `Continue` を検索してインストール。

### 4. Continue の設定

`~/.continue/config.yaml` を編集して使用。設定はファイル保存で自動反映される。

## Continue 設定内容

### モデル構成

| モデル | 用途 | コンテキスト長 |
|---|---|---|
| `qwen2.5:7b` | **チャットメイン・推奨** | 8192 tokens |
| `deepseek-coder:1.3b` | **タブ補完専用**（チャット不可） | — |

### カスタムコマンド（`/` コマンド）

| コマンド | 機能 |
|---|---|
| `/explain` | 選択コードを日本語で説明 |
| `/fix` | バグ・エラーを修正 |
| `/review` | コードレビュー（品質・セキュリティ等） |
| `/test` | テストコードを生成 |
| `/docstring` | docstring（ドキュメントコメント）を追加 |
| `/refactor` | リファクタリング提案・実施 |
| `/commit` | gitコミットメッセージを生成 |
| `/proofread` | 文章添削 |

### コンテキストプロバイダー（`@` 参照）

| 参照 | 内容 |
|---|---|
| `@currentFile` | 現在開いているファイル全体 |
| `@file` | 任意のファイルをコンテキストに追加 |
| `@terminal` | ターミナルの最新出力 |
| `@problems` | VS Code の Problems パネルの内容 |

## モデル評価結果（MacBook Air メモリ8GB での実測）

| モデル | 評価 | 日本語対応 | 備考 |
|---|---|---|---|
| `qwen2.5:1.5b` | ❌ 性能不十分 | △ 不安定 | 指示への追従が弱い |
| `qwen2.5:3b` | ❌ 性能不十分 | △ 不安定 | ファイルの直接編集不可のため削除 |
| `qwen2.5-coder:1.5b` | ❌ 性能不十分 | △ 不安定 | チャットでJSON返却バグあり |
| `deepseek-coder:1.3b` | — | — | コード補完専用（タブ補完のみ） |
| `phi3:mini` | ❌ 性能不十分 | ❌ 困難 | 日本語指示を無視することが多い |
| `phi4-mini:latest` | ❌ 性能不十分 | ❌ 日本語不十分 | 英語タスクなら使用可能な場合あり |
| `qwen2.5:7b` | ✅ **実用レベルに近い** | ✅ 安定 | メモリ8GBでは動作が重いが実用可能。**推奨** |

> **結論:** MacBook Air メモリ8GB 環境では `qwen2.5:7b` が唯一の実用候補。
> 1.5B・3B クラスのモデルは性能・日本語対応ともに不十分。

## トラブルシューティング

**Ollama に接続できない場合**
```bash
ollama serve
ollama list
```

**モデルが遅い・重い場合**
- `contextLength` を小さくする（例: 4096）
- `maxPromptTokens` を減らす（例: 256）

**中国語が混入する場合（qwen系）**
- `systemMessage` に `Do NOT use Chinese in any part of your response.` を追加済み

## 参考リンク

- [Continue 公式ドキュメント](https://docs.continue.dev/)
- [Ollama モデル一覧](https://ollama.com/library)
- [Continue カスタムエージェント設定](https://docs.continue.dev/customize/overview)

## 状態

🔧 構築・検証中
