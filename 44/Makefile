.SUFFIXES: .mhtml .html
.mhtml.html:; cp $*.mhtml $*.c; cc -traditional $*.c -E | grep -v '^#' | tr "%" "," > $*.html; rm $*.c

all: regist1.html

