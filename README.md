# パーティクルフィルタを用いた PDR+マップマッチングの自己位置推定

## 実行方法

### 仮想環境にログイン

```bash
pipenv shell
```

### パーティクルフィルタの実行

```bash
python main.py
```

## 自身で用意したデータを用いてパーティクルフィルタを実行

入力できるパラメータの組み合わせによって二通りあります

### フロアマップ＋ジャイロセンサ

[`track_real` 関数](https://github.com/kajiLabTeam/particle-filter/blob/205c1d1808996fd62f61740123fa1d10da3672e6/main.py#L35)にフロアマップのファイルパス・ジャイロセンサのファイルパス・出力先のファイルパス（二種類）を入力します

ジャイロセンサの生データに必要なカラムは[こちらの CSV](https://github.com/kajiLabTeam/particle-filter/blob/main/data/gyroscope/gyro1.csv)を参考にしてください

### フロアマップ＋自身で設定した座標・角度の変化量・歩幅

[`track_ideal` 関数](https://github.com/kajiLabTeam/particle-filter/blob/0e17d52f353a847d433ba1bd8dd2aea2a80712c3/main.py#L93)にフロアマップのファイルパス・自身で作成した座標＆歩行情報（Python 変数）・出力先のファイルパス（二種類）を入力します

自身で作成した座標＆歩行情報の形式は[こちらのファイル](https://github.com/kajiLabTeam/particle-filter/blob/0e17d52f353a847d433ba1bd8dd2aea2a80712c3/config/const/coordinate.py#L4)を参考にしてください

## 参考資料

### ドメインモデル

[こちらから〜](https://kjlb.esa.io/posts/5570)

### アルゴリズムの詳細

[こちらから〜](https://kjlb.esa.io/#path=%2F%E3%83%97%E3%83%AD%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%2F%E3%83%93%E3%83%83%E3%82%B0%E3%83%87%E3%83%BC%E3%82%BF%E3%82%92%E7%94%A8%E3%81%84%E3%81%A6%E5%B1%8B%E5%86%85%E6%8E%A8%E5%AE%9A%E3%81%AE%E7%B2%BE%E5%BA%A6%E5%90%91%E4%B8%8A%E3%81%95%E3%81%9B%E3%82%8B%E8%94%B5%2F%E3%83%91%E3%83%BC%E3%83%86%E3%82%A3%E3%82%AF%E3%83%AB%E3%83%95%E3%82%A3%E3%83%AB%E3%82%BF%E3%81%A8PDR%E3%81%A8%E3%83%9E%E3%83%83%E3%83%97%E3%83%9E%E3%83%83%E3%83%81%E3%83%B3%E3%82%B0%2F%E3%82%A2%E3%83%AB%E3%82%B4%E3%83%AA%E3%82%BA%E3%83%A0)

### 今までの実行結果

[こちらから〜](https://kjlb.esa.io/#path=%2F%E3%83%97%E3%83%AD%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%2F%E3%83%93%E3%83%83%E3%82%B0%E3%83%87%E3%83%BC%E3%82%BF%E3%82%92%E7%94%A8%E3%81%84%E3%81%A6%E5%B1%8B%E5%86%85%E6%8E%A8%E5%AE%9A%E3%81%AE%E7%B2%BE%E5%BA%A6%E5%90%91%E4%B8%8A%E3%81%95%E3%81%9B%E3%82%8B%E8%94%B5%2F%E3%83%91%E3%83%BC%E3%83%86%E3%82%A3%E3%82%AF%E3%83%AB%E3%83%95%E3%82%A3%E3%83%AB%E3%82%BF%E3%81%A8PDR%E3%81%A8%E3%83%9E%E3%83%83%E3%83%97%E3%83%9E%E3%83%83%E3%83%81%E3%83%B3%E3%82%B0%2F%E7%B5%90%E6%9E%9C)
