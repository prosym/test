<?php
//EOM及びEOM;は消去不可です。その間のみhtml記述可能

//config ---------------------------------------------------
$script    ='newregist.php';  /* 実行ファイル名 */
$LogFile   ='/home/hidden/48/newregist.log';  /* ログ保存ファイル名 セキュリティ注意 */
$mheaders = "From: prosym48@ipsj.or.jp";
$mparams = "-f webmaster@kitty.watalab.cs.uec.ac.jp";
$mtoaddr = "prosym48@ipsj.or.jp";
$msubject = "48th programming symposium registration";
$mheader = "第48回プログラミングシンポジウムへの登録を\n遅まきながら以下の通りに受け付けました．";

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

$Stay1='1名1室            ';
$Stay1cost='（会員 67,000  非会員 73,000）';
$Stay2='2名1室            ';
$Stay2cost='（会員 47,000  非会員 53,000）';
$Stay3='3名1室            ';
$Stay3cost='（会員 40,000  非会員 46,000）';
$Stay4='4名1室（学生に限る）';
$Stay4cost='（会員 29,000  非会員 35,000）';

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
</head><body>
EOM;

//title ----------------------------------------------------
	$TITLE= <<<EOM
<h1><img border="0" src="../img/mark2.gif" width="115" height="96"></h1>
<p align="right"><a href="http://www.ipsj.or.jp/prosym/">
「プログラミング・シンポジウム」</a>へ戻る</p>
<h1>プログラミング・シンポジウム <font color=#ff0000>遅まきながらの</font>参加申込み</h1>
EOM;

//notice ---------------------------------------------------
	$NOTICE = <<<EOM
<ul>
  <li> 参加費には予稿集代，宿泊費，食費，消費税を含みます．宿泊なしの参加は認めません．
  <li> 会場では参加費を受け取りません．お手数ですが，郵便振替，銀行振込み，現金書留などの手段で，事前に参加費の払込みを済ませるようお願いします．
  <li> 参加申込者には，請求書，参加章引換券，振替用紙を郵送しますので，<font color=#ff0000>至急</fonnt>払い込みを済ませて下さい．振替用紙を使って郵便局で払い込む場合は，手数料は無料です．
  <li> 開催期間中の中途での出入りや，人員の交替はご遠慮ください．（已むを得ない場合は幹事にご相談ください．）
</ul>
<ul>
  <li> 会場，宿泊施設の都合で，お申込みに応じかねる場合がありますので，あらかじめご了承ください．
  <li> 参加申込み後やむを得ず参加を取り消される場合は，2006年12月15日(金)までに連絡をお願いします．取消の連絡のない場合は，準備の都合上，参加費を徴収させていただきます．事情による代理の参加は認めます．
  <li> 発表者の方も参加申込みが必要です．
</ul>
<ul>
  <li> プログラムは <a href="48program.html">ここ</a>にあります．
  <li> 「※」は必須項目を表します．
</ul>
EOM;

//footer ---------------------------------------------------
	$FOOTER= <<<EOM
</body></html>
EOM;

?>
