#!/usr/bin/env python3
"""
Ollamaの動作確認スクリプト
- サービスの起動確認
- インストール済みモデルの一覧表示
- 簡単な疎通テスト
"""

import json
import sys
import urllib.request
import urllib.error

OLLAMA_BASE_URL = "http://localhost:11434"

# 推奨モデル一覧（実環境に合わせて更新）
RECOMMENDED_MODELS = [
    "qwen2.5-coder:1.5b",
    "phi4-mini:latest",
    "phi3:mini",
    "qwen2.5:1.5b",
]


def check_service() -> bool:
    """Ollamaサービスが起動しているか確認する"""
    try:
        req = urllib.request.Request(f"{OLLAMA_BASE_URL}/api/tags")
        with urllib.request.urlopen(req, timeout=3) as res:
            return res.status == 200
    except (urllib.error.URLError, OSError):
        return False


def get_installed_models() -> list[dict]:
    """インストール済みモデルの一覧を取得する"""
    try:
        req = urllib.request.Request(f"{OLLAMA_BASE_URL}/api/tags")
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read().decode())
            return data.get("models", [])
    except Exception as e:
        print(f"モデル一覧取得エラー: {e}")
        return []


def test_generate(model: str, prompt: str = "1+1=") -> str | None:
    """指定モデルで簡単な生成テストを行う"""
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 10,  # 最大10トークンのみ生成
        }
    }).encode()

    try:
        req = urllib.request.Request(
            f"{OLLAMA_BASE_URL}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as res:
            data = json.loads(res.read().decode())
            return data.get("response", "").strip()
    except urllib.error.HTTPError as e:
        return f"HTTPエラー {e.code}: {e.reason}"
    except Exception as e:
        return f"エラー: {e}"


def main():
    print("=" * 50)
    print("  Ollama 動作確認ツール")
    print("=" * 50)

    # 1. サービス起動確認
    print("\n[1] サービス確認...")
    if not check_service():
        print("  ✗ Ollamaサービスが起動していません。")
        print("  → `ollama serve` を実行してください。")
        sys.exit(1)
    print("  ✓ Ollamaサービス起動中")

    # 2. モデル一覧
    print("\n[2] インストール済みモデル:")
    models = get_installed_models()
    if not models:
        print("  （モデルなし）")
    else:
        for m in models:
            name = m.get("name", "不明")
            size_bytes = m.get("size", 0)
            size_gb = size_bytes / (1024 ** 3)
            print(f"  ・{name} ({size_gb:.1f} GB)")

    # 3. 推奨モデルの有無チェック
    print("\n[3] 推奨モデル確認:")
    installed_names = [m.get("name", "").lower() for m in models]
    available = []
    for rec in RECOMMENDED_MODELS:
        found = any(rec.lower() in name for name in installed_names)
        mark = "✓" if found else "✗"
        hint = "" if found else f"  → `ollama pull {rec}`"
        print(f"  {mark} {rec}{hint}")
        if found:
            available.append(rec)

    # 4. 疎通テスト（最初に見つかった推奨モデルで実施）
    if available:
        test_model = available[0]
        print(f"\n[4] 疎通テスト（{test_model}）...")
        result = test_generate(test_model)
        if result:
            print(f"  ✓ レスポンス取得成功: 「{result}」")
        else:
            print("  ✗ レスポンス取得失敗")
    else:
        print("\n[4] 疎通テストをスキップ（推奨モデル未インストール）")

    print("\n" + "=" * 50)
    print("確認完了")


if __name__ == "__main__":
    main()
