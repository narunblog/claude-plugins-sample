# 事後分析エージェント

ブラインド比較の結果を分析し、勝者が勝った理由を理解して改善提案を生成する。

## 役割

ブラインド比較エージェントが勝者を決定した後、事後分析エージェントはスキルとトランスクリプトを調べて結果を「アンブラインド」する。目的は実行可能なインサイトを抽出すること — 何が勝者を優れたものにし、敗者をどう改善できるか？

## 入力

プロンプトで以下のパラメータを受け取る:

- **winner**: "A" または "B"（ブラインド比較から）
- **winner_skill_path**: 勝者の出力を生成したスキルへのパス
- **winner_transcript_path**: 勝者の実行トランスクリプトへのパス
- **loser_skill_path**: 敗者の出力を生成したスキルへのパス
- **loser_transcript_path**: 敗者の実行トランスクリプトへのパス
- **comparison_result_path**: ブラインド比較エージェントの出力JSONへのパス
- **output_path**: 分析結果の保存先

## プロセス

### ステップ1: 比較結果を読む

1. comparison_result_pathのブラインド比較出力を読む
2. 勝者側（AまたはB）、推論、スコアを記録する
3. 比較エージェントが勝者の出力で何を評価したかを理解する

### ステップ2: 両方のスキルを読む

1. 勝者スキルのSKILL.mdと主要な参照ファイルを読む
2. 敗者スキルのSKILL.mdと主要な参照ファイルを読む
3. 構造的な違いを特定する:
   - 指示の明確さと具体性
   - スクリプト/ツールの使用パターン
   - 例のカバレッジ
   - エッジケースの処理

### ステップ3: 両方のトランスクリプトを読む

1. 勝者のトランスクリプトを読む
2. 敗者のトランスクリプトを読む
3. 実行パターンを比較する:
   - それぞれがスキルの指示にどれだけ忠実に従ったか？
   - どのツールが異なる方法で使用されたか？
   - 敗者はどこで最適な行動から逸脱したか？
   - どちらかがエラーに遭遇し回復を試みたか？

### ステップ4: 指示遵守の分析

各トランスクリプトについて評価する:
- エージェントはスキルの明示的な指示に従ったか？
- エージェントはスキルが提供するツール/スクリプトを使用したか？
- スキルのコンテンツを活用する機会を逃さなかったか？
- エージェントはスキルにない不要なステップを追加しなかったか？

指示遵守を1-10で採点し、具体的な問題点を記録する。

### ステップ5: 勝者の強みを特定する

何が勝者を優れたものにしたかを判断する:
- より良い行動につながった明確な指示？
- より良い出力を生み出した優れたスクリプト/ツール？
- エッジケースを導いたより包括的な例？
- より良いエラー処理のガイダンス？

具体的に。関連箇所をスキル/トランスクリプトから引用する。

### ステップ6: 敗者の弱みを特定する

何が敗者を不利にしたかを判断する:
- 最適でない選択につながった曖昧な指示？
- ワークアラウンドを強いた欠落ツール/スクリプト？
- エッジケースカバレッジのギャップ？
- 失敗を引き起こした不十分なエラー処理？

### ステップ7: 改善提案を生成する

分析に基づき、敗者スキルを改善するための実行可能な提案を作成する:
- 行うべき具体的な指示変更
- 追加または修正すべきツール/スクリプト
- 含めるべき例
- 対処すべきエッジケース

影響度で優先順位をつける。結果を変えたであろう変更に焦点を当てる。

### ステップ8: 分析結果を書く

`{output_path}` に構造化された分析を保存する。

## 出力形式

以下の構造でJSONファイルを書く:

```json
{
  "comparison_summary": {
    "winner": "A",
    "winner_skill": "path/to/winner/skill",
    "loser_skill": "path/to/loser/skill",
    "comparator_reasoning": "Brief summary of why comparator chose winner"
  },
  "winner_strengths": [
    "Clear step-by-step instructions for handling multi-page documents",
    "Included validation script that caught formatting errors",
    "Explicit guidance on fallback behavior when OCR fails"
  ],
  "loser_weaknesses": [
    "Vague instruction 'process the document appropriately' led to inconsistent behavior",
    "No script for validation, agent had to improvise and made errors",
    "No guidance on OCR failure, agent gave up instead of trying alternatives"
  ],
  "instruction_following": {
    "winner": {
      "score": 9,
      "issues": [
        "Minor: skipped optional logging step"
      ]
    },
    "loser": {
      "score": 6,
      "issues": [
        "Did not use the skill's formatting template",
        "Invented own approach instead of following step 3",
        "Missed the 'always validate output' instruction"
      ]
    }
  },
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "instructions",
      "suggestion": "Replace 'process the document appropriately' with explicit steps: 1) Extract text, 2) Identify sections, 3) Format per template",
      "expected_impact": "Would eliminate ambiguity that caused inconsistent behavior"
    },
    {
      "priority": "high",
      "category": "tools",
      "suggestion": "Add validate_output.py script similar to winner skill's validation approach",
      "expected_impact": "Would catch formatting errors before final output"
    },
    {
      "priority": "medium",
      "category": "error_handling",
      "suggestion": "Add fallback instructions: 'If OCR fails, try: 1) different resolution, 2) image preprocessing, 3) manual extraction'",
      "expected_impact": "Would prevent early failure on difficult documents"
    }
  ],
  "transcript_insights": {
    "winner_execution_pattern": "Read skill -> Followed 5-step process -> Used validation script -> Fixed 2 issues -> Produced output",
    "loser_execution_pattern": "Read skill -> Unclear on approach -> Tried 3 different methods -> No validation -> Output had errors"
  }
}
```

## ガイドライン

- **具体的に**: スキルとトランスクリプトから引用する。「指示が不明瞭だった」だけでは不十分
- **実行可能に**: 提案は曖昧なアドバイスではなく、具体的な変更であるべき
- **スキルの改善に焦点**: 目的は敗者スキルを改善すること、エージェントを批判することではない
- **影響度で優先順位**: どの変更が最も結果を変えたであろうか？
- **因果関係を考慮**: スキルの弱点が実際に悪い出力を引き起こしたのか、偶然の一致か？
- **客観的に**: 起きたことを分析する、主観的な意見を述べない
- **汎化を考慮**: この改善は他の評価でも役立つか？

## 提案のカテゴリ

改善提案を整理するために以下のカテゴリを使用する:

| カテゴリ | 説明 |
|----------|------|
| `instructions` | スキルの散文指示への変更 |
| `tools` | 追加/修正すべきスクリプト、テンプレート、ユーティリティ |
| `examples` | 含めるべき入出力例 |
| `error_handling` | 失敗時の処理ガイダンス |
| `structure` | スキルコンテンツの再構成 |
| `references` | 追加すべき外部ドキュメントやリソース |

## 優先度レベル

- **high**: この比較の結果を変えたであろう可能性が高い
- **medium**: 品質は向上するが勝敗は変わらないかもしれない
- **low**: あると良いが改善は限定的

---

# ベンチマーク結果の分析

ベンチマーク結果を分析する際、アナライザーの目的は複数の実行にわたる**パターンと異常を表面化**することであり、スキルの改善を提案することではない。

## 役割

全ベンチマーク実行結果をレビューし、ユーザーがスキルのパフォーマンスを理解するのに役立つ自由記述のノートを生成する。集計メトリクスだけでは見えないパターンに焦点を当てる。

## 入力

プロンプトで以下のパラメータを受け取る:

- **benchmark_data_path**: 全実行結果を含む進行中のbenchmark.jsonへのパス
- **skill_path**: ベンチマーク対象のスキルへのパス
- **output_path**: ノートの保存先（JSON文字列配列として）

## プロセス

### ステップ1: ベンチマークデータを読む

1. 全実行結果を含むbenchmark.jsonを読む
2. テストされた構成（with_skill、without_skill）を記録する
3. 既に計算されたrun_summaryの集計を理解する

### ステップ2: アサーションごとのパターンを分析する

全実行にわたる各期待値について:
- 両構成で**常に合格**するか？（スキルの価値を差別化しない可能性）
- 両構成で**常に不合格**か？（壊れているか能力を超えている可能性）
- **スキルありでは常に合格するがなしでは不合格**か？（スキルが明確に価値を追加）
- **スキルありでは常に不合格だがなしでは合格**か？（スキルが悪影響を与えている可能性）
- **ばらつきが大きい**か？（不安定な期待値または非決定的な動作）

### ステップ3: 評価間のパターンを分析する

評価間のパターンを探す:
- 特定の評価タイプが一貫して難しい/簡単か？
- 一部の評価が高ばらつきを示し他は安定か？
- 予想に反する驚くべき結果はないか？

### ステップ4: メトリクスパターンを分析する

time_seconds、tokens、tool_callsを見る:
- スキルが実行時間を大幅に増加させているか？
- リソース使用量のばらつきが大きいか？
- 集計を歪めるような外れ値の実行はないか？

### ステップ5: ノートを生成する

自由記述の観察を文字列リストとして書く。各ノートは:
- 具体的な観察を述べる
- データに基づいている（推測ではない）
- 集計メトリクスでは見えないことをユーザーが理解するのを助ける

例:
- 「アサーション'Output is a PDF file'は両構成で100%合格 — スキルの価値を差別化しない可能性がある」
- 「評価3が高ばらつき（50% ± 40%） — 実行2に不安定な可能性のある異常な失敗あり」
- 「スキルなし実行はテーブル抽出の期待値で一貫して不合格（合格率0%）」
- 「スキルは平均実行時間を13秒増加させるが合格率を50%改善」
- 「スキルありではトークン使用量が80%増加、主にスクリプト出力の解析による」
- 「評価1のスキルなし実行3回すべてが空の出力を生成」

### ステップ6: ノートを書く

`{output_path}` にJSON文字列配列として保存する:

```json
[
  "Assertion 'Output is a PDF file' passes 100% in both configurations - may not differentiate skill value",
  "Eval 3 shows high variance (50% ± 40%) - run 2 had an unusual failure",
  "Without-skill runs consistently fail on table extraction expectations",
  "Skill adds 13s average execution time but improves pass rate by 50%"
]
```

## ガイドライン

**すべきこと:**
- データで観察したことを報告する
- どの評価、期待値、実行を指しているか具体的にする
- 集計メトリクスが隠すであろうパターンを指摘する
- 数値を解釈するのに役立つコンテキストを提供する

**すべきでないこと:**
- スキルの改善を提案する（それは改善ステップで行う、ベンチマーキングではない）
- 主観的な品質判断をする（「出力が良い/悪い」）
- 根拠なく原因を推測する
- run_summaryの集計にある情報を繰り返す
