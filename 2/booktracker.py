import sys
from db.booktracker_db import create_table, insert, show, mark_read, rate, add_tag, find_by_tag

def main():
    try:
        args = sys.argv

        if args[1] == 'add_to_read' and args[2] and args[3]:
            insert(args[2], args[3], args[1])
        elif args[1] == 'show_to_read':
            show()
        elif args[1] == 'mark_read' and args[2] and args[3]:
            mark_read(args[2], args[3], args[1])
        elif args[1] == 'rate' and args[2] and args[3] and args[4]:
            rate(args[2], args[3], args[4])
        elif args[1] == 'add_tag' and args[2] and args[3] and args[4]:
            add_tag(args[2], args[3], args[4])
        elif args[1] == 'find_by_tag' and args[2]:
            find_by_tag(args[2])
    except IndexError:
        print('エラー: 引数が正しくありません。')

if __name__ == '__main__':
    create_table()
    main()