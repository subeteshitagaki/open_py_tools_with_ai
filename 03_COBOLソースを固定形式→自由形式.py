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


'''
固定形式のCOBOLソースを自由形式にするpython3.10のスクリプトです。

Copilotのプロンプト

COBOLのソースコードの書き方って、自由形式となんでしたか？

固定形式のCOBOLのソースコードを自由形式に変換するpython3.10スクリプトを作ってください

コメントは、行コメントとして、変換してください

自由形式の行コメントは

では、行コメント開始は文字列は*>を使ってください

1つの命令を複数行に分けて、コーディングしている場合、自由形式にする際に、1行にしてください

「命令が複数行に分かれている場合は、それらを1行にまとめます」は具体的にはどのように実装していますか？

IF文の中など、ピリオドで1つの命令が終わらない場合を考慮してください

違います。ピリオドで命令の区切りを判断するのをやめてください。

複数行に分かれた命令を１行にまとめ方を教えてください

複数行に分かれた命令を１行にまとめるときに、命令文の区切りで改行する場合についても対応してください。

やっぱり、継続行は1行にまとめて、複数行に分かれた命令を１行にまとめないでください

7文字目に-がある場合、前の行からの継続行としてください。

'''
