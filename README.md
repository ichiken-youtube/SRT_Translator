# SRT_Translator
本ツールは字幕用SRTファイルを翻訳するツールです。  
SRTファイルのフォーマットを保ったまま翻訳できる点が特徴です。  
また、事前に設定した単語帳により固有名詞などの翻訳精度を上げることができます。  

# セットアップ
必要なライブラリのインストール  
`pip install PySimpleGUI deepl`  

本リポジトリのルートディレクトリに設定ファイル`settings.py`を作成し、DeepLのAPIキーを以下のように記入してください。  
`DEEPL_API_KEY = "xxxxxxxx-xxxx-......:fx"`

# 今後の更新予定
現状、日本語→英語(米)の翻訳しかできないので、DeepLが対応している任意の言語に対応予定