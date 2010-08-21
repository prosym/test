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
my $c = new Config::Simple('52.ini')
    or die "Can't Read Configuration file.\n";
my $path = $c->param('Prosym.datapath');
my $mark = $c->param('Prosym.mark');
my $mail = $c->param('Prosym.mail');
my $home = $c->param('Prosym.home');
my $top =  $c->param('Prosym.prosymurl');
my $template = $c->param('Prosym.template');
$c->close;

$path = $path . "/" if ($path !~ /.*\/$/);

my $q = new CGI;
my $title = "第52回プログラミング・シンポジウム 発表申込み";
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
#		     -bgcolor=>'#FFC1C1', -linkcolor=>'#0000FF',
		     -bgcolor=>'#FFFFCC', -linkcolor=>'#0000FF',
		     -alinkcolor=>'#0000FF', -vlinkcolor=>'#660099');


print $q->p("発表申し込みは終了しました．");

print $q->end_html;


exit(0);


