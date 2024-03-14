import sys
import re
import deepl
import PySimpleGUI as sg
import settings

# DeepL APIキーを設定
translator = deepl.Translator(settings.DEEPL_API_KEY)

languages = ['EN-US','ZH']
filepath=''

def translate_subtitle(input_file,language,dict=''):
    output_file = input_file.rsplit('.', 1)[0] + "_"+language+".srt"

    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    #最終行が正規表現にマッチしないので改行追加
    content = content + '\n\n'
    # 字幕のテキスト部分を抽出
    pattern = re.compile(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n(.*?)\n\n', re.DOTALL)
    matches = pattern.findall(content)

    translated_content = content
    #print(matches)
    for text in matches:
        print('\nSource : '+text)
        if len(text) == 0:
            continue
        result=''
        if len(dict)>0:
            # テキストを英語に翻訳
            result = translator.translate_text(text, source_lang='JA', target_lang=language,glossary=dict)
        else:
            result = translator.translate_text(text, source_lang='JA', target_lang=language)
        print('Result : '+result.text)
        translated_content = translated_content.replace(text, result.text, 1)

    # 翻訳された内容を新しいファイルに書き出し
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(translated_content)
        print('\nファイル出力完了' + output_file)

def get_glossaries():
    '''Glossaryのリストを取得する'''
    glossaries = translator.list_glossaries()
    return [(glossary.name, glossary) for glossary in glossaries]

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]

    usage = translator.get_usage()
    API_status = ''
    if usage.any_limit_reached:
        print('Translation limit reached.')
        exit(1)
    if usage.character.valid:
        API_status = f"Character usage: {usage.character.count} of {usage.character.limit}"
    if usage.document.valid:
        API_status = f"Document usage: {usage.document.count} of {usage.document.limit}"
    # Glossaryリストの取得
    glossary_list = get_glossaries()
    glossary_names = [[glossary[1].target_lang,glossary[0]] for glossary in glossary_list]

    button_col = [
        [sg.Button('表示', key = '-DISPLAY-')],
        [sg.Button('更新', key = '-UPDATE-')],
        [sg.Text('')],
        [sg.Button('削除', key = '-DEL-BUTTON-')]
    ]

    frame1 = sg.Frame('',
        [
            [
                sg.Table(values=glossary_names, headings=['言語','辞書'], col_widths=[6,10],auto_size_columns=False, key='-GLOSSARY-LIST-',justification='left'),
                sg.Column(button_col)
            ],
            [
                sg.Input('言語', key='-GLOSSARY-LANG-', size=(10,50)),
                sg.Input('辞書名', key='-GLOSSARY-NAME-', size=(10,50)),
                sg.Text('->')
            ]
        ] ,
        size=(240, 225) #幅,高さ
    )

    frame2 = sg.Frame('',
        [
            [sg.Table(values=[],headings=["Source", "Target"], col_widths=[15,15], auto_size_columns=False, key='-WORD-TABLE-')],
            [
                sg.Input('原語', key='-SOURCE-WORD-', size=(10,50)),
                sg.Text('->'),
                sg.Input('翻訳', key='-TARGET-WORD-', size=(10,50)),
                sg.Button('登録', key = '-ADD-BUTTON-')
            ]
        ],
        size=(300, 225) #幅,高さ
    )

    # GUIレイアウトの定義
    layout = [
        [
            frame1,
            frame2
        ],
        [
            sg.Text(API_status)
        ],
        [
            sg.Input(filepath, key = '-FILE-PATH-'),
            sg.FileBrowse('srtファイル選択',key="file")
        ],
        [
            sg.Combo(languages,default_value=languages[0],key='-LANGUAGE-COMBO-'),
            sg.Checkbox('辞書を利用する', key = '-USE-GLS-'),
            sg.Button('翻訳実行', key = '-RUN-')
        ]

    ]

    # ウィンドウの作成
    window = sg.Window('SRT Traslator', layout)
    # イベントループ
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '-DISPLAY-':
            # 選択されたGlossary名を取得
            if values['-GLOSSARY-LIST-']:
                window['-GLOSSARY-LANG-'].update(glossary_names[values['-GLOSSARY-LIST-'][0]][0])
                window['-GLOSSARY-NAME-'].update(glossary_names[values['-GLOSSARY-LIST-'][0]][1])
                selected_glossary_name = glossary_names[values['-GLOSSARY-LIST-'][0]][1]
                for name, glossary in glossary_list:
                    if name == selected_glossary_name:
                        # Glossaryに登録された単語を取得して表示
                        words = translator.get_glossary_entries(glossary)
                        #print([[key, value] for key, value in words.items()])
                        window['-WORD-TABLE-'].update([[key, value] for key, value in words.items()])
        
        elif event == '-RUN-':
            if values['-USE-GLS-']:
                if values['-GLOSSARY-LIST-']:
                    print('辞書を使用します。 '+glossary_names[values['-GLOSSARY-LIST-'][0]][1])
                    translate_subtitle(values['-FILE-PATH-'],values['-LANGUAGE-COMBO-'],glossary_list[values['-GLOSSARY-LIST-'][0]][1].glossary_id)
                else:
                    print('辞書を選択してください。')
            else:
                translate_subtitle(values['-FILE-PATH-'],values['-LANGUAGE-COMBO-'])

        elif event == '-ADD-BUTTON-' and len(values['-GLOSSARY-NAME-'])>0:
            word_dic = {}
            if len(values['-GLOSSARY-LIST-'])>0:
                if values['-GLOSSARY-NAME-'] == glossary_names[values['-GLOSSARY-LIST-'][0]][1]:
                    for name, glossary in glossary_list:
                        if name == selected_glossary_name:
                            # Glossaryに登録された単語を取得して表示
                            word_dic = translator.get_glossary_entries(glossary)
                            translator.delete_glossary(glossary)
                            break
            my_glossary = translator.create_glossary(
                values['-GLOSSARY-NAME-'],
                source_lang='JA',
                target_lang=values['-GLOSSARY-LANG-'],
                entries=word_dic | {values['-SOURCE-WORD-']:values['-TARGET-WORD-']}
            )
            print(
                f"Created '{my_glossary.name}' ({my_glossary.glossary_id}) "
                f"{my_glossary.source_lang}->{my_glossary.target_lang} "
                f"containing {my_glossary.entry_count} entries"
            )
            if len(word_dic) == 0:#追加/新規辞書
                #words = translator.get_glossary_entries(glossary)
                window['-WORD-TABLE-'].update([glossary[0] for glossary in get_glossaries()])
            window['-WORD-TABLE-'].update([[key, value] for key, value in (word_dic | {values['-SOURCE-WORD-']:values['-TARGET-WORD-']}).items()])
            
            glossary_list = get_glossaries()
            glossary_names = [[glossary[1].target_lang,glossary[0]] for glossary in glossary_list]

        elif event == '-DEL-BUTTON-':
            for glossary in translator.list_glossaries():
                if glossary.name == values['-GLOSSARY-NAME-']:
                    translator.delete_glossary(glossary)
                    print('辞書削除完了 '+glossary.name)

        elif event == '-UPDATE-':
            glossary_list = get_glossaries()
            glossary_names = [[glossary[1].target_lang,glossary[0]] for glossary in glossary_list]
            window['-GLOSSARY-LIST-'].update([[glossary[1].target_lang,glossary[0]] for glossary in glossary_list])
            print('リスト更新完了')

    # ウィンドウを閉じる
    window.close()

