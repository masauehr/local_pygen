# Continue 設定ガイド

## 概要

このディレクトリの `config.json` は、VS Code Continue拡張機能用の設定テンプレートです。
現在の Continue は `~/.continue/config.yaml` 形式で設定します。

## 適用方法

`config.json` を参考に `~/.continue/config.yaml` を編集してください。
設定はファイル保存で自動反映されます。

## 設定内容

### モデル構成

| タイトル | モデル | 用途 | コンテキスト長 |
|---|---|---|---|
| Qwen2.5 Coder 1.5B | `qwen2.5-coder:1.5b` | コーディング特化（メイン） | 4096 tokens |
| Phi4 Mini | `phi4-mini:latest` | 汎用・高性能 | 4096 tokens |
| Phi3 Mini | `phi3:mini` | 軽量フォールバック | 2048 tokens |
| Qwen2.5 1.5B | `qwen2.5:1.5b` | 汎用 | 4096 tokens |

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
