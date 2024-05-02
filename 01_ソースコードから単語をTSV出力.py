import re

def tab_separate_words(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 演算子、括弧、等号不等号のリストを定義します
    symbols = ['=', '(', ')', '[', ']', '{', '}', '+', '-', '*', '/']

    # ブロックコメントの開始文字と終了文字をタプルとしてリストで定義します
    block_comments = [('"""', '"""'), ("'''", "'''")]

    # 行コメントの記号を定義します
    line_comments = ['#']

    tab_separated_lines = []
    for line in lines:
        # 各行コメント記号の前後にスペースがない場合も考慮します
        for comment in line_comments:
            if comment in line:
                line = line.split(comment)[0]

        # 各ブロックコメントを除去します
        for start, end in block_comments:
            line = re.sub(fr'{re.escape(start)}.*?{re.escape(end)}', '', line, flags=re.DOTALL)

        # 各記号の前後にスペースがない場合も考慮します
        for symbol in symbols:
            line = re.sub(fr'(?<=[^\s{re.escape(symbol)}]){re.escape(symbol)}(?=[^\s{re.escape(symbol)}])', f' {symbol} ', line)

        # 文字列内の単語は分割しないようにします
        # 文字列を見つけ、そのまま保持します
        strings = re.findall(r'"[^"]*"|\'[^\']*\'', line)
        for string in strings:
            line = line.replace(string, string.replace(' ', '<space>'))

        # `re.split()`関数は、正規表現を使用して文字列を分割します。
        # この場合、`re.split('\s+', line)`は行を単語に分割します。
        words = re.split('\s+', line)
        tab_separated_line = '\t'.join(words)

        # 文字列内のスペースを元に戻します
        tab_separated_line = tab_separated_line.replace('<space>', ' ')
        tab_separated_lines.append(tab_separated_line)

    with open(file_path, 'w') as file:
        file.write('\n'.join(tab_separated_lines))

# ファイルパスを指定して関数を呼び出します
tab_separate_words('your_file_path.txt')



'''
ソースコードから、ソースコード内の単語をタブ区切りで出力するpython3.10スクリプト

copilotのプロンプト

プログラムのソースコードから、単語をタブ区切りにするpython3.10スクリプトを作ってください

words = line.split()　に　丁寧なコメントを追加してください

=の前後にスペースがない可能性も考慮して

コメント行は無視してください。#でコメントが入る前提

コメントが行の途中から入る場合があるので、考慮してください

ブロックコメントも考慮して

"`'()[]{}+-*/の前後にスペースがない可能性も考慮して

"`'の前後にスペースがない可能性は考慮するを取り消します

文字列内は単語を分割しないでください

正規表現の前には詳細で丁寧なコメントを追加してください。

演算子、括弧、等号不等号の前後にスペースがないことの考慮は、演算子、括弧、等号不等号をリストで定義してください

ブロックコメント、行コメントの記号もリストで定義してください

文字列内は単語を分割しないでください

正規表現の前には詳細で丁寧なコメントを追加してください。

ブロックコメントと行コメントの文字の定義のリストを分けてください

ブロックコメントは開始文字と終了文字の定義をリストとして持ってください

ブロックコメントは開始文字と終了文字のタプルをリストとして持ってください

'''
