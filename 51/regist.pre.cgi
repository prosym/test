#!/usr/bin/ruby

require 'cgi'
cgi = CGI.new
cgi.out{
  'foo'
}

