# そろばん読上げ道場

子ども向けのそろばん練習アプリ（PWA）。読上算・読上暗算・見取算を級別に練習できます。

- iPhone: Safari で開く → 共有ボタン → 「ホーム画面に追加」
- 記録はスマホの中に保存されます（設定画面からバックアップできます）
- 級ごとの桁数・口数は仮の値です。設定画面で変更できます

## 開発
- `index.html` アプリ本体 / `sw.js` オフライン対応 / `manifest.webmanifest` ホーム画面用設定
- `tools/make_icons.py` アイコン生成 / `tools/make_voice.py` VOICEVOX 音声パーツ生成
- ローカル確認: `python -m http.server 8765`
- 更新したら `sw.js` の `CACHE` の番号を上げる
