#!/usr/bin/env perl

use strict;
use CGI;
#use CGI::Carp qw(fatalsToBrowser);
use POSIX qw(strftime);
use Jcode;
use Config::Simple;
use File::Copy;
use Email::Valid;

my $title     = "第50回プログラミング・シンポジウム 発表原稿提出確認ページ";
# http://www2u.biglobe.ne.jp/~MAS/perl/waza/yen.html

my $q = new CGI;
my $c = new Config::Simple('prosym50_submit.ini');
my $mark   = $c->param('Prosym50.mark');
my $admin  = $c->param('Prosym50.adminaddr2');
my $path0  = $c->param('Prosym50.datahome');
my $path   = $c->param('Prosym50.datahome') . $q->param('did');
my $htpath = $c->param('Prosym50.htdocshome') . $q->param('did');
my $homeurl= $c->param('Prosym50.homeurl') .  $q->param('did');
my $submit1= $c->param('Prosym50.submit1');
my $submit3= $c->param('Prosym50.submit3');
$c->close;

my $timestamp = strftime "%y%m%d%H%M%S", localtime;
my $savepfile = "";
my $savecfile = "";
my $paramerr  = "";
my @fonts     = ();

#--------------------------------------------------------#
# サブルーチン：                                         #
#	アップロードされたデータをファイルとして格納する #
#--------------------------------------------------------#
sub store_file {
    my ($fh, $fn) = @_;

#    my $mimetype = $q->uploadInfo($fh)->{'Content-Type'}; # MIMEタイプ取得
    my ($ex) = ($fh =~ m|(\.[^./\\]+)$|); # 拡張子
    my $tag = $q->param('tag'); ##
    $ex = $tag.$ex if ($tag ne "" and $tag =~ /^[A-Z0-9_-]+$/i); ##
    my $outputfn = "$path/$fn$ex";
    open(F, "> $outputfn") or die;
#    $savepfile = "$fn$ex";
    binmode(F);
    flock(F, 2);
    if (defined $fh) {
	while (<$fh>) {
	    print F $_;
	}
    }
    close F;

    return "$fn$ex";
}

#--------------------------------------------------------#
# サブルーチン：                                         #
#	アップロードされたデータをファイルとして格納する #
#--------------------------------------------------------#
sub print_errors {
    my $pdf = 1;
    foreach my $line (@fonts) {
	$pdf = 0 if ($line =~ /Not in PDF format/);
    }
    print $q->h2('<font color="brown">入力エラーです。以下の項目の入力を確認して下さい。</font>'), "\n";
    print '<ul>', "\n";
    print '<li>', "原稿のPDFファイル\n" if ($paramerr=~/\/PAPER/||$pdf!=1);
    if ($pdf != 1) {
	print '<ul>', "\n";
	print '<li>', '<font color="brown">指定されたファイルはPDFフォーマットではないようです。</font>', "\n";
	print '</ul>', "\n";
	$paramerr = $paramerr . "/PAPER/";
    }
    print '<li>', "原稿のページ数\n" if ($paramerr=~/\/PAGES/);
    print '<li>', "原稿のPDFファイルへのフォントデータの埋込み\n" if ($paramerr=~/\/FONTS/||(@fonts > 0 && $pdf == 1));
    if (@fonts > 0 && $pdf == 1) {
	print '<ul>', "\n";
	print '<li>', '<font color="brown">以下のフォント名のフォントデータの埋込みを確認して下さい。</font>', "\n";
	print '<ul>', "\n";
	foreach my $line (@fonts) {
	    print '<li>', $line, "\n";
	}
	print '</ul>', "\n";
	print '</ul>', "\n";
    } else {
	print '<ul>', "\n";
	print '<li>', '<font color="brown">「戻る」ボタンで戻ってフォント埋め込み確認チェックボックス（手動）を確認してください。</font>', "\n";
	print '</ul>', "\n";
    }

    print '<li>', "著作権譲渡契約書のPDFファイル\n" if ($paramerr=~/\/COPYRIGHT/);
    if ($paramerr=~/\/A2|\/A3|\/A4|\/A5|\/A6|\/A7/) {
	print '<li>', "著者情報\n";
	print '<ul>', "\n";
	for my $i ( 2 .. 7 ) {
	    print '<li>', "著者$i\n" if ($paramerr=~/\/A$i/);
	}
	print '</ul>', "\n";
    }

    print '<li>', "連絡先メールアドレス\n" if ($paramerr=~/\/EMAIL/);

    print '</ul>', "\n";
    print $q->start_form(-action=>$submit1);
    print '<input type="hidden" name="did" value="', $q->param('did'), '">',
        '<input type="hidden" name="pid" value="', $q->param('pid'), '">',
        '<input type="hidden" name="err" value="', $paramerr, '">',
        "\n";
    print $q->submit("←　戻る（再入力）");
    print $q->end_form;
}

#==================================================#
#                  メインルーチン                  #
#==================================================#

# 論文ファイル取得
my $pfh = $q->upload('paper');
if ($pfh ne "") {
    $savepfile = &store_file($pfh, "p" . $timestamp);
}

# 著作権譲渡ファイル取得
my $cfh = $q->upload('copyright');
if ($cfh ne "") {
    $savecfile = &store_file($cfh, "c" . $timestamp);
}

#--------------------------------------------#
#           パラメータをsaveする             #
#--------------------------------------------#
my $cfg = new Config::Simple(syntax=>'ini');
my $text = "";

$cfg->param('General.date', (strftime "%Y/%m/%d %H:%M:%S", localtime));
$cfg->param('Paper.type', $q->param('Paper.type'));

$text = $q->param('Paper.title');
$text =~ s/,/\\comma\\/g;	# ','があるとConfig::Simpleが配列扱いする
$cfg->param('Paper.title', $text);

if ($q->param('Paper.subtitle') ne "") {
    $text = $q->param('Paper.subtitle');
    $text =~ s/,/\\comma\\/g;	# ','があるとConfig::Simpleが配列扱いする
    $cfg->param('Paper.subtitle', $text);
}

$cfg->param('Paper.demo', $q->param('Paper.demo'));
$cfg->param('Presenter.present', $q->param('Presenter.present'));
my @st = $q->param('Presenter.status');
my $status = shift(@st);
while (my $str = shift(@st)) {
    $status = $status . ':' . $str;
}
$cfg->param('Presenter.status', $status);
$cfg->param('User.email', $q->param('User.email'));
if (!Email::Valid->address($q->param('User.email'))) {
    $paramerr = $paramerr . "/EMAIL";
}

$cfg->param('Paper.pages', $q->param('Paper.pages')) if ($q->param('Paper.pages') ne "");
$cfg->param('Paper.fonts', $q->param('Paper.fonts')) if ($q->param('Paper.fonts') ne "");
$cfg->param('Paper.copyright', $q->param('Paper.copyright')) if ($q->param('Paper.copyright') ne "");
if ($q->param('Notes.text2') ne "") {
    $text = $q->param('Notes.text2');
    $text =~ s/,/\\comma\\/g;	# ','があるとConfig::Simpleが配列扱いする
    $cfg->param('Notes.text2', $text);
}

$cfg->param('Author1.sname', $q->param('Author1.sname'));
$cfg->param('Author1.gname', $q->param('Author1.gname'));
$text = $q->param('Author1.affili');
$text =~ s/,/\\comma\\/g;	# ','があるとConfig::Simpleが配列扱いする
$cfg->param('Author1.affili', $text);

if ($q->param('Author2.sname') ne "") {
    $cfg->param('Author2.sname', $q->param('Author2.sname'));
    $cfg->param('Author2.gname', $q->param('Author2.gname'));
    $text = $q->param('Author2.affili');
    $text =~ s/,/\\comma\\/g;	# ','があるとConfig::Simpleが配列扱いする
    $cfg->param('Author2.affili', $text);

    if ($q->param('Author2.gname') eq "" ||
	$q->param('Author2.affili') eq "") {
	$paramerr = $paramerr . "/A2";
    }
}

if ($q->param('Author3.sname') ne "") {
    $cfg->param('Author3.sname', $q->param('Author3.sname'));
    $cfg->param('Author3.gname', $q->param('Author3.gname'));
    $text = $q->param('Author3.affili');
    $text =~ s/,/\\comma\\/g;	# ','があるとConfig::Simpleが配列扱いする
    $cfg->param('Author3.affili', $text);

    if ($q->param('Author3.gname') eq "" ||
	$q->param('Author3.affili') eq "") {
	$paramerr = $paramerr . "/A3";
    }
}

if ($q->param('Author4.sname') ne "") {
    $cfg->param('Author4.sname', $q->param('Author4.sname'));
    $cfg->param('Author4.gname', $q->param('Author4.gname'));
    $text = $q->param('Author4.affili');
    $text =~ s/,/\\comma\\/g;	# ','があるとConfig::Simpleが配列扱いする
    $cfg->param('Author4.affili', $text);

    if ($q->param('Author4.gname') eq "" ||
	$q->param('Author4.affili') eq "") {
	$paramerr = $paramerr . "/A4";
    }
}

if ($q->param('Author5.sname') ne "") {
    $cfg->param('Author5.sname', $q->param('Author5.sname'));
    $cfg->param('Author5.gname', $q->param('Author5.gname'));
    $text = $q->param('Author5.affili');
    $text =~ s/,/\\comma\\/g;	# ','があるとConfig::Simpleが配列扱いする
    $cfg->param('Author5.affili', $text);
    if ($q->param('Author5.gname') eq "" ||
	$q->param('Author5.affili') eq "") {
	$paramerr = $paramerr . "/A5";
    }
}

if ($q->param('Author6.sname') ne "") {
    $cfg->param('Author6.sname', $q->param('Author6.sname'));
    $cfg->param('Author6.gname', $q->param('Author6.gname'));
    $text = $q->param('Author6.affili');
    $text =~ s/,/\\comma\\/g;	# ','があるとConfig::Simpleが配列扱いする
    $cfg->param('Author6.affili', $text);
    if ($q->param('Author6.gname') eq "" ||
	$q->param('Author6.affili') eq "") {
	$paramerr = $paramerr . "/A6";
    }
}

if ($q->param('Author7.sname') ne "") {
    $cfg->param('Author7.sname', $q->param('Author7.sname'));
    $cfg->param('Author7.gname', $q->param('Author7.gname'));
    $text = $q->param('Author7.affili');
    $text =~ s/,/\\comma\\/g;	# ','があるとConfig::Simpleが配列扱いする
    $cfg->param('Author7.affili', $text);
    if ($q->param('Author7.gname') eq "" ||
	$q->param('Author7.affili') eq "") {
	$paramerr = $paramerr . "/A7";
    }
}

$cfg->write($path . '/submit.ini');

#----------------------------------#
#           エラー確認             #
#----------------------------------#
if ($savepfile ne "") {
    my $cmd = "perl " . 'prosym50_checkpdf.pl' . ' "' . "$path/$savepfile" . '"';
    @fonts = `$cmd`;
}
$paramerr = $paramerr . "/PAPER" if ($savepfile eq "");
$paramerr = $paramerr . "/PAGES" if ($cfg->param('Paper.pages') eq "");
$paramerr = $paramerr . "/FONTS" if ($cfg->param('Paper.fonts') eq "");
$paramerr = $paramerr . "/COPYRIGHT" if ($cfg->param('Paper.copyright') eq "PDF" && $savecfile eq "");

#--------------------------------#
#           表示する             #
#--------------------------------#
print $q->header(-type=>'text/html', -charset=>'UTF-8');
#print $q->header(-type=>'text/html', -charset=>'x-euc-jp');
#print $q->header(-type=>'text/html', -charset=>'x-sjis');
print $q->start_html(-LANG=>'ja-JP',
		     -title=>"$title",
		     -charset=>'UTF-8', -encoding=>'UTF-8',
		     -BGCOLOR=>'#FFC1C1', -LINKCOLOR=>'#0000FF',
		     -ALINKCOLOR=>'#0000FF', -VLINKCOLOR=>'#660099');
print $q->h2('<img border="0" src="', $mark, '" width="115" height="96"> ', "$title"), "\n";

#---------------------------------#
#           エラー表示            #
#---------------------------------#
if ($paramerr ne "" || @fonts > 0) {
    &print_errors();
    print $q->br, "\n";
    print 'どうしてもうまくいかない場合は、', $q->a({href=>'mailto:'. $admin}, $admin), 'までご連絡ください。', $q->br, "\n";
    print $q->end_html;
    $cfg->close;

    exit(1);
}

print '<table border="1" celspaceing="0" cellspan="0">', "\n";
#---- 種別 ----
print '<tr valign="top" align="left">';
#print '<td align="right">種別：</td>';
print '<td>種別：</td>';
print '<td>講演</td>' if ($cfg->param('Paper.type') eq "ORAL");
print '<td>ポスター</td>' if ($cfg->param('Paper.type') eq "POSTER");
print "</tr>\n";
#---- 題目 ----
print '<tr valign="top" align="left">';
#print '<td align="right">題目：</td>';
print '<td>題目：</td>';
$text = $cfg->param('Paper.title');
$text =~ s/\\comma\\/,/g;	# エスケープした ',' を戻す
print '<td>', $text, '</td>';
print "</tr>\n";
#---- 副題目 ----
if ($cfg->param('Paper.subtitle') ne "") {
    print '<tr valign="top" align="left">';
    print '<td>副題目：</td>';
    $text = $cfg->param('Paper.subtitle');
    $text =~ s/\\comma\\/,/g;	# エスケープした ',' を戻す
    print '<td>', $text, '</td>';
    print "</tr>\n";
}
#---- デモ ----
print '<tr valign="top" align="left">';
print '<td>デモ：</td>';
print '<td>';
print 'あり' if ($cfg->param('Paper.demo') eq "YDEMO");
print 'なし' if ($cfg->param('Paper.demo') eq "NODEMO");
print "</tr>\n";

#---- 著者 ----
for my $i ( 1 .. 7 ) {
    my $arg = "Author" . $i;
    next if ($cfg->param("$arg" . ".sname") eq "");
    print '<tr valign="top" align="left">';
    print '<td>', "著者$i：", '</td>';
    print '<td>';
    print $cfg->param("$arg" . ".sname"), " ", $cfg->param("$arg" . ".gname");
    print ' / ';
    $text = $cfg->param("$arg" . ".affili");
    $text =~ s/\\comma\\/,/g;	# エスケープした ',' を戻す
    print $text;
    print ' / 登壇' if ($arg eq $cfg->param('Presenter.present'));
    print '</td></tr>', "\n";
}

#---- 提出原稿 ----
copy "$path/$savepfile", "$htpath/$savepfile", or die;
print '<tr valign="top" align="left">';
#print '<td align="right">', '提出原稿：', '</td>';
print '<td>', '提出原稿：', '</td>';
print '<td>';
print $cfg->param('Paper.pages'), 'ページ / ';
print $q->a({href=>"$homeurl/$savepfile", target=>'_blank'}, "確認する");
print '</td></tr>', "\n";

#---- 著作権 ----
if ($cfg->param('Paper.copyright') eq "PDF") {
    copy "$path/$savecfile", "$htpath/$savecfile", or die;
}
print '<tr valign="top" align="left">';
#print '<td align="right">', '著作権譲渡契約書：', '</td>';
print '<td>', '著作権譲', $q->br, '渡契約書：', '</td>';
print '<td>';
print '郵送', $q->br, '（〒101-0062 東京都千代田区神田駿河台1-5 化学会館4F 社団法人情報処理学会 宛）' if ($cfg->param('Paper.copyright') eq "MAIL");
print 'FAX', $q->br, '（FAX番号：03-3518-8375 社団法人情報処理学会 宛）' if ($cfg->param('Paper.copyright') eq "FAX");
print 'PDF / ', $q->a({href=>"$homeurl/$savecfile", target=>'_blank'}, "確認する") if ($cfg->param('Paper.copyright') eq "PDF");
print '</td></tr>', "\n";

#---- 登壇発表者区分 ----
print '<tr valign="top" align="left">';
print '<td>', '登壇発表', $q->br, '者区分：', '</td>';
print '<td>';
my @st = split(/:/, $cfg->param('Presenter.status'));
my $s = shift(@st);
while ($s ne "") {
    print '学生' if ($s =~ /S/);
    print '65歳以上' if ($s =~ /E/);
    print '社会人' if ($s =~ /G/);
    $s = shift(@st);
    print ' / ' if ($s ne "");
}
print '</td></tr>', "\n";

#---- 連絡先 ----
print '<tr valign="top" align="left">';
print '<td>', '連絡先：', '</td>';
print '<td>', $cfg->param('User.email');
print '</td></tr>', "\n";

#---- 通信欄 ----
if ($cfg->param('Notes.text2') ne "") {
    print '<tr valign="top" align="left">';
    print '<td>', '通信欄：', '</td>';
    $text = $cfg->param('Notes.text2');
    $text =~ s/\\comma\\/,/g;	# エスケープした ',' を戻す
    if (length($text) > 100) {
	print '<td width="700">';
    } else {
	print '<td>';
    }
    print $text;
    print '</td></tr>', "\n";
}

print '</table>', "\n";

print $q->br;

print $q->start_form(-action=>$submit3);
print '<font color="brown">以上でよろしければ完了ボタンで提出を完了して下さい。</font>', "\n";
print '<input type="hidden" name="did" value="', $q->param('did'), '">',
    '<input type="hidden" name="pid" value="', $q->param('pid'), '">';
print '<input type="hidden" name="pfile" value="', $savepfile, '">' if ($savepfile ne "");
print '<input type="hidden" name="cfile" value="', $savecfile, '">' if ($savecfile ne "");
print "\n";
print $q->submit("　完了　→");
print $q->endform;

print $q->br, $q->br, $q->br, "\n";

print $q->start_form(-action=>$submit1);
print '<font color="brown">入力し直す場合は戻るボタンを押して下さい。</font>', "\n";
print '<input type="hidden" name="did" value="', $q->param('did'), '">',
    '<input type="hidden" name="pid" value="', $q->param('pid'), '">', "\n";
print $q->submit("←　戻る（再入力）");
print $q->endform;

print $q->end_html;

#--------------------------------#
#           正常終了             #
#--------------------------------#
$cfg->close;

exit(0);
