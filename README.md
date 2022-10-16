# nai2sd-Converter
NovelAIのプロンプトをSDwebUI用に変換するカスタムスクリプトです。
- NovelAIの{word}や[word]をSDwebUI用の倍率の(word:x)に変換
- 入れ子構造の括弧への対応
- '('や')'の前にバックスラッシュを付ける
が特徴です
# インストール
nai2sd_Converter.pyをダウンロードして、ローカルのwebUIフォルダ直下にあるscriptsファイルの中に入れてください
# 注意
```
{aaa,bbb,{ccc}}
```
のような、外側に括弧がついている入力には対応していません（現状意味がないと思うので）。
また、括弧の左右が同じ数でない場合は、おかしな変換が出てくるか
```
"SyntaxError:probably, your '{' and '}', or '[' and ']' are not same number"
```
と出ます。