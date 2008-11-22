#!/usr/bin/env perl

use strict;
use CGI;
#use CGI::Carp qw(fatalsToBrowser);
use Jcode;
use Config::Simple;
use File::Copy;
use Mail::Sendmail;

my $title  = "第50回プログラミング・シンポジウム 発表原稿提出完了";
# http://www2u.biglobe.ne.jp/~MAS/perl/waza/yen.html

my $q = new CGI;
my $c = new Config::Simple('prosym50_submit.ini');
my $mark   = $c->param('Prosym50.mark');
my $admin1 = $c->param('Prosym50.adminaddr1');
my $admin2 = $c->param('Prosym50.adminaddr2');
my $path   = $c->param('Prosym50.datahome') . $q->param('did');
my $htpath = $c->param('Prosym50.htdocshome') . $q->param('did');
my $regist = $c->param('Prosym50.registurl');
$c->close;

#==================================================#
#                  メインルーチン                  #
#==================================================#

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
if ($q->param('did') eq "" || $q->param('pid') eq "" || ! -d $htpath) {
    print $q->br;
    print $q->h2('不正なページです。'), $q->br, "\n";
    print 'お手数ですが、', $q->a({href=>'mailto:' . $admin2}, $admin2), 'までご連絡ください。', $q->br, "\n";
    print $q->end_html;
    exit(1);
}

#------------------------------------#
#        確定したファイルを記録      #
#------------------------------------#
my $pfile = $q->param('pfile');
my $cfile = $q->param('cfile');
my $pid = $q->param('pid');
my $ps = "$path/$pfile";
my $pd = "$path/$pid" . ".pdf";
if ( -f "$ps" ) {
    copy "$ps", "$pd", or die;
}
if ($cfile ne "") {
    my $cs = "$path/$cfile";
    my $cd = "$path/c$pid" . ".pdf";
    if ( -f "$cs" ) {
	copy "$cs", "$cd", or die;
    }
}

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
#           表示する             #
#--------------------------------#
print $q->br;
print $q->h2('発表原稿の提出が完了しました。'), $q->br, "\n";

print $q->ul(
	  $q->li('発表者も参加申込みが必要です。まだお済みでない場合は、',
		 $q->a({href=>"$regist", target=>'_blank'},
		       "ここから参加申\込み"),
		 'を行って下さい。'),
	  $q->li('ご不明な点は',
		 $q->a({href=>'mailto:' . $admin1},
		       $admin1), 'までご連絡ください。')
	     );

print $q->end_html;

#--------------------------------#
#           メイル処理           #
#--------------------------------#
my $mesg = "";

my $ini = "";
$ini = "$path/initial.ini" if ( -f "$path/initial.ini" );
$ini = "$path/submit.ini"  if ( -f "$path/submit.ini" ); 
my $cfg = new Config::Simple($ini) or die "Can't open ini file\n";

$mesg .= '下記の通り原稿の提出を受け付けました。' . "\n" . "\n";
$mesg .= '日時：' . $cfg->param('General.date') . "\n";
$mesg .= '種別：';
$mesg .= "講演\n" if ($cfg->param('Paper.type') eq "ORAL");
$mesg .= "ポスター\n" if ($cfg->param('Paper.type') eq "POSTER");
$mesg .= '題目：' . $cfg->param('Paper.title') . "\n";
if ($cfg->param('Paper.subtitle') ne "") {
    $mesg .= '副題目：' . $cfg->param('Paper.subtitle') . "\n";
}
$mesg .= 'デモ：';
$mesg .= "あり\n" if ($cfg->param('Paper.demo') eq "YDEMO");
$mesg .= "なし\n" if ($cfg->param('Paper.demo') eq "NODEMO");

#---- 著者 ----
for my $i ( 1 .. 7 ) {
    my $arg = "Author" . $i;
    next if ($cfg->param("$arg" . ".sname") eq "");
    $mesg .= "著者$i：";
    $mesg .= $cfg->param("$arg" . ".sname") . " " . $cfg->param("$arg" . ".gname");
    $mesg .= ' / ';
    $mesg .= $cfg->param("$arg" . ".affili");
    $mesg .= ' / 登壇' if ($arg eq $cfg->param('Presenter.present'));
    $mesg .= "\n";
}

$mesg .= 'ページ数：' . $cfg->param('Paper.pages') . "\n";

$mesg .= '著作権譲渡契約書：';
$mesg .= '郵送（〒101-0062 東京都千代田区神田駿河台1-5 化学会館4F 社団法人情報処理学会 宛）' if ($cfg->param('Paper.copyright') eq "MAIL");
$mesg .= 'FAX（FAX番号：03-3518-8375 社団法人情報処理学会 宛）' if ($cfg->param('Paper.copyright') eq "FAX");
$mesg .= 'PDF' if ($cfg->param('Paper.copyright') eq "PDF");
$mesg .= "\n";

#---- 連絡先 ----
$mesg .= '連絡先：' . $cfg->param('User.email') . "\n";

#---- 登壇発表者区分 ----
$mesg .= '登壇発表者区分：';
my @st = split(/:/, $cfg->param('Presenter.status'));
my $s = shift(@st);
while ($s ne "") {
    $mesg .= '学生' if ($s =~ /S/);
    $mesg .= '65歳以上' if ($s =~ /E/);
    $mesg .= '社会人' if ($s =~ /G/);
    $s = shift(@st);
    $mesg .= ' / ' if ($s ne "");
}
$mesg .= "\n";

#---- 通信欄 ----
if ($cfg->param('Notes.text2') ne "") {
    my $text = $cfg->param('Notes.text2');
    $text =~ s/\\comma\\/,/g;	# エスケープした ',' を戻す
#    $text =~ s/\x0Dn//g;
    $text = Encode::decode_utf8($text);
    $mesg .= '通信欄：' . $text . "\n";
}

#--------------------------------#
#           メイル送信           #
#--------------------------------#

my $subj = 'プログラミング・シンポジウム発表原稿提出完了のお知らせ';

$subj = encode("MIME-Header-ISO_2022_JP", $subj);
$mesg = encode("iso-2022-jp", $mesg);
    my %mailparams = (
		"Content-Type" => 'text/plain; charset="iso-2022-jp"',
		To             => $mailto,
		Cc             => $mail,
		From           => $mail,
		Subject        => $subj,
		Message        => $mesg,
		);
    sendmail(%mailparams);

#my $mailto = $cfg->param('User.email');
#$mailto =~ s/,/ /g;
#my $cmd = 'nkf -j ' . $mesgfile . ' | mail -a "From: ' . $admin2 . '" -s "' . $subj . '" -c ' . $admin2 . ' ' . $mailto;
#system $cmd;

#--------------------------------#
#           正常終了             #
#--------------------------------#
exit 0;
