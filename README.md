次の形式のファイルを読み取り、値を圧縮する。

```
1行目: タイトル
2-(n-1)行目: Tab/半角スペースで区切られたKeyとValueの組
n行目: Tab/半角スペースで区切られたデータラベル
n+1行目以降: Tab/半角スペースで区切られたデータ
ただし ***Comment*** の行はコメント
```

ファイルの例:

```
LabVIEW Measurement
Writer_Version	2
Reader_Version	2
***End_of_Header***
X_Value 電圧 Comment
	-10.530330
	-10.530330
```

圧縮の例（2列目に注目）:

```yaml
- [-10.530330, 6]
- 10.627565
- 8.069195
- -2.686037
- -4.602555
- -6.135511
- -7.340438
- -8.075276
- -8.678385
- -9.207881
- -10.053784
- [-10.530330, 100]
```

コマンド実行の例:

```sh
readlvm source.lvm:2 out.yaml
```
