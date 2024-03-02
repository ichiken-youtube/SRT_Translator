import sys
import re
import deepl
import settings

# DeepL APIキーを設定
translator = deepl.Translator(settings.DEEPL_API_KEY)

def translate_subtitle(input_file):
    output_file = input_file.rsplit('.', 1)[0] + "_EN.srt"

    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    content = content + '\n\n'
    # 字幕のテキスト部分を抽出
    pattern = re.compile(r'\d+\n\d{2}:\d{2}:\d{2}.\d{3} --> \d{2}:\d{2}:\d{2}.\d{3}\n(.*?)\n\n', re.DOTALL)
    matches = pattern.findall(content)

    translated_content = content
    print(matches)
    for text in matches:
        print(text)
        if len(text) == 0:
            continue
        # テキストを英語に翻訳
        result = translator.translate_text(text, source_lang="JA", target_lang="EN-US")
        #result = text
        #print(result)
        translated_content = translated_content.replace(text, result.text, 1)

    # 翻訳された内容を新しいファイルに書き出し
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(translated_content)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python translate_srt.py [srt file path]")
    else:
        translate_subtitle(sys.argv[1])
