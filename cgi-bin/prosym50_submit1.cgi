#!/usr/bin/env perl

use strict;
#use lib qw(/usr/pkg/lib/perl5/site_perl/5.8.0);
use CGI;
#use CGI::Carp qw(fatalsToBrowser);
use Jcode;
use Config::Simple;

my $title  = "第50回プログラミング・シンポジウム 発表原稿提出用フォーム";
# http://www2u.biglobe.ne.jp/~MAS/perl/waza/yen.html

my $q = new CGI;
my $c = new Config::Simple('prosym50_submit.ini')  or die "Can't Read Configuration file.\n";
my $mark   = $c->param('Prosym50.mark');
my $craf   = $c->param('Prosym50.jouto');
my $affex  = $c->param('Prosym50.prog48');
my $prog   = $c->param('Prosym50.prog50');
my $admin  = $c->param('Prosym50.adminaddr2');
my $path   = $c->param('Prosym50.datahome') . $q->param('did');
my $htpath = $c->param('Prosym50.htdocshome') . $q->param('did');
my $submit2= $c->param('Prosym50.submit2');
$c->close;

my $ini = "";
$ini = "$path/initial.ini" if ( -f "$path/initial.ini" );
$ini = "$path/submit.ini"  if ( -f "$path/submit.ini" ); 
my $cfg = new Config::Simple($ini);
my $text = "";

#==================================================#
#                  メインルーチン                  #
#==================================================#

#------------------------------------------#
#        作業ファイルの残骸を消去する      #
#------------------------------------------#
if (-d $htpath) {
#    foreach my $line (<"$htpath/*">) { # for Windows?
    foreach my $line (<$htpath/*>) {
	if (!($line =~ /index.htm/)) {
	    unlink("$line") if ( -f "$line");
	}
    }
}

#--------------------------------#
#        クエリーを受け取る      #
#--------------------------------#
#my $query = $ENV{'QUERY_STRING'};

#--------------------------------#
#           表示する             #
#--------------------------------#
print $q->header(-type=>'text/html', -charset=>'UTF-8');
#print $q->header(-type=>'text/html', -charset=>'x-euc-jp');
#print $q->header(-type=>'text/html', -charset=>'x-sjis');
print $q->start_html(-lang=>'ja-JP',
		     -title=>"$title",
		     -charset=>'UTF-8', -encoding=>'UTF-8',
		     -bgcolor=>'#FFC1C1', -linkcolor=>'#0000FF',
		     -alinkcolor=>'#0000FF', -vlinkcolor=>'#660099');
print $q->h2('<img border="0" src="', $mark, '" width="115" height="96"> ', "$title"), "\n";

#--------------------------------#
#           エラーの場合         #
#--------------------------------#
if ($cfg eq "") {
    print $q->br;
    print $q->h2('不正なページです。'), $q->br, "\n";
    if ($q->param('did') eq "") {
	print 'ERROR=unknown ID';
    } else {
	print 'ERROR=', $q->param('did');
    }
    print $q->br, $q->br, "\n";
    print 'お手数ですが、', $q->a({href=>'mailto:' . $admin}, $admin), 'までご連絡ください。', $q->br, "\n";
    print $q->end_html;
    exit(1);
}

#--------------------------------#
#           フォーム開始         #
#--------------------------------#
print $q->start_multipart_form(-action=>$submit2), "\n";
print $q->br;
print $q->h3('以下のフォームを埋めて、ページの最後にあるボタンより次に進んでください。');
print $q->br;

#==== ID ====
print '<input type="hidden" name="did" value="', $q->param('did'), '">',
    '<input type="hidden" name="pid" value="', $q->param('pid'), '">', "\n";

#==== 第１ブロック ====

print '<table border="1" celspaceing="0" cellspan="0">', "\n";
#---- 種別 ----
print '<tr valign="top" align="left">';
print '<td>種別：</td><td>講演</td>' if ($cfg->param('Paper.type') eq "ORAL");
print '<td>種別：</td><td>ポスター</td>' if ($cfg->param('Paper.type') eq "POSTER");
print "</tr>";
print '<input type="hidden" name="Paper.type" value="', $cfg->param('Paper.type'), '">', "\n";
#---- 題目 ----
print '<tr valign="top" align="left">';
print '<td>題目：</td>';
$text = $cfg->param('Paper.title');
$text =~ s/\\comma\\/,/g;	# エスケープした ',' を戻す
print '<td><input type="text" size="40" name="Paper.title" value="', $text, '"></td>';
print "</tr>\n";
#---- 副題目 ----
print '<tr valign="top" align="left">';
print '<td>副題目：</td>';
$text = $cfg->param('Paper.subtitle');
$text =~ s/\\comma\\/,/g;	# エスケープした ',' を戻す
print '<td><input type="text" size="40" name="Paper.subtitle" value="', $text, '"></td>';
print "</tr>\n";
#---- デモ ----
print '<tr valign="top" align="left">';
print '<td>デモ：</td>';
print '<td><input type="radio" name="Paper.demo" ';
if ($cfg->param('Paper.demo') eq "YDEMO") {
    print 'value="YDEMO" CHECKED>あり　　',
	    '<input type="radio" name="Paper.demo" value="NODEMO">なし';
} else {
    print 'value="YDEMO">あり　　',
	    '<input type="radio" name="Paper.demo" value="NODEMO" CHECKED>なし';
}
if ($cfg->param('Paper.type') eq "講演") {
    print $q->br;
    print 'デモは';
    print $q->a({href=>"$prog", target=>'_blank'}, "ポスターセッションの時間帯");
    print 'に行います';
}
print '</tr>', "\n";
print '</table>', "\n";

print $q->br, "\n";

#==== 第２ブロック ====

print '<table border="1" celspaceing="0" cellspan="0">', "\n";
#---- 提出原稿 ----
print '<tr valign="top" align="left">';
print '<td>';
print '<font color="red">＊</font>' if ($q->param('err')=~/\/PAPER/);
print '提出原稿：</td><td>',
      $q->filefield(-name=>'paper'), '（PDF形式のみ）</td>';
print '</tr>', "\n";
#---- ページ数 ----
print '<tr valign="top" align="left">';
print '<td>';
print '<font color="red">＊</font>' if ($q->param('err')=~/\/PAGES/);
print 'ページ数：</td><td><input type="text" size="2" name="Paper.pages"';
print 'value="', $cfg->param('Paper.pages'), '"' if ($cfg->param('Paper.pages') ne "");
print '>ページ（講演最大12ページ、ポスター最大6ページ、製本上なるべく偶数ページ）</td>';
print '</tr>', "\n";
#---- フォントデータの埋込み ----
print '<tr valign="top" align="left">';
print '<td>';
print '<font color="red">＊</font>' if ($q->param('err')=~/\/FONTS/);
print 'フォントデータの埋込み：', $q->br,
    '<font color="brown">注：必ず埋め込んで下さい</font>',
    '</td><td>はい、私はフォントデータを埋め込みました。<input type="checkbox" name="Paper.fonts">',
    '（←埋込み確認後にチェック）</td>';
print '</tr>', "\n";
print '</table>', "\n";

print $q->br, "\n";

#==== 第３ブロック ====

print '<table border="1" celspaceing="0" cellspan="0">', "\n";
print '<tr valign="top" align="left">';
print '<td>';
print '<font color="red">＊</font>' if ($q->param('err')=~/\/COPYRIGHT/);
print $q->a({href=>"$craf", target=>'_blank'}, "著作権譲渡契約書"),
    '：', $q->br,
    '<font color="brown">上記リンクより取得', $q->br,
    'して下さい</font></td>',
    '<td><input type="radio" name="Paper.copyright" value="MAIL"> 郵送 （〒101-0062 東京都千代田区神田駿河台1-5 化学会館4F 社団法人情報処理学会 宛）', $q->br,
    '<input type="radio" name="Paper.copyright" value="FAX"> FAX （FAX番号：03-3518-8375）', $q->br,
    '<input type="radio" name="Paper.copyright" value="PDF" CHECKED> PDF ',
    $q->filefield(-name=>'copyright'), '</td>';
print '</tr>', "\n";
print '</table>', "\n";

print $q->br, "\n";

#==== 第４ブロック ====

print '<table border="1" celspaceing="0" cellspan="0">', "\n";
print '<tr valign="top" align="center">';
#print '<td></td><td>氏</td><td>名</td><td>登壇発表者</td><td>参加区分</td>',
#    '<td>所属（発表プログラムに記載する組織名を簡潔に記入して下さい　',
#    $q->a({href=>"$affex", target=>'_blank'}, "過去の例"), '）</td>';
print '<td></td><td>氏</td><td>名</td><td>登壇発表者</td>',
    '<td>所属（発表プログラムに記載する組織名を簡潔に記入して下さい　',
    $q->a({href=>"$affex", target=>'_blank'}, "過去の例"), '）</td>';
print '</tr>', "\n";
#---- 著者 ----
for my $i ( 1 .. 7 ) {
    my $arg = "Author" . $i;
    print '<tr><td>';
    print '<font color="red">＊</font>' if ($q->param('err')=~/\/A$i/);
    print '著者', $i, '：</td><td><input type="text" size="10" ';
    print 'name="', "$arg.sname", '" ';
    print 'value="', $cfg->param("$arg.sname"), '">';
    print '</td><td><input type="text" size="10" ';
    print 'name="', "$arg.gname", '" ';
    print 'value="', $cfg->param("$arg.gname"), '">';
    print '</td><td><input type="radio" name="Presenter.present" ';
    print 'value="', $arg, '"';
    if ($cfg->param('Presenter.present') eq $arg) {
	print " CHECKED";
    }
    print '></td>';
#    print '<td><input type="radio" name="', "$arg.status", '" value="一般"';
#    if ($cfg->param("$arg.status") eq '一般') {
#	print " CHECKED";
#    }
#    print '>一般 /<input type="radio" name="', "$arg.status", '" value="学生"';
#    if ($cfg->param("$arg.status") eq '学生') {
#	print " CHECKED";
#    }
#    print '>学生</td>';
    print '<td><input type="text" size="30" ';
    print 'name="', "$arg.affili", '" ';
    $text = $cfg->param("$arg.affili");
    $text =~ s/\\comma\\/,/g;	# エスケープした ',' を戻す
    print 'value="', $text, '"></td>';
    print '</tr>', "\n";
}
#print '<tr><td></td><td></td><td></td><td></td><td><font color="brown" size="-1">（社会人学生は一般）</font></td></tr>';

print '</table>', "\n";
print '<font color="brown">注：著者が８名以上である場合や登壇発表者が複数である場合など、上記の入力フォームでは表現できない事項は下の「通信欄」に記載してください。</font>', $q->br, "\n";

print $q->br, "\n";

#==== 第５ブロック ====

my @st = $cfg->param('Presenter.status');
my $status = shift(@st);
while (my $str = shift(@st)) {
    $status = $status . ',' . $str;
}
print '<table border="1" celspaceing="0" cellspan="0">', "\n";
print '<tr valign="top" align="left">';
print '<td>登壇発表者の区分：</td>';
print '<td>';
print '<input type="checkbox" name="Presenter.status" value="S"';
print ' CHECKED' if ($status=~/S/);
print '> 学生 /';
print '<input type="checkbox" name="Presenter.status" value="E"';
print ' CHECKED' if ($status=~/E/);
print '> 65歳以上 /';
print '<input type="checkbox" name="Presenter.status" value="G"';
print ' CHECKED' if ($status=~/G/);
print '>社会人</td></tr>', "\n";
print '<tr><td></td><td><font color="brown" size="-1">当てはまるもの全てをチェックしてください</font></td></tr>', "\n";
print '</table>', "\n";
print '<font color="brown">注：学生または65歳以上の登壇発表者は所定の参加費割引を受けることができます。ただし、社会人学生は割引対象外です。</font>', $q->br, "\n";
#print 'param=', $cfg->param('Presenter.status');

print $q->br, "\n";

#==== 第６ブロック ====

print '<table border="1" celspaceing="0" cellspan="0">', "\n";
print '<tr valign="top" align="left">';
print '<td>';
print '<font color="red">＊</font>' if ($q->param('err')=~/\/EMAIL/);
print '連絡先', $q->br, 'メールアドレス：</td>';
print '<td><input type="text" size="60" name="User.email" value="',
    $cfg->param('User.email'), '"></td>';
print "</tr>\n";
print '</table>', "\n";

print $q->br, "\n";

#==== 第７ブロック ====

print '<table border="1" celspaceing="0" cellspan="0">', "\n";
print '<tr valign="top" align="left">';
print '<td>通信欄：', $q->br;
print $q->br, '上記フォームでは';
print $q->br, '表現できない事項';
print $q->br, 'やご要望など</td>';
if ($cfg->param('Notes.text2') ne "") {
    my $text = $cfg->param('Notes.text2');
    $text =~ s/\\comma\\/,/g;	# エスケープした ',' を戻す
    print '<td>',
          $q->textarea(-name=>"Notes.text2", -rows=>"10", -cols=>"35", -value=>"$text"),
          '</td>';
} else {
    print '<td>',
          $q->textarea(-name=>"Notes.text2", -rows=>"10", -cols=>"35"),
          '</td>';
}
print '</tr>', "\n";
print '</table>', "\n";

#---- 入力クリアボタン ----
print $q->reset("入力クリア"), $q->br;

print $q->br, "\n";
print $q->br, "\n";

#---- 次へボタン ----
print $q->submit("　次へ　→"), $q->br;

print $q->endform;

print $q->end_html;

#--------------------------------#
#           正常終了             #
#--------------------------------#
$cfg->close;

exit(0);
