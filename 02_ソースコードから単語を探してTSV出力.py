# reモジュール（正規表現を扱うためのモジュール）、csvモジュール（CSVファイルを扱うためのモジュール）、
# argparseモジュール（コマンドライン引数を扱うためのモジュール）、jsonモジュール（JSONを扱うためのモジュール）、
# osモジュール（OSの機能を扱うためのモジュール）をインポートします。
import re
import csv
import argparse
import json
import os

# print_lines_with_wordsという関数を定義します。この関数は、指定した単語が含まれる行を探し、その行番号、行、単語をタプルとしてリストに追加します。
# 結果はタブ区切りのファイルに出力します。
def print_lines_with_words(path: str, groups_file: str, output_file: str = None):
    # groups_fileという名前のファイルを開き、その内容をJSONとして読み込みます。
    with open(groups_file, 'r') as f:
        groups_dict = json.load(f)

    # 結果を保存するための空のリストを作成します。
    result = []
    # 引数1がディレクトリの場合、そのディレクトリ内の各ファイルに対して処理を行います。
    if os.path.isdir(path):
        filenames = [os.path.join(path, filename) for filename in os.listdir(path) if os.path.isfile(os.path.join(path, filename))]
    else:
        filenames = [path]

    # 各ファイルに対して処理を行います。
    for filename in filenames:
        # filenameという名前のファイルを開きます。
        with open(filename, 'r', encoding='utf-8') as file:
            # ファイルの各行に対して処理を行います。enumerate関数を使用して、行番号も取得します。
            for line_number, line in enumerate(file, 1):
                # 文字列リテラル（"または'で囲まれた文字列）を見つけるための正規表現パターンを定義します。
                string_pattern = r'"([^"]*)"|\'([^\']*)\''
                # 正規表現を使用して、行から文字列リテラルをすべて見つけます。
                string_literals = re.findall(string_pattern, line)
                # 各マッチは2つのグループを持つタプルです。一方は空で、もう一方にはマッチした文字列が含まれています。
                # filter関数を使用して空の要素を除去し、マッチした文字列だけを取得します。
                string_literals = [list(filter(None, sl))[0] for sl in string_literals]
                # 正規表現を使用して、行から文字列リテラルをすべて削除します。
                non_string_part = re.sub(string_pattern, '', line)
                # 各グループに対して処理を行います。
                for group, group_dict in groups_dict.items():
                    words = group_dict['words']
                    search_in_string = group_dict['search_in_string']
                    search_outside_string = group_dict['search_outside_string']
                    dot_separated = group_dict['dot_separated']
                    # 各単語に対して処理を行います。
                    for word in words:
                        # .で区切られた単語を探す場合、パターンを変更します。
                        if dot_separated:
                            pattern = r'\b' + re.escape(word) + r'\b|\.' + re.escape(word) + r'\b'
                        else:
                            pattern = r'\b' + re.escape(word) + r'\b'
                        # 文字列リテラルの中を検索対象にする場合、各文字列リテラルに対して処理を行います。
                        if search_in_string:
                            for string_literal in string_literals:
                                # 正規表現を使用して、単語が文字列リテラルに存在するかどうかをチェックします。
                                if re.search(pattern, string_literal):
                                    # 単語が存在する場合、結果のリストに行番号、行、単語を追加します。
                                    result.append((group, word, filename, line_number, line.strip()))
                        # 文字列リテラル以外の部分を検索対象にする場合、単語が存在するかどうかをチェックします。
                        if search_outside_string:
                            if re.search(pattern, non_string_part):
                                # 単語が存在する場合、結果のリストに行番号、行、単語を追加します。
                                result.append((group, word, filename, line_number, line.strip()))

    # output_fileがNoneの場合、デフォルトのファイル名を設定します。
    if output_file is None:
        output_file = path + "_word_search_report.tsv"

    # 結果をタブ区切りのファイルに出力します。
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        # ヘッダーを書き込みます。
        writer.writerow(['Group', 'Word', 'Filename', 'Line Number', 'Line'])
        # 結果を書き込みます。
        writer.writerows(result)

# スクリプトが直接実行された場合（つまり、このスクリプトが他のスクリプトからインポートされずに直接実行された場合）、以下のコードが実行されます。
if __name__ == "__main__":
    # argparseモジュールを使用して、コマンドライン引数を解析します。
    parser = argparse.ArgumentParser(description='Search for words in a file or directory.')
    parser.add_argument('path', type=str, help='The path of the file or directory to search')
    parser.add_argument('groups_file', type=str, help='The name of the JSON file containing the groups of words to search for')
    parser.add_argument('output_file', type=str, nargs='?', default=None, help='(Optional) The name of the file to output the results to')
    args = parser.parse_args()

    # 引数が指定されている場合、print_lines_with_words関数を呼び出します。
    if args.path and args.groups_file:
        print_lines_with_words(args.path, args.groups_file, args.output_file)
    else:
        # 引数が指定されていない場合、スクリプトの説明と使用方法を表示します。
        print("Python 3.10 script for searching words in a file or directory.")
        print("Usage: python script.py <path> <groups_file> [output_file]")
        print("path: The path of the file or directory to search")
        print("groups_file: The name of the JSON file containing the groups of words to search for")
        print("output_file: (Optional) The name of the file to output the results to")
        print("\nExample of groups_file:")
        print('{"group1": {"words": ["word1", "word2"], "search_in_string": true, "search_outside_string": false, "dot_separated": true}, "group2": {"words": ["word3", "word4"], "search_in_string": false, "search_outside_string": true, "dot_separated": false}}')


'''
ソースコードから、指定した文字列リストを探してTSV出力するpython3.10スクリプト

Copilotへのプロンプト

ソースコードから、指定した単語を含む行を出力するpython3.10のスクリプトを作ってください

指定した単語は、文字列のリストとして渡します。行番号、行、単語（文字列）のタプルをリストで出力してください

単語の一部が指定した文字列の場合を含めるか含めないかを選べるようにしてください。

行全体でなく、単語

if (partial_match and re.search(r'\b' + re.escape(word) + r'\b', line)) or (not partial_match and word == line.strip()):

re.search(r'\b' + re.escape(word) + r'\b', line)を具体的な例で挙動を教えてください

この例でThisを探すと見つかる？

この例でtestは見つかる？

.が単語の区切りとされていますが、単語の区切りの具体例をすべて教えてください


line = "Hello, world! This is a test."
word = "test"
re.search(r'\b' + re.escape(word) + r'\b', line)


ハイフンでつながれた単語やアポストロフィが含まれる単語の場合の挙動を具体例を出しておしえてください

ありがとうございます。理解しました。スクリプトのコメントに今の解説を詳細に記載してください。具体例もコメントでいれてください

partial_match は不要です。なしにしてください。

文字列の中も単語を検索するか？を選べるようにしてください。

依頼がわかりにくかったです。文字列の中を探すとは、"または'で囲まれた決め打ちの文字列の中に単語があるかを探すという意味でした

for match in re.findall(string_pattern, line):　はどういう意味かをpython初心者向けに詳細に教えてください。

matchという名前は予約語っぽい名前なので、別の名前にしてください

(1)"または'で囲まれた文字列と行のそれ以外も単語を探す対象にする。(2)"または'で囲まれた文字列だけ単語を探す対象にする。(3)"または'で囲まれた文字列以外を単語の探す対象にする　の３パターンを関数のパラメータなどで選択可能にしてください


関数の引数のwordsを{"group1":["this","is"],"group2":["that","was"]}のようにグループ名付きの文字列のリストの辞書型で渡すように改良して

結果は、辞書のキー(group1など),文字列("this"など),ソースコードの行数,ソースコードの行の内容のタブ区切りファイルで出力してください。ヘッダーもつけて

単語を探すときに、dbo.tbl1.field1のように、.で区切られている場合、パラメータ4を設定すると、tbl1で見つかるようにしたい

search_target (int): 検索対象を指定する数値（1: 文字列リテラルとそれ以外も対象、2: 文字列リテラルのみ対象、3: 文字列リテラル以外を対象）
を2つのパラメータにしてください。文字列リテラルを探す/探さない　と　文字列リテラル以外を探す/探さない

パラメータが多いので、words_dictのgroup毎にパラメータをかけるようにしたい

このpython3.10スクリプトに引数を渡して利用したい

引数でJSON文字列を渡していますが、これをJSONファイルを渡すにしてください

引数1がファイルでなく、フォルダだった場合、フォルダの中の各ファイルに対して処理をしてください

引数3がない場合、引数1+"_word_seach_report.tsv"としてください。
また引数なしの場合、python3.10スクリプトのバージョン、このスクリプトの説明、引数情報とJSONファイルのサンプルを標準出力に表示してくだい

ありがとうございます。スクリプトの各行の前にpython初心者向けの詳細なコメントを追加してください。

'''
