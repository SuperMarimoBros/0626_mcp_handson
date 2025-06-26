from mcp.server.fastmcp import FastMCP
import sqlite3
import os
from dotenv import load_dotenv
import requests

load_dotenv()
SLACK_API_URL = os.getenv("SLACK_API_URL")
if not SLACK_API_URL:
    raise ValueError("環境変数 SLACK_API_URL が設定されていません")
DB_FILE = "garbage_collection.db"

# Initialize FastMCP server
mcp = FastMCP("mcp-garbage")

@mcp.tool()
def search_garbage_collection(query: str) -> str:
    """
    クエリに基づいてゴミの集荷日を検索する
    
    Args:
        query: SQLのSELECTクエリ（ゴミ収集スケジュールテーブル: garbage_schedule）
    
    Returns:
        str: クエリ結果をフォーマットした文字列。結果がない場合はその旨を返す。
        
    テーブル構造:
        - 日付 (TEXT): ゴミ収集日の日付
        - 曜 (TEXT): 曜日
        - 地区 (TEXT): 収集対象地区
        - ゴミ種別コード (INTEGER): ゴミの種別を表すコード
        
    例:
        SELECT * FROM garbage_schedule WHERE 地区 = '中央区①'
        SELECT 日付, ゴミ種別コード FROM garbage_schedule WHERE 曜 = '月'
    
    注意:
        セキュリティ上の理由により、SELECT文のみ実行可能です。
    """
    # SELECT文以外を弾く簡易的なセキュリティチェック
    # このチェックは非常に基本的なもので、実際のアプリケーションではより堅牢なセキュリティ対策が必要です。
    if not query.strip().upper().startswith("SELECT"):
        return "Error: Only SELECT queries are allowed1213."

    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        try:
            cur.execute(query)
            results = cur.fetchall()
            
            if not results:
                return "クエリの実行は成功しましたが、結果が見つかりませんでした。"
            
            # 結果を辞書形式でフォーマットして返す
            formatted_results = []
            for row in results:
                row_dict = dict(row)
                formatted_results.append(str(row_dict))
            
            return f"クエリ結果:\n" + "\n".join(formatted_results)
            
        except sqlite3.Error as e:
            return f"SQLエラー: {str(e)}"

@mcp.tool()
def post_to_slack(message: str) -> str:
    """
    Slackにメッセージを投稿する
    
    Args:
        message: 投稿するメッセージ
        
    Returns:
        成功または失敗のメッセージ
    """
    if not SLACK_API_URL:
        return "Error: Slack API URL is not configured."
    
    try:
        response = requests.post(
            SLACK_API_URL, 
            json={"message": message},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return "メッセージがSlackに投稿されました。"
    except requests.RequestException as e:
        return f"Slackへの投稿に失敗しました: {str(e)}"

if __name__ == "__main__":
    mcp.run()