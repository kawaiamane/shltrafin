# シャルトラフ語 公式サイト / SHLTRAFIN

GitHub Pages用の複数ページサイト。翻訳機能なし。HTML/CSS/JSのみで閲覧でき、検索は `data/words.json` を参照します。

## ページ

- `index.html` ホーム
- `dictionary.html` サイト内単語検索（綴り・訳語・品詞・用例）
- `grammar.html` 章別文法解説
- `examples.html` ZpDICから同期された単語に付属する例文
- `about.html` 言語紹介

## GitHub Pages 公開

1. このZIPの**中身**をGitHubの公開リポジトリのルートにアップロード。`.github/workflows/sync.yml` も含めること。
2. Settings → Pages → Build and deployment → Deploy from a branch → `main` / `(root)` → Save。
3. `https://ユーザー名.github.io/リポジトリ名/` にアクセス。

## ZpDIC辞書データの同期

ZpDIC API v1は `X-Api-Key` が必要です。GitHub Pagesのブラウザ側コードにAPIキーを置いてはいけません。

1. **以前チャットに共有したAPIキーは失効・再発行**してください。
2. GitHubリポジトリの Settings → Secrets and variables → Actions → New repository secret。
3. Name: `ZPDIC_API_KEY`、Secret: **新しく再発行したキー**。
4. Actions → **Sync ZpDIC dictionary** → Run workflow を押す。
5. 正常に完了すると `data/words.json` が自動コミットされ、サイト内で単語検索できるようになります。毎日UTC 03:23に同期する設定です（GitHubのスケジュール実行には遅延や停止がありえます）。

GitHub Actionsがリポジトリにコミットできない場合、Settings → Actions → General → Workflow permissions を **Read and write permissions** にしてください。ブランチ保護ルールがある場合は別途調整が必要です。

### 注意

- **辞書が公開されていることを確認してください**。同期した単語データは公開GitHubリポジトリにコミットされ、誰でも取得できます。
- APIキーはZIP・HTML・JavaScript・JSON・コミット履歴に含めないでください。
- 初期の `data/words.json` は空です。初回の同期が完了するまで検索結果は表示されません。
- 単語の編集はZpDICで行い、次回同期で反映します。サイトからZpDICへの編集機能はありません。
- ZpDICの単語に付属する例文のみ同期します。独立した例文データは対象外です。
- `data/grammar.json` を編集してコミットすると文法ページの変更が保存・公開されます。`chapters` 配列に章を追加できます。`blocks` の種類は `paragraph`, `note`, `syntax`。
- 翻訳機能は実装していません。

## ローカル確認

`python -m http.server 8000` を実行して `http://localhost:8000` を開く。`file://` 直開きではJSONを読み込めないことがあります。

API仕様: https://zpdic.ziphil.com/api/v1

## 特殊フォント記法

本文、文法解説、例文、辞書データなどで `{shltrafin}` のように半角の `{}` で囲むと、囲まれた文字だけアップロードされた Metagraphy フォントで表示します。画面には `{}` 自体は表示されません。`data/grammar.json` でも利用できます。通常のテキストはそのまま表示します。

例: `これは {shltrafin} です。` → `shltrafin` の部分のみ専用フォント。

フォントファイルは `assets/Metagraphy-Regular.otf` に収録しています。
