# Claude Code プラグインサンプル

Claude Code 用のサンプルプラグインディレクトリです。

## 構成

- **`/plugins`** - サンプルプラグイン

## インストール

### 1. マーケットプレイスを追加する

Claude Code 内で以下のコマンドを実行し、このマーケットプレイスを登録します：

```shell
/plugin marketplace add narunblog/claude-plugins-sample
```

### 2. プラグインをインストールする

```shell
/plugin install {plugin-name}@plugins-sample
```

または `/plugin` を実行して **Discover** タブからプラグインを検索してインストールできます。

## 利用可能なプラグイン

| プラグイン | 説明 |
|-----------|------|
| [skill-creator](./plugins/skill-creator) | スキルの作成・修正・評価を行うサンプルプラグイン |

## プラグインの構成

各プラグインは以下の標準構成に従います：

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json      # プラグインメタデータ（必須）
├── .mcp.json            # MCP サーバー設定（任意）
├── commands/            # スラッシュコマンド（任意）
├── agents/              # エージェント定義（任意）
├── skills/              # スキル定義（任意）
└── README.md            # ドキュメント
```

## コントリビュート

新しいプラグインを追加するには、上記の構成に従って `/plugins` 配下にディレクトリを作成し、`.claude-plugin/marketplace.json` のマーケットプレイス設定を更新してください。

## ライセンス

各プラグインの LICENSE ファイルをご確認ください。

## ドキュメント

Claude Code プラグインの開発に関する詳細は、[公式ドキュメント](https://code.claude.com/docs/ja/plugins)をご参照ください。