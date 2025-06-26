# MCPハンズオン練習

2025/06/26に開催した「ゼロから学ぶ！〜MCP入門ハンズオン〜（by CDLE北海道）」(https://jdla.connpass.com/event/358239/)用の

Model Context Protocol (MCP) サーバーの実装練習のサンプルプロジェクト

以下のMCPハンズオン練習の手順に従って、構築するとローカルで同じものが構築できます！

[MCPハンズオン練習](https://supermarimobros.github.io/0626_mcp_handson/)

## 注意

ハンズオン時には、Slackへのメッセージ投稿の際のSlack APIを公開していましたが、

現在は公開しておりません。

他システムのAPI連携の参考コードとしてお使いください。

## 必要な環境

- uv (Pythonのパッケージ管理)
- Python 3.10以上（uvでPythonが入るのでなくても良いです。）


## プロジェクト構成

### mcp-basic-python
基本的なMCPサーバーの実装
- **機能**: 数値加算ツールと挨拶リソース
- **ツール**: `add(a, b)` - 2つの数値を加算
- **リソース**: `greeting://{name}` - パーソナライズされた挨拶
 - 注意：リソースはClaude Desktopでは認識されないです。（原因不明）

### mcp-practice-python  
実践的なゴミ収集管理MCPサーバー
- **機能**: ゴミ収集スケジュール検索とSlack通知
- **ツール**: 
  - `search_garbage_collection(query)` - SQLクエリでゴミ収集日検索
  - `post_to_slack(message)` - Slackへのメッセージ投稿
- **データベース**: 札幌市家庭ごみ収集日カレンダーのデータベース

### データベース生成コード

[札幌市家庭ごみ収集日カレンダー（2024年10月1日～2025年9月30日）](https://ckan.pf-sapporo.jp/dataset/garbage_collection_calendar/resource/a261bccd-4383-487f-aa2d-3a502469e7ad)

のCSVから本ハンズオンで使用するSQLiteデータベースを生成する参考コード

### docs
プロジェクトのドキュメント（HTML形式）