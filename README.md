# LLM Wiki

AI研究、AIエージェント、DX事例、開発標準化などの外部知識を収集・分類・要約し、テーマ別Wikiとして育てるためのプロジェクトです。

## 基本方針

このプロジェクトは、RAGのように毎回検索するだけではなく、集めた情報を構造化Markdownとして蓄積し、後から読み返せるWikiに育てることを目的とします。

最初は完全自動化ではなく、半自動化で運用します。

```text
収集
↓
分類
↓
raw note生成
↓
LLMで要約・論点抽出
↓
週次レビュー
↓
採用したものだけwikiへ反映
```

## ディレクトリ

- `00_inbox`: 未分類のURLや素材
- `01_topics`: テーマ別Wiki本体
- `02_crosscutting`: 複数テーマをまたぐ概念・比較・年表
- `03_outputs`: 週次ダイジェスト、記事種、ブリーフィング
- `04_templates`: Markdownテンプレート
- `05_prompts`: LLMに渡すプロンプト
- `06_scripts`: 収集・分類・ノート生成スクリプト
- `config`: テーマや情報源の設定
- `logs`: 実行ログ
- `99_archive`: 古い素材の退避

## 収集ルール

public repoとして運用するため、収集対象と保存粒度は `収集ルール.md` に従います。

## 初期運用

1. `00_inbox/urls/inbox.csv` にURLを追加する
2. `python 06_scripts/classify_items.py` でテーマ候補を付ける
3. `python 06_scripts/create_raw_notes.py` でraw noteを生成する
4. raw noteをLLMに読ませ、`05_prompts` のプロンプトで要約する
5. 人間がレビューして `01_topics/*/wiki` に昇格する

## 人生羅針盤との関係

LLM Wikiは外部知識を集める場所です。
人生羅針盤は、自分の判断、発信、プロダクトアイディアに昇格した知見を置く場所です。

