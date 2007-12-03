#!/bin/csh
foreach i (`cat p49.csv`)
  set did=`echo $i|sed 's/,[P,0-9]*//'`
  set pid=`echo $i|sed 's/.*,//'`
  echo mkdir $did
  mkdir $did
  sed -e "s/XPIDX/$pid/" -e "s/XDIDX/$did/" indexhtml.txt > $did/index.html
end
