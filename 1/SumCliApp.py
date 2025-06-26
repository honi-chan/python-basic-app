try:
    s = input().split(",")
    n = len(s)

    sum = 0
    for i in range(n):
        sum = sum + int(s[i])

    print(f'sum: {sum}')
except ValueError:
    print("ValueError: 整数以外が入力されました。")