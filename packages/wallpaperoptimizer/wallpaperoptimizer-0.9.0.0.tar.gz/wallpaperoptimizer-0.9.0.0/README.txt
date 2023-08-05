
【wallpaper optimizer】
  ～wallpaperoptimizer is wallpaper changer for multi screen.～

													Katsuhiro Ogikubo
													oggyist@gmail.com

1.はじめに
  wallpaper optimizerは、マルチモニタ使用下において壁紙を最適に配置する
  プログラムです。以下の動作モードと機能を備え、Linuxで動作します。

  ＜動作環境＞
  ・以下のデスクトップにて試しています
    GNOME2
    Unity(GNOME3)
    GNOME shell(GNOME3)
    Xfce4
    LXDE
    
  ・以下のディストリビューションにて試しています
    CentOS 6.3
    Ubuntu12.04 LTS
    Ubuntu12.10
    Ubuntu13.04
    Linux mint 14
    Linux mint 17
    Xubuntu(Ubuntu12.10)
    Lubuntu(Ubuntu12.10)
    Ubuntu GNOME shell Remix 12.10

  ＜動作モード＞
  ・コンソールより各種パラメータを指定して、壁紙を作成・設定
  ・コンソール下にて、指定時間ごとに壁紙を変更
  ・GNOMEパネルに配置するGNOMEアプレットとして動作(GNOME2)
  ・インジケータアプリとしての動作(GNOME3, Xfce4, LXDE)

  ＜機能＞
  ・画像を２つ指定し、モニタサイズと画像サイズから最適配置を行えます
  ・モニタに対しての画像配置を左右モニタごとに、上寄せ・下寄せ（左右）などと指定できます
  ・モニタ端からのマージンを指定できます（ウィジットの配置領域確保などに）
  ・チェンジャーのOn/Offをパネル上から変更できます(GNOME2のみ)
  ・壁紙設定は画像１つの指定でも動作できます
  
  また、以下のような機能は実装できていません。
  ・モニタを回転、縦置きで使用している場合
  ・アプレットモードでのヘルプ


2.インストール
  $ sudo pip install wallpaperoptimzer


3.アンインストール
  $ sudo pip uninstall wallpaperoptimzer


4.展開ディレクトリ
  setup.pyをご覧ください。
  実行時に、$HOME/.local/share/wallpaperoptimzierにログファイルを作成します。
  壁紙ファイル（保存ファイル名を指定しない場合など）は、
  $HOME/.local/share/wallpaperoptimzierに作成されます。


5.起動方法
5.1.コンソールでの実行例
  $ wallpaperoptimizer 2560x1920.jpg 1500x844.jpg -C

   事前に、~/$HOME/.local/share/wallpaperoptimizer/.walloptrcとのファイルを設置してください。
   例）
     1920x1080,left,~/Wallpaper/1920/
     1280x1024,right,~/Wallpaper/1280/

   設置しない場合は、引数「--display 1920x1080,1280x1024」の指定が必要です。

5.2.コンソールからの壁紙チェンジャー実行例
  $ wallpaperoptimizer -D -i 3600 &

5.3.GNOMEアプレットとしての実行
  GNOMEパネル上の任意箇所で右クリックし、「パネルへ追加」を選択。
  「Wallpaperoptimizer Applet」を選択。

5.4 インジケータアプリとしての実行
  インストールされたパスに応じて、以下のように実行してください。
  $ /usr/local/bin/wallpaperoptimiz &
      or
  $ /usr/bin/wallpaperoptimiz &


6.使いかた
6.1. コンソール
  ヘルプをご覧ください。
  $ wallpaperoptimizer -h または --help

6.2. アプレット／インジケータアプリ
  最初に起動されるメインウィンドウ内のボタン配置が、モニタを左右に配置したイメージ
  になります。マージンについてはワークスペース全体への指定となります。
  また、メインウィンドウの下に並ぶボタンが各操作ボタンです。ボタンによっては設定を
  行わないと有効にならないものがあります。


7.開発環境
  /etc/redhat-release
	Linux mint17
  uname -r
	3.13.0-24-generic
  関連してそうなdeb
    python-imaging
    python-glade2,
    libglade2-0
    python-gtk2

8.ライセンス
  GPLv3

9.使用ライブラリ
The Python Imaging Library is:
    Copyright © 1997-2005 by Secret Labs AB
    Copyright © 1995-2005 by Fredrik Lundh
    プログラム中でマルチバイト文字列を使っている箇所を取りやめ

10.変更履歴
v0.9.0.0 (2014.09.26) 0.9.0版リリース
 Linux mint 17への開発環境の変更およびXfce4(4.10.1)の仕様変更に対応

v0.8.2.0 (2014.04.07) 0.8.2版リリース
 xfconf-query xinerama-stretchの設定方法に誤りがあったのを修正

v0.8.1.0 (2013.08.10) 0.8.1版リリース
 PyPIに登録
 マルチバイト文字を埋め込んでいる処理を廃止

v0.8.0.0 (2013.04.06) 0.8版リリース
 Xfce4,LXDEに対応
 アイコンを新規に作成
 .desktopファイルを同梱

v0.7.0.1 (2013.02.12) 0.7版リリース
 プログラム構造について内部変更を実施

v0.6.0.0 (2013.02.12) 0.6版リリース
 GNOME3デスクトップ(Ubuntu Unityに対応)
 パッケージ配布のバグを修正
 設定ボタン周辺挙動の修正

v0.5.0.0 (2012.10.07) 0.5版リリース
 同じサイズの場合マージンを考慮した縮小が行われておらず、マージンが取れない問題を修正

v0.4.0.0 (2012.08.06) 0.4版リリース
 1画面のみの指定時は、各種設定ができずいきなり壁紙化する動作だったのを改善。

v0.3.0.0 (2012.07.09) 0.3版リリース無し
 python2.6下での開発に移行
 x86_64インストレーションに対応 (/usr/lib64/...)

v0.2.0.0 (2012.02.01) 初版(人柱版)リリース
