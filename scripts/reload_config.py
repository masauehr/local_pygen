#!/usr/bin/env python3
"""
Continue設定リロードスクリプト
- memo.md (YAML) を読み込んで config.json を更新
- Continue拡張の設定を動的に変更
"""

import json
import os
import sys
import yaml

# パス設定
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
MEMO_FILE = os.path.join(PROJECT_ROOT, "memo.md")
CONFIG_FILE = os.path.join(PROJECT_ROOT, "config", "config.json")

# デフォルト設定
DEFAULT_CONTEXT_LENGTH = 4096
DEFAULT_SYSTEM_MESSAGE = (
    "あなたは優秀なプログラミングアシスタントです。"
    "コードの生成・説明・デバッグを行います。"
    "回答は日本語で行い、コードにはコメントを日本語で付けてください。"
    "簡潔かつ正確に答えてください。"
)


def load_memo_config() -> dict:
    """memo.md から設定を読み込む"""
    try:
        with open(MEMO_FILE, 'r', encoding='utf-8') as f:
            # YAML部分を抽出（# から始まるコメントをスキップ）
            content = f.read()
            # 最初の # で始まる行をスキップしてYAMLをパース
            lines = content.split('\n')
            yaml_lines = []
            in_yaml = False
            for line in lines:
                if line.strip().startswith('#'):
                    continue
                if line.strip() and not in_yaml:
                    in_yaml = True
                if in_yaml:
                    yaml_lines.append(line)
            yaml_content = '\n'.join(yaml_lines)
            return yaml.safe_load(yaml_content)
    except Exception as e:
        print(f"memo.md 読み込みエラー: {e}")
        return {}


def convert_to_continue_format(memo_config: dict) -> dict:
    """memo.md の設定を Continue config.json 形式に変換"""
    continue_config = {
        "models": [],
        "tabAutocompleteModel": {
            "title": "Autocomplete",
            "provider": "ollama",
            "model": "deepseek-coder:1.3b",
            "apiBase": "http://localhost:11434"
        },
        "tabAutocompleteOptions": {
            "useCopyBuffer": False,
            "maxPromptTokens": 512,
            "debounceDelay": 500
        },
        "customCommands": []
    }

    if 'models' in memo_config:
        for model in memo_config['models']:
            continue_model = {
                "title": model.get('name', model.get('model', 'Unknown Model')),
                "provider": model.get('provider', 'ollama'),
                "model": model.get('model', ''),
                "apiBase": "http://localhost:11434",
                "contextLength": DEFAULT_CONTEXT_LENGTH,
                "systemMessage": DEFAULT_SYSTEM_MESSAGE
            }
            continue_config["models"].append(continue_model)

    return continue_config


def save_config(config: dict):
    """config.json を保存"""
    try:
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"設定を保存しました: {CONFIG_FILE}")
    except Exception as e:
        print(f"設定保存エラー: {e}")
        sys.exit(1)


def main():
    """メイン処理"""
    print("Continue設定リロードを開始します...")

    # memo.md から設定読み込み
    memo_config = load_memo_config()
    if not memo_config:
        print("memo.md から設定を読み込めませんでした。")
        sys.exit(1)

    print(f"読み込んだ設定: {memo_config}")

    # Continue形式に変換
    continue_config = convert_to_continue_format(memo_config)

    # config.json 保存
    save_config(continue_config)

    print("設定更新完了！")
    print("VS Code で Continue 拡張機能をリロードしてください。")
    print("（コマンドパレットから 'Developer: Reload Window' を実行）")


if __name__ == "__main__":
    main()</content>
<parameter name="filePath">/Users/masahiro/projects/local_pygen/scripts/reload_config.py