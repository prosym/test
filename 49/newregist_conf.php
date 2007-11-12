<?php
//EOM及びEOM;は消去不可です。その間のみhtml記述可能

//config ---------------------------------------------------
$script    ='newregist.php';  /* 実行ファイル名 */
$LogFile   ='/home/hidden/49/newregist.log';  /* ログ保存ファイル名 セキュリティ注意 */
$mheaders = "From: prosym49@ipsj.or.jp";
$mparams = "-f webmaster@kitty.watalab.cs.uec.ac.jp";
$mtoaddr = "prosym49@ipsj.or.jp";
$msubject = "49th programming symposium registration";
$mheader = "第49回プログラミングシンポジウムへの登録を\n以下の通りに受け付けました．";

/* 必須=1, not=0 */
$Needname = 1; //氏名
$Needkana = 1; //カナ氏名
$Needsex  = 1; //性別
$Needorg  = 0; //所属
$Needemail= 1; //メール
$Needaddr = 1; //住所
$Needphone= 0; //電話番号
$Needsent = 1; //送付区分
$Needenter= 1; //参加資格
$Needroom = 1; //希望する部屋
$Needatena= 0; //領収書の宛名
$Needrcpt = 1; //領収書
$Needsmoke= 1; //喫煙の調査

$Payment1='郵便振替 00150-4-83484';
$Payment2='銀行振込 みずほ銀行 虎ノ門支店 普通 1013945';
$Payment3='銀行振込 東京三菱銀行 本店 普通 7636858';

$Stay1='１名部屋            ';
$Stay1cost='（会員 ￥67,000  非会員 ￥73,000）';
$Stay2='２名部屋            ';
$Stay2cost='（会員 ￥47,000  非会員 ￥53,000）';
$Stay3='３名部屋            ';
$Stay3cost='（会員 ￥40,000  非会員 ￥46,000）';
$Stay4='４名部屋（学生に限る）';
$Stay4cost='（会員 ￥29,000  非会員 ￥35,000）';

$Bgcolor   ='#ffffff';   /* 壁色設定           */
$Fontsize  ='10pt';      /* 基本フォントサイズ */
$Textcolor ='#333333';   /* 基本文字色         */
$Errorcolor='#C00000';   /* エラー文字色       */
$Linkcolor ='#89796B';   /* 未リンクカラー     */
$Linkvisit ='#89796B';   /* 済リンクカラー     */
$Linkactive='#A3879E';   /* Click時カラー      */
$Linkhover ='#A3879E';   /* onMouse時カラー    */
$Tableborder='#89796B;';
$ReturnURL ='http://www.ipsj.or.jp/prosym/';  /* 戻りURL            */

$t_border  ='#89796B';   /* ログ出力画面borderカラー */

//header ---------------------------------------------------
	$HEADER= <<<EOM
<html><head><style type="text/css"><!--
   body      {background-color:$Bgcolor;line-height:130%;
              color:$Textcolor;font-size:$Fontsize;}
   td        {color:$Textcolor;font-size:$Fontsize;}
   .error    {color:$Errorcolor;font-weight:bold;}
   .key      {color:$Errorcolor;}
   .t_border {background-color:$t_border;}
    a:link   {color:$Linkcolor;}
    a:visited{color:$Linkvisit;}
    a:active {color:$Linkactive;}
    a:hover  {color:$Linkhover;}
-->
</style>
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Cache-Control" content="no-cache">
<meta http-equiv="Expires" content="Sun, 11 Nov 2007 16:00:00 GMT">
</head><body>
EOM;

//title ----------------------------------------------------
	$TITLE= <<<EOM
<h1><img border="0" src="../img/mark2.gif" width="115" height="96"></h1>
<p align="right"><a href="http://www.ipsj.or.jp/prosym/">
「プログラミング・シンポジウム」</a>へ戻る</p>
<h1>プログラミング・シンポジウム 参加申込み</h1>
EOM;

//notice ---------------------------------------------------
	$NOTICE = <<<EOM
<ul>
  <li> 会場では参加費を受け取りません．お手数ですが，郵便振替，銀行振込み，現金書留などの手段で，事前に参加費の払込みを済ませるようお願いします．
  <li> 参加申込者には，請求書，参加章引換券，振替用紙を郵送します．振替用紙を使って郵便局で払い込む場合は，手数料は無料です．それ以外の振込み方法の場合は，送金連絡票に必要事項を記入して，上記照会先にご連絡ください．
  <li> <font color=#ff0000>振込み締切日：12月21日（金）</font>
  <li> 部屋割りは学会におまかせください．
  <li> 会費は参加費と宿泊食事費に分けられます．参加費には予稿集代，消費税を含みます．宿泊食事費には，宿泊代，食費，消費税を含みます．宿泊なしの参加は認められません．
  <li> 複数の身分をお持ちの方は，高い方の料金を適用させていただきます．
  <li> 学生/65歳以上 の登壇（ポスター含む）発表者は参加費から 12,000円/6,000円 引きになります．
  <li> 参加される方（特に学生）で非会員の方は，この機会に入会されることをお勧めします．学生会員の年会費は 4,800円です．詳しくは <a href="http://www.ipsj.or.jp/06mem/kaiin/kaiin.html"> http://www.ipsj.or.jp/06mem/kaiin/kaiin.html</a>を参照ください．
  <li> 参加申込み後やむを得ず参加を取り消される場合は，参加者募集ページの照会先まで連絡をお願いします．取消しの連絡のない場合は，会費は原則お返ししません．
  <li> 発表者の方も参加申込みが必要です．
  <li> 会場，宿泊施設の都合で，お申込みに応じかねる場合がありますので，あらかじめご了承ください．
  <li> 開催期間中の中途での出入りや，人員の交替はご遠慮ください．（やむを記得な
い場合は幹事にご相談ください．）
  <li> プログラムは <a href="49program.html">ここ</a>にあります．
  <li> <font color=#0000ff>申込み内容の改訂の際にはブラウザの「戻る」機能はお使いにならず，最初から書き直されるようお願いいたします．</font>
  <li> <font color=#0000ff>申込み内容の改訂をされる際に，ブラウザやプロキシのキャッシュが障害になることがあります．その場合はブラウザでキャッシュをパージする操作や設定を行うか，あるいはプロキシを使わない設定にしてください．（「Proxy error」の無限ループに陥った場合は，ブラウザ再起動で抜け出せます．）</font>
  <li> 「※」は必須項目を表します．
</ul>
EOM;

//footer ---------------------------------------------------
	$FOOTER= <<<EOM
</body></html>
EOM;

?>
