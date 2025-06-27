
import sys
import requests
import time

def main():
    try:
        args = sys.argv
        
        f = open(r"url/{}".format(args[1]), "r", encoding="utf-8")
        f_lines = f.read().split('\n')

        logs = []
        for line in f_lines:
            url = 'https://{}/'.format(line)
            is_valid, time = check_URL(url)
            logs.append([line, is_valid, time])
        
        logs = sorted(logs, key=lambda x: x[2])
        for log in logs:
            print(f"{log[0]} {log[1]} {log[2]}ms")
        
        f.close()
    except FileNotFoundError:
        print("ファイルが存在しませんでした。")
    except IndexError:
        print('エラー: 引数が正しくありません。')

def check_URL(url):#URLの有効性をチェックする。戻り値はbool,ステータスコード（or Errorコード）
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"}
    try:
        response = requests.head(url, timeout=10,headers=headers)
        time = round(response.elapsed.total_seconds() * 1000)
        if response.status_code == 200:
            return 'ok' , time
        elif response.status_code == 405:  # Method Not Allowed
            allowed_methods = response.headers.get('Allow', '')
            if 'GET' in allowed_methods:
                response = requests.get(url, timeout=10,headers=headers)
                if response.status_code == 200:
                    return 'ok' , time
                else:
                    return 'ng' , time
            else:
                return 'ng' , time
        else:
            return 'ng' , time
    except requests.exceptions.RequestException as e:
        return 'ng' , 0

if __name__ == '__main__':
    start = time.time()

    main()

    end = time.time()
    time_diff = round((end - start) * 1000)
    print(f'合計実行時間 : {time_diff}ms')
