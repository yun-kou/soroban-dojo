"""VOICEVOX から読み上げ用の音声パーツを作る。

使い方:
  python tools/make_voice.py --list                 # 話者IDの一覧
  python tools/make_voice.py --speaker 3 --pack zundamon

VOICEVOX（エンジン）を起動した状態で実行する。voice/<pack>/ に WAV と manifest.json を出力する。
数字は「千・百・十・一の位」と「万・億・兆」「円なり」のパーツをつないで読む。
"""
import argparse, json, os, sys, urllib.parse, urllib.request

ENGINE = "http://127.0.0.1:50021"
SPEEDS = {"n": 1.0, "f": 1.5}  # n=ふつう用, f=はやい用（アプリ側で近い方を選んで微調整）

D = ["", "いち", "に", "さん", "よん", "ご", "ろく", "なな", "はち", "きゅう"]
PARTS = {}
for i, s in enumerate(["せん", "にせん", "さんぜん", "よんせん", "ごせん", "ろくせん", "ななせん", "はっせん", "きゅうせん"], 1):
    PARTS[f"t{i}"] = s
for i, s in enumerate(["ひゃく", "にひゃく", "さんびゃく", "よんひゃく", "ごひゃく", "ろっぴゃく", "ななひゃく", "はっぴゃく", "きゅうひゃく"], 1):
    PARTS[f"h{i}"] = s
for i in range(1, 10):
    PARTS[f"j{i}"] = ("" if i == 1 else D[i]) + "じゅう"
    PARTS[f"o{i}"] = D[i]
    PARTS[f"man{i}"] = D[i] + "まん"
    PARTS[f"oku{i}"] = D[i] + "おく"
PARTS.update({"man0": "まん", "oku0": "おく", "cho0": "ちょう"})
for i, s in enumerate(["いっちょう", "にちょう", "さんちょう", "よんちょう", "ごちょう", "ろくちょう", "ななちょう", "はっちょう", "きゅうちょう"], 1):
    PARTS[f"cho{i}"] = s
for i, s in enumerate(["いちえんなり", "にえんなり", "さんえんなり", "よえんなり", "ごえんなり", "ろくえんなり", "ななえんなり", "はちえんなり", "きゅうえんなり"], 1):
    PARTS[f"en{i}"] = s
PARTS.update({"en0": "えんなり", "negai": "ねがいましては", "hiite": "ひいては", "kuwae": "くわえて", "dewa": "では"})


def call(path, params=None, body=None):
    url = ENGINE + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, data=body, method="POST" if body is not None or params else "GET",
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def synth(text, speaker, speed):
    q = json.loads(call("/audio_query", {"text": text, "speaker": speaker}, b""))
    q.update(speedScale=speed, prePhonemeLength=0.0, postPhonemeLength=0.02,
             outputSamplingRate=24000, outputStereo=False)
    return call("/synthesis", {"speaker": speaker}, json.dumps(q).encode())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--speaker", type=int)
    ap.add_argument("--pack")
    a = ap.parse_args()
    if a.list:
        for sp in json.loads(call("/speakers")):
            for st in sp["styles"]:
                print(st["id"], sp["name"], st["name"])
        return
    if a.speaker is None or not a.pack:
        sys.exit("--speaker と --pack を指定してください")
    out = os.path.join(os.path.dirname(__file__), "..", "voice", a.pack)
    os.makedirs(out, exist_ok=True)
    for sk, sv in SPEEDS.items():
        for key, text in PARTS.items():
            with open(os.path.join(out, f"{key}_{sk}.wav"), "wb") as f:
                f.write(synth(text, a.speaker, sv))
        print("speed", sk, "done")
    with open(os.path.join(out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"keys": list(PARTS), "speeds": SPEEDS}, f, ensure_ascii=False)
    print(len(PARTS) * len(SPEEDS), "files ->", os.path.abspath(out))


if __name__ == "__main__":
    main()
