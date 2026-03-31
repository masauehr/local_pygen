#!/usr/bin/env python3
"""
Ollama チャットクライアント（CLIシンプル版）
- ターミナルからローカルLLMと対話できる
- ストリーミング出力対応
- 会話履歴を保持したマルチターン対話
"""

import json
import sys
import urllib.request
import urllib.error

OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5-coder:7b"

SYSTEM_PROMPT = (
    "あなたは優秀なプログラミングアシスタントです。"
    "コードの生成・説明・デバッグを行います。"
    "回答は日本語で行い、コードにはコメントを日本語で付けてください。"
    "簡潔かつ正確に答えてください。"
)


def stream_chat(model: str, messages: list[dict]) -> str:
    """
    チャット形式でストリーミング生成する。
    messages: [{"role": "user"/"assistant"/"system", "content": "..."}]
    戻り値: 生成されたテキスト全体
    """
    payload = json.dumps({
        "model": model,
        "messages": messages,
        "stream": True,
    }).encode()

    req = urllib.request.Request(
        f"{OLLAMA_BASE_URL}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    full_response = ""
    try:
        with urllib.request.urlopen(req, timeout=120) as res:
            for line in res:
                line = line.strip()
                if not line:
                    continue
                chunk = json.loads(line.decode())
                token = chunk.get("message", {}).get("content", "")
                if token:
                    print(token, end="", flush=True)
                    full_response += token
                if chunk.get("done"):
                    break
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"\nエラー {e.code}: {body}", file=sys.stderr)
    except urllib.error.URLError:
        print("\nOllamaサービスに接続できません。`ollama serve` を確認してください。", file=sys.stderr)

    print()  # 改行
    return full_response


def main():
    model = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL
    print(f"モデル: {model}")
    print("終了するには 'exit' または Ctrl+C を入力してください。\n")

    # 会話履歴（システムプロンプト込み）
    messages: list[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    while True:
        try:
            user_input = input("あなた: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n終了します。")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "終了"):
            print("終了します。")
            break

        messages.append({"role": "user", "content": user_input})

        print("AI: ", end="", flush=True)
        response = stream_chat(model, messages)

        if response:
            messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
