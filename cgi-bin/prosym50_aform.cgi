#!/usr/bin/env perl

use strict;
#use lib qw(/usr/pkg/lib/perl5/site_perl/5.8.0);
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use Email::Valid;
use Mail::Sendmail;
use Jcode;
use Config::Simple;
use Encode;
use utf8;

#--------------------------------#
#        設定ファイルより        #
#        各種パラメータを        #
#        読み込む                #
#--------------------------------#
my $c = new Config::Simple('prosym50.ini')
    or die "Can't Read Configuration file.\n";
my $path = $c->param('Prosym50.datapath');
my $mark = $c->param('Prosym50.mark');
my $mail = $c->param('Prosym50.mail');
my $home = $c->param('Prosym50.home');
my $top = $c->param('Prosym50.prosymurl');
my $template = $c->param('Prosym50.template');
$c->close;

$path = $path . "/" if ($path !~ /.*\/$/);

my $q = new CGI;
my $title = "第50回プログラミング・シンポジウム 発表申込み";
# http://www2u.biglobe.ne.jp/~MAS/perl/waza/yen.html
my $errmark = '<font color="brown">*</font>';

#==================================================#
#                  メインルーチン                  #
#==================================================#

#--------------------------------#
#        クエリーを受け取る      #
#--------------------------------#
my %form_data = ();
if ($ENV{'QUERY_STRING'} ne "") {
    my @pairs = split('&', $ENV{'QUERY_STRING'});
    foreach my $pair (@pairs) {
	(my $name, my $value) = split('=', $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$form_data{$name} = $value;
    }
}

#---------------------------------#
#        クエリーの内容をチェック #
#---------------------------------#
my $action = $form_data{'act'};

#---------------------------------#
#        フォームの内容をチェック #
#---------------------------------#
my $paramerr = "";
my $pid = "";
my $pwd = "";

$pid = $form_data{'pid'} if ($form_data{'pid'} ne "");
$pwd = $form_data{'pwd'} if ($form_data{'pwd'} ne "");
if ($pid eq "") {
    $pid = $q->param('User.emailuser') . "@" . $q->param('User.emaildomain');
}

if ($action eq "check") {
    $paramerr = check_params();
    if ($paramerr eq "") {
	$pwd = save_params($pid, $pwd);
    }
}

#-------------------------------------#
#        どの手順にあたるかをチェック #
#-------------------------------------#
my $page_select = 0;
if ($action eq "" || $action eq "check") {
    if ($action eq "" || ($action eq "check" && $paramerr ne "")) {
# STEP1: 初期の入力の場合、または再入力を促す場合
	$page_select = 1;
    } else {
# STEP2: 確認メイルを送る
	$page_select = 2;
    }
} elsif ($action eq "confirm") {
# STEP3: 入力内容確認
    $page_select = 3;
} elsif ($action eq "finish") {
# STEP4: 完了
    $page_select = 4;
} elsif ($action eq "edit") {
# STEP1(2): 再入力
    $page_select = 5;
}

if ($page_select == 0) {
    print $q->redirect($home);
    exit(0);
}

#--------------------------------#
#           表示する             #
#--------------------------------#
#>      6 年周期で赤、橙、黄、緑、青、紫とすることに決まっている。2005 年は
#>      緑だった。冬と夏は同系色の濃淡とする。すなわち、冬は濃い色、夏は薄い
#>      色にする。本棚できれいに見えるという理由だそうだ。
#FFAEB9
print $q->header(-type=>'text/html', -charset=>'UTF-8');
#print $q->header(-type=>'text/html', -charset=>'EUC-JP');
#print $q->header(-type=>'text/html', -charset=>'Shift_JIS');
print $q->start_html(-lang=>'ja-JP',
		     -title=>"$title",
		     -charset=>'UTF-8', -encoding=>'UTF-8',
		     -bgcolor=>'#FFC1C1', -linkcolor=>'#0000FF',
		     -alinkcolor=>'#0000FF', -vlinkcolor=>'#660099');

# ロゴとタイトル
print $q->h1('<img border="0" src="', $mark, '" width="115" height="96"> ',
	     "$title"), "\n";
print '<table border="2" celspaceing="0" cellspan="0">', "\n";
print '<td>', $q->h3('　申込みの流れ：１．必要事項入力 → ２．メール受信 → ３．内容確認 → ４．完了　'), '</td>', "\n";
print '</table>', "\n";

# for debug
#print $q->h3('act = "', $action, '"'), "\n";
#print $q->h3('pid = "', $pid, '"'), "\n";
#print $q->h3('pwd = "', $pwd, '"'), "\n";
#print $q->h3('err = "', $paramerr, '"'), "\n";
#print $q->h3('path = "', $path, '"'), "\n";

if ($page_select == 1) {
# STEP1: 初期の入力か、再入力を促す
    print_forms_page();
} elsif ($page_select == 2) {
# STEP2: 確認メイルを送る
    send_mail_passwd($pid, $pwd);
} elsif ($page_select == 3) {
# STEP3: 入力内容確認
    print_confirmation_page($pid, $pwd);
} elsif ($page_select == 4) {
# STEP4: 完了
    print_final_page($pid, $pwd);
} elsif ($page_select == 5) {
# STEP1(2): 再入力
    print_edit_page();
} else {
    print_error_msg('不正な条件です。');
}

#--------------------------------#
#           正常終了             #
#--------------------------------#
print $q->end_html;

exit(0);

#---------------------------------------------------------------------

#--------------------------------------------------------#
# サブルーチン：                                         #
#	フォームで入力されたパラメータをチェックする     #
#--------------------------------------------------------#
sub check_params {
    my $err = "";

# 氏名のチェック
    $err = $err . "/NAME" if ($q->param('User.name') eq "");

# 所属のチェック
    $err = $err . "/AFFILI" if ($q->param('User.affili') eq "");

# メールアドレスのチェック
    my $email = $q->param('User.emailuser') . "@" . $q->param('User.emaildomain');
    if ($q->param('User.emailuser') eq "" || 
	$q->param('User.emaildomain') eq "" ||
	!Email::Valid->address($email)) {
#	|| $email =~ /.*\@.*\@.*|^\@.*|.*\@$/) {
	$err = $err . "/EMAIL";
    }

# 郵送先のチェック
    $err = $err . "/ADDR" if ($q->param('User.address') eq "");

# 電話番号のチェック
    $err = $err . "/PHONE" if ($q->param('User.phone') eq "");

# 発表種別のチェック
    $err = $err . "/TYPE" if ($q->param('Paper.type') eq "");

# 発表題目のチェック
    $err = $err . "/TITLE" if ($q->param('Paper.title') eq "");

# 概要のチェック
    $err = $err . "/ABST" if ($q->param('Paper.abst') eq "");

# デモのチェック
    $err = $err . "/DEMO" if ($q->param('Paper.demo') eq "");

# 登壇発表のチェック
    $err = $err . "/A1" if ($q->param('Presenter.present') eq "");
    if ($q->param('Presenter.present') ne "") {
	my $a = $q->param('Presenter.present');
	if ($q->param($a . '.sname') eq "" ||
	    $q->param($a . '.gname') eq "" ||
	    $q->param($a . '.affili') eq "") {
	    my $i = $a;
	    $i =~ s/Author//;
	    $err = $err . "/A" . $i;
	}
    }

# 登壇発表の区分のチェック
    $err = $err . "/PR" if ($q->param('Presenter.status') eq "");

# 著者１情報のチェック
    if ($q->param('Author1.sname') eq "" ||
	$q->param('Author1.gname') eq "" ||
	$q->param('Author1.affili') eq "") {
	$err = $err . "/A1" if ($err !~ /\/A1/);
    }

# 著者２〜７情報のチェック
    for my $i ( 2 .. 7 ) {
	if ($q->param('Author' . $i . '.sname') ne "" ||
	    $q->param('Author' . $i . '.gname') ne "" ||
	    $q->param('Author' . $i . '.affili') ne "") {
	    if ($q->param('Author' . $i . '.sname') eq "" ||
		$q->param('Author' . $i . '.gname') eq "" ||
		$q->param('Author' . $i . '.affili') eq "") {
		$err = $err . '/A' . $i;
	    }
	}
    }

    return $err;
}

#--------------------------------------------------------#
# サブルーチン：                                         #
#--------------------------------------------------------#
sub print_forms {
    my ($fn, $t) = @_;

    open(IN, $fn) or die "Can't open the form file.\n";

    while (my $line = <IN>) {
	$line =~ s/__USER_NAME_MARK__/$errmark/ if ($paramerr =~ /\/NAME/);
	$line =~ s/__USER_AFFILI_MARK__/$errmark/ if ($paramerr =~ /\/AFFILI/);
	$line =~ s/__USER_EMAIL_MARK__/$errmark/ if ($paramerr =~ /\/EMAIL/);
	$line =~ s/__USER_ADDRESS_MARK__/$errmark/ if ($paramerr =~ /\/ADDR/);
	$line =~ s/__USER_PHONE_MARK__/$errmark/ if ($paramerr =~ /\/PHONE/);
	$line =~ s/__PAPER_TYPE_MARK__/$errmark/ if ($paramerr =~ /\/TYPE/);
	$line =~ s/__PAPER_TITLE_MARK__/$errmark/ if ($paramerr =~ /\/TITLE/);
	$line =~ s/__PAPER_ABST_MARK__/$errmark/ if ($paramerr =~ /\/ABST/);
	$line =~ s/__PAPER_TYPE_DEMO__/$errmark/ if ($paramerr =~ /\/DEMO/);

	$line =~ s/__AUTHOR1_MARK__/$errmark/ if ($paramerr =~ /\/A1/);
	$line =~ s/__AUTHOR2_MARK__/$errmark/ if ($paramerr =~ /\/A2/);
	$line =~ s/__AUTHOR3_MARK__/$errmark/ if ($paramerr =~ /\/A3/);
	$line =~ s/__AUTHOR4_MARK__/$errmark/ if ($paramerr =~ /\/A4/);
	$line =~ s/__AUTHOR5_MARK__/$errmark/ if ($paramerr =~ /\/A5/);
	$line =~ s/__AUTHOR6_MARK__/$errmark/ if ($paramerr =~ /\/A6/);
	$line =~ s/__AUTHOR7_MARK__/$errmark/ if ($paramerr =~ /\/A7/);

	$line =~ s/__PRESENTER_STATUS_MARK__/$errmark/ if ($paramerr =~ /\/PR/);

	$line =~ s/__[A-Z,0-9,_]*_MARK__//; # 残り制御用フラグを消去

	my $user_name = $t->param('User.name');
	my $user_affili = $t->param('User.affili');
	my $user_emailuser = $t->param('User.emailuser');
	my $user_emaildomain = $t->param('User.emaildomain');
	my $user_address = $t->param('User.address');
	$user_address =~ s/\x0Dn|\x0D//g;
	my $user_phone = $t->param('User.phone');
	$line =~ s/__USER_NAME__/\"$user_name\"/;
	$line =~ s/__USER_AFFILI__/\"$user_affili\"/;
	$line =~ s/__USER_EMAILUSER__/\"$user_emailuser\"/;
	$line =~ s/__USER_EMAILDOMAIN__/\"$user_emaildomain\"/;
	$line =~ s/__USER_ADDRESS__/$user_address/;
	$line =~ s/__USER_PHONE__/\"$user_phone\"/;

	my $paper_type = $t->param('Paper.type');
	my $paper_title = $t->param('Paper.title');
	my $paper_abst = $t->param('Paper.abst');
	my $paper_demo = $t->param('Paper.demo');
	$paper_abst =~ s/\x0Dn|\x0D//g;
	$line =~ s/__CHECKED_ORAL__/CHECKED/ if ($paper_type =~ /ORAL/);
	$line =~ s/__CHECKED_POSTER__/CHECKED/ if ($paper_type =~ /POSTER/);
	$line =~ s/__PAPER_TITLE__/\"$paper_title\"/;
	$line =~ s/__PAPER_ABST__/$paper_abst/;
	$line =~ s/__CHECKED_DEMO__/CHECKED/ if ($paper_demo =~ /YDEMO/);
	$line =~ s/__CHECKED_NODEMO__/CHECKED/ if ($paper_demo =~ /NODEMO/);

	my $paper_present = $t->param('Presenter.present');
	$line =~ s/__CHECKED_AUTHOR1__/CHECKED/
	    if ($paper_present =~ /Author1/);
	$line =~ s/__CHECKED_AUTHOR2__/CHECKED/
	    if ($paper_present =~ /Author2/);
	$line =~ s/__CHECKED_AUTHOR3__/CHECKED/
	    if ($paper_present =~ /Author3/);
	$line =~ s/__CHECKED_AUTHOR4__/CHECKED/
	    if ($paper_present =~ /Author4/);
	$line =~ s/__CHECKED_AUTHOR5__/CHECKED/
	    if ($paper_present =~ /Author5/);
	$line =~ s/__CHECKED_AUTHOR6__/CHECKED/
	    if ($paper_present =~ /Author6/);
	$line =~ s/__CHECKED_AUTHOR7__/CHECKED/
	    if ($paper_present =~ /Author7/);

	for my $i ( 1 .. 7 ) {
	    my $a = 'Author' . $i;
	    my $sname = $t->param($a . '.sname');
	    my $gname = $t->param($a . '.gname');
	    my $affili = $t->param($a . '.affili');
	    my $s = "__AUTHOR" . $i . "_SNAME__";
	    $line =~ s/$s/\"$sname\"/;
	    my $s = "__AUTHOR" . $i . "_GNAME__";
	    $line =~ s/$s/\"$gname\"/;
	    my $s = "__AUTHOR" . $i . "_AFFILI__";
	    $line =~ s/$s/\"$affili\"/;
	}

	my @st = $t->param('Presenter.status');
	my $status = shift(@st);
	while (my $str = shift(@st)) {
	    $status = $status . ',' . $str;
	}
	$line =~ s/__CHECKED_STUDENT__/CHECKED/ if ($status =~ /S/);
	$line =~ s/__CHECKED_SENIOR__/CHECKED/ if ($status =~ /E/);
	$line =~ s/__CHECKED_GENERAL__/CHECKED/ if ($status =~ /G/);

	if ($t->param('Notes.text') ne "") {
	    my $text = $t->param('Notes.text');
	    $text =~ s/\x0Dn|\x0D//g;
	    $line =~ s/__NOTES_TEXT__/$text/;
	}

	$line =~ s/__[A-Z,0-9,_]*__//g; # 残り制御用フラグを消去

	print $line;
    }

    return 0;
}

#--------------------------------------------------------#
# サブルーチン：                                         #
#	乱数パスワードを生成する                         #
#--------------------------------------------------------#
sub create_password {
# Perl の crypt 関数に使える SALT の文字は a〜z、A〜Z、0〜9、「.」と「/」
    my @salt = ('a'..'z','A'..'Z','0'..'9','.','/');
    my $crypt_password = "";

    do {
# SALT を作る。
	my $seed1 = int(rand(64));
	my $seed2 = int(rand(64));
	my $salt = $salt[$seed1] . $salt[$seed2];
# crypt 関数の仕様は crypt(テキスト, SALT)
	$crypt_password = crypt("@_", $salt);
# 「.」、「/」、「|」が含まれていたら破棄
    } while ($crypt_password =~ /\.|\/|\|/);

    return "$crypt_password";
}

#--------------------------------------------------------#
# サブルーチン：                                         #
#--------------------------------------------------------#
sub save_params {
    my ($pid, $pwd) = @_;

    my $cfg = "";
    my $fn = "";

    if ($pwd ne "") {
# パラメータ指定があれば開いてみる
	$fn = $pid . "=" . $pwd . ".ini";
	$cfg = new Config::Simple($path . $fn);
    }
    if ($cfg eq "") {
# 既に同じ名前のファイルがあるか確認してからopen
	do {
	    $cfg->close() if ($cfg ne "");
	    $pwd = create_password($pid);
	    $fn = $pid . "=" . $pwd . ".ini";
	    $cfg = new Config::Simple($path . $fn);
	} while ($cfg ne "");

	$cfg = new Config::Simple(syntax=>'ini');
    }

    $cfg->param('User.name', encode("utf8", $q->param('User.name')));
    $cfg->param('User.affili', encode("utf8", $q->param('User.affili')));
    $cfg->param('User.email', $pid);
    $cfg->param('User.passwd', $pwd);
    $cfg->param('User.emailuser', $q->param('User.emailuser'));
    $cfg->param('User.emaildomain', $q->param('User.emaildomain'));
    $cfg->param('User.address', encode("utf8", $q->param('User.address')));
    $cfg->param('User.phone', encode("utf8", $q->param('User.phone')));
    $cfg->param('Paper.type', $q->param('Paper.type'));
    $cfg->param('Paper.title', encode("utf8", $q->param('Paper.title')));
    $cfg->param('Paper.abst', encode("utf8", $q->param('Paper.abst')));
    $cfg->param('Paper.demo', $q->param('Paper.demo'));

    $cfg->param('Presenter.present', $q->param('Presenter.present'));
    my @st = $q->param('Presenter.status');
    my $status = shift(@st);
    while (my $str = shift(@st)) {
	$status = $status . ':' . $str;
    }
    $cfg->param('Presenter.status', $status);

    $cfg->param('Author1.sname', encode("utf8", $q->param('Author1.sname')))
	if ($q->param('Author1.sname') ne "");
    $cfg->param('Author1.gname', encode("utf8", $q->param('Author1.gname')))
	if ($q->param('Author1.gname') ne "");
    $cfg->param('Author1.affili', encode("utf8", $q->param('Author1.affili')))
	if ($q->param('Author1.affili') ne "");

    $cfg->param('Author2.sname', encode("utf8", $q->param('Author2.sname')))
	if ($q->param('Author2.sname') ne "");
    $cfg->param('Author2.gname', encode("utf8", $q->param('Author2.gname')))
	if ($q->param('Author2.gname') ne "");
    $cfg->param('Author2.affili', encode("utf8", $q->param('Author2.affili')))
	if ($q->param('Author2.affili') ne "");

    $cfg->param('Author3.sname', encode("utf8", $q->param('Author3.sname')))
	if ($q->param('Author3.sname') ne "");
    $cfg->param('Author3.gname', encode("utf8", $q->param('Author3.gname')))
	if ($q->param('Author3.gname') ne "");
    $cfg->param('Author3.affili', encode("utf8", $q->param('Author3.affili')))
	if ($q->param('Author3.affili') ne "");

    $cfg->param('Author4.sname', encode("utf8", $q->param('Author4.sname')))
	if ($q->param('Author4.sname') ne "");
    $cfg->param('Author4.gname', encode("utf8", $q->param('Author4.gname')))
	if ($q->param('Author4.gname') ne "");
    $cfg->param('Author4.affili', encode("utf8", $q->param('Author4.affili')))
	if ($q->param('Author4.affili') ne "");

    $cfg->param('Author5.sname', encode("utf8", $q->param('Author5.sname')))
	if ($q->param('Author5.sname') ne "");
    $cfg->param('Author5.gname', encode("utf8", $q->param('Author5.gname')))
	if ($q->param('Author5.gname') ne "");
    $cfg->param('Author5.affili', encode("utf8", $q->param('Author5.affili')))
	if ($q->param('Author5.affili') ne "");

    $cfg->param('Author6.sname', encode("utf8", $q->param('Author6.sname')))
	if ($q->param('Author6.sname') ne "");
    $cfg->param('Author6.gname', encode("utf8", $q->param('Author6.gname')))
	if ($q->param('Author6.gname') ne "");
    $cfg->param('Author6.affili', encode("utf8", $q->param('Author6.affili')))
	if ($q->param('Author6.affili') ne "");

    $cfg->param('Author7.sname', encode("utf8", $q->param('Author7.sname')))
	if ($q->param('Author7.sname') ne "");
    $cfg->param('Author7.gname', encode("utf8", $q->param('Author7.gname')))
	if ($q->param('Author7.gname') ne "");
    $cfg->param('Author7.affili', encode("utf8", $q->param('Author7.affili')))
	if ($q->param('Author7.affili') ne "");

# 備考
    $cfg->param('Notes.text', encode("utf8", $q->param('Notes.text')))
	if ($q->param('Notes.text') ne "");

    $cfg->write($path . $fn);
    $cfg->close();

    return $pwd;
}

#--------------------------------------------------------#
# サブルーチン：                                         #
#--------------------------------------------------------#
sub print_forms_page {
# フォーム開始
    print $q->start_multipart_form(-action=>$home . '?act=check'), "\n";

# 入力誤りの指摘
    if ($paramerr ne "") {
	print $q->h2("$errmark", 'で示した項目に入力誤りがあります。');
    }

# フォームの中身を表示
    print_forms($template, $q);

# 終了処理
    print $q->endform;

    print $q->br;
    print $q->h3('ご不明な点がございましたら',
		 $q->a({href=>'mailto:' . $mail}, $mail),
		 'までお問い合わせください。');

    return 0;
}

#--------------------------------------------------------#
# サブルーチン：                                         #
#--------------------------------------------------------#
sub print_edit_page {
    my $fn = $pid . "=" . $pwd;
    my $cfg = new Config::Simple($path . $fn . ".ini");

    if ($cfg eq "") {
# 記録した情報が見つからない場合
	print_error_msg('情報が見つかりません。<br>既に申込みを完了されている場合には、再度入力し直してください。');

	return 0;
    }

# フォーム開始
    print $q->start_multipart_form(-action=>$home . '?act=check&pid=' . $pid . '&pwd=' . $pwd), "\n";

# フォームの中身を表示
    print_forms($template, $cfg);
    $cfg->close();

# 終了処理
    print $q->endform;

    print $q->br;
    print $q->h3('ご不明な点がございましたら',
		 $q->a({href=>'mailto:' . $mail}, $mail),
		 'までお問い合わせください。');

    return 0;
}

#--------------------------------------------------------#
# サブルーチン：                                         #
#--------------------------------------------------------#
sub print_mailsent {
    print $q->h2('手順２ ： ', "$pid", '宛に確認メールを送りました。');
    print $q->br;
    print $q->h2('メールに記載されたURLを開いて内容確認を行い、申込みを完了させてください。');
    print $q->h2('<blink><font color="brown">まだこの時点では申込みは完了していません。</font></blink>');
    print $q->br;
    print $q->h3('ご不明な点がございましたら',
		 $q->a({href=>'mailto:' . $mail}, $mail),
		 'までお問い合わせください。');

    return 0;
}

#--------------------------------------------------------#
# サブルーチン：                                         #
#--------------------------------------------------------#
sub print_confirmation_page {
    my ($pid, $pwd) = @_;

    my $text = "";
    my $fn = $pid . "=" . $pwd;
    my $cfg = new Config::Simple($path . $fn . ".ini");

    if ($cfg eq "") {
# 記録した情報が見つからない場合
	print_error_msg('指定されたURLが無効です。<br>指定したURLの中に空白文字や改行文字などの特殊文字が混入していないか確認してみてください。<br>既に申込みを完了されている場合には、再度入力し直してください。');

	return 0;
    }
    $cfg->close();

# ファイルに書出し
    $text = print_confirmation_text($pid, $pwd);

# フォーム開始
    print $q->start_multipart_form(-action=>$home . '?act=finish&pid=' . $pid . '&pwd=' . $pwd), "\n";

    print $q->h2('手順３ ： 登録内容を確認して、よろしければ「完了」ボタンを押して申込みを終了してください。');
    print $q->h3('<font color="brown">※表示内容が入力した内容と異なる場合は、ブラウザの「更新」ボタンを押してページを再読込みしてみてください。</font>');
    print $q->br;

    open(IN, $text) or die "Can't open the working file.\n";
    while (my $line = <IN>) {
	print $line, $q->br, "\n";
    }
    close(IN);

    print $q->br, "\n";
    print $q->submit("　申込み完了　");
    print $q->endform;

    print $q->br, $q->br, $q->br, "\n";

    print $q->start_multipart_form(-action=>$home . '?act=edit&pid=' . $pid . '&pwd=' . $pwd), "\n";
    print '入力内容を修正する場合はこちら → ', $q->submit("　修正　");
    print $q->endform;

    print $q->h3('ご不明な点がございましたら',
		 $q->a({href=>'mailto:' . $mail}, $mail),
		 'までお問い合わせください。');

# 作業中の残骸を消去する
    if ( -e $text) {
	unlink($text);
    }
    return 0;
}

#--------------------------------------------------------#
# サブルーチン：                                         #
#--------------------------------------------------------#
sub print_confirmation_text {
    my ($pid, $pwd) = @_;
    my $fn = $pid . "=" . $pwd;

    open(OUT, '> ' . $path . $fn . ".txt")
	or die "Can't open a working file.\n";

    my $cfg = new Config::Simple($path . $fn . ".ini");

    print OUT '申込み者氏名：', $cfg->param('User.name'), "\n";
    print OUT '申込み者所属：', $cfg->param('User.affili'), "\n";
    print OUT 'メールアドレス：', $cfg->param('User.emailuser') . "@" . $cfg->param('User.emaildomain'), "\n";
    my $address = $cfg->param('User.address');
    $address =~ s/\x0Dn|\x0D//g;
    print OUT '郵送先：', $address, "\n";
    print OUT '電話番号：', $cfg->param('User.phone'), "\n";
    print OUT "\n";
    print OUT '種別：講演', "\n" if ($cfg->param('Paper.type') eq "ORAL");
    print OUT '種別：ポスター', "\n" if ($cfg->param('Paper.type') eq "POSTER");
    print OUT '題目：', $cfg->param('Paper.title'), "\n";
    my $abst = $cfg->param('Paper.abst');
    $abst =~ s/\x0Dn|\x0D//g;
    print OUT '概要：', $abst, "\n";
    print OUT 'デモ：';
    print OUT "あり\n" if ($cfg->param('Paper.demo') eq "YDEMO");
    print OUT "なし\n" if ($cfg->param('Paper.demo') eq "NODEMO");
    print OUT "\n";
    print OUT '著者情報：', "\n";
    for my $i ( 1 .. 7 ) {
	my $a = 'Author' . $i;
	if ($cfg->param($a . '.sname') ne "") {
	    print OUT '著者', $i, '：',
	    $cfg->param($a . '.sname') . ' ' . $cfg->param($a . '.gname') ;
	    print OUT ' / ';
	    print OUT $cfg->param($a . '.affili');
	    print OUT "\n";
	}
    }
    print OUT "\n";

    my $p = $cfg->param('Presenter.present');
    $p =~ s/Author//;
    print OUT '登壇発表者：著者' . $p, "\n" if ($p ne "");

    my @st = split(/:/, $cfg->param('Presenter.status'));
#    print OUT '登壇発表者区分：', $cfg->param('Presenter.status'), "\n";
    print OUT '登壇発表者区分：';
    my $s = shift(@st);
    while ($s ne "") {
	print OUT '学生' if ($s =~ /S/);
	print OUT '65歳以上' if ($s =~ /E/);
	print OUT '社会人' if ($s =~ /G/);
	$s = shift(@st);
#	print OUT ' &amp ' if ($s ne "");
	print OUT ' / ' if ($s ne "");
    }
    if ($cfg->param('Presenter.status') =~ /E/) {
	print OUT ' （参加費割引対象：65歳以上）';
    } elsif ($cfg->param('Presenter.status') =~ /S/ &&
	     $cfg->param('Presenter.status') !~ /G/) {
	print OUT ' （参加費割引対象：学生）';
    }
    print OUT "\n";

    my $text = $cfg->param('Notes.text');
    $text =~ s/\x0Dn|\x0D//g;
    if ($text ne "") {
	print OUT "\n";
	print OUT '備考：', $text, "\n";
    }

    close(OUT);

    return ($path . $fn . ".txt");
}

#--------------------------------------------------------#
# サブルーチン：                                         #
#--------------------------------------------------------#
sub print_final_page {
    my ($pid, $pwd) = @_;

    my $fn = $pid . "=" . $pwd . ".ini";
    my $cfg = "";
    if ($pwd ne "") {
# パラメータ指定があれば開いてみる
	$cfg = new Config::Simple($path . $fn);
    }
    if ($cfg eq "") {
	print_error_msg('登録情報がありません。<br>既に申込みを完了した後でないか確認してみてください。');
	return 0;
    }

    print $q->h2($cfg->param('User.name'), ' 様', $q->br, '発表申込みはこれで完了いたしました。', $q->br, '採否の結果は、幹事会での審議を経て、１０月下旬頃にお知らせいたします。', $q->br, 'また、原稿の提出〆切は１１月末の予定です。', $q->br, $q->br, 'お申込みありがとうございます。');
    print $q->h3('ご不明な点がございましたら',
		 $q->a({href=>'mailto:' . $mail}, $mail),
		 'までお問い合わせください。');
    print $q->br, "\n";
    print $q->a({href=>$top}, 'プログラミング・シンポジウムのトップページへ'),
    "\n";

# 受理メイルを送信する
    send_mail_acceptance($pid, $pwd, $cfg->param('User.name'));

    $cfg->close();

# 完了したので登録情報のファイル名を _OK 付きに変更しておく
    my $fnok = $pid . "=" . $pwd . "_OK.ini";
    rename($path . $fn, $path . $fnok);

    return 0;
}

#--------------------------------------------------------#
# サブルーチン：                                         #
#--------------------------------------------------------#
sub print_error_msg {
    print $q->start_multipart_form(-action=>$home), "\n";
    print $q->h2('<font color="brown">エラー</font> ： ', "@_");
    print $q->h3('ご不明な点がございましたら',
		 $q->a({href=>'mailto:' . $mail}, $mail),
		 'までお問い合わせください。');
    print $q->submit("　入力画面へ　");
    print $q->endform;

    return 0;
}

#--------------------------------------------------------#
# サブルーチン：                                         #
#--------------------------------------------------------#
sub send_mail_passwd {
    my ($pid, $pwd) = @_;

    my $url=$home . '?act=confirm&pid=' . $pid . '&pwd=' . $pwd;
    my $mailto = $pid;

    my $subj = "プログラミング・シンポジウム発表申込み仮登録のお知らせ";
    my $mesg = "";

    $mesg .= encode("utf8", $q->param('User.name')) . ' 様' . "\n\n";
    $mesg .= '下記のURLにアクセスして発表申込みを完了させて下さい。' . "\n\n";
    $mesg .= $url . "\n\n";
    $mesg .= '※注：この時点ではまだ申込みは完了していません。' . "\n\n";
    $mesg .= 'ご不明な点がございましたら、' . $mail . ' まで気軽にお問い合わせ下さい。' . "\n";
    $mesg .= '--' . "\n";
    $mesg .= '情報処理学会 プログラミング・シンポジウム幹事会' . "\n";

    #--------------------------------#
    #           メイル送信           #
    #--------------------------------#
    $subj = encode("MIME-Header-ISO_2022_JP", $subj);
    $mesg = encode("iso-2022-jp", $mesg);
    my %mailparams = (
		"Content-Type" => 'text/plain; charset="iso-2022-jp"',
		To             => $mailto,
		From           => $mail,
		Subject        => $subj,
		Message        => $mesg,
		);
    sendmail(%mailparams);

    #--------------------------------#
    #           画面表示             #
    #--------------------------------#
    print_mailsent();

    return 0;
}

sub send_mail_acceptance {
    my ($pid, $pwd, $uname) = @_;

    my $mailto = $pid;

    my $subj = 'プログラミング・シンポジウム発表申込み完了のお知らせ';
    my $mesg = "";
    my $text = "";

    $text = print_confirmation_text($pid, $pwd);
    open(IN, $text) or die "Can't open the working file.\n";

    $mesg .= encode("utf8", $uname) .  ' 様' . "\n\n";
    $mesg .= '下記の通り発表申込みを受付けました。' . "\n\n";
    $mesg .= '採否の結果は、幹事会での審議を経て、１０月下旬頃にお知らせいたします。' . "\n";
    $mesg .= 'また、原稿の提出〆切は１１月末の予定です。お申込みありがとうございます。' . "\n\n";
    $mesg .= 'ご不明な点がございましたら、' . $mail . ' までお問い合わせください。' . "\n\n";

    while (my $line = <IN>) {
	$mesg .= $line;
    }
    close(IN);

    $mesg .= '--' . "\n";
    $mesg .= '情報処理学会 プログラミング・シンポジウム幹事会' . "\n";

    #--------------------------------#
    #           メイル送信           #
    #--------------------------------#
    $subj = encode("MIME-Header-ISO_2022_JP", $subj);
    $mesg = encode("iso-2022-jp", $mesg);
    my %mailparams = (
		"Content-Type" => 'text/plain; charset="iso-2022-jp"',
		To             => $mailto,
		From           => $mail,
		Subject        => $subj,
		Message        => $mesg,
		);
    sendmail(%mailparams);

# 作業中の残骸を消去する
    if ( -e $text ) {
	unlink($text);
    }

    return 0;
}
