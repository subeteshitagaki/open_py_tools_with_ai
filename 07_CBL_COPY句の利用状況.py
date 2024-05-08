import os  # osモジュールをインポートします。これにより、ファイルやディレクトリを操作するための関数が利用できます。
import sys  # sysモジュールをインポートします。これにより、コマンドライン引数を取得するための関数が利用できます。
import glob  # globモジュールをインポートします。これにより、特定のパターンに一致するファイル名を取得するための関数が利用できます。
import re  # reモジュールをインポートします。これにより、正規表現を使用するための関数が利用できます。

def extract_copy_files(file_path):  # COPY句が参照しているファイル名を抽出する関数を定義します。
    with open(file_path, 'r') as file:  # 指定されたパスのファイルを読み取りモードで開きます。
        lines = file.readlines()  # ファイルの内容を行ごとに読み込み、それをリストとして保存します。

    # 各行を調べ、'COPY'で始まる行からファイル名を抽出します。抽出したファイル名はリストに保存されます。
    copy_files = [re.findall(r'(?<=COPY ).*?(?=\.)', line) for line in lines if line.lstrip().startswith('COPY')]
    copy_files = [item for sublist in copy_files for item in sublist]  # リストをフラット化します（ネストされたリストを単一のリストに変換します）。
    return copy_files  # 抽出したファイル名のリストを返します。

def write_to_file(output_folder, file_name, copy_files):  # 抽出したファイル名を出力ファイルに書き込む関数を定義します。
    with open(os.path.join(output_folder, file_name), 'w') as file:  # 指定されたパスのファイルを書き込みモードで開きます。
        for copy_file in copy_files:  # 抽出したファイル名のリストをループします。
            file.write(copy_file + '\n')  # 各ファイル名を出力ファイルに書き込みます。

def main(input_path, output_folder):  # メインの関数を定義します。
    if os.path.isdir(input_path):  # 入力パスがディレクトリであるかどうかを確認します。
        cobol_files = glob.glob(f"{input_path}/**/*.cbl", recursive=True)  # ディレクトリ内のすべての.cblファイルを取得します。
    else:
        cobol_files = [input_path]  # 入力パスがディレクトリでない場合（つまり、ファイルである場合）、そのパスをリストに保存します。

    for file_path in cobol_files:  # 取得したすべての.cblファイルをループします。
        copy_files = extract_copy_files(file_path)  # 各ファイルからCOPY句が参照しているファイル名を抽出します。
        file_name = os.path.basename(file_path)  # ファイルのベース名（パスからディレクトリ部分を除いた部分）を取得します。
        write_to_file(output_folder, file_name, copy_files)  # 抽出したファイル名を出力ファイルに書き込みます。

if __name__ == "__main__":  # スクリプトが直接実行された場合（つまり、インポートされた場合ではない場合）に、以下のコードを実行します。
    main(sys.argv[1], sys.argv[2])  # メインの関数を呼び出します。コマンドライン引数をそのまま渡します。


'''
07_CBL_COPY句の利用状況
python3.10のスクリプトを作ってください。
COBOLのソースコードから、利用しているCOPY句を出力する
引数1 COBOLのソースコードのファイル名またはフォルダ
引数2 結果の出力先フォルダ

引数1がフォルダの場合、フォルダの下のファイルすべてを調べる



COPYという文字列を含む変数がある可能性があります。考慮してください


COPY句で読み込むファイルのみを出力して

出力するのはCOPY句の名前までで、最後の.などは出力抑止してください

python初心者用に各行に詳細なコメントを追加してください。また長いディスクレーマーは表示しないでください
'''


