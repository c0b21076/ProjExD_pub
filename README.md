# プロジェクト演習Ⅰ・テーマD
## 第1回
### 環境構築

## 第2回
### tkinterで電卓実装
#### 追加機能 (branch名:calculate)
- 四則演算ボタン:=を入力した際に四則演算を行う
- クリアボタン:entryに入力していた数字をdeleteする
- 割合ボタン:entryに入力していた数字を%表示する
- 2乗ボタン:entryに入力していた数字を2乗する

## 第3回
### tkinterで迷路ゲーム実装
#### 3限：基本機能
- ゲーム概要：
    - rensyu03/maze.pyを実行すると、1500x900のcanvasに迷路が描画され，迷路に
      沿ってこうかとんを移動させるゲーム
    - 実行するたびに迷路の構造は変化する
- 操作方法：矢印キーでこうかとんを上下左右に移動する
- プログラムの説明
    - maze_makerモジュールのshow_maze関数でcanvasに迷路を描画する
    - PhotoImageクラスのコンストラクタとcreate_imageメソッドでこうかとんの画像を(1, 1)に描画する
    - bindメソッドでKeyPressにkey_down関数を，KeyReleaseにkey_up関数を紐づける
    - main_proc関数で矢印キーに応じて，こうかとんを上下左右に1マス移動させる
#### 4限：追加機能
- 実行するたびにこうかとんの画像が変わる
- 進む方向が壁か床か判断し床ならば進む
- スタート地点とゴール地点の色をわかりやすく変えた

## 第4回
### Pygameでゲーム実装
#### 3限：基本機能
- ゲーム概要：
- rensyu04/dodge_bomb.pyを実行すると，1600x900のスクリーンに草原が描画され，こうかとんを
移動させ飛び回る爆弾から逃げるゲーム
- こうかとんが爆弾と接触するとゲームオーバーで終了する
- 操作方法：矢印キーでこうかとんを上下左右に移動する
- プログラムの説明
- dodge_bomb.pyをコマンドラインから実行すると，pygameの初期化，main関数の順に処理が進む
- ゲームオーバーによりmain関数から抜けると，pygameの初期化を解除し，プログラムが終了する
- main関数では，clockの生成，スクリーンの生成，背景画像の描画，こうかとんの描画，爆弾の描画
を行う
- main関数の無限ループでは，キー操作に応じたこうかとんの移動，指定速度に応じた爆弾の移動を
行う
- Rectクラスのcolliderectメソッドにより，こうかとんと爆弾の接触を判定する
- check_bound関数では，こうかとんや爆弾の座標がスクリーン外にならないようにチェックする

#### 4限：追加機能
- 開始時に爆弾の座標がこうかとんの上にならないようにした
- 開始直後に終了しないように爆弾の位置によって爆弾の動く向きを変更した
- 壁に爆弾が当たるたびに爆弾のサイズが大きくなるように変更したかったができなかった

## 第5回
### Pygameでゲーム実装
#### 4限：追加機能
- 開始直後に爆弾がこうかとんに直撃して終了することがないように爆弾の生成位置によって
爆弾の初期移動方向が変化するメソッドspeed()をBombクラスに加えた

## 第6回
### Pygameでゲーム実装
#### 45限：ゲーム作成
- ゲーム概要：
  - こうかとんを操作し、UFOをかわしつつ倒すシューティングゲーム
  - こうかとんがUFOに接触すると残機が1減る
  - 3回接触すると残機がなくなりゲーム終了
  - こうかとんは卵を発射することでUFOを攻撃することができる
  - UFOを倒すことでスコアを稼ぐ
- 操作方法：
  - ENTERキーでゲーム開始
  - WASDキーでこうかとんを移動
  - SPACEキーで卵発射
  - ESCAPEキーでゲーム終了
- プログラムの説明：
  - game.pyを実行するとGameクラスが開始
  - Gameクラス
    - Gameクラス内でクロックの生成、画面の生成が行われる
    - game_start_screen関数はスタート画面の描画用
    - game_over_screen関数は終了画面の描画用
    - main関数内ではループを用いてこうかとんなどの描画やキー操作に応じた移動を行う
    - フラグによりゲームの状態を判定し、スタート画面や終了画面等の表示を行う
  - Backgroundクラス
    - 背景画像のロードを行う
    - 背景のスクロール設定をすることで画面の端に来たら反対側に表示されるようにする
  - Planeクラス
    - Planeクラス内ではこうかとんの動きの制御を行う
    - 通常時、無敵状態時、残機の画像をリストに格納
    - 敵と接触時に回転するように角度を変えたものをリストに格納
    - 現在の状態を判定するためのフラグを設定
    - draw_lives関数で残機を描画
    - change_img関数でフラグ(状態)に合わせて描画する画像を選択
    - create_bullet関数で弾丸を生成するクラスの呼び出しを行う
    - update関数でchange_img関数の呼び出しと、キー操作によるこうかとんの座標の変化、接触時の座標の変化を行う
  - Bullet
    - 弾丸の画像のロード
    - update関数で弾丸の座標の変化を行う
  - Mob
    - 敵キャラの画像をロード
    - 敵キャラのサイズをランダムで変化するように
    - 敵キャラの初期位置をランダムで変化するように
    - update関数で敵キャラの座標の変化を行う  
- 参考資料：
- https://pythonmemo.com/pygame/pygame002  

## 第7回
### Pygameでゲーム実装
#### 45限：ゲーム作成
- ゲーム概要：
  - こうかとんを操作し、UFOをかわしつつ倒すシューティングゲーム
  - こうかとんがUFOに接触すると残機が1減る
  - 3回接触すると残機がなくなりゲーム終了
  - こうかとんは卵を発射することでUFOを攻撃することができる
  - UFOを倒すことでスコアを稼ぐ
  - 特定の点数稼ぐことでクリアすることができる
- 操作方法：
  - ENTERキーでゲーム開始
  - WASDキーでこうかとんを移動
  - SPACEキーで卵発射
  - ESCAPEキーでゲーム終了
- プログラムの説明：
  - game.pyを実行するとGameクラスが開始
  - Gameクラス
    - Gameクラス内でクロックの生成、画面の生成が行われる
    - game_start_screen関数はスタート画面の描画用
    - game_over_screen関数は終了画面の描画用
    - main関数内ではループを用いてこうかとんなどの描画やキー操作に応じた移動を行う
    - フラグによりゲームの状態を判定し、スタート画面や終了画面等の表示を行う
  - Backgroundクラス
    - 背景画像のロードを行う
    - 背景のスクロール設定をすることで画面の端に来たら反対側に表示されるようにする
  - Planeクラス
    - Planeクラス内ではこうかとんの動きの制御を行う
    - 通常時、無敵状態時、残機の画像をリストに格納
    - 敵と接触時に回転するように角度を変えたものをリストに格納
    - 現在の状態を判定するためのフラグを設定
    - draw_lives関数で残機を描画
    - change_img関数でフラグ(状態)に合わせて描画する画像を選択
    - create_bullet関数で弾丸を生成するクラスの呼び出しを行う
    - update関数でchange_img関数の呼び出しと、キー操作によるこうかとんの座標の変化、接触時の座標の変化を行う
  - Bullet
    - 弾丸の画像のロード
    - update関数で弾丸の座標の変化を行う
  - Mob
    - 敵キャラの画像をロード
    - 敵キャラのサイズをランダムで変化するように
    - 敵キャラの初期位置をランダムで変化するように
    - update関数で敵キャラの座標の変化を行う  
    - 今回のアップデートで敵が球を打つようになった
  - sound関数
    - 音が出るようになった
- 参考資料：
- https://pythonmemo.com/pygame/pygame002
