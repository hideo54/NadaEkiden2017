# 灘校駅伝大会2017

灘校の駅伝大会の際、各選手のタイムを正確に記録するためのプログラムです。タスキに貼られているNFCタグを利用します。

## 必要な環境

* Python 2系
* nfcpy
* FeliCaカードを読み取り可能なNFCリーダー

## 大会前の準備

1. `salt.txt`に任意の文字を記入(改行なし)
2. `python writer.py [タスキ番号]`を実行し、該当するタスキのNFCタグを当てる

## 大会時

`python reader.py`を実行すると、タスキのNFCタグが当てられる度にタイムが出力されます。

## 作成者

@hideo54

### 連絡先

* E-mail: contact@hideo54.com
* Twitter: @hideo54
