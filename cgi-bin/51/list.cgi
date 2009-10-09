#!/usr/bin/env perl

use strict;

use CGI;
use Config::Simple;


my $c    = new Config::Simple('51.ini');
my $path = $c->param('Prosym.datapath');

my $q     = new CGI;
my $title = 'Prosym51';

# printout
print $q->header(-type=>'text/html', -charset=>'UTF-8');
print $q->start_html(-lang=>'ja-JP',
                     -title=>"$title",
                     -charset=>'UTF-8', -encoding=>'UTF-8',
#                    -bgcolor=>'#FFC1C1', -linkcolor=>'#0000FF',
                     -bgcolor=>'#FFFFCC', -linkcolor=>'#0000FF',
                     -alinkcolor=>'#0000FF', -vlinkcolor=>'#660099');


sub print_each {
  my ($q, $file) = @_;
  my $c = new Config::Simple($file);
  my $authors = '';
  my @stat = stat $file;
  my $date = localtime $stat[9];

  for (1..9) {
    my $key = "Author$_";
    if ($c->param("$key.sname")) {
      my $sname = $c->param("$key.sname");
      my $gname = $c->param("$key.gname");
      my $affili= $c->param("$key.affili");
      $authors .= "$sname $gname ($affili)<br/>"
    }
  }
  my $abst = $c->param('Paper.abst');

  print $q->dl(
    $q->dt("Date"),     $q->dd($date),
    $q->dt("Title"),    $q->dd($c->param('Paper.title')),
    $q->dt("Authors"),  $q->dd($authors),
    $q->dt("Abstract"), $q->dd($abst),
    $q->dt("Type"),     $q->dd($c->param('Paper.type'))
  );
}

print $q->h1("list");

my $globpat = $path . "/*";
my $count = 0;

print "<ul>\n";
for my $file (<$path/*>) {
  print "<li>\n";
  print_each($q, $file);
  print "</li>\n";
  $count += 1;
}
print "</ul>\n";


print $q->p("Total: $count");
print $q->end_html;

