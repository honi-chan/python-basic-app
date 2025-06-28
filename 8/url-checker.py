import sys
import time
import requests
from multiprocessing import Process, Queue

# ----------------------------
# 定数・共通設定
# ----------------------------
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

TIMEOUT = 10  # 秒

# ----------------------------
# 結果を整形して出力する
# ----------------------------
def display_results(results):
    results.sort(key=lambda x: x[2])  # 応答時間(ms)で昇順
    for domain, status, elapsed in results:
        print(f"{domain} {status} {elapsed}ms")

# ----------------------------
# URL応答をチェックする関数
# ----------------------------
def check_url_status(domain, queue):
    url = f"https://{domain}/"
    try:
        response = requests.head(url, timeout=TIMEOUT, headers=HEADERS)
        elapsed = round(response.elapsed.total_seconds() * 1000)
        
        if response.status_code == 200:
            queue.put((domain, 'ok', elapsed))
            return
        elif response.status_code == 405:
            allowed = response.headers.get("Allow", "")
            if 'GET' in allowed:
                response = requests.get(url, timeout=TIMEOUT, headers=HEADERS)
                if response.status_code == 200:
                    queue.put((domain, 'ok', elapsed))
                    return
        queue.put((domain, 'ng', elapsed))
    except requests.exceptions.RequestException:
        queue.put((domain, 'ng', 0))

# ----------------------------
# 並列にURLチェックを実行
# ----------------------------
def parallel_check(domains):
    queue = Queue()
    processes = []

    for domain in domains:
        p = Process(target=check_url_status, args=(domain, queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    results = []
    while not queue.empty():
        results.append(queue.get())
    return results

# ----------------------------
# ファイルからドメイン名を読み込む
# ----------------------------
def load_domains_from_file(filename):
    try:
        f = open(f"url/{filename}", "r", encoding="utf-8")
        f_lines = f.read().split('\n')
        f.close()

        return f_lines
    except FileNotFoundError:
        print("ファイルが存在しませんでした。")

# ----------------------------
# メイン関数
# ----------------------------
def main():
    try:
        args = sys.argv
        filename = args[1]
        domains = load_domains_from_file(filename)
        results = parallel_check(domains)
        display_results(results)
    except IndexError:
        print("エラー: 引数が正しくありません。")

# ----------------------------
# 実行開始
# ----------------------------
if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(f"合計実行時間 : {round((end - start) * 1000)}ms")
