# 必要なモジュールをインポートします
import sys
import re
import os
import csv
import json


def list_program_commands(directory=None, output_file=None):
    # Pythonスクリプトと同じ場所にあるJSONファイルを読み込みます
    script_directory = os.path.dirname(os.path.realpath(__file__))
    json_file = os.path.join(script_directory, os.path.basename(
        sys.argv[0]).rsplit('.', 1)[0] + '.json')
    ignore_file = os.path.join(script_directory, os.path.basename(
        sys.argv[0]).rsplit('.', 1)[0] + '_ignore.json')

    # JSONファイルから一般的なLinuxコマンドのリストとシェルのリストを読み込みます
    with open(json_file, 'r') as file:
        data = json.load(file)
        common_linux_commands = data['common_linux_commands']
        shell_commands = data['shell_commands']

    # _ignore.jsonファイルから無視する単語のリストを読み込みます
    with open(ignore_file, 'r') as file:
        ignore_commands = json.load(file)['ignore_commands']

    # 引数が未指定の場合のデフォルト値を設定します
    if directory is None:
        directory = "."
    if output_file is None:
        output_file = directory + "_SHvsPGM.tsv"

    # CSVファイルに出力します
    with open(output_file, 'w', newline='') as out_file:
        writer = csv.writer(out_file, delimiter='\t')
        writer.writerow(["Shell Script", "Command",
                        "Line Number"])  # ヘッダー行を書き込みます
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".sh"):
                    shell_script = os.path.join(root, file)
                    with open(shell_script, 'r') as in_file:
                        lines = in_file.readlines()
                    for i, line in enumerate(lines, start=1):
                        # 正規表現で行の最初の単語（コマンド）を抽出します
                        match = re.match(r'^\s*([a-zA-Z0-9_\-\/]+)', line)
                        # コマンドが見つかった場合
                        if match:
                            command = match.group(1)
                            # コマンドが一般的なLinuxコマンド等でなく、次の文字が'='でなければ
                            if command not in common_linux_commands and not line[match.end():].lstrip().startswith('='):
                                # シェルの中でシェルを呼び出す行の場合、行全体を単語として出力します
                                if command in shell_commands:
                                    writer.writerow(
                                        [shell_script, line.strip(), i])
                                else:
                                    writer.writerow(
                                        [shell_script, command, i])  # 各行を書き込みます


if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else None
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
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


'''
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
単語の次が=の場合は除外してください

common_linux_comandsはjsonファイルから読み込むようにしてください

jsonファイル名はpythonスクリプトの拡張子を.jsonに変えたものにしてください。

jsonファイルはpythonスクリプトと同じ場所にある想定にしてください

jsonファイルにdo,done,break,dos2unixを追加してください。追加したjsonファイルを表示してください。また、無視する単語のリストをpythonスクリプトと同じフォルダにある想定のpythonスクリプト+"_ignore.json"というファイルで用意するので、その単語は除外するようにしてください。

_ignore.jsonファイルのサンプルを作って

shellの中でshellを呼び出す行は、行全体を単語として出力して

['sh', 'bash', 'zsh', 'csh', 'ksh', 'fish', 'dash', 'tcsh']の内容を、
linuxコマンドのjsonファイルの中に、common_linux_comandsと別で保存してください

jsonファイルをソートしてください。python3.10スクリプトの各行の前にpython初心者向けに、詳細な説明をコメントでいれてください

'''
