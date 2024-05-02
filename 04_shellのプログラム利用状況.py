# 必要なモジュールをインポートします
import sys
import re
import os
import csv

def list_program_commands(directory=None, output_file=None):
    # 一般的なLinuxコマンド、制御構造、変数への代入を除外するためのリスト（アルファベット順）
    # これらはシェルスクリプト内で頻繁に使用されるため、プログラムとは判断しないようにします
    common_linux_commands = sorted({"alias", "apropos", "at", "awk", "base64", "bc", "bg", "bind", "builtin", "bunzip2", "bzip2", "cal", "caller", "cat", "cd", "chgrp", "chmod", "chown", "clear", "command", "cp", "crontab", "curl", "cut", "date", "dc", "dd", "declare", "df", "dig", "dirs", "dmesg", "du", "echo", "else", "env", "exit", "export", "expr", "factor", "fg", "fi", "file", "find", "ftp", "getopts", "grep", "groupadd", "groupdel", "gzip", "hash", "head", "help", "history", "hostname", "if", "ifconfig", "jobs", "kill", "last", "less", "let", "ln", "local", "logout", "ls", "man", "mkdir", "more", "mount", "mv", "netstat", "nice", "nohup", "nslookup", "od", "passwd", "ping", "popd", "printenv", "printf", "ps", "pushd", "pwd", "read", "reboot", "renice", "reset", "return", "rm", "rmdir", "rsync", "scp", "script", "sed", "seq", "set", "setenv", "shopt", "shutdown", "sleep", "sort", "source", "ssh", "stat", "strings", "sudo", "suspend", "tail", "tar", "test", "tic", "time", "times", "toe", "top", "touch", "traceroute", "trap", "true", "tput", "tset", "type", "typeset", "ulimit", "umask", "umount", "uname", "unalias", "unset", "unxz", "useradd", "userdel", "wait", "wget", "which", "who", "whoami", "yes", "zip"})

    # 引数が未指定の場合のデフォルト値を設定します
    # directoryがNoneの場合、カレントディレクトリ（"."）を解析対象とします
    if directory is None:
        directory = "."
    # output_fileがNoneの場合、ディレクトリ名に"_SHvsPGM.tsv"を追加したものを出力ファイル名とします
    if output_file is None:
        output_file = directory + "_SHvsPGM.tsv"

    # CSVファイルに出力します
    # 'w'オプションで新規作成または上書きモード、newline=''で改行コードの自動変換を無効化します
    with open(output_file, 'w', newline='') as out_file:
        # csv.writerを使ってCSVファイルを書き込むオブジェクトを作成します
        # delimiter='\t'でフィールドの区切り文字をタブに設定します
        writer = csv.writer(out_file, delimiter='\t')
        # writerowメソッドで一行書き込みます。ここではヘッダー行を書き込みます
        writer.writerow(["Shell Script", "Command", "Line Number"])
        # os.walkでディレクトリを再帰的に探索します
        for root, dirs, files in os.walk(directory):
            # ディレクトリ内の全てのファイルに対して処理を行います
            for file in files:
                # ファイルがシェルスクリプト（.shで終わる）ならば解析します
                if file.endswith(".sh"):
                    # ファイルのフルパスを作成します
                    shell_script = os.path.join(root, file)
                    # ファイルを読み込みモードで開きます
                    with open(shell_script, 'r') as in_file:
                        # readlinesメソッドで全ての行を読み込みます
                        lines = in_file.readlines()
                    # enumerate関数で行番号と行の内容を取得します
                    for i, line in enumerate(lines, start=1):
                        # 正規表現で行の最初の単語（コマンド）を抽出します 解説1参照
                        command = re.match(r'^\s*([a-zA-Z0-9_\-\/]+)', line)
                        # コマンドが見つかった場合
                        if command:
                            # groupメソッドでマッチした文字列を取得します 解説2参照
                            command = command.group(1)
                            # コマンドが一般的なLinuxコマンド等でなければ
                            if command not in common_linux_commands:
                                # writerowメソッドで一行書き込みます
                                writer.writerow([shell_script, command, i])

# スクリプトが直接実行された場合の処理です
if __name__ == "__main__":
    # コマンドライン引数を取得します。引数がなければNoneを設定します
    directory = sys.argv[1] if len(sys.argv) > 1 else None
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    # 関数を呼び出して処理を実行します
    list_program_commands(directory, output_file)


# 解説1
# この行では、Pythonのre.match関数を使用して、各行の最初の単語（コマンド）を抽出しています。
# re.match関数は、正規表現パターンと文字列を引数に取り、文字列の先頭がパターンに一致するかどうかをチェックします。
# 一致する場合、matchオブジェクトを返します。一致しない場合、Noneを返します。
# 
# ここで使用している正規表現パターン'^\s*([a-zA-Z0-9_\-\/]+)'は次のように解釈されます：
# 
# ^は文字列の先頭を表します。
# \s*は空白文字（スペース、タブ、改行など）が0回以上続くことを表します。つまり、行の先頭に空白文字があっても無視します。
# ([a-zA-Z0-9_\-\/]+)は英字（大文字または小文字）、数字、アンダースコア、ハイフン、スラッシュが1回以上続く文字列をキャプチャします。
# これがコマンド名に相当します。


# 解説2
# この行では、groupメソッドを使用して、正規表現に一致した文字列（この場合はコマンド名）を取得しています。
# group(1)は、正規表現内の1番目の括弧（(と)で囲まれた部分）に一致した文字列を返します。
# この場合、それはコマンド名になります。



# Copilotへのプロンプト
#
# シェルスクリプトから、シェルスクリプト内で利用しているプログラムをリストアップするpython3.10のスクリプトを作ってください
#
# commands = re.findall(r'^\s*([a-zA-Z0-9_-]+)', data, re.MULTILINE)　に何をしているかできるだけ情報量の多いコメントを追加してください。
#
# 素晴らしいコメントです。わかりやすい。linuxのコマンドを除いて、プログラムの実行だけを対象にしてください
#
# if else fi を除外してください
#
# 変数への代入も除外してください
# 
# プログラムの行を返すのとは別に、プログラムだけを返すように改善して
# 
# programs = {command for command in commands if '/' in command}　はどういう意味？
# 
# プログラムですが、プログラムを使う行の最初の単語を取得してください
# 
# テスト用のコードとサンプルも準備してください
# 
# 実行結果も出力してください
# 
# common_linux_commandsを保守しやすいように、アルファベット順にして
# 
# サンプルファイルだと、何が返ってくるかおしえてください
#
# 想定通りでよかったです。何行目にあったかも一緒に出力可能ですか？
# 
# シェルファイル名 , プログラム,行番号　のタブ区切りファイル出力するように改善してください
#
# 引数１にフォルダを指定された場合、フォルダ内のシェルファイル全部に対して、実行するように改良してください
#
# 第一引数を未指定の場合、カレントディレクトリを対象にする。　第２引数が未指定の場合、第一引数に拡張子.tsvを追加したファイルが指定されたものとする
#
# csvファイルはヘッダーつけて欲しい
# 
# 第二引数を省略時に、第一引数に拡張子.tsvをつけたものになるとしていましたが、第一引数に"_SHvsPGM.tsv"を追加したものにしてください
# 
# python初心者でもわかるように、丁寧なコメントを追加してください。
# 
# command = re.match(r'^\s*([a-zA-Z0-9_-/]+)', line)　と　command = command.group(1)　のコメントをもっと、初心者向けに詳細な説明にしてください。
#
