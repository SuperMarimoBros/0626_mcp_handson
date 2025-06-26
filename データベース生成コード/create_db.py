import pandas as pd
import sqlite3


FILE_NAME = 'garvagecollectioncalendar202410.csv'
df = pd.read_csv(FILE_NAME, encoding='utf-8')

print(df.shape)
print(df.head())

# データをmelt（縦持ちに変換）
df_melted = df.melt(id_vars=["日付", "曜"], var_name="地区", value_name="ゴミ種別コード")

# 空の値（土日など）を除外
df_melted = df_melted.dropna(subset=["ゴミ種別コード"])

# ゴミ種別コードを整数型に変換
df_melted["ゴミ種別コード"] = df_melted["ゴミ種別コード"].astype(int)

print(df_melted.shape)
print(df_melted.head())

# CSVファイルの保存
output_csv = 'garbage_collection.csv'
df_melted.to_csv(output_csv, index=False, encoding='utf-8')

# SQLiteデータベースに保存
db_name = 'garbage_collection.db'
conn = sqlite3.connect(db_name)

try:
    # テーブルに保存（既存のテーブルがあれば置き換え）
    df_melted.to_sql('garbage_schedule', conn, if_exists='replace', index=False, dtype={
        '日付': 'TEXT',
        '曜': 'TEXT',
        '地区': 'TEXT',
        'ゴミ種別コード': 'INTEGER'
    })
    print(f"\nデータを {db_name} に保存しました")
    
    # 保存されたデータの確認
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM garbage_schedule")
    count = cursor.fetchone()[0]
    print(f"保存されたレコード数: {count}")

    # サンプルデータの表示
    cursor.execute("SELECT * FROM garbage_schedule WHERE 地区 = '中央区①' AND 日付 = '2025-06-24'")
    sample_data = cursor.fetchall()
    print("\nサンプルデータ:")
    for row in sample_data:
        print(row)

    
    # サンプルデータの表示
    cursor.execute("SELECT * FROM garbage_schedule LIMIT 5")
    sample_data = cursor.fetchall()
    print("\n保存されたデータのサンプル:")
    for row in sample_data:
        print(row)
    
    # テーブル構造の確認
    cursor.execute("PRAGMA table_info(garbage_schedule)")
    columns = cursor.fetchall()
    print("\nテーブル構造:")
    for col in columns:
        print(f"- {col[1]} ({col[2]})")

finally:
    conn.close()
    print(f"\nデータベース接続を閉じました")