import sqlite3

dbname = 'booktracker.db'

def create_table():
    # 1.データベースに接続
    conn = sqlite3.connect(dbname)

    # 2.sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()

    # 3.テーブルのCreate文を実行(例ではpersonsテーブルを作成)
    cur.execute(
        'CREATE TABLE IF NOT EXISTS booktracker(book_name STRING, author STRING, status STRING, rating INTEGER, tag STRING, PRIMARY KEY(book_name, author))')

    # 4.データベースに情報をコミット
    conn.commit()

    # 5.データベースの接続を切断
    cur.close()
    conn.close()

def insert(book_name, author, status):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    try:
        cur.execute('''
            INSERT INTO booktracker (book_name, author, status, rating, tag)
            VALUES (?, ?, ?, null, null)
        ''', (book_name, author, status))
        print(f'✅ “{book_name}” by {author} を「読みたい」に追加')
    except sqlite3.IntegrityError:
        print("登録済みです。")

    conn.commit()
    cur.close()
    conn.close()

def show():
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM booktracker WHERE status = "add_to_read"')
    rows = cur.fetchall()
    
    if not rows:
        print("📚 登録された本がありません。")
    else:
        print("📖 登録済みの本一覧：")
        for i in range(len(rows)):
            row = rows[i]
            print(f'{i + 1}. (“{row[0]}”, “{row[1]}”)')

    cur.close()
    conn.close()

def mark_read(book_name, author, status):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    
    cur.execute(
        'UPDATE booktracker SET status = ? WHERE book_name = ? AND author = ?',
        (status, book_name, author)
    )
    print(f'✅ “{book_name}” を「読了」に移動')

    conn.commit()
    cur.close()
    conn.close()

def rate(book_name, author, rate):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    
    cur.execute(
        'UPDATE booktracker SET rating = ? WHERE book_name = ? AND author = ?',
        (rate, book_name, author)
    )
    print(f'✅ “{book_name}” の評価を {rate} に設定')

    conn.commit()
    cur.close()
    conn.close()

def add_tag(book_name, author, tag):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    
    cur.execute(
        'UPDATE booktracker SET tag = ? WHERE book_name = ? AND author = ?',
        (tag, book_name, author)
    )
    print(f'✅ “{book_name}” にタグ “{tag}” を追加')

    conn.commit()
    cur.close()
    conn.close()

def find_by_tag(tag):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM booktracker WHERE tag = ?', (tag,))
    rows = cur.fetchall()
    
    if not rows:
        print("📚 本がありません。")
    else:
        print("📖 本一覧：")
        for i in range(len(rows)):
            row = rows[i]
            print(f'– (“{row[0]}”, “{row[1]}”) 評価:{row[3]} タグ:{row[4]}')
            
    cur.close()
    conn.close()

