# Continue 設定ガイド

## 概要

このディレクトリの `config.yaml` が、VS Code Continue拡張機能用の設定ファイルです。
実際の設定は `~/.continue/config.yaml` で管理します。

> ※ `config.json` は旧設定ファイル名。参考として保存していますが現在は非推奨です。

## 適用方法

`config.yaml` を参考に `~/.continue/config.yaml` を編集してください。
設定はファイル保存で自動反映されます。

## 設定内容

### モデル構成

| タイトル | モデル | 用途 | コンテキスト長 |
|---|---|---|---|
| Qwen2.5 7B | `qwen2.5:7b` | **チャットメイン・推奨** | 8192 tokens |
| Qwen2.5 3B | `qwen2.5:3b` | **チャットサブ** | 4096 tokens |
| Phi4 Mini | `phi4-mini:latest` | 汎用（参考） | 4096 tokens |
| Phi3 Mini | `phi3:mini` | 軽量（参考） | 4096 tokens |
| DeepSeek Coder 1.3B | `deepseek-coder:1.3b` | **タブ補完専用**（チャット不可） | — |

#### モデル評価結果（MacBook Air メモリ8GB での実測）

| モデル | 評価 | 日本語対応 |
|---|---|---|
| `qwen2.5:1.5b` | ❌ 性能不十分 | △ 不安定 |
| `qwen2.5:3b` | △ サブ利用可 | △ やや不安定 | ファイルの直接編集不可 |
| `qwen2.5-coder:1.5b` | ❌ 性能不十分 | △ 不安定 |
| `deepseek-coder:1.3b` | — コード補完専用 | — |
| `phi3:mini` | ❌ 性能不十分 | ❌ 困難 |
| `phi4-mini:latest` | ❌ 性能不十分 | ❌ 日本語不十分 |
| `qwen2.5:7b` | ✅ **実用レベルに近い** | ✅ 安定 |

> メモリ8GBでは `qwen2.5:7b` が動作は重いが唯一の実用候補。

### タブ補完

`qwen2.5-coder:1.5b` を使用（軽量・高速）。
デバウンス 500ms で過剰なAPI呼び出しを抑制。

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

### コンテキストプロバイダー（`@` 参照）

| 参照 | 内容 |
|---|---|
| `@file` | 任意のファイルをコンテキストに追加 |
| `@code` | 関数・クラスを名前で参照 |
| `@currentFile` | 現在開いているファイル全体 |
| `@terminal` | ターミナルの最新出力 |
| `@problems` | VS Code の Problems パネルの内容 |

## モデルの事前ダウンロード

```bash
# コーディング特化（メイン・タブ補完共用）
ollama pull qwen2.5-coder:1.5b

# 汎用・高性能
ollama pull phi4-mini:latest

# 軽量フォールバック
ollama pull phi3:mini

# 汎用
ollama pull qwen2.5:1.5b
```

## トラブルシューティング

**Ollama に接続できない場合**
```bash
# サービス起動確認
ollama serve

# 別ターミナルで動作確認
ollama list
```

**モデルが遅い・重い場合**
- `tabAutocompleteModel` を `qwen2.5-coder:3b` や `phi3:mini` に変更
- `contextLength` を小さくする（例: 2048）
- `maxPromptTokens` を減らす（例: 256）
