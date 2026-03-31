# CLAUDE.md — local_pygen プロジェクト作業指示

## プロジェクト概要

ローカルLLM（Ollama）+ Continue拡張 + VS Code を組み合わせた
Claude Code 類似のAIエージェントシステムの構築プロジェクト。

## 技術コンテキスト

- **LLMランタイム**: Ollama（ローカル動作、APIは `http://localhost:11434`）
- **VS Code 拡張**: Continue（設定ファイル: `~/.continue/config.json`）
- **対象モデル**: 軽量モデル（7B以下）を主に想定
- **スクリプト言語**: Python 3.x

## 作業上の注意事項

### Continue 設定ファイルの扱い
- `~/.continue/config.json` は実際の設定ファイル（パス確認必須）
- APIキーや認証情報を含む場合は `.gitignore` に追加すること
- 設定変更後は VS Code の再起動 or Continue の再読み込みが必要

### Ollama API
- ベースURL: `http://localhost:11434`
- モデル一覧確認: `ollama list`
- 動作確認: `ollama run <モデル名>`

### モデル選定の優先順位
1. `qwen2.5-coder:7b` — コーディング性能が高い（メモリ余裕がある場合）
2. `qwen2.5-coder:3b` — 低メモリ環境向け
3. `phi3:mini` — 超軽量フォールバック

## このプロジェクトで Claude Code がやること

- Continue の `config.json` 設定の調整・最適化
- カスタムスラッシュコマンド（`prompts/`）の作成・改善
- Ollama API を叩く Python スクリプトの作成
- 軽量モデル向けプロンプトエンジニアリングの試行

## やってはいけないこと

- `~/.continue/config.json` に含まれる認証情報をコードやコメントに転記しない
- Ollama のモデルファイル（`.gguf` 等）をこのリポジトリに含めない
