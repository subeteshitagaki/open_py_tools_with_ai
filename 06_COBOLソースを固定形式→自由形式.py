# osモジュールをインポートします。これにより、ファイルやディレクトリを操作するための関数が利用できます。
import os

# 固定形式のCOBOLソースコードを自由形式に変換する関数を定義します。
def convert_fixed_format_to_free_format(input_path, output_folder=None, output_comments=False):
    # 出力フォルダが指定されていない場合、入力パスと同じ場所に'output'フォルダを作成します。
    if output_folder is None:
        output_folder = os.path.join(os.path.dirname(input_path), 'output')
        # os.makedirs関数を使用して、必要に応じてディレクトリを作成します。
        os.makedirs(output_folder, exist_ok=True)

    # 入力パスがディレクトリであるかどうかを確認します。
    if os.path.isdir(input_path):
        # ディレクトリ内のすべてのファイルをループします。
        for filename in os.listdir(input_path):
            # ファイルが.cblで終わる場合、それはCOBOLソースコードファイルとみなされます。
            if filename.endswith(".cbl"):
                # COBOLソースコードファイルを変換します。
                convert_cobol_file(os.path.join(input_path, filename), output_folder, output_comments)
    # 入力パスがファイルであるかどうかを確認します。
    elif os.path.isfile(input_path):
        # ファイルを変換します。
        convert_cobol_file(input_path, output_folder, output_comments)
    else:
        # 入力パスが有効なディレクトリまたはファイルでない場合、エラーメッセージを表示します。
        print(f"{input_path} is not a valid directory or file.")

# COBOLソースコードファイルを変換する関数を定義します。
def convert_cobol_file(input_file, output_folder, output_comments):
    # 出力ファイルの名前を決定します。出力フォルダが指定されていない場合、入力ファイルと同じ場所に出力ファイルを作成します。
    output_file = os.path.join(output_folder, os.path.basename(input_file).rsplit('.', 1)[0] + "_free.txt")
    # 入力ファイルを読み取りモードで開き、出力ファイルを書き込みモードで開きます。
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        # 現在の行を初期化します。
        current_line = ''
        # 入力ファイルのすべての行をループします。
        for line in f_in:
            # 7文字目がアスタリスクの場合、それはコメント行とみなされます。
            if line[6] == '*':
                # output_commentsがTrueの場合、コメント行を出力します。
                if output_comments:
                    f_out.write('*> ' + line[7:72].rstrip() + '\n')
            # 7文字目がDの場合、それはDEBUG行とみなされ、無視されます。
            elif line[6] == 'D':
                continue
            else:
                # 行から順序番号領域（列73-80）を削除します。
                line = line[:72]
                # 行から識別領域（列1-6）を削除します。
                line = line[6:]
                # 7文字目がハイフンの場合、それは継続行とみなされます。
                if line[0] == '-':
                    # 継続行を現在の行に追加します。
                    current_line = current_line.rstrip() + line[1:].lstrip()
                else:
                    # 現在の行が存在する場合、それを出力ファイルに書き込みます。
                    if current_line:
                        f_out.write(current_line + '\n')
                    # 新しい現在の行を開始します。
                    current_line = line.rstrip() + ' '
        # 最後の行が存在する場合、それを出力ファイルに書き込みます。
        if current_line:
            f_out.write(current_line + '\n')

# 使用例
# 'path_to_your_folder_or_file'を自由形式のCOBOLソースコードに変換し、'path_to_output_folder'に出力します。
# コメント行は出力されません（既定値）。
convert_fixed_format_to_free_format('path_to_your_folder_or_file', 'path_to_output_folder')

# 'path_to_your_folder_or_file'を自由形式のCOBOLソースコードに変換し、'path_to_output_folder'に出力します。
# コメント行も出力します。
convert_fixed_format_to_free_format('path_to_your_folder_or_file', 'path_to_output_folder', True)




'''
思い出してください


固定形式のCOBOLソースを自由形式にするpython3.10のスクリプトです。

Copilotのプロンプト

固定形式のCOBOLのソースコードを自由形式に変換するpython3.10スクリプトを作ってください

コメントは、行コメントとして、変換してください

自由形式の行コメントは、コメント開始は文字列は*>を使ってください

継続行は1行にまとめて、複数行に分かれた命令を１行にまとめないでください

7文字目に-がある場合、前の行からの継続行としてください。

上記のプロンプトで、以下のスクリプトを作ってもらいました。
def convert_cobol_multiline_to_singleline(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        current_line = ''
        for line in f_in:
            # If the line is a comment line in fixed format (asterisk in column 7)
            if line[6] == '*':
                # Write the line as a comment line in free format
                f_out.write('*> ' + line[7:72].rstrip() + '\n')
            else:
                # Remove sequence number area (columns 73-80)
                line = line[:72]
                # Remove identification area (columns 1-6)
                line = line[6:]
                # If the line is a continuation line (hyphen in column 7), add it to the current line
                if line[0] == '-':
                    current_line = current_line.rstrip() + line[1:].lstrip()
                else:
                    # If there is a current line, write it to the output file
                    if current_line:
                        f_out.write(current_line + '\n')
                    # Start a new current line
                    current_line = line.rstrip() + ' '

        # Write the last line to the output file
        if current_line:
            f_out.write(current_line + '\n')

# 使用例
convert_cobol_multiline_to_singleline('multiline.cbl', 'singleline.cbl')



１つ目の引数に、ファイル名またはフォルダ名を指定するので、フォルダ名の場合は、フォルダにある各ファイルを処理してください。
出力フォルダに入力ファイル名と同じファイル名で出力する。

２つ目の引数に、出力先のフォルダを指定します。未指定の場合、1つ目のファイルまたはフォルダと同じ場所にoutputフォルダを作成し、出力してください


7文字目がDの場合、DEBUG行として、無視してください。


関数名ですが、固定形式から自由形式への変換なので、適切な関数名に変更してください

スクリプトの各行の前に、python初心者向けに詳細な説明をコメントで追加してください

３つ目の引数でコメント行を出力する/しないを指定できるようにしてください。既定は出力しない

'''
