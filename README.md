# readlvm

LVMファイルを読み取り、YAMLフォーマットに変換する。
結果はstdoutに出力する。

```sh
python -m readyaml [OPTIONS] LVM_FILE [> OUTPUT_FILE]
```

## オプション

- `-e=ENCODING`, `--encoding=ENCODING`
  LVMファイルのエンコーディング。使用可能なエンコーディングについては、https://docs.python.org/ja/3.8/library/codecs.html を参照してください。省略された場合`"utf-8"`を使う。

- `-c=COL_LIST`, `--columns=COL_LIST`
  指定されたデータ列以外を破棄する。`COL_LIST`は列番号（1始まり）をカンマで区切った文字列。

## LVMファイルについて

次の形式のLVMファイルを読み取ることができる。

```
1行目: タイトル
2-(n-1)行目: Tab/半角スペースで区切られたKeyとValueの組
n行目: Tab/半角スペースで区切られた1つまたは3つ以上のデータラベル
n+1行目以降: Tab/半角スペースで区切られた1つまたは3つ以上のデータ（先頭1つと、末尾は省略可能）
ただし ***Comment*** の行はコメント
```

LVMファイルの例:

```
LabVIEW Measurement
Writer_Version	2
Reader_Version	2
***End_of_Header***
X_Value 電圧 Comment
	-10.530330
	-10.530330
```
